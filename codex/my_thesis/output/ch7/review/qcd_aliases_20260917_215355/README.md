# QCD cleaning aliases

## New macros

```latex
\newcommand{\minDphiJetMet}{\ensuremath{\min\DphiJetMet}\xspace}
\newcommand{\metOverMinDphiJetPt}{\ensuremath{\frac{\met}{\minDphiJetPt}}\xspace}
```

The first macro prints the minimum jet--MET angular separation. The second prints the MET-to-closest-jet-pT ratio as a fraction. Thresholds remain outside these variable macros, permitting their reuse in prose and scans. `\ensuremath` permits use in text or math mode; `\xspace` supplies a following space when appropriate. `\frac` replaces the previous inline slash in prose and the selection table and keeps the existing stacked fraction in the display equation.

## Updated existing macros

```latex
\newcommand{\DphiJetMet}{\ensuremath{\Delta\phi(\met,\pt^{\mathrm{jet}})}\xspace}
\newcommand{\minDphiJetPt}{\ensuremath{\pt^{\mathrm{jet}(\min{\Delta\phi)}}}\xspace}
```

Both use `\pt` and upright `\mathrm{jet}`. The angle follows the user's MET-first convention. `\pt` is the existing alias for `\pT`, so its physical meaning and displayed transverse-momentum symbol are unchanged.

## Chapter usage

```latex
\minDphiJetMet>0.4 \quad\text{or}\quad \metOverMinDphiJetPt>6.
```

CH7 uses the aliases in the variable discussion, cleaning equation and selection table. The thresholds and logical OR are unchanged; no scientific prose was rewritten. The manuscript reference label and table/figure numbering commands are unchanged. The project writing skill and a user-authorised memory update note record the preference.

## Verification

The chapter preview compiled successfully and the revised equation and table pages were visually checked. The final log has no undefined references or commands. An overfull hbox of 4.86186 pt is reported in the signal-benchmark paragraph (source lines 108--111), outside the edited QCD text. Existing template warnings remain. The user's concurrent edit to the signal-benchmark opening was preserved; it appears in the before/after snapshot diff but was not made by this task.

The output was updated at `output/pdf/CH7_draft.pdf` (22 pages). No full thesis PDF was rebuilt.
