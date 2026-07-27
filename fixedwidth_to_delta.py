# Databricks notebook source
# MAGIC %md
# MAGIC # Medicaid Fixed-Width Extract -> Delta Table Loader
# MAGIC
# MAGIC Generic, layout-catalog-driven parser. One notebook handles all 9
# MAGIC domains (MEMBER, PROVIDER, MEDICAL_CLAIMS, PHARMACY_CLAIMS, FINANCE,
# MAGIC PRIOR_AUTH, TPL, DRUG_REBATE, REFERENCE) -- the field positions,
# MAGIC COBOL PIC types, and target Delta column types all come from
# MAGIC `layout_catalog.json`, which is generated directly from the same
# MAGIC schema definitions used to build the copybooks (`*.cpy`). Copybook,
# MAGIC layout catalog, and sample data can never drift out of sync because
# MAGIC they share one source of truth.
# MAGIC
# MAGIC Run as a Databricks Job task with widgets:
# MAGIC   - `domain`        : one of the 9 domain names above, or `ALL`
# MAGIC   - `input_path`    : Volume/DBFS path to the fixed-width .txt file
# MAGIC                       (for `ALL`, treated as a directory containing
# MAGIC                       <DOMAIN>.txt for each domain)
# MAGIC   - `catalog_path`  : path to layout_catalog.json (Volume/DBFS/Repo)
# MAGIC   - `target_catalog`: Unity Catalog catalog name for output tables
# MAGIC   - `target_schema` : Unity Catalog schema (database) for output tables
# MAGIC   - `write_mode`    : overwrite | append

# COMMAND ----------

import json
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

# ---------------------------------------------------------------------------
# Detect whether we're actually running inside a Databricks notebook/job.
# This lets the same file be imported and unit-tested locally (e.g. in a
# CI pipeline or a plain PySpark session) without requiring dbutils/widgets.
# ---------------------------------------------------------------------------
try:
    dbutils  # noqa: F821  (injected by the Databricks runtime)
    RUNNING_IN_DATABRICKS = True
except NameError:
    RUNNING_IN_DATABRICKS = False


# COMMAND ----------

def _spark_dtype_from_string(type_name):
    """Map the layout catalog's spark_type string to an actual Spark type."""
    if type_name == "string":
        return T.StringType()
    if type_name == "date":
        return T.DateType()
    if type_name == "int":
        return T.IntegerType()
    if type_name.startswith("decimal"):
        p, s = type_name[type_name.index("(") + 1 : type_name.index(")")].split(",")
        return T.DecimalType(int(p), int(s))
    raise ValueError(f"Unsupported spark_type: {type_name}")


def build_field_expression(field):
    """Build the Spark Column expression that extracts and casts one
    field out of the raw fixed-width 'value' column, per the layout
    catalog entry for that field.

    field: dict with keys start,length,kind,decimals,signed,spark_type,name
    """
    start, length = field["start"], field["length"]
    raw = F.substring(F.col("value"), start, length)

    if field["kind"] == "X":
        return F.rtrim(raw).alias(field["name"])

    # Numeric (9 / S9) fields ------------------------------------------------
    if field["signed"]:
        sign_char = F.substring(raw, 1, 1)
        digits = F.substring(raw, 2, length - 1)
    else:
        sign_char = F.lit("+")
        digits = raw

    spark_type = field["spark_type"]

    if spark_type == "date":
        sentinel = "9" * length
        parsed = F.to_date(digits, "yyyyMMdd")
        return F.when(raw == sentinel, F.lit(None).cast(T.DateType())) \
                .otherwise(parsed).alias(field["name"])

    if spark_type == "string":
        # Identifier-like numeric field (SSN, NPI, Zip, Phone, Tax_ID, ...).
        # Preserve the original zero-padded digit string as-is.
        return raw.alias(field["name"])

    if spark_type == "int":
        base = digits.cast(T.LongType())
        signed_val = F.when(sign_char == "-", -base).otherwise(base)
        return signed_val.cast(T.IntegerType()).alias(field["name"])

    if spark_type.startswith("decimal"):
        dtype = _spark_dtype_from_string(spark_type)
        precision, scale = dtype.precision, dtype.scale
        int_len = precision - scale
        int_part = F.substring(digits, 1, int_len)
        if scale > 0:
            dec_part = F.substring(digits, int_len + 1, scale)
            value_str = F.concat(int_part, F.lit("."), dec_part)
        else:
            value_str = int_part
        signed_str = F.when(sign_char == "-", F.concat(F.lit("-"), value_str)).otherwise(value_str)
        return signed_str.cast(dtype).alias(field["name"])

    raise ValueError(f"Unhandled spark_type {spark_type} for field {field['name']}")


def parse_fixed_width(spark: SparkSession, layout: dict, input_path: str):
    """Parse one fixed-width extract file according to its layout-catalog
    entry. Returns (good_df, bad_df) -- bad_df holds any lines whose
    length didn't match the expected record length, so they can be routed
    to a quarantine/rejects table instead of silently corrupting the load.
    """
    record_length = layout["record_length"]
    fields = [f for f in layout["fields"] if not f["is_filler"]]

    raw = spark.read.text(input_path)  # single column: 'value'
    raw = raw.withColumn("_raw_length", F.length("value"))

    good_raw = raw.filter(F.col("_raw_length") == record_length)
    bad_raw = raw.filter(F.col("_raw_length") != record_length)

    exprs = [build_field_expression(f) for f in fields]
    good_df = good_raw.select(*exprs)
    return good_df, bad_raw


def load_domain(spark, domain, layout, input_path, target_catalog, target_schema, write_mode):
    df, bad = parse_fixed_width(spark, layout, input_path)

    bad_count = bad.limit(1000).count()
    if bad_count > 0:
        print(f"[{domain}] WARNING: {bad_count}+ row(s) with unexpected length were quarantined, "
              f"not loaded into the modeled table.")
        reject_table = f"{target_catalog}.{target_schema}.{domain.lower()}_rejects"
        bad.write.mode("append").saveAsTable(reject_table)

    table_name = f"{target_catalog}.{target_schema}.{domain.lower()}"
    (df.write
       .mode(write_mode)
       .option("mergeSchema", "true")
       .saveAsTable(table_name))
    print(f"[{domain}] loaded {df.count()} rows -> {table_name}")
    return table_name


# COMMAND ----------
# Driver section -- only runs automatically inside an actual Databricks
# job/notebook. When this file is imported elsewhere (e.g. for local
# testing with a plain SparkSession), only the functions above are
# defined and nothing executes.

def main():
    dbutils.widgets.text("domain", "MEMBER")
    dbutils.widgets.text("input_path", "/Volumes/main/medicaid_landing/raw/MEMBER.txt")
    dbutils.widgets.text("catalog_path", "/Volumes/main/medicaid_landing/config/layout_catalog.json")
    dbutils.widgets.text("target_catalog", "main")
    dbutils.widgets.text("target_schema", "medicaid_modeled")
    dbutils.widgets.dropdown("write_mode", "overwrite", ["overwrite", "append"])

    domain = dbutils.widgets.get("domain")
    input_path = dbutils.widgets.get("input_path")
    catalog_path = dbutils.widgets.get("catalog_path")
    target_catalog = dbutils.widgets.get("target_catalog")
    target_schema = dbutils.widgets.get("target_schema")
    write_mode = dbutils.widgets.get("write_mode")

    with open(catalog_path) as f:  # Unity Catalog Volumes are POSIX-readable
        full_catalog = json.load(f)

    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {target_catalog}.{target_schema}")

    if domain.upper() == "ALL":
        # input_path is treated as a directory containing <DOMAIN>.txt
        results = []
        for dname, layout in full_catalog.items():
            path = input_path.rstrip("/") + "/" + layout["file"]
            results.append(load_domain(spark, dname, layout, path,
                                        target_catalog, target_schema, write_mode))
        print("Loaded tables:", results)
    else:
        layout = full_catalog[domain.upper()]
        load_domain(spark, domain.upper(), layout, input_path,
                    target_catalog, target_schema, write_mode)


if RUNNING_IN_DATABRICKS:
    main()
