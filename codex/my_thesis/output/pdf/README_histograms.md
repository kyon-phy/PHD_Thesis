# Loose-SR histograms

Final figures: `loose_nonresonance_met` and `loose_resonance_mbtau`, each in
vector PDF, editable SVG, and 4800 × 3060 pixel PNG (600 dpi).
The `_preview.png` files are smaller previews.

The full-precision bin values come from the corresponding TRExFitter
`*_prefit.yaml` files in `/Users/zang/Desktop/fit_results`. Their complete paths
and SHA-256 hashes are recorded in `histogram_validation.json`. The supplied
`*_source.yaml` copies are byte-identical to these sources.

All nine background components, signal yields, total background yields and
upper/lower uncertainties are preserved without smoothing, rebinning,
normalisation or division by bin width. The bin edges are 0, 200, ..., 1600 GeV.
The y axis remains logarithmic from 0.1 to 100 events. Values below the frame
remain in the source data. The visible signal trace retains the original ROOT
plot convention of lying on the lower frame when the signal is below it.

The source PDFs' total-background vector paths were independently checked
against the YAML values. Their maximum relative discrepancies are less than
0.002%, consistent with the original PDF's rounded drawing coordinates.
The new figures use the full-precision YAML values, not those rounded paths.
The plotted background component heights and unchanged numerical arrays are
checked by the generation script. The exported PDFs contain no raster images.

The labels, legend order, selection thresholds, and axis limits follow the
supplied screenshots. The lower ratio panels are removed. Axis titles follow
Figure 4 and Figure 9 of the local tau-nu-b paper draft
`ATL-COM-PHYS-2026-015.pdf` (26 May 2026).

The revised typography uses 14 pt axis numbers, 16 pt axis titles, 13 pt legend
text, and approximately 13 pt upper-left labels. The five label rows share a
compact 16 pt baseline spacing. The top-background legend entries are now
`single t` and `t` with the second `t` barred, following the paper's notation.
The enlarged text is checked for label/legend overlap and edge clipping.

Colours for ttbar, single top and diboson match that paper. The paper's W+jets
and Z+jets colours are assigned to Wtaunu and Znunu, respectively, while the
separate decay channels remain separate. The remaining colours are drawn from
the [ATLAS MPL colour definitions](https://atlas-mpl.readthedocs.io/en/latest/colors.html).
The exact mapping is in the generation script and validation record.

To reproduce, run `regenerate_histograms.py` with Python, NumPy, Matplotlib,
and PyYAML. Source PDFs can additionally be inspected with PyMuPDF.
