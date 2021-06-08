#include <fun4all/Fun4AllDstInputManager.h>
#include <fun4all/Fun4AllServer.h>

R__LOAD_LIBRARY(libfun4all.so)

void writeMetaData(std::string inputFile, std::string inputPath, std::string logFileName)
{
  gSystem->Load("libfun4all.so");
  gSystem->Load("libg4dst.so");

  std::string inputFilePath = inputPath + "/" + inputFile;

  std::cout << "Getting metadata" << std::endl;
  std::string metadataFileName = inputFilePath.substr(0, inputFilePath.size() - 5) + ".txt";
 
  ifstream logFile;
  logFile.open(logFileName.c_str());

  std::string metadataStart = "====== Your production details ======";
  std::string metadataEnd = "=====================================";
  std::string seedString = "PHRandomSeed::GetSeed() seed: ";
  std::string line;

  ofstream metadataFile;
  metadataFile.open(metadataFileName.c_str());

  bool breakout = false;
  while(getline(logFile, line))
  {
    if (line.find(metadataStart) != std::string::npos) 
    {
      metadataFile << line << "\n";
      while(getline(logFile, line))
      {
        metadataFile << line << "\n";
        if (line.find(metadataEnd) != std::string::npos)
        {
          metadataFile << "\nSeeds:" << "\n";
          breakout = true;
          break;
        }
        if (breakout) break;
      }
    }
    if (line.find(seedString) != std::string::npos)
    {
      std::string thisSeed = line.substr(seedString.size(), line.size());
      metadataFile << thisSeed << "\n";
    }
  }    

  metadataFile.close();

  Fun4AllServer *se = Fun4AllServer::instance();

  Fun4AllInputManager *dstin = new Fun4AllDstInputManager("DSTin");
  dstin->AddFile(inputFilePath);
  se->registerInputManager(dstin);

  se->run(1);
  se->End();
  delete se;
  gSystem->Exit(0);

  std::cout << "Successfully ran an event on this DST!" << std::endl;
}
