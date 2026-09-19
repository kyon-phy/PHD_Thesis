# Chapter 7 draft: source and author notes

Date: 15 September 2026.

The editable manuscript is `Chapters/CH7_event_selection.tex`. The preview reads this file directly, together with `Chapters/Appendix/Appendix2.tex` (multijet study, Appendix B) and `Chapters/Appendix/Appendix3.tex` (SR0b optimisation, Appendix C). Internal analysis documents guide the draft but are not cited in its prose, captions or bibliography.

## Source map

### Analysis definitions and SR1b optimisation

- `/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/sections/SR_Optimization.tex`: baseline selection, full scan grid, significance formula, 30% fractional background uncertainty, `b > 2` requirement, negative-weight prescription, optimisation benchmarks, cutflows and final SR1b cuts.
- `/Users/zang/Desktop/ICEPP/博士课题/leptoquark/paper_draft/ANA-EXOT-2025-06-PAPER/sections/selections.tex`: final four-region definitions, total jet multiplicities, common final tau threshold and one-bin treatment.
- The preselection table in this draft is explicitly the common starting selection for optimisation. The final `pT(tau) > 200 GeV` requirement remains in the final SR table because `pT(tau)` is scanned. The `N_b = 1` and `pT(b) > 50 GeV` requirements belong to the SR1b scan baseline, not the common zero-/one-b-jet preselection.
- `sections/object.tex` in the paper: baseline tau multiplicity uses Loose identification, with Tight required for the selected signal tau. At least one jet and the QCD cleaning are required. Object kinematic definitions are delegated to Chapter 6.

### Variables and the theory connection

- `/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/2111.04748v3.pdf`, Endo, Iguro et al., *Non-resonant new physics search at the LHC for the b -> c tau nu anomalies*, PDF pp. 3-4, 7-8 and 12: high-mT sensitivity, angular requirements, the additional b tag and jet-multiplicity restriction. Existing key `Endo2022NonResonant` is reused. Public identity and text checked at https://arxiv.org/html/2111.04748v3.
- Its proposed numerical cuts, object working points, tau/MET balance cut, detector simulation and statistical interpretation are not imported as this analysis's choices. Resonant selection and visible-mass threshold come from the analysis sources.
- `Chapters/CH3_LQ_search.tex`, Eqs. `eq:u1_current_expanded`, `eq:u1_beta_texture` and Section `subsec:lq_collider_benchmark`: established flavour current, beta indices and s-tau versus b-tau final states. Cross-referenced rather than deriving the flavour model again.
- The massless transverse-mass definition, on-shell-W bound under a correct single-W assignment, and visible-mass smearing are explained at the observable level. No claim is made that all SM events obey a W endpoint, or that a visible invariant mass equals the leptoquark mass.

### Significance reference

- The INT note cites `ATL-PHYS-PUB-2020-025`. The same original public reference, *Formulae for Estimating Significance*, has been added to `References/references.bib`.
- Public metadata verified at https://cds.cern.ch/record/2736148. The local copy `/Users/zang/Desktop/ICEPP/博士课题/leptoquark/papers/significance estimation.pdf` was read to verify Eq. (1), including the absolute background uncertainty. That local PDF carries an earlier circulation watermark, so the bibliography cites the public report identity rather than the local file.
- The draft explicitly uses `sigma_b = 0.30 b`, not an absolute uncertainty of 0.30 events, and distinguishes the optimisation ranking from the final likelihood and confidence limits.

### Efficiencies

- SR1b-Res cutflow benchmark: `(M_U, g_U, beta_L23) = (1.5 TeV, 1.5, 0.6)`, weighted baseline 35.2, selected 4.2, cumulative retention 11.9%.
- SR1b-NonRes cutflow benchmark: `(2.5 TeV, 2.5, 1.0)`, weighted baseline 111.0, selected 6.6, cumulative retention 5.9%.
- These are ratios to each benchmark's one-b-jet scan baseline. They are not generator-level acceptance times efficiency and are not efficiencies for an individual tau or b-tagging working point.
- The four `A epsilon` examples are taken from `ANA-EXOT-2025-06-PAPER-auxmat.tex`, table `tab:Accp_Eff_right_handed_comparison`, at the separate benchmark `(1.5 TeV, 1, 0.2)` with `beta_R33 = 0`: SR0b-Res 0.30%, SR0b-NonRes 0.13%, SR1b-Res 0.64%, SR1b-NonRes 0.069%. The source excludes interference from this efficiency table.
- Cross sections, generated decay modes and generator filters must have consistent conventions in `N_s = L sigma_s A epsilon`. No separate numerical acceptance or reconstruction efficiency has been inferred from the quoted products.

## SR0b and the user-confirmed decision

- The local source `sections/Appendices/SR0b_optimisation` in the INT directory has no filename extension and is not included by `sections/Appendix.tex`. It is a short supplementary draft, including an unresolved empty figure reference, not a completed scan report.
- It specifies the scan from 200 to 1500 GeV in 100 GeV steps, `(1.5 TeV, 0.5, 1.8)` and `(3.0 TeV, 2.0, 1.8)` benchmarks, maxima at 600 and 400 GeV, and an approximately 20% resonant significance improvement.
- User clarification in this task: **200 GeV is retained to align SR0b-Res with SR1b-Res; the MET > 600 GeV significance study belongs in an appendix.** This decision is reflected in Section 7.3 and the new Appendix C.
- The short scan source does not define its precise significance implementation, uncertainty model or handling of interference. Appendix C therefore reports its documented benchmark scan outcomes without claiming a new full likelihood optimisation, a 20% limit improvement or a verified all-benchmark optimum. No missing scan curve has been reconstructed or invented.

## QCD study

- Source: `sections/Appendices/QCDCleaningCut.tex` in the INT directory. The loose study selection is the MET trigger, one tau, no selected electron or muon, and at least one jet. It must not be confused with the full SR preselection or final cuts.
- The retained region is `DeltaPhi_min > 0.4 OR MET/pT(closest jet) > 6`. The rejected region requires **both** variables to be below their thresholds. The source's final scan caption has an inconsistent OR/sign description; the body, explicit numerator and nominal selection establish the intended logic, which is used in the draft.
- Rejection/retention at this stage: approximately 86% multijet rejection and 3.6% signal loss, hence 96.4% signal retention. They are sample-dependent study numbers, not universal efficiencies over the model grid.
- The source reports no simulated multijet events after full SR cuts. The draft states the finite-simulation scope explicitly and does not turn this into a measured zero rate, quantified upper limit or data validation.
- Z -> invisible plus a misidentified tau remains a separate source with genuine MET. The source's medium-but-not-tight tau cross-check is described as a simulation check.
- The signal panel of the two-dimensional distribution identifies `M_U = 1.5 TeV`; no unreported couplings or scan statistics are assigned to it.

## Figure provenance and checks

The seven PDFs are copied without modification to `Figs/CH7/`. Exact original paths and SHA-256 hashes are in `figure_manifest.json`.

- SR1b and SR0b: `figures/Aux/post_fit_plots/SR1b_Res_InvM.pdf`, `SR1b_NonRes_mT.pdf`, `SR0b_Res_InvM.pdf`, `SR0b_NonRes_mT.pdf` from the paper directory. These are the assets used in its main results figure.
- QCD: `figures/appendix/QCDCleaningCut/DPhi_signal.pdf`, `DPhi_multijets.pdf`, `rejection_scan.pdf` from the INT directory.
- All seven original figures were rendered and visually inspected. The SR plots say “Background-only fit”. The resonant visible-mass plots contain a red arrow at 800 GeV. The non-resonant mT plots display 600-1500 GeV and have no red arrow. The draft describes the actual displayed content rather than repeating the paper's generic caption that calls all panels N-1 distributions with arrows.
- The resonance and non-resonance signal curves correspond to `(1.5 TeV, 1.5, 0.6)` and `(3.0 TeV, 2.5, 1.0)`, respectively, as specified by the paper caption. The visible line style is dotted.
- Original ATLAS/Internal labels in source assets are retained. No internal note or own-analysis paper is cited in the thesis captions.

## Source differences not silently combined

- The INT optimisation text reports MC-statistical bounds of 31% and 40%, while the later paper says below 30%. The draft retains the directly documented `b > 2` scan requirement and does not claim a universal 30% MC-statistical bound. The separate assumed 30% background systematic uncertainty in the scan is retained.
- The INT text variously describes the visible-mass resolution as about 50% and about 500 GeV at 1.5 TeV. The draft describes a broad visible distribution without quoting an ambiguous fractional resolution.
- The source tables use `[50,250]` while their prose uses strict inequalities. The draft follows the prose `50 < pT < 250 GeV`; exact endpoint treatment has no practical distribution-level effect and was not independently inferred from configuration.

## Thesis depth and writing checks

Relevant event-selection material in all three reference theses was read: Aoki Chapter 7, Sugizaki Section 6.2, and Zhang Section 6.1. Only the shared practice of connecting physical signatures and background effects to definitions, then summarising selections in tables, was used. No distinctive prose or structure was copied.

The primary agent checked the assembled text for first use, source consistency, signal-efficiency denominators, QCD OR/AND logic, flavour interpretation, final SR definitions and figure conditions. Independent readers were not requested.

Build and visual-validation outcomes are recorded in `CH7_completion_notes.md` after final checks.
