set GCC_HOME=/apps/gcc/4.9.2
setenv PATH ${GCC_HOME}/bin:${PATH}
setenv LD_LIBRARY_PATH ${GCC_HOME}/lib64:${GCC_HOME}/lib

alias python /apps/python/3.8.7/bin/python3

setenv BMS_OSNAME `/group/halld/Software/build_scripts/osrelease.pl`
#setenv BMS_OSNAME `$BUILD_SCRIPTS/osrelease.pl`

# python on the cue
set pypath=/apps/python/PRO/lib/python3.4/

setenv PATH $pypath/bin:$PATH
setenv LD_LIBRARY_PATH $pypath/lib:$LD_LIBRARY_PATH

setenv CERN_ROOT /u/site/cernlib/x86_64_rhel7/2005
setenv CERN_LIB $CERN_ROOT/lib 
setenv PATH $CERN_ROOT/bin:$PATH

#source /group/halld/Software/builds/Linux_CentOS7.7-x86_64-gcc4.8.5/root/root-6.08.06/bin/thisroot.csh
source /apps/root/6.18.04/setroot_CUE.csh
