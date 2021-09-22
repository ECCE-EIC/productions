#This file contains all the possible configurations for ECCE simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#ECCE nightlies
nightlyBuild = ['prop.4', 'prop.2', 'prop.1']

#macros tags
macrosVersion = {
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
  "prop.3.3-production-singleElectron-0-20GeV" : "485db0e"
  "prop.4.0-production" : "df8db21",
  "prop.4.0-production-pythia8" : "247ac01",
  "prop.4.0-production-singlePion-0-20GeV" : "408060a",
  "prop.4.0-production-singleElectron-0-20GeV" : "79e1691",
}

#PWGs
ecceWorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy']

#Generators
ecceGenerator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP']

#Collision type
ecceCollision = ['singlePion', 'singleElectron', 'ep_18x100lowq2', 
                 'ep-5x41', 'ep-5x41-q2-low', 'ep-5x41-q2-high', 'ep-5x41-q2-1', 'ep-5x100-q2-very-low',
                 'ep-10x100', 'ep-10x100-q2-low', 'ep-10x100-q2-high', 'ep-10x100-q2-10', 'ep-10x100nc-q2-2', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-500'
                 'ep-18x100', 'ep-18x100-q2-low', 'ep-18x100-q2-high', 
                 'ep-18x275', 'ep-18x275-q2-low', 'ep-18x275-q2-high', 'ep-18x275-q2-100', 'ep-18x275-q2-10', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-1000', 'ep-18x275cc',
                 'eAu-10x100-q2-1'
                ]
