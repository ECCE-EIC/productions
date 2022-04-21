#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['prop.4', 'prop.2', 'prop.1', 'ana.8', 'ana.13', 'ana.23', 'ana.26', 'ana.27', 'new', 'prop.5', 'prop.6', 'prop.6','ana.45', 'ana.57']

# ana.57, April 10 2022

#macros tags
macrosVersion = {
  "prop1" : "9cad06f",
  "prop.2.1-production" : "c131177",
  "prop.2.1-production-pythia8" : "228d5b5",
  "prop.2.1-production-singlePion-0-20GeV" : "f6b93ca",
  "prop.2.1-production-singleElectron-0-20GeV" : "af4c3a2",
  "prop.3.1-production" : "df8db21",
  "prop.3.1-production-pythia8" : "247ac01",
  "prop.3.1-production-singlePion-0-20GeV" : "408060a",
  "prop.3.1-production-singleElectron-0-20GeV" : "79e1691",
  "prop.3.2-production-singleElectron-0-20GeV" : "485db0e",
  "prop.3.3-production-singlePion-0-20GeV" : "7527712",
  "prop.3.3-production-singleElectron-0-20GeV" : "485db0e",
  "prop.4.0-production" : "7e3088e",
  "prop.4.0-production-pythia8" : "d1a4d8e",
  "prop.4.0-production-singlePion-0-20GeV" : "2bfe6d0",
  "prop.4.0-production-singleElectron-0-20GeV" : "216438e",
#Diff and Tagg
# r1
  "diff_tagg_physics_IP6_June_16_2021" : "9266a35",
  "Diff_Tagg_Sim_July_03_2021" : "8fa40c8",
  "Diff_Tagg_Sim_July_03_2021_eA_110GeV_IP8" : "Diff_Tagg_Sim_July_03_2021_eA_110GeV_IP8",
# r2
  "Diff_Tagg_Sim_July_14_2021_eA_110GeV_IP8" : "Diff_Tagg_Sim_July_14_2021_eA_110GeV_IP8",
  "Diff_Tagg_Sim_July_14_2021" : "Diff_Tagg_Sim_July_14_2021",
  "Diff_Tagg_Sim_July_14_2021_41GeV" : "Diff_Tagg_Sim_July_14_2021_41GeV",
  "Diff_Tagg_Sim_July_14_2021_100GeV" : "Diff_Tagg_Sim_July_14_2021_100GeV",
# r3
  "prop.2.1-production-DiffractiveAndTagging_IP8-r3" : "Diff_Tagg_IP8_08.03.21",
  "prop.2.1-production-DiffractiveAndTagging-r3" : "Diff_Tagg_IP6_08.03.21",
  "prop.2.1-production-DiffractiveAndTagging-41GeV-r3" : "Diff_Tagg_IP6_41GeV_08.03.21",
  "prop.2.1-production-DiffractiveAndTagging-100GeV-r3" : "Diff_Tagg_IP6_100GeV_08.03.21",
# r4
  "prop.2.1-production-DiffractiveAndTagging_IP8-r4" : "Diff_Tagg_IP8_08.14.21",
  "prop.2.1-production-DiffractiveAndTagging-r4" : "Diff_Tagg_IP6_08.14.21",
  "prop.2.1-production-DiffractiveAndTagging-41GeV-r4" : "Diff_Tagg_IP6_41GeV_08.14.21",
  "prop.2.1-production-DiffractiveAndTagging-100GeV-r4" : "Diff_Tagg_IP6_100GeV_08.14.21",
# r5
  "prop.2.1-production-DiffractiveAndTagging-IP8-r5" : "Diff_Tagg_IP8_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-IP8-41GeV-r5" : "Diff_Tagg_IP8_41GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-IP8-100GeV-r5" : "Diff_Tagg_IP8_100GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-IP8-110GeV-r5" : "Diff_Tagg_IP8_110GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-r5" : "Diff_Tagg_IP6_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-41GeV-r5" : "Diff_Tagg_IP6_41GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-62GeV-r5" : "Diff_Tagg_IP6_62GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-82GeV-r5" : "Diff_Tagg_IP6_82GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-100GeV-r5" : "Diff_Tagg_IP6_100GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-110GeV-r5" : "Diff_Tagg_IP6_110GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-165GeV-r5" : "Diff_Tagg_IP6_165GeV_08.26.21",
  "prop.2.1-production-DiffractiveAndTagging-220GeV-r5" : "Diff_Tagg_IP6_220GeV_08.26.21",

# r6
  # IP6
#  "prop.4-production-DiffractiveAndTagging-r6" : "Diff_Tagg_IP6_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-41GeV-r6" : "Diff_Tagg_IP6_41GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-62GeV-r6" : "Diff_Tagg_IP6_62GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-82GeV-r6" : "Diff_Tagg_IP6_82GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-100GeV-r6" : "Diff_Tagg_IP6_100GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-135GeV-r6" : "Diff_Tagg_IP6_135GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-150GeV-r6" : "Diff_Tagg_IP6_150GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-165GeV-r6" : "Diff_Tagg_IP6_165GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-200GeV-r6" : "Diff_Tagg_IP6_200GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-220GeV-r6" : "Diff_Tagg_IP6_220GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-249GeV-r6" : "Diff_Tagg_IP6_249GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP6-275GeV-r6" : "Diff_Tagg_IP6_275GeV_r6",
# Special Runs
  # No beampipe
  "prop.4-production-DiffractiveAndTagging-IP6-41GeV-r6-nobeampipe" : "Diff_Tagg_IP6_41GeV_r6_no_beam_pipe",
  "prop.4-production-DiffractiveAndTagging-IP6-275GeV-r6-nobeampipe" : "Diff_Tagg_IP6_275GeV_r6_no_beam_pipe",
  # No B0
  "prop.4-production-DiffractiveAndTagging-IP6-41GeV-r6-noB0" : "Diff_Tagg_IP6_41GeV_r6_noB0",
  "prop.4-production-DiffractiveAndTagging-IP6-100GeV-r6-noB0" : "Diff_Tagg_IP6_100GeV_r6_noB0",
  "prop.4-production-DiffractiveAndTagging-IP6-135GeV-r6-noB0" : "Diff_Tagg_IP6_135GeV_r6_noB0",
  "prop.4-production-DiffractiveAndTagging-IP6-275GeV-r6-noB0" : "Diff_Tagg_IP6_275GeV_r6_noB0",
  # 3T Field
  "prop.4.3-production-DiffractiveAndTagging-IP6-275GeV-r6-3T_field" : "Diff_Tagg_IP6_275GeV_r6_3T_field",
  "prop.4.3-production-DiffractiveAndTagging-IP6-41GeV-r6-3T_field" : "Diff_Tagg_IP6_41GeV_r6_3T_field",
  "prop.4.3-production-DiffractiveAndTagging-IP6-100GeV-r6-3T_field" : "Diff_Tagg_IP6_100GeV_r6_3T_field",
  # 0.7T Field
  "prop.4.3-production-DiffractiveAndTagging-IP6-275GeV-r6-0p7T_field" : "Diff_Tagg_IP6_275GeV_r6_0p7T_field",
  "prop.4.3-production-DiffractiveAndTagging-IP6-41GeV-r6-0p7T_field" : "Diff_Tagg_IP6_41GeV_r6_0p7T_field",
  "prop.4.3-production-DiffractiveAndTagging-IP6-100GeV-r6-0p7T_field" : "Diff_Tagg_IP6_100GeV_r6_0p7T_field",

  # IP8
#  "prop.4-production-DiffractiveAndTagging-IP8-r6" : "Diff_Tagg_IP8_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-41GeV-r6" : "Diff_Tagg_IP8_41GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-62GeV-r6" : "Diff_Tagg_IP8_62GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-82GeV-r6" : "Diff_Tagg_IP8_82GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-100GeV-r6" : "Diff_Tagg_IP8_100GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-135GeV-r6" : "Diff_Tagg_IP8_135GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-150GeV-r6" : "Diff_Tagg_IP8_150GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-165GeV-r6" : "Diff_Tagg_IP8_165GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-200GeV-r6" : "Diff_Tagg_IP8_200GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-220GeV-r6" : "Diff_Tagg_IP8_220GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-249GeV-r6" : "Diff_Tagg_IP8_249GeV_r6",
  "prop.4-production-DiffractiveAndTagging-IP8-275GeV-r6" : "Diff_Tagg_IP8_275GeV_r6",
  "prop.4.3-production-DiffractiveAndTagging-IP8-275GeV-r6-3T_field" : "Diff_Tagg_IP8_275GeV_r6_3T_field",

# October concept   
  #IP6
  "prop.5-production-DiffractiveAndTagging-IP6-275GeV-r7" : "Diff_Tagg_IP6_275GeV_r7.prop.5",
  #IP68
  "prop.5-production-DiffractiveAndTagging-IP8-275GeV-r7" : "Diff_Tagg_IP8_275GeV_r7.prop.5",

# December concept   
  #IP6
  "prop.6-production-DiffractiveAndTagging-IP6-275GeV-r8" : "Diff_Tagg_IP6_275GeV_r8.prop.6",
  #IP8
  "prop.6-production-DiffractiveAndTagging-IP8-275GeV-r8" : "Diff_Tagg_IP8_275GeV_r8.prop.6",

# January concept   
  #IP6
  "prop.7-production-DiffractiveAndTagging-IP6-275GeV-r9" : "Diff_Tagg_IP6_275GeV_r9.prop.7",
  "prop.7-production-DiffractiveAndTagging-IP6-100GeV-r9" : "Diff_Tagg_IP6_100GeV_r9.prop.7",
  "prop.7-production-DiffractiveAndTagging-IP6-41GeV-r9" : "Diff_Tagg_IP6_41GeV_r9.prop.7",
  #IP8
  "prop.7-production-DiffractiveAndTagging-IP8-275GeV-r9" : "Diff_Tagg_IP8_275GeV_r9.prop.7",

# Detector R&D 
  "Dhevan_IP8_RP_v1" : "Dhevan_IP8_RP_v1",
  "lo_Q2_tagger_IP6.prop.7" : "lo_Q2_tagger_IP6.prop.7",
  "lo_Q2_tagger_5x41_IP6.prop.7" : "lo_Q2_tagger_5x41_IP6.prop.7",
  "lo_Q2_tagger_5x100_IP6.prop.7" : "lo_Q2_tagger_5x100_IP6.prop.7",
  "lo_Q2_tagger_10x100_IP6.prop.7" : "lo_Q2_tagger_10x100_IP6.prop.7",
  "lo_Q2_tagger_18x100_IP6.prop.7" : "lo_Q2_tagger_18x100_IP6.prop.7",

# March r10   
  #IP6
  "prop.7.1-production-DiffractiveAndTagging-IP6-275GeV-hi_acc-r10" : "Diff_Tagg_IP6_275GeV-hi_acc-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-275GeV-hi_div-r10" : "Diff_Tagg_IP6_275GeV-hi_div-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP6-82GeV-hi_div-r10" : "Diff_Tagg_IP6_82GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-82GeV-hi_acc-r10" : "Diff_Tagg_IP6_82GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP6-249GeV-hi_div-r10" : "Diff_Tagg_IP6_249GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-249GeV-hi_acc-r10" : "Diff_Tagg_IP6_249GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP6-62GeV-hi_div-r10" : "Diff_Tagg_IP6_62GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-62GeV-hi_acc-r10" : "Diff_Tagg_IP6_62GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP6-41GeV-hi_div-r10" : "Diff_Tagg_IP6_41GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-41GeV-hi_acc-r10" : "Diff_Tagg_IP6_41GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP6-10x100GeV-hi_div-r10" : "Diff_Tagg_IP6_10x100GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-10x100GeV-hi_acc-r10" : "Diff_Tagg_IP6_10x100GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP6-5x100GeV-hi_div-r10" : "Diff_Tagg_IP6_5x100GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP6-5x100GeV-hi_acc-r10" : "Diff_Tagg_IP6_5x100GeV-hi_acc-r10-prop.7.1",

  # IP6 eA
  "prop.7.1-production-DiffractiveAndTagging-IP6-275GeV-eA-r10" : "Diff_Tagg_IP6_275GeV-eA-r10-prop.7.1",
  # 10x100 eAu 
  "prop.7.1-production-DiffractiveAndTagging-IP6-10x249GeV-eA-r10" : "Diff_Tagg_IP6_10x249GeV-eA-r10-prop.7.1",
  # 5x41 eAu 
  "prop.7.1-production-DiffractiveAndTagging-IP6-5x102GeV-eA-r10" : "Diff_Tagg_IP6_5x102GeV-eA-r10-prop.7.1",

   # IP8

  "prop.7.1-production-DiffractiveAndTagging-IP8-10x100GeV-hi_div-r10" : "Diff_Tagg_IP8_10x100GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP8-10x100GeV-hi_acc-r10" : "Diff_Tagg_IP8_10x100GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP8-41GeV-hi_div-r10" : "Diff_Tagg_IP8_41GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP8-41GeV-hi_acc-r10" : "Diff_Tagg_IP8_41GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP8-275GeV-hi_div-r10" : "Diff_Tagg_IP8_275GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP8-275GeV-hi_acc-r10" : "Diff_Tagg_IP8_275GeV-hi_acc-r10-prop.7.1",

  "prop.7.1-production-DiffractiveAndTagging-IP8-82GeV-hi_div-r10" : "Diff_Tagg_IP8_82GeV-hi_div-r10-prop.7.1",
  "prop.7.1-production-DiffractiveAndTagging-IP8-82GeV-hi_acc-r10" : "Diff_Tagg_IP8_82GeV-hi_acc-r10-prop.7.1",

}

#/*--------------------------------------------------*/
#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP', 'DEMP', "EIC_mesonMC", 'CLASDIS', 'eSTARlight', 'Sartre', 'EpIC', 'KM20']

#Collision type

ecceCollision = ['singlePion', 'singleElectron', 'ep_18x100lowq2', 
                 'ep-5x41', 'ep-5x41-q2-low', 'ep-5x41-q2-high', 'ep-5x41-q2-1', 'ep-5x100-q2-very-low',
                 'ep-10x100', 'ep-10x100-q2-low', 'ep-10x100-q2-high', 'ep-10x100-q2-10', 'ep-10x100nc-q2-2', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-500'
                 'ep-18x100', 'ep-18x100-q2-low', 'ep-18x100-q2-high', 
                 'ep-18x275', 'ep-18x275-q2-low', 'ep-18x275-q2-high', 'ep-18x275-q2-100', 'ep-18x275-q2-10', 'ep-18x275cc',
                 'ep-18x275nc-q2-2', 'ep-18x275nc-q2-10', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-1000',
                ]

DiffTaggCollision = [
# pion form factor
'ep-5x41-pionFF-IP6', 'ep-5x100-pionFF-IP6', 'ep-10x100-pionFF-IP6', 
'ep-5x41-pionFF-3T-IP6', 'ep-5x100-pionFF-3T-IP6', 'ep-10x100-pionFF-3T-IP6', 
'ep-5x41-pionFF-IP8', 'ep-5x100-pionFF-IP8', 'ep-10x100-pionFF-IP8', 
# Kaon form factor
'ep-5x41-KLambda-IP6', 'ep-5x41-KSigma-IP6', 
'ep-5x41-KLambda-IP6-nobeampipe', 'ep-5x41-KSigma-IP6-nobeampipe', 
# Pion Structure Function Study
'ep-5x41-PiStruc-IP6', 'ep-5x100-PiStruc-IP6', 'ep-10x100-PiStruc-IP6', 'ep-10x135-PiStruc-IP6', 'ep-18x275-PiStruc-IP6',
'ep-5x41-PiStruc-IP8', 'ep-5x100-PiStruc-IP8', 'ep-10x100-PiStruc-IP8', 'ep-10x135-PiStruc-IP8', 'ep-18x275-PiStruc-IP8',
'ep-5x41-PiStruc-noB0-IP6', 'ep-5x100-PiStruc-noB0-IP6', 'ep-10x100-PiStruc-noB0-IP6', 'ep-10x135-PiStruc-noB0-IP6', 'ep-18x275-PiStruc-noB0-IP6',
# u-Channel Omega
'ep-5x100-upi0-IP6', 
# Short range correlation
'ep-5x41-SRC-IP6', 
# eA diffractive study
'ePb-18x110-IP6', 'ePb-18x110-tau10-IP6', 'ePb-18x108-JPsi-q2-1-10-IP6', 'eZr-18x122-JPsi-q2-1-10-IP6', 
'ePb-18x108-e-IP6', 'ePb-18x108-e-IP8', 'ePb-18x108-mu-IP6', 'ePb-18x108-mu-IP8',
'ePb-18x108-e-3T_field-IP6', 'ePb-18x108-e-3T_field-IP8', 'ePb-18x108-mu-3T_field-IP6', 'ePb-18x108-mu-3T_field-IP8',
'eZr-18x122-JPsi-e-IP6', 'eZr-18x122-JPsi-e-IP8', 'ePb-18x108-JPsi-e-IP6', 'ePb-18x108-JPsi-e-IP8', 'eAu-18x110-JPsi-e-IP6', 'eAu-18x110-JPsi-e-IP8',
'eZr-18x122-JPsi-mu-IP6', 'eZr-18x122-JPsi-mu-IP8', 'ePb-18x108-JPsi-mu-IP6', 'ePb-18x108-JPsi-mu-IP8', 'eAu-18x110-JPsi-mu-IP6', 'eAu-18x110-JPsi-mu-IP8', 
'eAu-18x110-Rho-IP6',
'ePb-18x108-NonDiff-IP6', 'ePb-18x108-AllDiff-IP6', 'ePb-18x108-NonDiff-IP8', 'ePb-18x108-AllDiff-IP8',
# XYZ meson search
'ep-5x100-XYZ-IP6', 'ep-5x41-XYZ-twopi-IP6', 'ep-5x100-XYZ-twopi-IP6', 'ep-10x100-XYZ-twopi-IP6', 'ep-18x275-XYZ-twopi-IP6', 'ep-5x100-XYZ-pi4-IP6',
'ep-5x100-XYZ-3T-IP6', 'ep-5x41-XYZ-twopi-3T-IP6', 'ep-5x100-XYZ-twopi-3T-IP6', 'ep-10x100-XYZ-twopi-3T-IP6', 'ep-18x275-XYZ-twopi-3T-IP6', 'ep-5x100-XYZ-pi4-3T-IP6', 'ep-5x100-XYZ-BG-IP6', 'ep-18x100-XYZ-BG-IP6', 'ep-5x41-XYZ-BG-IP6', 'ep-18x275-XYZ-BG-IP6',
# u-channel omega electroproduction
'ep-5x41-uomega-Q2-0-1-IP6','ep-5x41-uomega-Q2-1-5-IP6', 
'ep-5x41-uomega-Q2-0-1-hi_div-IP6','ep-5x41-uomega-Q2-1-5-hi_div-IP6', 
# A1n e-He3
'ep-5x41-NeutronSS-IP6', 
'eHe3-5x41-NeutronSS-lowx-IP6', 'eHe3-5x41-NeutronSS-midx-IP6', 'eHe3-5x41-NeutronSS-highx-IP6', 
'eHe3-18x110-NeutronSS-lowx-IP6', 'eHe3-18x110-NeutronSS-midx-IP6', 'eHe3-18x110-NeutronSS-highx-IP6', 
'eHe3-18x166-NeutronSS-lowx-IP6', 'eHe3-18x166-NeutronSS-midx-IP6', 'eHe3-18x166-NeutronSS-highx-IP6',
'ep-18x275-upsilon-IP6',
'eHe3-10x100-NeutronSS-q2-100-IP6', 'eHe3-10x100-NeutronSS-q2-10-IP6', 'eHe3-10x100-NeutronSS-q2-2-IP6', 'eHe3-10x100-NeutronSS-q2-500-IP6', 
'eHe3-18x166-NeutronSS-q2-1000-IP6', 'eHe3-18x166-NeutronSS-q2-100-IP6', 'eHe3-18x166-NeutronSS-q2-10-IP6', 'eHe3-18x166-NeutronSS-q2-2-IP6',
'eHe3-5x41-NeutronSS-q2-10-IP6', 'eHe3-5x41-NeutronSS-q2-2-IP6', 'eHe3-5x41-NeutronSS-q2-50-IP6',
'eHe3-5x41-NeutronSS-lowx-v2.2-IP6', 'eHe3-5x41-NeutronSS-midx-v2.2-IP6', 'eHe3-5x41-NeutronSS-highx-v2.2-IP6', 
'eHe3-18x166-NeutronSS-lowx-v2.2-IP6', 'eHe3-18x166-NeutronSS-midx-v2.2-IP6', 'eHe3-18x166-NeutronSS-highx-v2.2-IP6',

# eA nobeampipe study
'eAu-18x110-JPsi-e-IP6-nobeampipe', 'eAu-18x110-JPsi-mu-IP6-nobeampipe', 'ePb-18x108-AllDiff-IP6-nobeampipe',
'ePb-18x108-JPsi-e-IP6-nobeampipe', 'ePb-18x108-JPsi-mu-IP6-nobeampipe', 'eZr-18x122-JPsi-mu-IP6-nobeampipe',
'eZr-18x122-JPsi-e-IP6-nobeampipe', 'ePb-18x108-NonDiff-IP6-nobeampipe',

'ePb-18x108-JPsi-e-eA-hi_acc-IP6', 'ePb-18x108-JPsi-e-eA-hi_div-IP6', 'ePb-18x108-JPsi-mu-eA-hi_acc-IP6', 'ePb-18x108-JPsi-mu-eA-hi_div-IP6',

'eHe3-5x41-NeutronSS-lowx-v2.2-hi_div-IP6', 'eHe3-5x41-NeutronSS-midx-v2.2-hi_div-IP6', 'eHe3-5x41-NeutronSS-highx-v2.2-hi_div-IP6', 
'eHe3-5x41-NeutronSS-lowx-v2.2-hi_acc-IP6', 'eHe3-5x41-NeutronSS-midx-v2.2-hi_acc-IP6', 'eHe3-5x41-NeutronSS-highx-v2.2-hi_acc-IP6', 
'eHe3-18x166-NeutronSS-lowx-v2.2-hi_div-IP6', 'eHe3-18x166-NeutronSS-midx-v2.2-hi_div-IP6', 'eHe3-18x166-NeutronSS-highx-v2.2-hi_div-IP6',
'eHe3-18x166-NeutronSS-lowx-v2.2-hi_acc-IP6', 'eHe3-18x166-NeutronSS-midx-v2.2-hi_acc-IP6', 'eHe3-18x166-NeutronSS-highx-v2.2-hi_acc-IP6',

# XYZ meson production
'ep-5x100-XYZ-pi4-hi_acc-IP6', 'ep-5x100-XYZ-pi4-hi_div-IP6', 'ep-5x100-XYZ-twopi-hi_acc-IP6', 'ep-5x100-XYZ-twopi-hi_div-IP6', 'ep-18x275-XYZ-twopi-hi_acc-IP6', 'ep-18x275-XYZ-twopi-hi_div-IP6',

# Xinbai
'ep-10x100-coh_JPsi_1e-2_20-Xinbai-hi_acc-IP6', 'ep-10x100-coh_JPsi_1e-2_20-Xinbai-hi_div-IP6', 
'ep-10x100-coh_JPsi_1_20-Xinbai-hi_div-IP6', 'ep-10x100-coh_JPsi_1_20-Xinbai-hi_acc-IP6', 
'eAu-10x100-incoh_JPsi_1_20-Xinbai-eA-IP6', 'eAu-10x100-incoh_JPsi_1e-2_20-Xinbai-eA-IP6',

'eAu-5x41-incoh_JPsi_1_20-Xinbai-eA-IP6', 'eAu-5x41-incoh_JPsi_1e-2_20-Xinbai-eA-IP6',

'ep-5x41-JPsi_1_20-Xinbai-hi_acc-IP6', 'ep-5x41-JPsi_1_20-Xinbai-hi_div-IP6',
'ep-5x41-JPsi_1e-2_1-Xinbai-hi_acc-IP6', 'ep-5x41-JPsi_1e-2_1-Xinbai-hi_div-IP6',

'ep-10x100-JPsi_1_20-Xinbai-hi_acc-IP6', 'ep-10x100-JPsi_1_20-Xinbai-hi_div-IP6',
'ep-10x100-JPsi_1e-2_1-Xinbai-hi_acc-IP6', 'ep-10x100-JPsi_1e-2_1-Xinbai-hi_div-IP6',

'eAu-10x100-JPsi_1_20-Xinbai-eA-IP6', 'eAu-10x100-JPsi_1e-2_1-Xinbai-eA-IP6', 
'eAu-5x41-JPsi_1_20-Xinbai-eA-IP6', 'eAu-5x41-JPsi_1e-2_1-Xinbai-eA-IP6', 

]

ExclusiveCollision = ['ep-10x100IPRO4_GK-DVCS-IP6', 'ep-10x100BH_GK-DVCS-IP6', 'ep-5x41IPRO4_GK-DVCS-IP6', 'ep-5x41BH_GK-DVCS-IP6', 'ep-18x275IPRO4_GK-DVCS-IP6', 'ep-18x275BH_GK-DVCS-IP6', 
'ep-5x41-DVCS-pi0-IP6','ep-10x100-DVCS-pi0-IP6', 'ep-18x275-DVCS-pi0-IP6',
'ep-5x41_GK-DVCS-IP6','ep-10x100_GK-DVCS-IP6', 'ep-18x275_GK-DVCS-IP6',
'eA-5x41_Ph-DVCS-IP6', 'eA-5x41_Nh-DVCS-IP6', 'eA-10x100_Ph-DVCS-IP6', 'eA-10x100_Nh-DVCS-IP6', 'eA-10x110_Ph-DVCS-IP6', 'eA-10x110_Nh-DVCS-IP6', 'eA-18x110_Ph-DVCS-IP6', 'eA-18x110_Nh-DVCS-IP6',
'eA-5x41_Ph-DVCS-IP8', 'eA-5x41_Nh-DVCS-IP8', 'eA-10x100_Ph-DVCS-IP8', 'eA-10x100_Nh-DVCS-IP8', 'eA-10x110_Ph-DVCS-IP8', 'eA-10x110_Nh-DVCS-IP8', 'eA-18x110_Ph-DVCS-IP8', 'eA-18x110_Nh-DVCS-IP8',
'ep-5x41-TCS-hel_plus-IP6', 'ep-5x41-TCS-hel_minus-IP6', 'ep-10x100-TCS-hel_plus-IP6', 'ep-10x100-TCS-hel_minus-IP6', 'ep-18x275-TCS-hel_plus-IP6', 'ep-18x275-TCS-hel_minus-IP6', 'ep-5x41-TCS-muon-IP6', 'ep-18x275-TCS-muon-IP6',
'ep-18x275-JPsi-e-IP6', 'ep-18x275-JPsi-e-IP8',
'ep-10x100-DVCS-IP6', 'ep-5x41-DVCS-IP6',
'ep-18x275-DVCS-IP6',
'ep-18x275-DVCS-Full-IP6',
#---------
'ep-18x275-JPsi-e-lumi10-IP6', 'ep-18x275-JPsi-e-lumi10-IP8',
'ep-5x41-JPsi-e-lumi10-IP6',   'ep-5x41-JPsi-e-lumi10-IP8',
'ep-5x100-JPsi-e-lumi10-IP6',  'ep-5x100-JPsi-e-lumi10-IP8',
'ep-10x100-JPsi-e-lumi10-IP6', 'ep-10x100-JPsi-e-lumi10-IP8',
'ep-10x100-JPsi-IP6',          'ep-10x100-JPsi-IP8',
'ep-10x100-Pi0-IP6',           'ep-18x275-Pi0-IP6',
#---------
'eZr-18x122-Phi-IP6', 'eZr-18x122-Phi-IP8', 'ePb-18x108-Phi-IP6', 'ePb-18x108-Phi-IP8', 'eAu-18x110-Phi-IP6', 'eAu-18x110-Phi-IP8',
'ep-5x41-JPsi-muon-IP6', 'ep-5x100-JPsi-muon-IP6', 'ep-10x100-JPsi-muon-IP6', 'ep-18x275-JPsi-muon-IP6',
'ePb-18x110-phiKK-IP6', 'ePb-18x108-phi-IP6', 'ePb-18x108-phi-IP8', 
'ep-18x275-DVCS-Igor-IP6',
#--------
# 3T Field Study
'ep-18x275-JPsi-e-3T-IP6',
'ep-5x41-JPsi-muon-3T-IP6',
'ep-5x41-JPsi-e-lumi10-3T-IP6', 
'ep-5x100-JPsi-e-lumi10-3T-IP6', 
'ep-10x100-JPsi-e-lumi10-3T-IP6',
'ep-18x275-JPsi-e-lumi10-3T-IP6',
#--------
# 0.7T Field Study
'ep-5x41-JPsi-e-lumi10-0p7T-IP6', 
'ep-5x100-JPsi-e-lumi10-0p7T-IP6', 
'ep-10x100-JPsi-e-lumi10-0p7T-IP6',
'ep-18x275-JPsi-e-lumi10-0p7T-IP6',

'ePb-18x108-phi-KK-bnonsat-IP6',
'ePb-18x108-phi-KK-bsat-IP6',
'ePb-18x108-phi-KK-bnonsat-IP8',
'ePb-18x108-phi-KK-bsat-IP8',

'ep-18x275-DVCS-BH-Full-IP6', 'ep-18x275-DVCS-Full-IP6',
'ep-5x41-DVCS-BH-Full-IP6', 'ep-5x41-DVCS-Full-IP6',

'ep-18x275-DVCS-hi_div-IP6', 'ep-18x275-DVCS-BH-hi_div-IP6', 'ep-18x275-DVCS-Full-hi_div-IP6',
'ep-18x275-DVCS-hi_acc-IP6', 'ep-18x275-DVCS-BH-hi_acc-IP6', 'ep-18x275-DVCS-Full-hi_acc-IP6',

'ep-5x41-DVCS-hi_div-IP6', 'ep-5x41-DVCS-BH-hi_div-IP6', 'ep-5x41-DVCS-Full-hi_div-IP6',
'ep-5x41-DVCS-hi_acc-IP6', 'ep-5x41-DVCS-BH-hi_acc-IP6', 'ep-5x41-DVCS-Full-hi_acc-IP6',

'ep-10x100-DVCS-hi_div-IP6', 'ep-10x100-DVCS-BH-hi_div-IP6', 'ep-10x100-DVCS-Full-hi_div-IP6',
'ep-10x100-DVCS-hi_acc-IP6', 'ep-10x100-DVCS-BH-hi_acc-IP6', 'ep-10x100-DVCS-Full-hi_acc-IP6',

'ep-5x41-DVCS-hi_div-IP8', 'ep-5x41-DVCS-BH-hi_div-IP8', 'ep-5x41-DVCS-Full-hi_div-IP8',
'ep-5x41-DVCS-hi_acc-IP8', 'ep-5x41-DVCS-BH-hi_acc-IP8', 'ep-5x41-DVCS-Full-hi_acc-IP8',

'ep-10x100-DVCS-hi_div-IP8', 'ep-10x100-DVCS-BH-hi_div-IP8', 'ep-10x100-DVCS-Full-hi_div-IP8',
'ep-10x100-DVCS-hi_acc-IP8', 'ep-10x100-DVCS-BH-hi_acc-IP8', 'ep-10x100-DVCS-Full-hi_acc-IP8',

'ep-18x275-DVCS-hi_div-IP8', 'ep-18x275-DVCS-BH-hi_div-IP8', 'ep-18x275-DVCS-Full-hi_div-IP8',
'ep-18x275-DVCS-hi_acc-IP8', 'ep-18x275-DVCS-BH-hi_acc-IP8', 'ep-18x275-DVCS-Full-hi_acc-IP8',

# /*--------------------------------------------------*/
# eA DVCS

'ePb-18x108-JPsi-e-eA-IP6', 'ePb-18x108-JPsi-mu-eA-IP6',

'eA-5x41_Ph-hi_acc-DVCS-IP6', 'eA-5x41_Ph-hi_div-DVCS-IP6', 'eA-5x41_Nh-hi_acc-DVCS-IP6', 'eA-5x41_Nh-hi_div-DVCS-IP6',
'eA-5x41_Ph-hi_acc-DVCS-IP8', 'eA-5x41_Ph-hi_div-DVCS-IP8', 'eA-5x41_Nh-hi_acc-DVCS-IP8', 'eA-5x41_Nh-hi_div-DVCS-IP8',

# /*--------------------------------------------------*/
# TCS
'ep-5x41-TCS-hel_plus-hi_acc-IP6', 'ep-5x41-TCS-hel_plus-hi_div-IP6', 
'ep-5x41-TCS-hel_minus-hi_acc-IP6', 'ep-5x41-TCS-hel_minus-hi_div-IP6',
'ep-18x275-TCS-hel_plus-hi_acc-IP6', 'ep-18x275-TCS-hel_plus-hi_div-IP6', 
'ep-18x275-TCS-hel_minus-hi_acc-IP6', 'ep-18x275-TCS-hel_minus-hi_div-IP6',

'ep-18x275-JPsi-e-lumi10-hi_acc-IP6', 'ep-5x41-JPsi-e-lumi10-hi_acc-IP6',  'ep-5x100-JPsi-e-lumi10-hi_acc-IP6', 'ep-10x100-JPsi-e-lumi10-hi_acc-IP6',
'ep-18x275-JPsi-e-lumi10-hi_div-IP6', 'ep-5x41-JPsi-e-lumi10-hi_div-IP6',  'ep-5x100-JPsi-e-lumi10-hi_div-IP6', 'ep-10x100-JPsi-e-lumi10-hi_div-IP6',

# eA Phi production
'ePb-18x108-phi-KK-bsat-eA-IP6', 'ePb-18x108-phi-KK-bnonsat-eA-IP6', 'ePb-18x108-phi-eA-IP6' ,'ePb-18x108-phi-eA-IP6',

]

ecceCollision.extend(DiffTaggCollision)
ecceCollision.extend(ExclusiveCollision)
