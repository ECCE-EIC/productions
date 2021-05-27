#include <fun4all/Fun4AllDstInputManager.h>
#include <fun4all/Fun4AllServer.h>

R__LOAD_LIBRARY(libfun4all.so)

void testScript(std::string inputFile, std::string inputPath)
{
  gSystem->Load("libfun4all.so");
  gSystem->Load("libg4dst.so");

  std::string inputFilePath = inputPath + "/" + inputFile;

  Fun4AllServer *se = Fun4AllServer::instance();

  Fun4AllInputManager *dstin = new Fun4AllDstInputManager("DSTin");
  dstin->AddFile(inputFilePath);
  se->registerInputManager(dstin);

  se->run(1);
  se->End();
  delete se;
  gSystem->Exit(0);
}
