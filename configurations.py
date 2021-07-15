#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['new', 'ana.8', 'ana.13']

#macros tags
macrosVersion = {
  "June-2021-Concept-v0.1" : "38efad6",
  "v0.1" : "74c9a85",
  "latest_master" : "463a3bb", #from 2021/06/11
  "latest" : "9daf451", #from 2021/05/11
  "20210618" : "db6dd0c",
  "20210624" : "5f210c7",
  "diff_tagg_physics_IP6_June_16_2021" : "9266a35",
  "Diff_Tagg_Sim_July_03_2021" : "8fa40c8",
  "Diff_Tagg_Sim_July_03_2021_eA_110GeV_IP8" : "Diff_Tagg_Sim_July_03_2021_eA_110GeV_IP8"
}

#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'DEMP']

#Collision type
#ecceCollision = ['singlePion', 'singleElectron', 'ep_5x100', 'ep_10x100', 'ep_18x100', 'ep_18x100lowq2', 'ep_18x100highq2']
ecceCollision = ['singlePion', 'singleElectron', 'ep_5x100', 'ep_10x100', 'ep_18x100', 'ep_18x100lowq2', 'ep_18x100highq2', 'pionFF', 'NeutronSS', 'u_channel_pi0', 'ePb_diffractive', 'SRC']
