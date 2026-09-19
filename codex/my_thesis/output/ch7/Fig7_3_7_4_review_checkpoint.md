# Fig. 7.3 / 7.4 review checkpoint

Status (2026-09-20): completed. Both Res and NonRes now use noWeights_BSM and the same benchmark parameters as their cutflows: (1.5 TeV, 1.5, 0.6) and (2.5 TeV, 2.5, 1.0). Fig. 7.4 was updated from 3.0 to 2.5 TeV in all six signal curves, legend labels and its caption. Res EPS/PDF files are byte-identical to the previous version; all NonRes EPS content except signal path and mass label is byte-identical. Backgrounds, uncertainties and paper L-shaped arrows are preserved. CH7 compiled to 22 pages; Fig. 7.4 is on page 10.

The user asked which component gives yields closer to the historical cutflow, with one component used consistently in both regions. At full SR selection, Res BSM=4.208596 and combined=4.092040 versus cutflow 4.2; NonRes BSM=7.167700 and combined=5.619347 versus cutflow 6.6. BSM is closer in both regions and matches the BSM-only definition of the original cutflow. The MU2500 combined value is explicitly calculated from BSM + inf; this exact production directory has no MU2500 combined ROOT file. The MU1500 saved comb file was verified against that sum. Details: `figure_audit/bsm_vs_combined_cutflow.json`.

Current signal bin provenance: `figure_audit/bsm_signal_bins.json`. Current full/loose SR integrals: `figure_audit/cutflow_comparison.json`. Previous 3.0 TeV version is backed up under `figure_audit/before_nonres_2500/`. Known remaining issue from the verification: the nlightjets and dphi loose configurations also remove the b-jet pT cut, which the current captions do not mention. Their selection has not been changed. Eight raster INT-note panels still lack exact historical numerical-source provenance.

Historical pause: the account usage tool had reported 99% used in the weekly window. No figure edits had been made at that checkpoint. On resumption the allowance had reset; no reset credit was consumed.

## User's requested work

1. Reorder the upper-right legend into two columns, starting with U1 in the upper-left cell; remove the empty upper-left legend cell.
2. Identify whether the plots ultimately come from ROOT or PDF/EPS. Compare all background and signal bin values and their relative positions against INT note Figs. 6.2 and 6.3. If any differ, identify the cause. Tell the user the precise source paths.
3. Audit the uncertainty bands, particularly thesis Fig. 7.3(f) versus the last panel of INT Fig. 6.2. Determine from files/configuration whether statistical and/or systematic uncertainties are included. The user expects INT bands to be statistical only, but this remains a hypothesis to verify. If both are statistical-only, explain the differing band sizes from the actual inputs/transforms.
4. Mark the SR variable cuts with red arrows like the INT note and describe the red arrows in the captions. Determine which final cuts apply to each variable and the arrow direction. Do not invent a cut where none is applied.
5. Move the Events y-axis title to the top for the light-jet multiplicity and delta-phi plots, matching the other panels and paper style.
6. Match subfigure labels to the actual x-axis notation, including tau_had rather than tau where the axes use it. Check exact superscript/subscript and upright had convention from the actual plots/paper.

## Important constraints

- Match taunub-paper background colours, process names, notation, and axis-title sizes/alignment.
- Preserve every histogram bin, stack height, signal value and uncertainty value during purely stylistic edits. If the audit identifies a genuine source/data error, document the cause and correction explicitly; never silently adjust curves to make them resemble the note.
- No data points in CH7. Remove empty Data/Bkg lower panels when present.
- No ATLAS Internal line; retain sqrt(s) and region labels at the established spacing/positions.
- Default figure placement is [htpb]. Use existing aliases for quantities and units.
- Caption pattern: `The red dashed line represents the signal at $(\MU,\gU,\beta_L^{23})=(1.5~\TeV,1.5,0.6)$.` Respect the user's chosen style. No repeated N-1 definition. Use `N-1 distributions in the loose SR1b-Res/NonRes region` with the existing macros.
- Preserve the user's concurrent edits: reload the current TeX/scripts before each targeted change. This directory is now inside the Git repository rooted at `Thesis`; the earlier non-Git description is obsolete. Do not edit references, INT note or paper source files.
- Pause and save another checkpoint if the user-requested quota condition is reached again. Do not consume reset credits without an explicit user request.

## Files already located

Editable chapter:
`Chapters/CH7_event_selection.tex`

Figure blocks currently use:
`Figs/CH7/SR1b_Res_{InvM,met,mT,tau_pT,nlightjets,dphi}.pdf`
`Figs/CH7/SR1b_NonRes_{InvM,met,mT,tau_pT,nlightjets,dphi}.pdf`

Labels:
`fig:ch7_sr1b_res_distributions`
`fig:ch7_sr1b_nonres_distributions`

Latest available compiled preview:
`output/ch7/build/CH7_preview.pdf`
Stable delivered copy:
`output/pdf/CH7_draft.pdf`
Check the .aux to confirm current figure numbering. The latest caption/prose edits may postdate the PDF.

Potential production/provenance files discovered, NOT YET inspected in this turn:
`scripts/ch7/restyle_eps.py`
`scripts/ch7/restyle_qcd_pdf.py`
`scripts/ch7/validate_yields_and_scan.py`
`output/ch7/CH7_completion_notes.md`
`tmp/ch7_plot_deps/` contains pypdf and other plotting dependencies.

INT note source:
`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/sections/SR_Optimization.tex`
Its resonance/non-resonance figure includes are around lines 129-143 and the corresponding later NonRes figure block; inspect the current source for exact filenames. Resonance originals previously referenced `figures/SR_Optimization/resonance_plots/SR_1tau0l1b_loose_sch_*_N_minus_1_*.pdf`.

EPS/fit-result root:
`/Users/zang/Desktop/fit_results`

Paper root:
`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/paper_draft/ANA-EXOT-2025-06-PAPER`
Paper figures:
`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/paper_draft/ANA-EXOT-2025-06-PAPER/figures`

The output format being PDF does not establish whether the upstream data were ROOT, YAML or EPS. Read the production script and provenance before drawing that conclusion.

## Historical resumption plan (completed)

1. Check usage and resume only when authorised and sufficient quota is available.
2. Read restyle_eps.py and CH7_completion_notes.md, then locate exact input EPS/PDF, any associated ROOT/YAML and uncertainty configuration.
3. Establish a per-panel provenance and quantitative comparison record. Compare bin edges, normalisation, signal benchmark/couplings, signal scaling factors, bin-width normalisation, loose cuts and N-1 selection, and statistical versus systematic errors. Check transforms/cropping have not shifted or rescaled content.
4. Inspect rendered source and output plots, especially delta-phi, together with the numerical inputs. Keep hypotheses separate from verified findings.
5. Modify the reproducible plotting/restyling path, verify numerical invariants, then update the two caption blocks and subfigure labels with minimal changes.
6. Compile CH7, render the revised figure pages, verify all requested layout changes, and deliver the provenance/uncertainty findings plus the updated PDF.

## Build / tools

Known working build from thesis root:
`/Library/TeX/texbin/latexmk -norc -pdf -cd- -interaction=nonstopmode -halt-on-error -synctex=1 -outdir=output/ch7/build output/ch7/CH7_preview.tex`

Ghostscript: `/usr/local/bin/gs`. Use png16m when rendering; pngalpha produced black artefacts in earlier work.
Python: `/Users/zang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` (pypdf/pdfplumber available; check plotting dependencies).

Applicable skills already read: project/global writing skills, source-routing.md, PDF skill at `/Users/zang/.codex/plugins/cache/openai-primary-runtime/pdf/26.909.12148/skills/pdf/SKILL.md`. The PDF artifact marker has NOT been run in this turn because no authoring has begun. Run it once immediately before PDF authoring, with edit/count/format appropriate to the actual deliverable, then render and inspect. Use code/vector tools for these scientific plots; do not alter data with generative image editing.
