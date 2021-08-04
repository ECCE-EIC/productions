#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['prop.2', 'prop.1', 'ana.8', 'ana.13']

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
  "prop.2.1-production-DiffractiveAndTagging-100GeV-r3" : "Diff_Tagg_IP6_100GeV_08.03.21"

}


#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP', 'DEMP', "EIC_mesonMC"]

#Collision type
ecceCollision = ['singlePion', 'singleElectron', 'ep-5x100', 'ep-10x100', 'ep-18x100', 'ep-18x100-q2-low', 'ep-18x100-q2-high', 'ep-18x275cc',
                 'ep-10x100nc-q2-500', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-2', 'ep-18x275-q2-100', 'ep-18x275-q2-10', 
                 'ep-18x275nc-q2-1000', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-10', 'ep-18x275nc-q2-2', 'ep-5x41-q2-1', 'ep-10x100-q2-10']

DiffTaggCollision = ['ep-5x100-pionFF', 'ep-5x41-NeutronSS', 'ep-5x100-upi0', 'ep-5x41-SRC', 'ep-5x100-XYZ', 'ep-10x100-PiStruc', 'ep-5x41-KLambda', 'ep-5x41-KSigma', 'ePb-18x110', 'ePb-18x110-tau10', 'ePb-18x108-JPsi-q2-1-10', 'eZr-18x122-JPsi-q2-1-10']

ecceCollision.extend(DiffTaggCollision)

