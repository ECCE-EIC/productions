export PENV_BASE=`pwd`
export PENV_LOG=/home/paus/ecce/logs
export PENV_CONDOR_REQ="( GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_tier3\" && ( regexp(\"T3B.*\",MACHINE) ) )"

export PATH=${PATH}:${PENV_BASE}/bin:/cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/utils/bin
export PYTHONPATH=${PYTHONPATH}:${PENV_BASE}/python
