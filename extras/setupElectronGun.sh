declare -A myStrings

myStrings["Input::SIMPLE = false;"]="Input::SIMPLE = true;" 
myStrings["Input::READEIC = true;"]="Input::READEIC = false;"
myStrings["add_particles(\"pi-\", 5);"]="add_particles(\"e-\", 1);"
myStrings["set_eta_range(-3, 3);"]="set_eta_range(-3.5, 3.5);"
myStrings["set_pt_range(0.1, 20.);"]="set_p_range(0.1, 20.);"

for i in "${!myStrings[@]}"; do changeStrings.sh Fun4All_G4_EICDetector.C "${i}" "${myStrings[$i]}"; done

echo "setupElectronGun.sh complete"
