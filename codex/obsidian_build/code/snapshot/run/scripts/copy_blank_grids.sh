#!/bin/bash

target_dir=/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig
# cd to the target directory
cd $target_dir

# sample name to be copied
sample_M1500="fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_0_23L0_2_noWeights_unblind_test"

# target grid names
target_grid_list_M1500=(
"fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU0_5_23L0_2_noWeights_unblind_test"
"fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU0_5_23L0_4_noWeights_unblind_test"
"fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU0_5_23L0_8_noWeights_unblind_test"


)

# copy the sample to the target grids
for grid in ${target_grid_list[@]}; do
    cp -r $sample_M1500 $grid
done


# copy the fit results to the blank grids
# MLQ = 1.5 TeV
# cp -r fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_0_23L0_2_noWeights_unblind_test fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU0_5_23L0_2_noWeights_unblind_test
cp -r fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_0_23L0_2_noWeights_unblind_test fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU0_75_23L0_2_noWeights_unblind_test

