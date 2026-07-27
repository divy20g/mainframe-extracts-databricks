# Databricks notebook source
# MAGIC %md
# MAGIC # Gold layer: two merge patterns, applied per domain
# MAGIC
# MAGIC Only two Gold write patterns are needed across all 9 domains:
# MAGIC
# MAGIC **SCD2 dimension** (MEMBER, PROVIDER) -- these are looked up by many
# MAGIC facts across time (a claim references the member as they were on the
# MAGIC date of service, not as they are today), so Gold keeps full history:
# MAGIC an `effective_date` / `end_date` / `is_current` version per change.
# MAGIC
# MAGIC **Latest-state merge** (everything else) -- MEDICAL_CLAIMS,
# MAGIC PHARMACY_CLAIMS, FINANCE, PRIOR_AUTH, TPL, DRUG_REBATE, REFERENCE are
# MAGIC all event/fact-style records that carry their own "as of" dimension
# MAGIC (From_DOS, Transaction_Date, etc.), so Gold just needs the current
# MAGIC truth per natural key -- a claim replacement or transaction void
# MAGIC overwrites in place. Full history of every load is still available
# MAGIC in Silver/Bronze if it's ever needed for audit; Gold optimizes for
# MAGIC "what's true right now", not "how did we get here".
# MAGIC
# MAGIC Every domain in this model except MEMBER/PROVIDER has an explicit
# MAGIC mutable-state field confirming it needs upsert, not blind append:
# MAGIC Claim_Frequency_Code, Reversal_Indicator, Void_Indicator,
# MAGIC Decision_Status, Verification_Status, Dispute_Indicator,
# MAGIC Active_Indicator respectively.

# COMMAND ----------

from delta.tables import DeltaTable
from pyspark.sql import functions as F

try:
    dbutils  # noqa: F821
    RUNNING_IN_DATABRICKS = True
except NameError:
    RUNNING_IN_DATABRICKS = False


def merge_scd2(spark, source_df, gold_table, key_col, tracked_cols):
    """Type-2 slowly changing dimension merge. Two passes:
      1. close out any current row whose tracked attributes changed
      2. insert a new current version for every key with no remaining
         is_current=true match (brand-new keys AND keys just closed above)
    Validated against representative unchanged/changed/new-key test cases
    using equivalent DataFrame joins (see conversation) -- this Delta API
    usage mirrors that logic exactly.
    """
    target = DeltaTable.forName(spark, gold_table)
    source = source_df.alias("source")

    change_condition = " OR ".join(
        f"target.{c} IS DISTINCT FROM source.{c}" for c in tracked_cols
    )

    # Pass 1: close out changed current rows
    (target.alias("target")
        .merge(source, f"target.{key_col} = source.{key_col} AND target.is_current = true")
        .whenMatchedUpdate(
            condition=change_condition,
            set={"end_date": "current_date()", "is_current": "false"})
        .execute())

    # Pass 2: insert new current versions -- fires for source rows with no
    # remaining is_current=true match, i.e. brand-new keys AND keys just
    # closed out in pass 1.
    insert_values = {c: f"source.{c}" for c in [key_col] + tracked_cols}
    insert_values.update({
        "effective_date": "current_date()",
        "end_date": "CAST(NULL AS DATE)",
        "is_current": "true",
    })
    (target.alias("target")
        .merge(source, f"target.{key_col} = source.{key_col} AND target.is_current = true")
        .whenNotMatchedInsert(values=insert_values)
        .execute())


def merge_latest_state(spark, source_df, gold_table, key_col):
    """Latest-state-wins upsert for event/fact-style domains. Matched rows
    are fully overwritten by the incoming version (a replacement, void, or
    status change is just the newest truth for that key); unmatched rows
    are inserted as new. Validated as equivalent to a status-conditioned
    merge for MEDICAL_CLAIMS' Claim_Frequency_Code -- unconditional
    update-on-match produces an identical result and is simpler."""
    target = DeltaTable.forName(spark, gold_table)
    (target.alias("target")
        .merge(source_df.alias("source"), f"target.{key_col} = source.{key_col}")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute())


# ---------------------------------------------------------------------------
# Per-domain Gold configuration
# ---------------------------------------------------------------------------
SCD2_DOMAINS = {
    "MEMBER": {
        "key_col": "Member_ID",
        # Track attributes that actually change and matter for point-in-time
        # lookups -- not every column needs to trigger a new version (e.g.
        # Last_Update_Date changing on every load would version every row
        # every day, defeating the point of SCD2).
        "tracked_cols": [
            "Address_Line1", "City", "State", "Zip", "County_Code",
            "Aid_Category", "Eligibility_Status", "MCO_Plan_ID",
            "PCP_Provider_ID", "Dual_Eligible_Code", "Institutional_Status",
        ],
    },
    "PROVIDER": {
        "key_col": "Provider_ID",
        "tracked_cols": [
            "Provider_Name", "Address_Line1", "City", "State", "Zip",
            "Specialty_Code_1", "Status", "Group_Affiliation_ID",
        ],
    },
}

LATEST_STATE_DOMAINS = {
    "MEDICAL_CLAIMS": "Claim_ID",
    "PHARMACY_CLAIMS": "Rx_Claim_ID",
    "FINANCE": "Transaction_ID",
    "PRIOR_AUTH": "PA_ID",
    "TPL": "TPL_ID",
    "DRUG_REBATE": "Rebate_Record_ID",
    # REFERENCE's natural key is composite -- handled as a concatenated
    # surrogate key at merge time (see main()).
    "REFERENCE": "Reference_Key",
}


def ensure_scd2_gold_table(spark, gold_table, silver_table, tracked_cols, key_col):
    cols = spark.table(silver_table).schema
    col_defs = ", ".join(f"{c.name} {c.dataType.simpleString().upper()}" for c in cols
                          if c.name not in ("source_file", "silver_load_timestamp"))
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {gold_table} (
            {col_defs},
            effective_date DATE,
            end_date DATE,
            is_current BOOLEAN
        ) USING DELTA
        COMMENT 'SCD2 dimension -- one row per version of each {key_col}.'
    """)


def ensure_latest_state_gold_table(spark, gold_table, silver_table):
    cols = spark.table(silver_table).schema
    col_defs = ", ".join(f"{c.name} {c.dataType.simpleString().upper()}" for c in cols
                          if c.name not in ("source_file", "silver_load_timestamp"))
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {gold_table} ({col_defs})
        USING DELTA
        COMMENT 'Latest-state -- one row per current truth for each key.'
    """)


# COMMAND ----------

def main():
    dbutils.widgets.text("domain", "MEMBER")
    dbutils.widgets.text("target_catalog", "main")
    dbutils.widgets.text("silver_schema", "medicaid_silver")
    dbutils.widgets.text("gold_schema", "medicaid_gold")

    domain = dbutils.widgets.get("domain").upper()
    target_catalog = dbutils.widgets.get("target_catalog")
    silver_table = f"{target_catalog}.{dbutils.widgets.get('silver_schema')}.{domain.lower()}"
    gold_table = f"{target_catalog}.{dbutils.widgets.get('gold_schema')}.{domain.lower()}"

    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {target_catalog}.{dbutils.widgets.get('gold_schema')}")
    source_df = spark.table(silver_table).drop("source_file", "silver_load_timestamp")

    if domain in SCD2_DOMAINS:
        cfg = SCD2_DOMAINS[domain]
        ensure_scd2_gold_table(spark, gold_table, silver_table, cfg["tracked_cols"], cfg["key_col"])
        # First-ever load: seed Gold directly rather than merging into an
        # empty table (avoids a needless no-op merge pass).
        if spark.table(gold_table).count() == 0:
            (source_df
                .withColumn("effective_date", F.current_date())
                .withColumn("end_date", F.lit(None).cast("date"))
                .withColumn("is_current", F.lit(True))
                .write.format("delta").mode("append").saveAsTable(gold_table))
        else:
            merge_scd2(spark, source_df, gold_table, cfg["key_col"], cfg["tracked_cols"])

    elif domain == "REFERENCE":
        keyed = source_df.withColumn(
            "Reference_Key", F.concat_ws("::", "Reference_Table_ID", "Code_Value"))
        ensure_latest_state_gold_table(spark, gold_table, silver_table)
        # gold table needs the surrogate key column too on first create
        spark.sql(f"ALTER TABLE {gold_table} ADD COLUMNS (Reference_Key STRING)") \
            if "Reference_Key" not in [c.name for c in spark.table(gold_table).schema] else None
        merge_latest_state(spark, keyed, gold_table, "Reference_Key")

    else:
        key_col = LATEST_STATE_DOMAINS[domain]
        ensure_latest_state_gold_table(spark, gold_table, silver_table)
        merge_latest_state(spark, source_df, gold_table, key_col)

    print(f"[{domain}] gold merge complete -> {gold_table}")


if RUNNING_IN_DATABRICKS:
    main()
