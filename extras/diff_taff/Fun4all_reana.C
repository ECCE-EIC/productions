
//#include <G4_Bbc.C>
//#include <G4_DSTReader_EICDetector.C>
//#include <G4_FwdJets.C>
//#include <G4_Global.C>
//#include <G4_Input.C>
//#include <G4_Jets.C>
//#include <G4_Production.C>

#include <G4_User.C>

#include <TROOT.h>

#include <fun4all/Fun4AllDstInputManager.h>

#include <fun4all/Fun4AllDstOutputManager.h>
#include <fun4all/Fun4AllOutputManager.h>
#include <fun4all/Fun4AllServer.h>

#include <phool/recoConsts.h>

R__LOAD_LIBRARY(libfun4all.so)

int Fun4all_reana(){

    gSystem->Load("libfun4all.so");
    gSystem->Load("libg4dst.so");

  Enable::USER = true;

    
    Fun4AllServer *se = Fun4AllServer::instance();

//    se->Verbosity(INT_MAX - 10); 
//    se->Verbosity(1); 
    se->Verbosity(0); 
    
    Fun4AllInputManager *hitsin= new Fun4AllDstInputManager("DSTin");

    hitsin->AddListFile("myFileList.txt");

    // #Add your analysis modules here
    
    se->registerInputManager(hitsin);

  if (Enable::USER) UserAnalysisInit();

//    Int_t nEvents=10000;
    Int_t nEvents=100;

//    Int_t nEvents=1;

    se->run(nEvents);

    se->End();
    
    return 0;

}

