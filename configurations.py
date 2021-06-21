#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG']

#ECCE nightlies
nightlyBuild = ['new', 'ana.8', 'ana.13']

#macros tags
macrosVersion = {
  "latest_master" : "463a3bb", #from 2021/06/11
  "latest" : "9daf451", #from 2021/05/11
  "20210618" : "db6dd0c",
  "v0.1" : "74c9a85"
}

#PWGs
ecceWorkingGroup = ['DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro']

#Collision type
ecceCollision = ['ep_5x100', 'ep_10x100', 'ep_18x100']
