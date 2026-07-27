# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze layer: raw fixed-width ingestion
# MAGIC
# MAGIC Auto Loader reads each domain's landing prefix as plain text (one row
# MAGIC per line, no parsing) and appends to a bronze Delta table, carrying
# MAGIC file-level provenance so any downstream question ("which source file
# MAGIC did this row come from") is answerable without re-touching S3.
# MAGIC
# MAGIC Bronze is never overwritten and never parsed -- it's the append-only
# MAGIC audit trail. If a copybook layout changes or a bug is found in Silver's
# MAGIC parsing logic, you replay Silver from Bronze; you never need to go
# MAGIC back to the mainframe extract itself.

# COMMAND ----------

from pyspark.sql import functions as F

try:
    dbutils  # noqa: F821
    RUNNING_IN_DATABRICKS = True
except NameError:
    RUNNING_IN_DATABRICKS = False


BRONZE_SCHEMA_COLUMNS = [
    # (name, description)
    ("value", "the full raw fixed-width line, byte-for-byte, untouched"),
    ("record_length", "length of value -- cheap sanity check available in Bronze itself"),
    ("source_file", "_metadata.file_path -- exact S3 object this row came from"),
    ("file_modification_time", "_metadata.file_modification_time"),
    ("ingest_timestamp", "when this row was written to Bronze"),
    ("domain", "which of the 9 domains this row belongs to"),
]


def bronze_ingest_stream(spark, domain, raw_path, checkpoint_root, bronze_table):
    """Auto Loader streaming read of one domain's landing prefix -> Bronze
    Delta table. Uses trigger(availableNow=True): drains everything that's
    arrived since the last run, then stops -- fits a daily job-scheduled
    run rather than an always-on cluster."""
    stream = (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "text")
        .option("cloudFiles.useNotifications", "true")
        .option("cloudFiles.schemaLocation", f"{checkpoint_root}/{domain}/bronze_schema")
        .load(raw_path)
        .select(
            F.col("value"),
            F.length("value").alias("record_length"),
            F.col("_metadata.file_path").alias("source_file"),
            F.col("_metadata.file_modification_time").alias("file_modification_time"),
            F.current_timestamp().alias("ingest_timestamp"),
            F.lit(domain).alias("domain"),
        ))

    query = (stream.writeStream
        .format("delta")
        .option("checkpointLocation", f"{checkpoint_root}/{domain}/bronze_checkpoint")
        .trigger(availableNow=True)
        .toTable(bronze_table))
    query.awaitTermination()
    return query


def ensure_bronze_table_exists(spark, bronze_table):
    """Create the bronze table with explicit types and a comment, rather
    than letting the first streaming write infer it implicitly."""
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {bronze_table} (
            value STRING COMMENT 'raw fixed-width line, untouched',
            record_length INT,
            source_file STRING,
            file_modification_time TIMESTAMP,
            ingest_timestamp TIMESTAMP,
            domain STRING
        )
        USING DELTA
        COMMENT 'Append-only raw ingestion. Never parsed, never overwritten.'
    """)


# COMMAND ----------

def main():
    dbutils.widgets.text("domain", "MEMBER")
    dbutils.widgets.text("raw_path", "/Volumes/main/medicaid_landing/raw/MEMBER/")
    dbutils.widgets.text("checkpoint_root", "/Volumes/main/medicaid_landing/checkpoints")
    dbutils.widgets.text("target_catalog", "main")
    dbutils.widgets.text("target_schema", "medicaid_bronze")

    domain = dbutils.widgets.get("domain").upper()
    raw_path = dbutils.widgets.get("raw_path")
    checkpoint_root = dbutils.widgets.get("checkpoint_root")
    bronze_table = f"{dbutils.widgets.get('target_catalog')}.{dbutils.widgets.get('target_schema')}.{domain.lower()}"

    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {dbutils.widgets.get('target_catalog')}.{dbutils.widgets.get('target_schema')}")
    ensure_bronze_table_exists(spark, bronze_table)
    bronze_ingest_stream(spark, domain, raw_path, checkpoint_root, bronze_table)
    print(f"[{domain}] bronze load complete -> {bronze_table}")


if RUNNING_IN_DATABRICKS:
    main()
