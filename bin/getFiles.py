RUNS="001 002 003 004 005 006 007 008 009 010"

for r in $RUNS
do
 
  f="ep_noradcor.18x100lowq_run${r}.root"

  if [ -e "/tmp/$f" ]
  then
    echo " File /tmp/$f exists already."
  else
    echo " Downloading file $f to /tmp/$f."
    ~cmsprod/bin/mc cp  eic/eictest/ECCE/ProductionInputFiles/SIDIS/pythia6/ep_18x100/$f /tmp/$f
  fi


  echo "\
  gfal-copy file:///tmp/ep_noradcor.18x100lowq_run${r}.root \
            gsiftp://se01.cmsaf.mit.edu:2811//cms/store/user/paus/ecce/ep_noradcor.18x100lowq_run${r}.root \
  "

  gfal-copy file:///tmp/ep_noradcor.18x100lowq_run${r}.root \
            gsiftp://se01.cmsaf.mit.edu:2811//cms/store/user/paus/ecce/ep_noradcor.18x100lowq_run${r}.root

done
