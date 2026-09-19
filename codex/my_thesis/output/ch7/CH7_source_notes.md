# Chapter 7: revised source and author notes

15 September 2026. This revision follows the user's latest priority: use the internal note for detailed analysis studies, and the final taunub paper for disagreements. Neither is cited in the manuscript.

## Source map

- 7.1/7.2: INT sections/SR_Optimization.tex and reference-PDF Chapter 6, pp.28–36. The baseline block is Table 6.4 (the user's “6.4”). The scan grid is Table 6.1, the cutflows Tables 6.2–6.3, and the significance Eq.(6.1). The thesis uses the same Z expression with an absolute background uncertainty sigma_b=0.30b, rather than the INT's dimensionally ambiguous “sigma=30%”.
- Kinematic motivation: Endo, Iguro et al., arXiv:2111.04748v3, pp.3–4, 7–8, 12. Existing public key Endo2022NonResonant remains. Analysis cuts are not replaced by the phenomenology proposal.
- 16 September 2026 update: the variable-by-variable source check is recorded in Iguro_variable_motivations.md beside this file. Section 7.1.1 now motivates mT through sensitivity in the high-energy tail, following Eq.(2), Section 4.2 and Section 5 of Endo et al.; the previously added longitudinal-momentum explanation was general reconstruction reasoning, not the paper's stated search motivation. SR1b separates tau-pT, MET, mT, invariant-mass, angle and multiplicity explanations. Iguro's balance cut, charge selection and proposed model-discriminating angles are not imported into the analysis.
- Significance: the INT's original public reference ATL-PHYS-PUB-2020-025, Formulae for Estimating Significance, Eq.(1). Metadata and formula checked in the preceding draft at https://cds.cern.ch/record/2736148 and in the local reference PDF. Z is on the left, with the square root on the right, in one displayed line.
- Interference: INT Appendices/SignalValidation.tex, Interference_study.tex, reference-PDF §12.2 and Appendix N. Thesis Eq.(5.4) supplies the earlier SM–BSM decomposition. The scan uses pure BSM yields; the final excess contains S+I. Hard tau pT, MET and mT selections suppress interference in SR1b. Paper sections/results.tex controls the SR0b reduction: about 20% at 1.5 TeV and 30–40% at higher masses.
- SR0b: reference-PDF §12.1, pp.103–105. Leading s/c fractions are 30%/60% in Res and 33%/11% in NonRes for the stated truth benchmark. The c-jet contribution can contain a cν resonance. These are truth-selection fractions, not measured reconstructed-jet flavours. Chapter 3 supplies the flavour-current and coupling definitions.
- Final selections and efficiencies: paper sections/selections.tex and ANA-EXOT-2025-06-PAPER-auxmat.tex. Total jet limits are 4/2 for both flavour categories. Example Aε values come from the final auxiliary table.
- Background fractions: final auxiliary table tab:SR_VRW_yields_postfit, lines 105–142. The text explicitly identifies these as predictions after control-region constraints. W+jets fractions computed from the table are 70.6%/69.1% in SR1b Res/NonRes and 76.1%/82.2% in SR0b. Other rounded percentages use the same denominators. Process explanations follow INT Chapter 7 and paper sections/background.tex.
- Tau-pair study: reference-PDF §12.4, p.107 and Tables 12.1–12.3, pp.112/114. Available tau-pair samples have beta23=0, betaL33=1 and betaR33=0. Cross-section scaling retains their acceptance and shapes. Supplementary signal factors are 1.37, 1.33, 1.05, 1.07 for SR1b Res/NonRes and SR0b Res/NonRes. Coupling-limit examples 2.18→2.07 and 1.96→1.91 come directly from those tables. No new generation or exclusion fit was performed for this revision.
- QCD: INT Appendices/QCDCleaningCut.tex and its original three plots. The rejection-ratio formula uses AND, whereas the accepted region uses OR. The 86% QCD rejection and 3.6% signal loss apply to the loose study selection. Zero surviving simulated multijet events is not described as a measured zero rate.
- SR0b MET scan: local Appendices/SR0b_optimisation and reference-PDF Appendix N, pp.164–166. Scan range 200–1500 GeV, steps 100 GeV, with leading systematics. The approximately 20% significance gain is documented in the local appendix draft. The later PDF additionally discusses up to 30% changes in coupling-plane sensitivity at 1.5 TeV; that is a different quantity. The user-confirmed reason for the final 200 GeV choice is alignment with SR1b.

Reference PDF:
 /Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/ANA_EXOT_2025_06_INT1.pdf
Its printed date is 20 April 2026. Chapter 12 is more complete than the working-directory TeX/PDF.

## Figure provenance

The 12 loose SR1b plots cover the six variables of INT Figs.6.2–6.3. Two additional SR0b plots are used. Original EPS and companion prefit YAML files are in:
 /Users/zang/Desktop/fit_results/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots/

These are later stored EPS versions with merged W/Z backgrounds and the paper palette, not byte-identical copies of the older INT PDF panels. Postfit EPS files are not used. The companion prefit YAML arrays identify the numerical predictions as pre-fit, despite a stale “Background-only fit” EPS annotation. That annotation has been removed.

figure_manifest.json records exact paths, source/edited hashes, bin edges, original background yields, and protected drawing hashes. scripts/ch7/restyle_eps.py preserves the top-pad drawing through the last signal histogram, including all coordinates, fill paths, uncertainties, logarithmic axis and binning. It removes observed-data commands, data legend and ratio pad. The x labels move by exactly 259 drawing units to the retained axis. Page cropping at 65 pt does not change plot scale.

The sqrt(s) line moves to the original ATLAS baseline, with the original line spacing to the region line. Legend colours/names match the paper. Dimensionless dphi/njet plots use Events rather than the inherited incorrect Events / 100 GeV, with no rescaling. Lower-case phi is used. “Light jets” here means jets that are not b-tagged.

The SR0b NonRes mT file displays 600–1500 GeV even though its name contains N_minus_1. The caption describes this displayed range without claiming a below-threshold distribution.

The three QCD distribution/scan PDFs contain JPEG images. scripts/ch7/restyle_qcd_pdf.py uses PDF clipping to move existing label pixels and preserves image bytes. A render comparison gives zero changed pixels outside the declared label rectangles. See qcd_figure_manifest.json.

The fake-MET schematic from INT Figure C.1 is included in the main multijet-suppression subsection. Its two original panels, figures/appendix/QCDCleaningCut/signal.pdf and multiJets.pdf, are copied byte-for-byte to Figs/CH7/QCD/fake_met_signal.pdf and fake_met_multijets.pdf. They contain no data points, stacked histograms or ATLAS label and require no restyling. The fake-MET mechanism and combined angular/ratio requirement are explained in the main text; the loose selection, two-dimensional distributions, scan, efficiencies and residual-background checks remain in the appendix. The cut was cross-checked against paper sections/object.tex: reject events with both minimum angle below 0.4 and momentum ratio below 6.

## Source discrepancies retained for the author

1. The old INT reports 31%/40% MC-statistical bounds; the paper says below 30%. The thesis uses the paper for the final analysis and labels the older cutflow as an optimisation study. The assumed 30% systematic in Z is a separate quantity.
2. INT §12.4/Table 12.1 label the high-mass tau-pair cross-section ratio beta23=1.0, but the comparison-column header says 1.4. Tau-pair and tau-nu gU values also differ slightly. The thesis uses the documented approximate method, directly stated fit factors and limit examples; it does not reproduce the inconsistent raw-yield table or assert a newly verified beta-dependent efficiency.
3. The local SR0b draft reports maximum 20% improvement without a complete plot. The later PDF separately discusses coupling limits and interference. The final MET threshold follows the paper and the user's alignment explanation.
4. Visible-mass resolution is described inconsistently as 50% and 500 GeV at 1.5 TeV. The thesis explains a broad visible mass without adopting the ambiguous fraction.
5. Final selection prose uses strict inequalities while some source tables use interval brackets. No implementation claim about exact endpoints is inferred.

## Obsidian

Updated through obsidian_agent with version checks and read-back:
9_Scripts/B-anomaly favoured region计算与绘图.md

Added “INT Chapter 6 的计算逻辑与 Results 写作入口（2026-09-15 核对）”: C/CLL mapping, the historical 90% interval and reference-beta ambiguity, final 1σ/2σ convention, and fixed-mass/fixed-beta boundaries. Existing code-snapshot evidence and the missing precise extraction record of CLL endpoints remain explicitly qualified. No current remote-code verification is claimed.

Independent readers were not requested and were not run.
