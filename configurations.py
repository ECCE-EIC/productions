#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['prop.2', 'prop.1', 'ana.8', 'ana.13']

#macros tags
macrosVersion = {
  "prop.2.1-production" : "c131177",
  "prop.2.1-production-pythia8" : "228d5b5",
  "prop.2.1-production-singlePion-0-20GeV" : "f6b93ca",
  "prop.2.1-production-singleElectron-0-20GeV" : "af4c3a2"
}

#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP']

#Collision type
ecceCollision = ['singlePion', 'singleElectron', 'ep_18x100lowq2', 
                 'ep-5x41', 'ep-5x41-q2-low', 'ep-5x41-q2-high', 'ep-5x41-q2-1',
                 'ep-10x100', 'ep-10x100-q2-low', 'ep-10x100-q2-high', 'ep-10x100-q2-10', 'ep-10x100nc-q2-2', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-500'
                 'ep-18x100', 'ep-18x100-q2-low', 'ep-18x100-q2-high', 
                 'ep-18x275', 'ep-18x275-q2-low', 'ep-18x275-q2-high', 'ep-18x275-q2-100', 'ep-18x275-q2-10', 'ep-18x275cc',
                 'ep-18x275nc-q2-2', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-1000',
                ]
