declare -A myStrings

myStrings["Input::SIMPLE = true;"]="Input::SIMPLE = false;" 
myStrings["//  Input::READEIC = true;"]="Input::READEIC = true;"
myStrings["// Enable::DSTOUT = true;"]="Enable::DSTOUT = true;"
myStrings["Enable::TRACKING_EVAL = Enable::TRACKING && true;"]="Enable::TRACKING_EVAL = false;"
myStrings["Enable::CEMC_EVAL = Enable::CEMC_CLUSTER && true;"]="Enable::CEMC_EVAL = false;"
myStrings["Enable::HCALIN_EVAL = Enable::HCALIN_CLUSTER && true;"]="Enable::HCALIN_EVAL = false;"
myStrings["Enable::HCALOUT_EVAL = Enable::HCALOUT_CLUSTER && true;"]="Enable::HCALOUT_EVAL = false;"
myStrings["Enable::FEMC_EVAL = Enable::FEMC_CLUSTER && true;"]="Enable::FEMC_EVAL = false;"
myStrings["Enable::FHCAL_EVAL = Enable::FHCAL_CLUSTER && true;"]="Enable::FHCAL_EVAL = false;"
myStrings["Enable::EEMC_EVAL = Enable::EEMC_CLUSTER && true;"]="Enable::EEMC_EVAL = false;"
myStrings["Enable::EHCAL_EVAL = Enable::EHCAL_CLUSTER && true;"]="Enable::EHCAL_EVAL = false;"
myStrings["Enable::FWDJETS_EVAL = Enable::FWDJETS && true;"]="Enable::FWDJETS_EVAL = false;"
myStrings["Enable::EVENT_EVAL = true;"]="Enable::EVENT_EVAL = false;"

for i in "${!myStrings[@]}"; do changeStrings.sh Fun4All_G4_EICDetector.C "${i}" "${myStrings[$i]}"; done
