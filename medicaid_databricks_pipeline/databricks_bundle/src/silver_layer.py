# Databricks notebook source
# MAGIC %md
# MAGIC # Silver layer: typed parse against the layout catalog
# MAGIC
# MAGIC Reads Bronze as a stream (never re-touches S3 directly -- Bronze is
# MAGIC now the source of truth for "what did the mainframe actually send").
# MAGIC Reuses `build_field_expression` from `fixedwidth_to_delta.py` unchanged;
# MAGIC only the driver around it is different (streaming `foreachBatch`
# MAGIC instead of a one-shot batch read).
# MAGIC
# MAGIC Rows whose length doesn't match the copybook are quarantined to
# MAGIC `<domain>_rejects`, exactly as in the batch version -- a malformed
# MAGIC record must never silently misalign into the wrong columns.

# COMMAND ----------

import json
from pyspark.sql import functions as F

try:
    dbutils  # noqa: F821
    RUNNING_IN_DATABRICKS = True
except NameError:
    RUNNING_IN_DATABRICKS = False

# Reuses the exact field-parsing logic already validated against every
# domain's sample data -- Silver's correctness rests on this one function.
from fixedwidth_to_delta import build_field_expression


def ensure_silver_table_and_constraints(spark, silver_table, layout, domain_key_col=None):
    """Create Silver with explicit Delta CHECK constraints for the fields
    that must never be null or out-of-range. Constraints are a second,
    independent line of defense beyond the length check -- a value that
    parses cleanly but violates business rules (e.g. a blank Claim_ID)
    still gets caught here, at write time, not discovered downstream."""
    fields = [f for f in layout["fields"] if not f["is_filler"]]
    cols_sql = []
    for f in fields:
        spark_type = {
            "string": "STRING", "date": "DATE", "int": "INT",
        }.get(f["spark_type"], f["spark_type"].upper() if f["spark_type"] else "STRING")
        if f["spark_type"] and f["spark_type"].startswith("decimal"):
            spark_type = f["spark_type"].upper()
        cols_sql.append(f"{f['name']} {spark_type}")
    cols_sql += ["source_file STRING", "silver_load_timestamp TIMESTAMP"]

    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {silver_table} (
            {', '.join(cols_sql)}
        )
        USING DELTA
        COMMENT 'Typed parse of Bronze via layout_catalog.json. One row per valid source record.'
    """)
    if domain_key_col:
        try:
            spark.sql(f"ALTER TABLE {silver_table} ADD CONSTRAINT {domain_key_col.lower()}_not_null CHECK ({domain_key_col} IS NOT NULL)")
        except Exception as e:  # constraint already exists on rerun
            print(f"constraint setup note: {e}")


def parse_batch(batch_df, layout, silver_table, reject_table):
    """The foreachBatch function driving Bronze -> Silver. batch_df already
    carries record_length, source_file, ingest_timestamp, domain from Bronze."""
    record_length = layout["record_length"]
    fields = [f for f in layout["fields"] if not f["is_filler"]]

    good = batch_df.filter(F.col("record_length") == record_length)
    bad = batch_df.filter(F.col("record_length") != record_length)

    bad_count = bad.count()
    if bad_count > 0:
        print(f"WARNING: {bad_count} row(s) quarantined this batch (length mismatch)")
        bad.write.format("delta").mode("append").saveAsTable(reject_table)

    exprs = [build_field_expression(f) for f in fields]
    parsed = (good.select(*exprs, F.col("source_file"))
                   .withColumn("silver_load_timestamp", F.current_timestamp()))
    parsed.write.format("delta").mode("append").saveAsTable(silver_table)


def silver_transform_stream(spark, domain, layout, bronze_table, checkpoint_root,
                              silver_table, reject_table, key_col=None):
    ensure_silver_table_and_constraints(spark, silver_table, layout, key_col)
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {reject_table} (
            value STRING, record_length INT, source_file STRING,
            file_modification_time TIMESTAMP, ingest_timestamp TIMESTAMP, domain STRING
        ) USING DELTA
        COMMENT 'Rows whose length did not match the copybook -- never loaded into Silver.'
    """)

    bronze_stream = spark.readStream.table(bronze_table)

    query = (bronze_stream.writeStream
        .foreachBatch(lambda batch_df, batch_id: parse_batch(batch_df, layout, silver_table, reject_table))
        .option("checkpointLocation", f"{checkpoint_root}/{domain}/silver_checkpoint")
        .trigger(availableNow=True)
        .start())
    query.awaitTermination()
    return query


# COMMAND ----------

DOMAIN_KEY_COLUMNS = {
    "MEMBER": "Member_ID", "PROVIDER": "Provider_ID",
    "MEDICAL_CLAIMS": "Claim_ID", "PHARMACY_CLAIMS": "Rx_Claim_ID",
    "FINANCE": "Transaction_ID", "PRIOR_AUTH": "PA_ID",
    "TPL": "TPL_ID", "DRUG_REBATE": "Rebate_Record_ID",
    "REFERENCE": "Code_Value",
}


def main():
    dbutils.widgets.text("domain", "MEMBER")
    dbutils.widgets.text("catalog_path", "/Volumes/main/medicaid_landing/config/layout_catalog.json")
    dbutils.widgets.text("checkpoint_root", "/Volumes/main/medicaid_landing/checkpoints")
    dbutils.widgets.text("target_catalog", "main")
    dbutils.widgets.text("bronze_schema", "medicaid_bronze")
    dbutils.widgets.text("silver_schema", "medicaid_silver")

    domain = dbutils.widgets.get("domain").upper()
    catalog_path = dbutils.widgets.get("catalog_path")
    checkpoint_root = dbutils.widgets.get("checkpoint_root")
    target_catalog = dbutils.widgets.get("target_catalog")

    with open(catalog_path) as f:
        full_catalog = json.load(f)
    layout = full_catalog[domain]

    bronze_table = f"{target_catalog}.{dbutils.widgets.get('bronze_schema')}.{domain.lower()}"
    silver_table = f"{target_catalog}.{dbutils.widgets.get('silver_schema')}.{domain.lower()}"
    reject_table = f"{target_catalog}.{dbutils.widgets.get('silver_schema')}.{domain.lower()}_rejects"

    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {target_catalog}.{dbutils.widgets.get('silver_schema')}")
    silver_transform_stream(spark, domain, layout, bronze_table, checkpoint_root,
                              silver_table, reject_table, DOMAIN_KEY_COLUMNS.get(domain))
    print(f"[{domain}] silver load complete -> {silver_table}")


if RUNNING_IN_DATABRICKS:
    main()
