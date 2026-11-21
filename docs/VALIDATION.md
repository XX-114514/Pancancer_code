# Publication validation

This snapshot preserves the seven source scripts byte for byte. The checks below validate packaging and command availability; they do not re-estimate scientific results.

- Parse each script as Python and run its `--help` entry point.
- Match all seven SHA256 values against `CODE_PROVENANCE.tsv` and the frozen draft source.
- Check repository-relative Markdown links and the 19-entry figure map.
- Review tracked files for accidental credentials, private input files, scientific tables, arrays and rendered outputs.
- Run the input verifier against the matching private draft package.

The original private draft acceptance records cover the complete figure replay. A full re-render on every platform is separate from the publication checks. Fonts, renderer versions and PDF/SVG metadata can affect output bytes.

## 2026-11-21 publication receipt

All seven scripts passed Python parsing and `--help` execution in the local Python 3.12 validation runtime, with matplotlib 3.10.8 and NetworkX 3.4.2 supplied in an isolated task directory. This was a command-entry check, not a recreation of the original full plotting environment. All seven frozen source hashes matched. Relative documentation links passed. The matching external package verifier reported `INPUT_MANIFEST_VERIFIED 96`. No rendered figures, input arrays, private scientific tables or manuscript content were included in this repository.
