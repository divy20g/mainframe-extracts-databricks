# Medicaid Fixed-Width -> Bronze Ingestion (Databricks Asset Bundle)

## What this does
Parses the 9 fixed-width Medicaid mainframe extracts (MEMBER, PROVIDER,
MEDICAL_CLAIMS, PHARMACY_CLAIMS, FINANCE, PRIOR_AUTH, TPL, DRUG_REBATE,
REFERENCE) and loads each into a typed Bronze Delta table under
`<target_catalog>.<target_schema>.<domain>` (e.g. `main.medicaid_bronze.member`).

**Scope**: this job's job is parse-and-load into Bronze, full stop. Bronze
here means "parsed and typed," not "raw unparsed lines" -- Silver and Gold
already exist elsewhere with their own fixed schemas, and mapping Bronze
into those Silver tables is a separate, later job that isn't part of this
bundle. `bronze_layer.py` and `silver_layer.py` under `src/` implement a
different split (raw-line Bronze + a re-parsing Silver step) for a setup
where Silver doesn't already exist -- don't wire those into this job if
your Silver/Gold tables are already fixed; use `fixedwidth_to_delta.py`
alone, as configured below.

One generic notebook (`src/fixedwidth_to_delta.py`) handles every domain --
field positions, COBOL PIC types, and target Delta column types (string /
date / int / decimal(p,s)) are all read from `src/layout_catalog.json`,
which is generated directly from the same schema used to build the
copybooks in `../copybooks/*.cpy`. Nothing about field layout is
hand-duplicated between the copybook, the parser, and the sample data.

## Before you deploy
1. Upload the 9 sample `.txt` extracts (or your real mainframe extracts,
   once byte-for-byte layout is confirmed against the copybooks) to a
   Unity Catalog Volume, e.g.:
   `/Volumes/main/medicaid_landing/raw/MEMBER.txt`, `.../PROVIDER.txt`, etc.
2. Upload `src/layout_catalog.json` to
   `/Volumes/main/medicaid_landing/config/layout_catalog.json`
   (or wherever you point the `catalog_path` job parameter).
3. Edit `databricks.yml`: set your workspace host under `targets.dev.workspace.host`
   (and `targets.prod` if used).
4. Edit `resources/medicaid_fixedwidth_ingestion.job.yml`:
   - `node_type_id` under `job_clusters` to match an instance type available
     in your cloud/workspace
   - the `raw_volume_path` / `catalog_path` / `target_catalog` / `target_schema`
     job parameters if your Volume paths or target catalog differ from the
     defaults

## Running it

**Option A -- deploy as a scheduled/triggered job (production path):**
```bash
databricks bundle validate -t dev
databricks bundle deploy   -t dev
databricks bundle run      -t dev medicaid_fixedwidth_ingestion
```
Each of the 9 tasks runs independently (no task depends on another --
they don't join against each other during this Bronze load), so they
execute in parallel on the shared job cluster. `target_schema` already
defaults to `medicaid_bronze` in `resources/medicaid_fixedwidth_ingestion.job.yml`.

**Option B -- one CLI run with parameters overridden, no redeploy needed:**
```bash
databricks bundle run -t dev medicaid_fixedwidth_ingestion \
  --params target_catalog=main,target_schema=medicaid_bronze,write_mode=overwrite
```
Useful for pointing the same deployed job at a different catalog/schema
(e.g. testing against a `dev` schema before running against the real one)
without editing and redeploying the YAML.

**Option C -- interactive run in a notebook (fastest for a first test):**
Attach `src/fixedwidth_to_delta.py` to any cluster as a notebook, use
**Run > Edit parameters** (or the widgets bar at the top once you run the
first cell) to set:

| widget | value |
|---|---|
| `domain` | `ALL` (loads all 9 domains in one run) or a single domain name |
| `input_path` | Volume folder containing the `.txt` files, e.g. `/Volumes/main/medicaid_landing/raw` |
| `catalog_path` | `/Volumes/main/medicaid_landing/config/layout_catalog.json` |
| `target_catalog` | `main` |
| `target_schema` | `medicaid_bronze` |
| `write_mode` | `overwrite` for a first test, `append` once this runs daily |

Then **Run all**. With `domain=ALL`, `input_path` is treated as a
directory and the notebook loops over every entry in the layout catalog,
writing `main.medicaid_bronze.member`, `main.medicaid_bronze.provider`,
etc. -- one call, nine typed tables.

## Rejected / malformed rows
Any input line whose length doesn't match the copybook's expected record
length is NOT silently truncated or misaligned -- it's routed to
`<target_catalog>.<target_schema>.<domain>_rejects` instead of the modeled
table, and a warning is printed in the task's driver log. Check that table
after a run if the loaded row count looks short.

## Re-running / schema changes
`write_mode` defaults to `overwrite` (full reload each run) with
`mergeSchema=true`, so adding a new field to a schema in `schemas.py` and
regenerating the copybook + layout catalog will pick up automatically on
the next deploy + run. Switch `write_mode` to `append` for incremental
loads once you're ingesting real periodic mainframe drops rather than
doing full sample reloads.

## Testing the parsing logic without Databricks
`src/fixedwidth_to_delta.py` is written so the parsing functions
(`parse_fixed_width`, `build_field_expression`) can be imported and unit
tested against a plain local PySpark session -- the Databricks-only
driver code (widgets, `dbutils`, `spark.sql(CREATE SCHEMA...)`) only runs
when the file is executed inside an actual Databricks notebook/job
(detected via the presence of the injected `dbutils` global).
