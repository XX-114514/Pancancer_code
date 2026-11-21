# PanCancer manuscript figure code

Reproducible plotting scripts for the **2026-11-20 draft** of the PanCancer manuscript. The workflow assembles **7 main figures and 12 supplementary figures** from frozen plotting inputs, exporting PNG, PDF and editable SVG.

[中文说明](README.zh-CN.md) · [Figure map](docs/FIGURES.md) · [Input contract](docs/INPUTS.md) · [Code provenance](docs/CODE_PROVENANCE.tsv)

## Scope and version

This repository contains the exact seven Python scripts in the accepted **story v2 draft review package**: five plotting/verification scripts and two document-production scripts. Each script’s SHA256 is recorded in `docs/CODE_PROVENANCE.tsv`.

The code covers the resolved atlas and annotation dotplot, composition modules and sensitivity, immune RNA states and clinical readouts, lymph-node organization, vascular spatial patterns, imaging neighborhoods and molecular context. Later UMAP-label edits and the separate Claude publication revision are distinct versions and are not substituted into this snapshot.

The scripts consume saved coordinates, marker summaries and statistical estimates. They do not rerun integration, annotation, NMF, communication tests or clinical models. CM identifiers retain the measurement/version namespaces defined in the manuscript.

## Repository layout

```text
scripts/
  plotting/
    run_all_figures.py             # Execute branches and assemble all 19 figures
    render_R4_portable.py          # Atlas, annotation, networks, spatial and imaging panels
    render_composition_and_LN.py   # Legacy composition, lymph-node and molecular panels
    render_story_panels.py         # Immune states, clinical and cancer-context panels
    verify_plot_inputs.py          # Verify external file sizes, hashes and path containment
  manuscript/
    build_manuscript.py            # Editable English/Chinese DOCX from external content
    package_supplementary_figures.py # Supplementary vector PDF with English legends
docs/
  FIGURES.md                      # Every final ID, renderer, intermediate ID and role
  FIGURE_INPUT_MAP.tsv             # Exact relative input locations; no observations
  INPUTS.md                       # Required package layout and key formats
  CODE_PROVENANCE.tsv             # SHA256 of the frozen source scripts
requirements-plotting.txt
requirements-documents.txt
requirements.txt
```

## Environment

The original full figure replay used **Python 3.10.19**, NumPy 1.26.4, pandas 2.3.3, matplotlib 3.10.8 and NetworkX 3.4.2. Document production used a separate Python 3.12 runtime. For a combined environment, use Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

For plotting alone, Python 3.10 with `requirements-plotting.txt` is the recorded environment. `requirements-documents.txt` preserves the original document dependency pins, including Pillow 13.0.0; use Python 3.12 for that set rather than installing it into the original Python 3.10 plotting environment. Rendering uses matplotlib’s headless Agg backend.

## Required plotting inputs

Supply the companion plotting package **outside the Git checkout**. Set `PLOT_PACKAGE` to the directory containing `input_manifest.json` and `inputs/`, not to the parent manuscript directory. For the previously delivered complete review bundle this is its `plotting/` directory.

```text
${PLOT_PACKAGE}/
  input_manifest.json
  inputs/
    r4/
    immune/
    integrated_evidence/
    R4_figure_tables/
    plot_tables/
    figure_configuration.json
```

The reviewed companion package contains 96 frozen input files. The public repository supplies code and an input map; expression matrices, plotting arrays, scientific tables, manuscript prose, learned W/H weights and credentials are not included. The inputs must come from the matching draft package. See [INPUTS.md](docs/INPUTS.md) for formats and dictionaries.

## Rebuild all figures

Run from this repository root, replacing the example paths with your own locations:

```bash
export PLOT_PACKAGE=/absolute/path/to/private/review_package/plotting
export FIGURE_OUTPUT=/absolute/path/to/new_output_directory

python scripts/plotting/verify_plot_inputs.py --package-root "$PLOT_PACKAGE"
python scripts/plotting/run_all_figures.py \
  --package-root "$PLOT_PACKAGE" \
  --output "$FIGURE_OUTPUT"
```

The output directory must **not already exist**. It contains:

- `figures/`: all 19 final figure IDs, each as `.png`, `.pdf` and `.svg`.
- `figure_manifest.json`: 57 output-file SHA256 hashes and branch provenance.
- `intermediate/`: branch-specific plots, processed source tables and receipts.
- `r4.log`, `composition.log`, `story.log`: branch logs.

The three branches execute sequentially. Large atlas scatter plots dominate painting time; no raw-matrix processing is performed. Intermediate renderers produce additional historical panels before the assembler selects the manuscript figure IDs. Follow [FIGURES.md](docs/FIGURES.md), rather than equating an intermediate file number to a final manuscript number.

### Rebuild one branch

```bash
python scripts/plotting/render_story_panels.py \
  --inputs "$PLOT_PACKAGE/inputs" \
  --output /absolute/path/to/new_story_output

python scripts/plotting/render_composition_and_LN.py \
  --root "$PLOT_PACKAGE/inputs" \
  --prior "$PLOT_PACKAGE/inputs/R4_figure_tables" \
  --configuration "$PLOT_PACKAGE/inputs/figure_configuration.json" \
  --output /absolute/path/to/new_composition_output

python scripts/plotting/render_R4_portable.py \
  --root "$PLOT_PACKAGE/inputs/r4" \
  --run "$PLOT_PACKAGE/inputs/r4/R4_preprint_20261120_v1" \
  --output /absolute/path/to/new_r4_output
```

For the vascular panel alone, use the R4 command with `--vascular-only`. It emits the intermediate `Figure4_spatial_organization`; the assembler maps it to manuscript `Figure6_vascular_architecture`.

## Rebuild the manuscript artifacts

Use the matching private bilingual content JSON and the **assembled** figure directory:

```bash
python scripts/manuscript/build_manuscript.py \
  --content /absolute/path/to/manuscript_content_v2_PRIVATE.json \
  --figures "$FIGURE_OUTPUT/figures" \
  --output /absolute/path/to/new_manuscript_output

python scripts/manuscript/package_supplementary_figures.py \
  --content /absolute/path/to/manuscript_content_v2_PRIVATE.json \
  --figures "$FIGURE_OUTPUT/figures" \
  --output /absolute/path/to/Supplementary_figures.pdf
```

DOCX rendering to page images/PDF is a separate review step requiring a suitable office renderer and Chinese fonts. The document builder does not perform that step. Inspect every rendered page, including figure captions, after changing layout or fonts.

## Reproducibility and interpretation

The accepted draft package records an actual all-figure replay, followed by a vascular-footer redraw through the shared rendering function. The final code also passed a separate runtime data-flow check; its mock images were excluded from the manuscript. The repository’s publication checks are documented in [VALIDATION.md](docs/VALIDATION.md).

Coordinates, input rows, denominators, effect estimates and correction families remain frozen. Zero and missing measurements retain their original definitions. The TNBC program panel reads the accepted source aggregate at its recorded precision. Composition, RNA programs, relative protein states, inferred spatial abundance and clinical gene-panel readouts are distinct measurements.

Hash checks establish input/output integrity. Byte-identical PDF/SVG output across operating systems is not guaranteed because fonts, metadata and rendering libraries can differ. These scripts reproduce presentation of the supplied analysis outputs; scientific re-estimation requires the upstream data and analysis workflows.

## Source and related records

- [Pancancer_log](https://github.com/XX-114514/Pancancer_log): methods and sanitized project execution records.
- Snapshot: accepted 2026-11-20 story v2 review package; source-code hashes in [CODE_PROVENANCE.tsv](docs/CODE_PROVENANCE.tsv).
- Exact graph/figure mapping: [FIGURES.md](docs/FIGURES.md).

No software license has been selected for this repository. The author should choose a license before representing these scripts as released under a specific open-source license. Author, funding, ethics and data-availability statements belong to the manuscript’s reviewed declarations.
