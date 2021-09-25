#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['prop.2', 'prop.1', 'ana.8', 'ana.13', 'ana.23']

# ana.23: August 22, 2022

#macros tags
macrosVersion = {
  "prop1" : "9cad06f",
  "prop.2.1-production" : "c131177",
  "prop.2.1-production-pythia8" : "228d5b5",
  "prop.2.1-production-singlePion-0-20GeV" : "f6b93ca",
  "prop.2.1-production-singleElectron-0-20GeV" : "af4c3a2",
#}

#Diff and Tagg

#DiffTagg_macrosVersion = {
# r1
  "diff_tagg_physics_IP6_June_16_2021" : "9266a35",
  "Diff_Tagg_Sim_July_03_2021" : "8fa40c8",
  "Diff_Tagg_Sim_July_03_2021_eA_110GeV_IP8" : "Diff_Tagg_Sim_July_03_2021_eA_110GeV_IP8",
  "prop1" : "9cad06f",
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
  "prop.2.1-production-DiffractiveAndTagging-r6" : "Diff_Tagg_IP6_r6",
  "prop.2.1-production-DiffractiveAndTagging-41GeV-r6" : "Diff_Tagg_IP6_41GeV_r6",
  "prop.2.1-production-DiffractiveAndTagging-62GeV-r6" : "Diff_Tagg_IP6_62GeV_r6",
  "prop.2.1-production-DiffractiveAndTagging-82GeV-r6" : "Diff_Tagg_IP6_82GeV_r6",
  "prop.2.1-production-DiffractiveAndTagging-100GeV-r6" : "Diff_Tagg_IP6_100GeV_r6",
  "prop.2.1-production-DiffractiveAndTagging-165GeV-r6" : "Diff_Tagg_IP6_165GeV_r6",
  "prop.2.1-production-DiffractiveAndTagging-220GeV-r6" : "Diff_Tagg_IP6_220GeV_r6",
  "prop.2.1-production-DiffractiveAndTagging-275GeV-r6" : "Diff_Tagg_IP6_275GeV_r6",
}

#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP', 'DEMP', "EIC_mesonMC", 'CLASDIS', 'eSTARlight', 'Sartre', 'EpIC']

#Collision type

ecceCollision = ['singlePion', 'singleElectron', 'ep_18x100lowq2', 
                 'ep-5x41', 'ep-5x41-q2-low', 'ep-5x41-q2-high', 'ep-5x41-q2-1',
                 'ep-10x100', 'ep-10x100-q2-low', 'ep-10x100-q2-high', 'ep-10x100-q2-10', 'ep-10x100nc-q2-2', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-500'
                 'ep-18x100', 'ep-18x100-q2-low', 'ep-18x100-q2-high', 
                 'ep-18x275', 'ep-18x275-q2-low', 'ep-18x275-q2-high', 'ep-18x275-q2-100', 'ep-18x275-q2-10', 'ep-18x275cc',
                 'ep-18x275nc-q2-2', 'ep-18x275nc-q2-10', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-1000',
                ]

DiffTaggCollision = ['ep-5x41-pionFF', 'ep-5x100-pionFF', 'ep-10x100-pionFF', 
'ep-5x41-NeutronSS', 'ep-5x100-upi0', 'ep-5x41-SRC', 'ep-5x100-XYZ', 'ep-10x100-PiStruc', 'ep-5x41-KLambda', 'ep-5x41-KSigma', 'ePb-18x110', 'ePb-18x110-tau10', 'ePb-18x108-JPsi-q2-1-10', 'eZr-18x122-JPsi-q2-1-10', 
'ep-5x41-XYZ-twopi', 'ep-5x100-XYZ-twopi', 'ep-10x100-XYZ-twopi', 'ep-18x275-XYZ-twopi', 'ep-5x100-XYZ-pi4',
'eZr-18x122-JPsi-e-IP6', 'eZr-18x122-JPsi-e-IP8', 'ePb-18x108-JPsi-e-IP6', 'ePb-18x108-JPsi-e-IP8',
'eZr-18x122-JPsi-mu-IP6', 'eZr-18x122-JPsi-mu-IP8', 'ePb-18x108-JPsi-mu-IP6', 'ePb-18x108-JPsi-mu-IP8', 'ep-5x41-uomega-Q2-0-1','ep-5x41-uomega-Q2-1-5', 'ePb-18x108-e-IP6', 'ePb-18x108-e-IP8', 'ePb-18x108-mu-IP6', 'ePb-18x108-mu-IP8',
'ep-5x41-PiStruc', 'ep-5x100-PiStruc', 'ep-10x100-PiStruc', 'ep-18x275-PiStruc',
'eHe3-5x41-NeutronSS-lowx', 'eHe3-5x41-NeutronSS-midx', 'eHe3-5x41-NeutronSS-highx', 'eHe3-18x110-NeutronSS-lowx', 'eHe3-18x110-NeutronSS-midx', 'eHe3-18x110-NeutronSS-highx']

ExclusiveCollision = ['ep-10x100IPRO4_GK-DVCS', 'ep-10x100BH_GK-DVCS', 'ep-5x41IPRO4_GK-DVCS', 'ep-5x41BH_GK-DVCS', 'ep-18x275IPRO4_GK-DVCS', 'ep-18x275BH_GK-DVCS', 
'ep-5x41-DVCS-pi0','ep-10x100-DVCS-pi0', 'ep-18x275-DVCS-pi0',
'ep-5x41_GK-DVCS','ep-10x100_GK-DVCS', 'ep-18x275_GK-DVCS',
'eA-5x41_Ph-DVCS', 'eA-5x41_Nh-DVCS', 'eA-10x110_Ph-DVCS', 'eA-10x110_Nh-DVCS', 'eA-18x110_Ph-DVCS', 'eA-18x110_Nh-DVCS',
'eA-5x41_Ph-DVCS-IP8', 'eA-5x41_Nh-DVCS-IP8', 'eA-10x110_Ph-DVCS-IP8', 'eA-10x110_Nh-DVCS-IP8', 'eA-18x110_Ph-DVCS-IP8', 'eA-18x110_Nh-DVCS-IP8',
'ep-5x41-TCS-hel_plus', 'ep-5x41-TCS-hel_minus', 'ep-10x100-TCS-hel_plus', 'ep-10x100-TCS-hel_minus', 'ep-18x275-TCS-hel_plus', 'ep-18x275-TCS-hel_minus', 
'ep-18x275-JPsi-e', 'ep-18x275-JPsi-e-IP8',
'ep-10x100-JPsi', 'ep-10x100-JPsi-IP8',
'eZr-18x122-Phi-IP6', 'eZr-18x122-Phi-IP8', 'ePb-18x108-Phi-IP6', 'ePb-18x108-Phi-IP8', 'eAu-18x110-Phi-IP6', 'eAu-18x110-Phi-IP8',
'ePb-18x110-phiKK-IP6']

ecceCollision.extend(DiffTaggCollision)

ecceCollision.extend(ExclusiveCollision)

