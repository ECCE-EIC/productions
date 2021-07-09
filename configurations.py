#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['prop.1', 'ana.8', 'ana.13']

#macros tags
macrosVersion = {
  "June-2021-Concept-v0.1" : "38efad6",
  "v0.1" : "74c9a85",
  "latest_master" : "463a3bb", #from 2021/06/11
  "latest" : "9daf451", #from 2021/05/11
  "20210618" : "db6dd0c",
  "20210624" : "5f210c7",
  "20210708" : "4cafa64",
  "prop.1" : "9cad06f"
}

#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP']

#Collision type
ecceCollision = ['singlePion', 'singleElectron', 'ep_5x100', 'ep_10x100', 'ep_18x100', 'ep_18x100_q2_low', 'ep_18x100_q2_high', 'ep_18x275cc',
                 'ep_10x100nc_q2_500', 'ep_10x100nc_q2_100', 'ep_10x100nc_q2_10', 'ep_10x100nc_q2_2', 'ep_18x275_q2_100', 'ep_18x275_q2_10', 
                 'ep_18x275nc_q2_1000', 'ep_18x275nc_q2_100', 'ep_18x275nc_q2_10', 'ep_18x275nc_q2_2']
