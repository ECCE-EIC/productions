declare -A myStrings

myStrings["Input::SIMPLE = false;"]="Input::SIMPLE = true;" 
myStrings["Input::READEIC = true;"]="Input::READEIC = false;"
myStrings["INPUTGENERATOR::SimpleEventGenerator[0]->add_particles(\"pi-\", 5);"]="INPUTGENERATOR::SimpleEventGenerator[0]->add_particles(\"pi+\", 1);"
myStrings["INPUTGENERATOR::SimpleEventGenerator[0]->set_eta_range(-3, 3);"]="INPUTGENERATOR::SimpleEventGenerator[0]->set_eta_range(-3.5, 3.5);"
myStrings["INPUTGENERATOR::SimpleEventGenerator[0]->set_pt_range(0.1, 20.);"]="INPUTGENERATOR::SimpleEventGenerator[0]->set_p_range(0.1, 20.);"

for i in "${!myStrings[@]}"; do changeStrings.sh Fun4All_G4_EICDetector.C "${i}" "${myStrings[$i]}"; done

echo "setupPionGun.sh complete"
