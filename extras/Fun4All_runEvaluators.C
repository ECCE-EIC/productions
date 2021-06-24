#ifndef MACRO_FUN4ALLG4RUNEVALUATORS_C
#define MACRO_FUN4ALLG4RUNEVALUATORS_C

#include <dirent.h>
#include <stdlib.h>

#include <GlobalVariables.C>

#include <G4Setup_EICDetector.C>
#include <G4_DSTReader_EICDetector.C>
#include <G4_EventEvaluator.C>
#include <G4_FwdJets.C>
#include <G4_Global.C>
#include <G4_Input.C>
#include <G4_Production.C>
#include <G4_User.C>

#include <fun4all/Fun4AllServer.h>

R__LOAD_LIBRARY(libfun4all.so)

bool checkForDir(std::string name)
{
  DIR* dir = opendir(name.c_str());

  return dir == NULL ? 0 : 1;
}

int Fun4All_runEvaluators(
    const int nEvents = 1,
    const string &inputFile = "myInputFile.root",
    const string &inputDir = ".",
    const int skip = 0,
    const string &outdir = ".")
{
  Fun4AllServer *se = Fun4AllServer::instance();
  se->Verbosity(0);

  Input::READHITS = true;
  INPUTREADHITS::filename[0] = inputDir + "/" + inputFile;

  InputInit();

  //-----
  // What to run
  //-----
  
  Enable::DSTREADER = false;
  Enable::USER = false;

  Enable::EVENT_EVAL = true;
  Enable::TRACKING_EVAL = true;
  Enable::CEMC_EVAL = true;
  Enable::HCALIN_EVAL = true;
  Enable::HCALOUT_EVAL = true;
  Enable::FEMC_EVAL = true;
  Enable::FHCAL_EVAL = true;
  Enable::EEMC_EVAL = true;
  Enable::FWDJETS_EVAL = true;

  Enable::CEMC_CLUSTER = true;

  //-----
  // Output file headers and path
  //-----
  
  std::string evalDir = outdir;
  std::string outdirLastChar = outdir.substr(outdir.size() - 1, 1);
  if (outdirLastChar != "/") evalDir += "/";

  unsigned int revisionWidth = 5;
  unsigned int revisionNumber = 0;
  std::ostringstream evalRevision;
  evalRevision << std::setfill('0') << std::setw(revisionWidth) << to_string(revisionNumber);
  evalDir += "eval_" + evalRevision.str();

  while (checkForDir(evalDir))
  {
    evalDir = evalDir.substr(0, evalDir.size() - revisionWidth);
    revisionNumber++;
    evalRevision.str("");
    evalRevision.clear();
    evalRevision << std::setfill('0') << std::setw(revisionWidth) << to_string(revisionNumber);
    evalDir += evalRevision.str(); 
  }

  std::string makeDirectory = "mkdir -p " + evalDir;
  system(makeDirectory.c_str());

  string outputroot = evalDir + "/" + inputFile;
  string remove_this = ".root";
  size_t pos = outputroot.find(remove_this);
  if (pos != string::npos)
  {
    outputroot.erase(pos, remove_this.length());
  }

  //-----
  // Reader and User analysis
  //-----

  if (Enable::DSTREADER) G4DSTreader_EICDetector(outputroot + "_DSTReader.root");
  if (Enable::USER) UserAnalysisInit();

  //-----
  // Evaluators
  //-----

  if (Enable::EVENT_EVAL) Event_Eval(outputroot + "_eventtree.root");

  if (Enable::TRACKING_EVAL) Tracking_Eval(outputroot + "_g4tracking_eval.root");

  if (Enable::CEMC_EVAL) CEMC_Eval(outputroot + "_g4cemc_eval.root");

  if (Enable::HCALIN_EVAL) HCALInner_Eval(outputroot + "_g4hcalin_eval.root");

  if (Enable::HCALOUT_EVAL) HCALOuter_Eval(outputroot + "_g4hcalout_eval.root");

  if (Enable::FEMC_EVAL) FEMC_Eval(outputroot + "_g4femc_eval.root");

  if (Enable::FHCAL_EVAL) FHCAL_Eval(outputroot + "_g4fhcal_eval.root");

  if (Enable::EEMC_EVAL) EEMC_Eval(outputroot + "_g4eemc_eval.root");

  //if (Enable::FWDJETS_EVAL) Jet_FwdEval();

  //--------------
  // Set up Input Managers
  //--------------

  InputManagers();

  //-----
  // Run
  //-----

  se->skip(skip);
  se->run(nEvents);

  //-----
  // Exit
  //-----

  se->End();
  std::cout << "All done" << std::endl;
  delete se;

  gSystem->Exit(0);
  return 0;
}

#endif
