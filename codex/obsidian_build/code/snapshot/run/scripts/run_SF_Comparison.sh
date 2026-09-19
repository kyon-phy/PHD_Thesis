#! /bin/bash

# test
# dataset1='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_v03_sys/mc20a/BG/user.zang.700338.Sh.DAOD_PHYS.e8351_s3681_r13167_p6490.2025-05-v1.0-taunub-sys-t4_output/test'
# dataset2='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_offical_v03/user.zang.700338.Sh.DAOD_PHYS.e8351_s3681_r13167_p6697.v3.0-t0_output/test'

# Wenu
# dataset1='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_v03_sys/mc20a/BG/user.zang.700338.Sh.DAOD_PHYS.e8351_s3681_r13167_p6490.2025-05-v1.0-taunub-sys-t4_output'
# dataset2='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_offical_v03/user.zang.700338.Sh.DAOD_PHYS.e8351_s3681_r13167_p6697.v3.0-t0_output'

#Wtaunu
# dataset1='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_v03_sys/mc20a/BG/user.zang.700544.Sh.DAOD_PHYS.e8373_s3681_r13167_p6490.2025-05-v1.0-taunub-sys-t4_output'
# dataset2='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_offical_v03/user.zang.700544.Sh.DAOD_PHYS.e8373_s3681_r13167_p6697.v3.0-t0_output'

# ttbar dilep
# dataset1='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_v03_sys/mc20a/BG/user.zang.410472.PhPy8EG.DAOD_PHYS.e6348_s3681_r13167_p6490.2025-05-v1.0-taunub-sys-t3_output'
# dataset2='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_offical_v03/user.zang.410472.PhPy8EG.DAOD_PHYS.e6348_s3681_r13167_p6697.v3.0-t0_output'

# Wmunu BFilter
dataset1='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_v03_sys/mc20a/BG/user.zang.700341.Sh.DAOD_PHYS.e8351_s3681_r13167_p6490.2025-05-v1.0-taunub-sys-t3_output'
dataset2='/afs/cern.ch/work/z/zang/LQanalysis/samples/BG/GN1_TopCPToolKit_offical_v03/user.zang.700341.Sh.DAOD_PHYS.e8351_s3681_r13167_p6697.v3.0-t0_output'


# sysName='el_id_effSF_TightLH_Loose_VarRad_NOSYS,el_reco_effSF_TightLH_Loose_VarRad_NOSYS,el_isol_effSF_TightLH_Loose_VarRad_NOSYS'
sysName='weight_ftag_effSF_GN2v01_Continuous_NOSYS'

# python3 SF_Comparison_el.py \
python3 SF_Comparison_jet.py \
  --filepath1 $dataset1 \
  --filepath2 $dataset2 \
  --tree reco \
  --out sf_ratio.root \
  --bins 100 --xmin 0.8 --xmax 1.2 \
  --sfs $sysName \
  --png_dir ""
