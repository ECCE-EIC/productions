#ifndef MACRO_G4USER_C
#define MACRO_G4USER_C

#include <fun4all/Fun4AllServer.h>

//#include <fun4all/Fun4AllInputManager.h>
//#include <fun4all/Fun4AllDstInputManager.h>

R__LOAD_LIBRARY(libfun4all.so)

//#include <difftaggana/diff_tagg_ana.h>
#include <diff_tagg_ana.h>
//#include <anatutorial/Diff_Tagg_example.h>

R__LOAD_LIBRARY(libdifftaggana.so)

class PHG4Reco;

namespace Enable
{
// if you want this to run by default, initialize this to true
// Otherwise you have to use Enable::USER = true; in your macro
  bool USER = false;
  int USER_VERBOSITY = 0;
}

namespace G4USER
{
// here you can set parameters in your macro via
// G4USER::myparam = 1;
// add as many as you need
  int myparam = 0;
}

// This initializes the G4 part if you have a detector implemented
// You need to tell its dimensions to the surrounding black hole
void UserInit()
{
  // set the black hole dimensions surrounding the detector
  // XXX: maximum radius of your detector
  // YYY: maximum extension in z
  // ZZZ: maximum extension in -z (use -ZZZ)
  //BlackHoleGeometry::max_radius = std::max(BlackHoleGeometry::max_radius, XXX);
  //BlackHoleGeometry::max_z = std::max(BlackHoleGeometry::max_z, YYY);
  //BlackHoleGeometry::min_z = std::min(BlackHoleGeometry::min_z, ZZZ);



}

// If you have a detector - here goes the setup
void UserDetector(PHG4Reco *g4Reco)
{
  return;
}

// Any analysis goes here (registering your module with Fun4All)
void UserAnalysisInit()
{
  Fun4AllServer* se = Fun4AllServer::instance();

  diff_tagg_ana *myAnalysisModule = new diff_tagg_ana("diff_tagg_ana","out.root");

//  Diff_Tagg_example *myAnalysisModule = new Diff_Tagg_example("diff_tagg","out.root");

  se->registerSubsystem(myAnalysisModule);
  
  // AnalysisModule *myAnalysisModule = new AnalysisModule();

//  Fun4AllInputManager *in = new Fun4AllDstInputManager("in");
//  in->fileopen(fname);
//  se->registerInputManager(in);
//  se->run();
//  se->End();

//  return;
}

#endif
