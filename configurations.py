#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLab', 'MIT', 'OSG@Jlab']

#ECCE nightlies
nightlyBuild = ['new', 'ana.8']

#macros tags
macrosVersion = {
  "latest" : " 9daf451", #from 2021/05/11
  "v0.1" : "74c9a85"
}

#PWGs
ecceWorkingGroup = ['SIDIS', 'HFandJets', 'ExclusiveReactions', 'Spectroscopy']

#Generators
ecceGenerator = ['pythia6', 'pythia8', 'BeAGLE', 'topeg', 'elSpectro']

#Collision type
ecceCollision = ['ep_5x100', 'ep_10x100', 'ep_18x100']
