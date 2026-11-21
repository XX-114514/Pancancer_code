# External input contract

The scripts require the matching 2026-11-20 companion plotting package, supplied separately. The public [figure map](FIGURE_INPUT_MAP.tsv) identifies renderers. Exact input filenames and scientific coverage are recorded in the private package manifest.

`--package-root` must contain `input_manifest.json` and `inputs/`. The manifest has a `files` array with `path`, `bytes` and `sha256` entries. Paths are relative to that package root. The verifier checks sizes, hashes and path containment.

Inputs comprise coordinate arrays, category dictionaries, marker summaries, saved statistical estimates and display configuration. Coordinate rows and category codes must remain aligned. Missingness definitions, correction families and original precision must be preserved. The plotting scripts consume saved outputs rather than fitting statistical models.

The document builder expects a separate bilingual content JSON and the assembled figure directory. Figure IDs must match the assembled outputs.

Use trusted companion files: an inherited imaging loader uses `allow_pickle=True`. Exact schema requirements are expressed by the frozen scripts. Do not substitute later-release inputs into this snapshot. Input distribution is a separate access step; no public data endpoint is promised here.
