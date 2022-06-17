#This file contains all the possible configurations for Detector 1 simulations

#Production sites
sites = ['BNL', 'JLAB', 'MIT', 'OSG', 'OSG@BNL']

#Detector 1 nightlies
nightlyBuild = ['test.build']

#macros tags
macrosVersion = {
  "test1" : "9cad06f",
}

#PWGs
det1WorkingGroup = ['General', 'DiffractiveAndTagging', 'Electroweak', 'ExclusiveReactions', 'HFandJets', 'Inclusive', 'SIDIS', 'Spectroscopy', 'AI']

#Generators
det1Generator = ['particleGun', 'pythia6', 'pythia8', 'BeAGLE', 'Djangoh', 'MILOU3D', 'LAger', 'UVA', 'DPM', 'topeg', 'elSpectro', 'LQGENEP', 'DEMP', "EIC_mesonMC", 'CLASDIS', 'eSTARlight', 'Sartre', 'EpIC']

#Collision type

dete1Collision = ['singlePion', 'singlePion-wVtxConstraint', 'singleElectron', 'singleMuon', 'singleMuonPlus', 'singlePionPlus', 'singlePositron',
                 'ep-5x41', 'ep-5x41-q2-low', 'ep-5x41-q2-high', 'ep-5x41-q2-1', 'ep-5x100-q2-very-low', 'ep-5x41-wVtxConstraint',
                 'eHe3-5x41-q2-2', 'eHe3-5x41-q2-10', 'eHe3-5x41-q2-50', 'eHe3-5x41cc',
                 'ep-10x100', 'ep-10x100-q2-low', 'ep-10x100-q2-1-to-100', 'ep-10x100-q2-100','ep-10x100-q2-high', 'ep-10x100-q2-10', 'ep-10x100nc-q2-2', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-500', 'ep-10x100-wVtxConstraint',
                 'eHe3-10x100-q2-2', 'eHe3-10x100-q2-10', 'eHe3-10x100-q2-100', 'eHe3-10x100-q2-500',
                 'ep-18x100', 'ep-18x100-q2-low', 'ep-18x100-q2-high', 'ep_18x100lowq2',
                 'eHe3-18x166-q2-2', 'eHe3-18x166-q2-10', 'eHe3-18x166-q2-100', 'eHe3-18x166-q2-1000', 'eHe3-18x166cc',
                 'ep-18x275', 'ep-18x275-q2-low', 'ep-18x275-q2-high', 'ep-18x275-q2-100', 'ep-18x275-q2-10', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-1000', 'ep-18x275cc', 'ep-18x275-q2-1-to-100', 'ep-18x275-noMagField',
                 'eAu-10x100-q2-1-to-100', 'eAu-10x100-q2-100', 'eAu-18x275-q2-1-to-100', 'eAu-18x275-q2-100',
                ]

DiffTaggCollision = ['ep-5x41-pionFF', 'ep-5x100-pionFF', 'ep-10x100-pionFF', 
                     'ep-5x41-NeutronSS', 'ep-5x100-upi0', 'ep-5x41-SRC', 'ep-5x100-XYZ', 'ep-10x100-PiStruc', 'ep-5x41-KLambda', 'ep-5x41-KSigma', 'ePb-18x110', 'ePb-18x110-tau10', 'ePb-18x108-JPsi-q2-1-10', 'eZr-18x122-JPsi-q2-1-10', 
                     'ep-5x41-XYZ-twopi', 'ep-5x100-XYZ-twopi', 'ep-10x100-XYZ-twopi', 'ep-18x275-XYZ-twopi', 'ep-5x100-XYZ-pi4',
                     'eZr-18x122-JPsi-e-IP6', 'eZr-18x122-JPsi-e-IP8', 'ePb-18x108-JPsi-e-IP6', 'ePb-18x108-JPsi-e-IP8',
                     'eZr-18x122-JPsi-mu-IP6', 'eZr-18x122-JPsi-mu-IP8', 'ePb-18x108-JPsi-mu-IP6', 'ePb-18x108-JPsi-mu-IP8', 'ep-5x41-uomega-Q2-0-1','ep-5x41-uomega-Q2-1-5', 'ePb-18x108-e-IP6', 'ePb-18x108-e-IP8', 'ePb-18x108-mu-IP6', 'ePb-18x108-mu-IP8',
                     'ep-5x41-PiStruc', 'ep-5x100-PiStruc', 'ep-10x100-PiStruc', 'ep-18x275-PiStruc'
                    ]

ExclusiveCollision = ['ep-10x100IPRO4_GK-DVCS', 'ep-10x100BH_GK-DVCS', 'ep-5x41IPRO4_GK-DVCS', 'ep-5x41BH_GK-DVCS', 'ep-18x275IPRO4_GK-DVCS', 'ep-18x275BH_GK-DVCS', 
                      'ep-5x41-DVCS-pi0','ep-10x100-DVCS-pi0', 'ep-18x275-DVCS-pi0',
                      'eA-5x41_Ph-DVCS', 'eA-5x41_Nh-DVCS', 'eA-10x110_Ph-DVCS', 'eA-10x110_Nh-DVCS', 'eA-18x110_Ph-DVCS', 'eA-18x110_Nh-DVCS',
                      'eA-5x41_Ph-DVCS-IP8', 'eA-5x41_Nh-DVCS-IP8', 'eA-10x110_Ph-DVCS-IP8', 'eA-10x110_Nh-DVCS-IP8', 'eA-18x110_Ph-DVCS-IP8', 'eA-18x110_Nh-DVCS-IP8',
                      'ep-5x41-TCS-hel_plus', 'ep-5x41-TCS-hel_minus', 'ep-10x100-TCS-hel_plus', 'ep-10x100-TCS-hel_minus', 'ep-18x275-TCS-hel_plus', 'ep-18x275-TCS-hel_minus', 
                      'ep-18x275-JPsi-e', 'ep-18x275-JPsi-e-IP8',
                      'ep-10x100-JPsi', 'ep-10x100-JPsi-IP8',
                      'ep-10x100nc-q2-500', 'ep-10x100nc-q2-100', 'ep-10x100nc-q2-10', 'ep-10x100nc-q2-2',
                      'ep-18x275nc-q2-1000', 'ep-18x275nc-q2-100', 'ep-18x275nc-q2-10', 'ep-18x275nc-q2-50', 'ep-18x275nc-q2-2',
                      'ep-5x41nc-q2-50', 'ep-5x41nc-q2-10', 'ep-5x41nc-q2-2', 'ep-5x41cc-q2-1',
                      'eD-10x100nc-q2-500', 'eD-10x100nc-q2-100', 'eD-10x100nc-q2-10', 'eD-10x100nc-q2-2',
                      'eD-18x137nc-q2-1000', 'eD-18x137nc-q2-100', 'eD-18x137nc-q2-10', 'eD-18x137nc-q2-2', 'eD-18x137cc-q2-1',
                      'eD-5x41nc-q2-50', 'eD-5x41nc-q2-10', 'eD-5x41nc-q2-2', 'eD-5x41cc-q2-1'
                     ]

det1Collision.extend(DiffTaggCollision)
det1Collision.extend(ExclusiveCollision)
