# PanCancer preprint v3 code

This directory contains the figure and supplementary-table scripts shipped with the 2026-11-28 manuscript. The repository root also retains the earlier November 20 figure release.

| Component | Entry point | Input and scope |
| --- | --- | --- |
| Figure 1 | `render_figure1_hd.py` | Frozen atlas coordinates, identity map, marker summary, source registry, resource configuration and author artwork. See `--help`. |
| Figure 1 earlier renderer | `render_figure1.py` | Same frozen atlas inputs with its own schematic renderer. |
| Figure 2 labels | `legacy_v1/relabel_fig2.py` | Existing Figure 2 PDF and output PDF. |
| Figures 3, 4, 6 and S1 | `legacy_v1/make_figs.py` | Frozen run outputs rooted at `TFINE_ROOT`. Figure 3 includes a synthetic scaling demonstration. |
| Figure 5 | [R4 figure renderer](../scripts/plotting/render_R4_portable.py) | Prior vascular panels and qualified spatial summaries. The manuscript reuses these panels in its own layout. |
| Tables S1 and S2 | `legacy_v1/make_supp_tables.py` | Arguments are project log checkout, frozen T-cell run directory and output directory. |
| Table S3 | `render_figure1.py` | Identity mapping emitted by the Figure 1 workflow. |
| Historical document build | `assemble_preprint_v3.py`, `legacy_v1/md2docx.py` | Earlier assembly workflow preserved for provenance. The assembly script still emits v2 filenames. |

Install the plotting and document requirements at the repository root. The legacy scripts additionally require SciPy, scikit-learn and PyMuPDF. See `requirements-legacy.txt`.

The scripts use qualified companion inputs identified in their entry points. Cell-level and patient-level input tables, original artwork, manuscript files and fitted objects are distributed separately according to the manuscript's availability statement. The plotting scripts reproduce presentation from frozen outputs when the matching inputs are available. The full upstream analysis is documented in [Pancancer_log](https://github.com/XX-114514/Pancancer_log).

No software license or archival DOI is declared for this snapshot.
