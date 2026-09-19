# Trigger figure sources

These are unmodified vector PDF figures downloaded from the original ATLAS
publication pages on 6 September 2026. The local reference library is unchanged.

- `trigger_electron_efficiency.pdf`: TRIG-2018-05, Figure 17(a),
  https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/TRIG-2018-05/fig_17a.pdf
  (`ATLASElectronTriggerRun2`, arXiv:1909.00761).
  This is also the plot shown in Aoki's thesis, Figure 5.4 (printed page 59).
- `trigger_muon_efficiency_barrel.pdf` and `trigger_muon_efficiency_endcap.pdf`:
  TRIG-2018-01, Figures 14(a,b),
  https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/TRIG-2018-01/fig_14a.pdf
  and https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/TRIG-2018-01/fig_14b.pdf
  (`ATLASMuonTriggerRun2`, arXiv:2004.13447).
  These are also the plots shown in Aoki's thesis, Figure 5.5.
- `trigger_met_efficiency.pdf`: TRIG-2019-01, Figure 10(a),
  https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/TRIG-2019-01/fig_10a.pdf
  (`ATLASMETTriggerRun2`, arXiv:2005.09554).

The lepton figures measure trigger OR combinations, not isolated low-threshold
chains. The MET figure uses Z-to-dimuon events and dimuon pT as its horizontal
variable; it is not an analysis-specific SR efficiency measurement.

The HLT table in CH5 is a source-based reference menu, not a completed audit of
analysis code. Source PDFs are in `codex/references/triggers/`:
`Atlas_LowestUnprescaled.pdf` (PDF pages 49, 61, 70-72, 77-78), and
`Atlas_RecommendedMetTriggers2015.pdf`, `Atlas_RecommendedMetTriggers2016.pdf`,
`Atlas_RecommendedMetTriggers2017.pdf` (the last also covers 2018).
The 2015 MET variant, early-2016 lepton choices, and high-threshold lepton ORs
still need confirmation against the analysis configuration. No OR or exact
chain choice is inferred merely from the reference performance figures.
