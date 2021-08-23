export PENV_BASE=`pwd`
export PENV_LOG=/home/paus/ecce/logs
export PENV_CONDOR_REQ="( GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_tier3\" && ( regexp(\"T3B.*\",MACHINE) ) )"

export PATH=${PATH}:${PENV_BASE}/bin:/cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/utils/bin
export PYTHONPATH=${PYTHONPATH}:${PENV_BASE}/python

if   [ "$1" == "T3" ]
then
  export PENV_CONDOR_REQ="( BOSCOGroup == \"bosco_t3\" && ( regexp(\"T3B.*\",MACHINE) ) )"
  #export PENV_CONDOR_REQ="( BOSCOGroup == \"t3serv008.mit.edu\" && ( regexp(\"T3B.*\",MACHINE) ) )"
elif [ "$1" == "T2" ]
then
  export PENV_CONDOR_REQ="( GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_lns\" )"
elif [ "$1" == "T23" ]
then
  export PENV_CONDOR_REQ="( GLIDEIN_Site == \"MIT_CampusFactory\" && ( BOSCOGroup == \"bosco_lns\" || BOSCOGroup == \"bosco_tier3\" ) )"
elif [ "$1" == "EN" ]
then
  export PENV_CONDOR_REQ="( BOSCOCluster == \"eofe7.mit.edu\" && BOSCOGroup == \"paus\" )"
fi  
