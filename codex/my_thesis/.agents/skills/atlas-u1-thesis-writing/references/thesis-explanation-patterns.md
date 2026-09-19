# Thesis-Level Explanation Patterns

Use these patterns flexibly. Do not repeat a stage that has already been
established clearly in the same chapter. Central topics normally require the
full chain; necessary context needs a compact self-contained version;
peripheral material should be brief or cited.

## Reader model and first use

Assume graduate-level physics knowledge, but not specialist knowledge of ATLAS,
collider or flavour physics, leptoquarks, Monte Carlo simulation,
reconstruction, or profile-likelihood inference.

At first necessary use, prefer:

1. definition;
2. physical mechanism;
3. observable or experimental consequence;
4. relevance to this analysis; and
5. implementation detail, only if needed.

Afterwards use the standard term without redefining it. Introduce concepts
before software names, working points, acronyms, or ATLAS-specific jargon.

## Selectable patterns

### Important equation

Why the equation is introduced -> equation -> new symbols and convention ->
relevant term or scaling -> physical consequence.

Derive only what supports the later argument. Do not present an equation
without explaining what the reader should learn from it.

### Detector subsystem

Measured quantity -> physical principle -> detector technology -> relevant
performance -> analysis relevance.

Emphasise systems that materially affect tau leptons, jets, b-tagging, missing
transverse momentum, triggers, or the dominant uncertainties. Avoid a hardware
inventory detached from the analysis.

### Monte Carlo simulation

Role of simulation -> PDFs -> hard-scattering matrix element -> parton shower
-> hadronisation and decays -> detector simulation -> reconstruction and comparison
with collision data. Introduce concrete generator configurations afterwards.
Discuss event weights only where their inputs and use are explained.

### Reconstructed object

Physical particle -> detector signature -> reconstruction -> identification or
calibration -> analysis definition and relevant performance.

### Selection or category

Signal physics -> characteristic observable -> selection or category ->
background effect -> sensitivity.

Explain the topology before listing detailed cuts. A selection table should
summarise an argument already made in the prose.

### Control or validation region

Target background -> enrichment mechanism -> relation to the signal region ->
information transfer -> validation purpose or fitted consequence.

### Statistical inference

Inference goal -> likelihood -> Poisson counts -> signal and background
expectations -> signal strength -> nuisance parameters and constraints ->
control-region correlations -> profiling -> profile-likelihood test statistic
-> fit types -> p-values and \(CL_s\) -> implementation in TRExFitter or
RooFit.

### Figure or table

Analytical purpose -> feature the reader should notice -> physical or
statistical implication.

The surrounding prose must interpret the important feature. A caption may
describe the content but should not carry the entire argument.

## Using the reference dissertations

Use the three reference ATLAS dissertations only to identify explanatory
practices common to all three: what background a broader physics reader needs,
the order in which concepts are introduced, and approximate depth. Do not infer
a preferred rule from a feature found in only one thesis unless the user asks
to use that thesis as a specific example.

Never imitate an individual dissertation's wording, sentence structure,
distinctive organisation, emphasis, or writing voice.

## Depth control

- Give greatest depth to \(U_1\) flavour structure, the relevant \(\beta\)
  couplings, CKM rotation, \(b\to c\tau\nu\), resonant and non-resonant
  production, tau reconstruction and identification, b-tagging, missing
  transverse momentum, background estimation, and profile-likelihood
  statistics.
- Keep unused derivations, peripheral detector engineering, software mechanics,
  and configuration details brief unless they affect the analysis or an
  uncertainty.
- Prefer a concise citation over a textbook digression that does not support a
  later argument.
- The target is not maximum detail. Every important step should make clear what
  it is, why it happens, why it matters here, and what follows from it.
