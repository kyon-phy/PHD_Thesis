# --------------------------------------------------------
#  Triggers
# --------------------------------------------------------
datataking_years = ['2015','2016','2017','2018','2022','2023','2024']

trig_singleEle={
    '2015': ['HLT_e24_lhmedium_L1EM20VH || HLT_e60_lhmedium || HLT_e120_lhloose'],
    '2016': ['HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0'],
    '2017': ['HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0'],
    '2018': ['HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0'],
    '2022': ['HLT_e26_lhtight_ivarloose_L1EM22VHI || HLT_e60_lhmedium_L1EM22VHI || HLT_e140_lhloose_L1EM22VHI'],
    '2023': ['HLT_e26_lhtight_ivarloose_L1eEM26M || HLT_e60_lhmedium_L1eEM26M || HLT_e140_lhloose_L1eEM26M'],
    '2024': ['HLT_e26_lhtight_ivarloose_L1eEM26M || HLT_e60_lhmedium_L1eEM26M || HLT_e140_lhloose_L1eEM26M'],
}
trig_diMuon = {
    '2015' : ['HLT_mu18_mu8noL1'],
    '2016' : ['HLT_mu22_mu8noL1'],
    '2017' : ['HLT_mu22_mu8noL1'],
    '2018' : ['HLT_mu22_mu8noL1'],
    '2022' : ['HLT_mu22_mu8noL1_L1MU14FCH'],
    '2023' : ['HLT_mu22_mu8noL1_L1MU14FCH'],
    '2024' : ['HLT_mu22_mu8noL1_L1MU14FCH'],
    }
trig_diEle = {
    '2015' : ['HLT_2e12_lhloose_L12EM10VH'],
    '2016' : ['HLT_2e17_lhvloose_nod0'],
    '2017' : ['HLT_2e24_lhvloose_nod0'],
    '2018' : ['HLT_2e24_lhvloose_nod0'],
    '2022' : ['HLT_2e24_lhvloose_L12EM20VH'],
    '2023' : ['HLT_2e24_lhvloose_L12eEM24L'],
    '2024' : ['HLT_2e24_lhvloose_L12eEM24L'],
    }
trig_EleMu = {
    '2015' : ['HLT_e17_lhloose_mu14'],
    '2016' : ['HLT_e17_lhloose_nod0_mu14'],
    '2017' : ['HLT_e17_lhloose_nod0_mu14'],
    '2018' : ['HLT_e17_lhloose_nod0_mu14'],
    '2022' : ['HLT_e17_lhloose_mu14_L1EM15VH_MU8F'],
    '2023' : ['HLT_e17_lhloose_mu14_L1eEM18L_MU8F'],
    '2024' : ['HLT_e17_lhloose_mu14_L1eEM18L_MU8F'],
    }

trig_singleMuon={
    '2015': ['HLT_mu20_iloose_L1MU15 || HLT_mu40'],
    '2016': ['HLT_mu26_ivarmedium || HLT_mu50'  ],
    '2017': ['HLT_mu26_ivarmedium || HLT_mu50'  ],
    '2018': ['HLT_mu26_ivarmedium || HLT_mu50'  ],
    '2022': ['HLT_mu24_ivarmedium_L1MU14FCH || HLT_mu50_L1MU14FCH'  ],
    '2023': ['HLT_mu24_ivarmedium_L1MU14FCH || HLT_mu50_L1MU14FCH'  ],
    '2024': ['HLT_mu24_ivarmedium_L1MU14FCH || HLT_mu50_L1MU14FCH'  ],
}

trig_tauMu={
    '2015' : ['HLT_mu14_iloose_tau25_medium1_tracktwo || HLT_mu14_tau25_medium1_tracktwo'],
    '2016' : ['HLT_mu14_tau25_medium1_tracktwo || HLT_mu14_ivarloose_tau25_medium1_tracktwo'],
    '2017' : ['HLT_mu14_ivarloose_tau25_medium1_tracktwo'],
    '2018' : ['HLT_mu14_ivarloose_tau25_medium1_tracktwoEF'],
    '2022' : ['HLT_mu14_ivarloose_tau35_mediumRNN_tracktwoMVA_03dRAB_L1MU8F_TAU20IM'],
    '2023' : ['HLT_mu14_ivarloose_tau35_mediumRNN_tracktwoMVA_03dRAB_L1MU8F_TAU20IM'],
    '2024' : ['HLT_mu14_ivarloose_tau35_mediumRNN_tracktwoMVA_03dRAB_L1MU8F_cTAU30M'],

}

trig_tauEle={
    '2015' : ['HLT_e17_lhmedium_nod0_tau25_medium1_tracktwo || HLT_e17_lhmedium_nod0_iloose_tau25_medium1_tracktwo'],
    '2016' : ['HLT_e17_lhmedium_nod0_tau25_medium1_tracktwo || HLT_e17_lhmedium_nod0_ivarloose_tau25_medium1_tracktwo'],
    '2017' : ['HLT_e17_lhmedium_nod0_ivarloose_tau25_medium1_tracktwo'],
    '2018' : ['HLT_e17_lhmedium_nod0_ivarloose_tau25_medium1_tracktwoEF'],
    '2022' : ['HLT_e24_lhmedium_ivarloose_tau20_mediumRNN_tracktwoMVA_03dRAB_L1EM22VHI'],
    '2023' : ['HLT_e24_lhmedium_ivarloose_tau20_mediumRNN_tracktwoMVA_03dRAB_L1eEM26M'],
    '2024' : ['HLT_e24_lhmedium_ivarloose_tau20_mediumRNN_tracktwoMVA_03dRAB_L1eEM26M'],
}

trig_singleTau = {
    '2015': [
            "HLT_tau80_medium1_tracktwo_L1TAU60"
    ],

    '2016': [
            "HLT_tau80_medium1_tracktwo_L1TAU60 || "
            "HLT_tau125_medium1_tracktwo || "
            "HLT_tau160_medium1_tracktwo"
    ],
    '2017': [
            "HLT_tau160_medium1_tracktwo_L1TAU100"
    ],
    '2018': [
            "HLT_tau160_medium1_tracktwoEF_L1TAU100 || "
#                "HLT_tau200_medium1_tracktwoEF_L1TAU100 || "
            "HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100 || "
#                "HLT_tau200_mediumRNN_tracktwoMVA_L1TAU100"
    ],
    '2022': [
            "HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100 || "
    ],
    '2023': ["HLT_tau160_mediumRNN_tracktwoMVA_L1TAU100 || "
                "HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140"
    ],
    '2024': [
            "HLT_tau160_mediumRNN_tracktwoMVA_L1eTAU140 || ",
            "HLT_tau200_mediumRNN_tracktwoMVA_L1eTAU140",
    ]
}

trig_diTau = {
    '2015': [
            "HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1TAU20IM_2TAU12IM"
    ],

    '2016': [
            "HLT_tau35_loose1_tracktwo_tau25_loose1_tracktwo || " # Period A (No SF avail)
            "HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo || " # Period B-D3 with J25 / after TAU20IM_2TAU12IM_J25_2J20_3J12
            "HLT_tau80_medium1_tracktwo_L1TAU60_tau50_medium1_tracktwo_L1TAU12" # Period D4-END 
    ],
    '2017': [
            "HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo || " #B1-B4
            "HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_03dR30_L1DR-TAU20ITAU12I-J25 || " #B5-B7
            "HLT_tau35_medium1_tracktwo_tau25_medium1_tracktwo_L1DR-TAU20ITAU12I-J25 || " #B5-B7
            "HLT_tau40_medium1_tracktwo_tau35_medium1_tracktwo || " #B5-B7
            "HLT_tau80_medium1_tracktwo_L1TAU60_tau50_medium1_tracktwo_L1TAU12 || "  #B1-B4 and B5-B7
            "HLT_tau80_medium1_tracktwo_L1TAU60_tau35_medium1_tracktwo_L1TAU12IM_L1TAU60_DR-TAU20ITAU12I || "  #B5-B7
            "HLT_tau80_medium1_tracktwo_L1TAU60_tau60_medium1_tracktwo_L1TAU40 || " #B8-END
    ],
    '2018': [
            "HLT_tau80_medium1_tracktwoEF_L1TAU60_tau60_medium1_tracktwoEF_L1TAU40 || " # Period B-END
            "HLT_tau80_medium1_tracktwoEF_L1TAU60_tau35_medium1_tracktwoEF_L1TAU12IM_L1TAU60_DR-TAU20ITAU12I || " # Period B-END
            "HLT_tau40_medium1_tracktwoEF_tau35_medium1_tracktwoEF || " # Period B-END
            "HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_L1DR-TAU20ITAU12I-J25 || " # Period B-END
            "HLT_tau35_medium1_tracktwoEF_tau25_medium1_tracktwoEF_03dR30_L1DR-TAU20ITAU12I-J25 || " # Period B-END
            "HLT_tau80_mediumRNN_tracktwoMVA_L1TAU60_tau60_mediumRNN_tracktwoMVA_L1TAU40 || " # Period K-END
            "HLT_tau80_mediumRNN_tracktwoMVA_L1TAU60_tau35_mediumRNN_tracktwoMVA_L1TAU12IM_L1TAU60_DR-TAU20ITAU12I || " # Period K-END
            "HLT_tau40_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA || " # Period K-END
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_L1DR-TAU20ITAU12I-J25 || " # Period K-END
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dR30_L1DR-TAU20ITAU12I-J25 || " # Period K-END
    ],
    '2022': [
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB30_L1DR-TAU20ITAU12I-J25 || "
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1TAU20IM_2TAU12IM_4J12p0ETA25 || "
            "HLT_tau40_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA_03dRAB_L1TAU25IM_2TAU20IM_2J25_3J20 || "
            "HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1TAU60_2TAU40 || "
            "HLT_tau80_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA_03dRAB30_L1TAU60_DR-TAU20ITAU12I"
    ],

    '2023': [
            "HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1TAU60_2TAU40 || "
            "HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1eTAU80_2eTAU60 || "
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1TAU20IM_2TAU12IM_4J12p0ETA25 || "
            "HLT_tau40_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA_03dRAB_L1TAU25IM_2TAU20IM_2J25_3J20 || "
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB30_L1DR-TAU20ITAU12I-J25 || "
            "HLT_tau80_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA_03dRAB30_L1TAU60_DR-TAU20ITAU12I || "
    ],
    # some run3 triggers renamed, not yet documented in twiki
    # https://gitlab.cern.ch/atlas/athena/-/blob/main/Trigger/TriggerCommon/TriggerMenuMT/python/HLT/Menu/Physics_pp_run3_v1.py#L1414-1506
    '2024': [
            "HLT_tau80_mediumRNN_tracktwoMVA_tau60_mediumRNN_tracktwoMVA_03dRAB_L1eTAU80_2eTAU60 || ",
            "HLT_tau80_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA_03dRAB30_L1eTAU80_2cTAU30M_DR-eTAU30eTAU20 || ",
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB_L1cTAU30M_2cTAU20M_4jJ30p0ETA25 || ",
            "HLT_tau40_mediumRNN_tracktwoMVA_tau35_mediumRNN_tracktwoMVA_03dRAB_L1cTAU35M_2cTAU30M_2jJ55_3jJ50 || ",
            "HLT_tau35_mediumRNN_tracktwoMVA_tau25_mediumRNN_tracktwoMVA_03dRAB30_L1cTAU30M_2cTAU20M_DR-eTAU30MeTAU20M-jJ55",
    ]
}

trig_met = {
    '2015': ['HLT_xe70_mht'],
    '2016': ['HLT_xe90_mht_L1XE50 || HLT_xe100_mht_L1XE50 || HLT_xe110_mht_L1XE50'],
    '2017': ['HLT_xe110_pufit_L1XE55 || HLT_xe110_pufit_L1XE50'],
    '2018': ['HLT_xe110_pufit_xe70_L1XE50 || HLT_xe110_pufit_xe65_L1XE50'],
    '2022': ['HLT_xe65_cell_xe90_pfopufit_L1XE50'],
    '2023': ['HLT_xe65_cell_xe90_pfopufit_L1XE50'],
    '2024': ['HLT_xe65_cell_xe90_pfopufit_L1jXE110'],
}

# Trigger-passed flag only
triggerChainsPerYear = { x : [] for x in datataking_years} 
for yy in datataking_years:
    triggerChainsPerYear[yy]+=trig_singleMuon[yy]
    triggerChainsPerYear[yy]+=trig_singleEle[yy]
    triggerChainsPerYear[yy]+=trig_diMuon[yy]
    triggerChainsPerYear[yy]+=trig_diEle[yy]
    triggerChainsPerYear[yy]+=trig_EleMu[yy]
    triggerChainsPerYear[yy]+=trig_singleTau[yy]
    triggerChainsPerYear[yy]+=trig_diTau[yy]
    triggerChainsPerYear[yy]+=trig_tauMu[yy]
    triggerChainsPerYear[yy]+=trig_tauEle[yy]
    triggerChainsPerYear[yy]+=trig_met[yy]


# Tau triggers for STT SF - names of the chains are slightly different in Run2! 
# Check /cvmfs/atlas.cern.ch/repo/sw/database/GroupData/TauAnalysisTools/00-04-00/EfficiencyCorrections/Trigger/RNN/
tauTriggerChainsPerYear = {
    "2015": ["HLT_tau80L1TAU60_medium1_tracktwo",
            "HLT_tau35_medium1_tracktwo",
            "HLT_tau25_medium1_tracktwo"],
    "2016": ["HLT_tau80L1TAU60_medium1_tracktwo",
             "HLT_tau35_medium1_tracktwo",
             "HLT_tau25_medium1_tracktwo"],
    "2017": ["HLT_tau160L1TAU100_medium1_tracktwo",
            "HLT_tau35_medium1_tracktwo",
            "HLT_tau25_medium1_tracktwo"],
    "2018": ["HLT_tau160L1TAU100_medium1_tracktwoEF_OR_mediumRNN_tracktwoMVA",
             "HLT_tau80L1TAU60_medium1_tracktwoEF_OR_mediumRNN_tracktwoMVA",
             "HLT_tau60_medium1_tracktwoEF_OR_mediumRNN_tracktwoMVA",
             "HLT_tau35_medium1_tracktwoEF_OR_mediumRNN_tracktwoMVA",
             "HLT_tau25_medium1_tracktwoEF_OR_mediumRNN_tracktwoMVA",
             ],
    "2022": ["HLT_tau160_mediumRNN_tracktwoMVA",
             "HLT_tau80_mediumRNN_tracktwoMVA",
             "HLT_tau60_mediumRNN_tracktwoMVA",
             "HLT_tau40_mediumRNN_tracktwoMVA",
             "HLT_tau35_mediumRNN_tracktwoMVA",
             "HLT_tau25_mediumRNN_tracktwoMVA"],
    "2023": ["HLT_tau160_mediumRNN_tracktwoMVA",
             "HLT_tau80_mediumRNN_tracktwoMVA",
             "HLT_tau60_mediumRNN_tracktwoMVA",
             "HLT_tau40_mediumRNN_tracktwoMVA",
             "HLT_tau35_mediumRNN_tracktwoMVA",
             "HLT_tau25_mediumRNN_tracktwoMVA"],
    "2023": ["HLT_tau160_mediumRNN_tracktwoMVA",
             "HLT_tau80_mediumRNN_tracktwoMVA",
             "HLT_tau60_mediumRNN_tracktwoMVA",
             "HLT_tau40_mediumRNN_tracktwoMVA",
             "HLT_tau35_mediumRNN_tracktwoMVA",
             "HLT_tau25_mediumRNN_tracktwoMVA"],
}

# Trigger matching is supported only for single-leg triggers
triggerMatchChainsPerYear = { x : [] for x in datataking_years}
for yy in triggerMatchChainsPerYear.keys():
    triggerMatchChainsPerYear[yy] += trig_singleEle[yy]
    triggerMatchChainsPerYear[yy] += trig_singleMuon[yy]
    triggerMatchChainsPerYear[yy] += trig_singleTau[yy]



# Triggers used for Scale Factors
triggerChainsSF = { bucket : {x : [] for x in datataking_years[:-1]} for bucket in ["SLT"]} 
for yy in datataking_years[:-1]:
    triggerChainsSF['SLT'][yy] += trig_singleEle[yy]
    triggerChainsSF['SLT'][yy] += trig_singleMuon[yy]


allTriggers = list(set(substring.strip() for chains_list in triggerChainsPerYear.values() for chain in chains_list for substring in chain.split('||')))
