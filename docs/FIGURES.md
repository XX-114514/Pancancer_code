# Figure map

The final figure IDs below are assembled by `run_all_figures.py`. Intermediate names retain the branch renderer’s original numbering. Figure IDs belong to the 2026-11-20 draft.

| Manuscript figure ID | Renderer | Intermediate figure ID | Argument role |
|---|---|---|---|
| `Figure1_resolved_atlas` | `render_R4_portable.py` | `Figure2_unified_atlas` | Establish cellular identities and quantitative marker support |
| `Figure2_composition_landscape` | `render_composition_and_LN.py` | `Figure3_composition_landscapes` | Show recurring composition and its measurable robustness |
| `Figure3_immune_state_combination` | `render_story_panels.py` | `Figure3_immune_state_combination` | Connect a stable T-cell composition core to state organization |
| `Figure4_immune_clinical_readouts` | `render_story_panels.py` | `Figure4_immune_clinical_readouts` | Establish the clinical association of a fixed immune phenotype |
| `Figure5_lymph_node_organization` | `render_composition_and_LN.py` | `Figure5_T_state_spatial_context` | Locate the immune state question in an explicit tissue setting |
| `Figure6_vascular_architecture` | `render_R4_portable.py` | `Figure4_spatial_organization` | Demonstrate repeated vascular architecture across spatial sections |
| `Figure7_cancer_context` | `render_story_panels.py` | `Figure7_cancer_context` | Define cancer-specific immune context for the vascular readout |
| `FigureS01_source_coverage` | `render_R4_portable.py` | `FigureS01_complete_source_coverage` | Establish the source denominator |
| `FigureS02_annotation_dotplot` | `render_R4_portable.py` | `FigureS02_annotation_dotplot` | Support identity interpretation |
| `FigureS03_module_networks` | `render_R4_portable.py` | `FigureS03_all_module_networks` | Show complete module membership |
| `FigureS04_source_cancer_coordinates` | `render_R4_portable.py` | `FigureS04_source_and_cancer_embedding` | Show sampling context in the embedding |
| `FigureS05_spatial_denominators` | `render_R4_portable.py` | `FigureS05_spatial_denominator_sensitivity` | Resolve the vascular pair from broader module structure |
| `FigureS06_identity_key` | `render_R4_portable.py` | `FigureS10_full_identity_UMAP` | Link atlas colors to exact identities |
| `FigureS07_immune_atlas` | `render_story_panels.py` | `FigureS07_immune_atlas` | Define the immune discovery resource |
| `FigureS08_T_state_dimensions` | `render_story_panels.py` | `FigureS08_T_state_dimensions` | Disentangle identity and state variation |
| `FigureS09_prediction_information` | `render_story_panels.py` | `FigureS09_prediction_information` | Distinguish clinical association from added prediction information |
| `FigureS10_source_composition` | `render_composition_and_LN.py` | `FigureS14_legacy_source_contexts` | Preserve cancer-specific composition scope |
| `FigureS11_imaging_neighborhoods` | `render_R4_portable.py` | `Figure5_imaging_neighborhoods` | Provide cell-neighborhood measurements of the vascular relationship |
| `FigureS12_molecular_context` | `render_composition_and_LN.py` | `Figure8_communication_across_designs` | Distinguish composition, LR expression and differential association |

Every assembled figure is exported as PNG, PDF and SVG. The manifest records 57 output-file hashes. The R4 and composition branches also render intermediate panels outside the final manuscript selection; these remain in `intermediate/` with their source tables and logs.

For exact package-relative inputs, see [FIGURE_INPUT_MAP.tsv](FIGURE_INPUT_MAP.tsv). This file contains input locations and measurement scope, not research observations.
