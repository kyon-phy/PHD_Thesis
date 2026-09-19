# Physics Verification Checklist

This is a verification checklist, not a list of material that must appear in
every paragraph. Apply only the checks relevant to the requested passage.

## \(U_1\) theory and flavour

- Verify the \(U_1\) gauge representation, electric charge, interaction
  convention, and chirality rather than assuming them from the particle name.
- State the flavour basis and explain both indices of each \(\beta\) coupling.
- Track the \(SU(2)_L\) doublet structure and CKM rotation explicitly. Prefer
  terms such as \(V_{cs}\beta_L^{23}\) and
  \(V_{cb}\beta_L^{33}\) to vague phrases such as "CKM-related effects".
- Check how \(\beta_L^{23}\), \(\beta_L^{33}\), and
  \(\beta_R^{33}\) enter the low-energy \(b\to c\tau\nu\)
  amplitude, collider production, decays, widths, and branching fractions.
- Explain the relation to \(R(D^{(*)})\) without implying that a motivated or
  compatible parameter point is experimentally established.
- Preserve the analysis convention for vector-leptoquark gauge couplings and
  any Yang-Mills or minimal-coupling assumptions; do not import another
  convention silently.
- Check coupling and mass scaling, approximation regime, width assumptions,
  and whether an EFT description is valid for the stated kinematics.

## Collider signal

- Distinguish resonant on-shell or single production, non-resonant
  \(t\)-channel exchange, and pair production. Do not use one topology's
  interpretation for another.
- Identify the initial-state flavour, leptoquark decay, visible objects, and
  neutrino source for the final state under discussion.
- Relate each topology to its characteristic observable, such as a
  reconstructed leptoquark-mass structure or the high-\(m_{\mathrm T}\) tail.
- Check Standard Model interference, including its sign, phase-space
  dependence, and coupling scaling. Do not assume a purely positive
  signal-strength or simple \(\beta^2\) scaling when interference is included.

## Simulation, detector, and objects

- Before generator details, establish the Monte Carlo chain:
  PDFs -> hard-scattering matrix element -> parton shower -> hadronisation and
  decays -> detector simulation -> reconstruction and comparison with collision data.
  Check event weights where their concrete use is discussed, not as mandatory
  content in the overview.
- For each reconstructed object, distinguish the physical particle, detector
  signature, reconstruction, identification or calibration, and the final
  analysis definition.
- Treat missing transverse momentum as a reconstructed transverse vector.
  Distinguish it from its magnitude and from the physical invisible particles
  that produce genuine momentum imbalance.
- Check hadronically decaying tau-lepton reconstruction and identification,
  b-tagging, jets, overlap removal, calibration, and working points at the
  depth relevant to the analysis.
- Separate truth-level, particle-level, detector-level, and reconstructed
  quantities.

## Analysis methodology and backgrounds

- For each selection or category, connect signal physics, characteristic
  observable, selection, background effect, and expected sensitivity.
- Treat the 0b category as genuine \(U_1\to s\tau\) signal sensitivity when
  large \(\beta_L^{23}\) enhances that decay. Do not describe it solely as
  b-tag inefficiency or a light-jet proxy.
- Explain non-obvious cuts physically; a cut table is not a substitute for the
  signal-topology argument.
- For each control or validation region, identify the target background,
  enrichment mechanism, relation to the signal region, information transfer,
  and validation or fitted consequence.
- Distinguish normalisation from shape effects, experimental from theoretical
  uncertainties, statistical from systematic uncertainties, and pre-fit from
  post-fit quantities.
- Check whether a background is simulation-based, data-driven, or hybrid, and
  state what is constrained by data.

## Statistics and results

- Establish the inference goal before presenting software or fit settings.
- Verify the likelihood construction, Poisson terms, signal and background
  expectations, signal-strength parameter, nuisance parameters and
  constraints, control-region correlations, profiling, and test statistic.
- Check how signal-SM interference and coupling-dependent templates enter the
  likelihood and limit interpretation.
- Explain fit types, p-values, \(CL_s\), expected and observed limits, and
  Asimov datasets precisely when they are first needed.
- Do not describe a nuisance parameter as "constrained" without distinguishing
  a genuine data constraint from an arbitrary prior range or modelling choice.
- Use restrained result language and preserve the distinctions among
  "excluded", "constrained", "favoured", "compatible with", "motivated by",
  and "can explain".
