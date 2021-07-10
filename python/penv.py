#---------------------------------------------------------------------------------------------------
# Python Module File to describe out production environment.
#
# Author: C.Paus                                                                      (Jul 07, 2021)
#---------------------------------------------------------------------------------------------------
import os,sys

DEBUG = 0

#---------------------------------------------------------------------------------------------------
"""
Class:  GenFile(location='undefined', fileName='undefined', nEvents=2000000)

Each generator input file can be described by this class. Very important: file names have to be
unique. Even if the location is different fileName has to be unique.
"""
#---------------------------------------------------------------------------------------------------
class GenFile:
    "Description of a Generator Input file"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,location='/tmp',fileName='ep_noradcor.18x100lowq_run001.root',nEvents=2000000):
        self.location = location
        self.fileName = fileName
        self.nEvents = nEvents

    #-----------------------------------------------------------------------------------------------
    # present what we have
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print(" File: %s in %s (nEvts: %d)"%(self.fileName,self.location,self.nEvents))

#---------------------------------------------------------------------------------------------------
"""
Class:  Request(tag='undefined', hash='undefined', sample)

A request includes a specific configuration (tag and hash) and a sample to be processed.
"""
#---------------------------------------------------------------------------------------------------
class Request:
    "Description of a Request"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,tag,hash,sample):
        self.tag = tag
        self.hash = hash
        self.sample = sample

        self.loadCompletedJobs()
        self.loadQueuedJobs()

    #-----------------------------------------------------------------------------------------------
    # load all jobs that are queued (this is MIT specific, but can be easily replaced)
    #-----------------------------------------------------------------------------------------------
    def loadCompletedJobs(self):

        # initialize from scratch
        cmd = 'list /cms/store/user/paus/%s/%s/%s/%s/%s | grep .root$'\
              %(self.tag,self.hash,self.sample.physicsGroup,self.sample.generator,self.sample.collisions)
        if DEBUG > 0:
            print("CMD: %s"%cmd)
        for line in os.popen(cmd).readlines():
            f = line[:-1].split('/')
            lfn = f[-1]
            lfn = lfn.replace('.root','')
            lfn = lfn.replace('DST_','')
            if DEBUG > 0:
                print(' COMPLETED: %s'%(lfn))
            self.sample.addCompleted(lfn)

    #-----------------------------------------------------------------------------------------------
    # load all jobs that are queued (again specific but can be easily replaced: condor, slurm, ..)
    #-----------------------------------------------------------------------------------------------
    def loadQueuedJobs(self):

        # initialize from scratch
        cmd = 'condor_q paus -global -constraint JobStatus!=5 -format \'%s\n\' Args 2> /dev/null' \
              + '| grep \'%s %s\''%(self.tag,self.hash) \
              + '| grep \'%s %s %s\''%(self.sample.physicsGroup,self.sample.generator,self.sample.collisions)
        if DEBUG > 0:
            print("CMD: %s"%cmd)
        for line in os.popen(cmd).readlines():
            f = line[:-1].split(' ')
            lfn = "%s_%s_%s_%s_%s_%s"%(f[6],f[7],f[8],f[5],f[3],f[4])
            if DEBUG > 0:
                print(' QUEUED: %s'%(lfn))
            self.sample.addQueued(lfn)

    #-----------------------------------------------------------------------------------------------
    # present what we have
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print(" Tag: %s  Hash: %s"%(self.tag,self.hash))
        sample.show()

#---------------------------------------------------------------------------------------------------
"""
Class:  Sample(genInput='undefined', dataset='undefined', nEventsPerJob=2000)

Each sample we are producing can be described by this class.
"""
#---------------------------------------------------------------------------------------------------
class Sample:
    "Description of a datasample to be produced"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,
                 physicsGroup = "SIDIS",
                 generator = "pythia6",
                 collisions = "ep_18x100lowq2",
                 #genInput='inputFileLists/eic-smear_SIDIS_pythia6_ep_18x100_q2_low.list',
                 nEventsPerLfn=2000):

        # copy the key parameters
        self.physicsGroup = physicsGroup
        self.generator = generator
        self.collisions = collisions

        # derive
        self.dataset = "{}_{}_{}".format(self.physicsGroup,self.generator,self.collisions)
        #self.genInput = genInput
        self.genInput = 'inputFileLists/%s_%s_%s.list'%(self.physicsGroup,self.generator,self.collisions)
        self.nEventsPerLfn = nEventsPerLfn

        # define the content container
        self.genFiles = []
        self.nEventsTotal = 0
        self.allLfns = {}      # 0-missing, 1-queued, 2-completed

        # read the generator input files
        self.loadGenInput()

        # generate all resulting lfns
        self.makeLfns()
        
    #-----------------------------------------------------------------------------------------------
    # add one lfn that is in the queue
    #-----------------------------------------------------------------------------------------------
    def addQueued(self,lfn):
        if lfn in self.allLfns.keys():
            if self.allLfns[lfn] != 0:
                print(" WARNING -- queued lfn (%s) not in zero state: %d"%(lfn,self.allLfns[lfn]))
            self.allLfns[lfn] = 1
        else:
            print(" ERROR -- found lfn (%s) not in the list of all lfns."%lfn)
            print(" CRASH: %d"%(self.allLfns[lfn]))

    #-----------------------------------------------------------------------------------------------
    # add one lfn that is completed
    #-----------------------------------------------------------------------------------------------
    def addCompleted(self,lfn):
        if lfn in self.allLfns.keys():
            if self.allLfns[lfn] != 0:
                print(" WARNING -- completed lfn (%s) not in zero state: %d"%(lfn,self.allLfns[lfn]))
            self.allLfns[lfn] = 2
        else:
            print(" ERROR -- found lfn (%s) not in the list of all lfns."%lfn)
            print(" CRASH: %d"%(self.allLfns[lfn]))

    #-----------------------------------------------------------------------------------------------
    # read the generator input files
    #-----------------------------------------------------------------------------------------------
    def loadGenInput(self):

        # give notice that file already exists
        if os.path.exists(self.genInput):
            print(" INFO -- generator input file found: %s."%(self.genInput))
        else:
            print(" ERROR -- generator input file not found: %s."%(self.genInput))

        with open(self.genInput,'r') as fH:
            data = fH.read()

        for line in data.split('\n'):
            f = line.split(' ')
            if len(f) == 1 and f[0] != '':
                g = f[0].split('/')
                gF = GenFile("/".join(g[:-1]),g[-1],2000000)
                print(" WARNING -- line (%s) needs to contain 2 parameters (<fileName> <nEventsInFile>). Hardwired 2M for now!!"%line)
                self.genFiles.append(gF)
                self.nEventsTotal += gF.nEvents
            elif len(f) == 2:
                g = f[0].split('/')
                gF = GenFile("/".join(g[:-1]),g[-1],int(f[1]))
                self.genFiles.append(gF)
                self.nEventsTotal += gF.nEvents
            else:
                pass
                #print(" ERROR -- line (%s) needs to contain 2 parameters (<fileName> <nEventsInFile>)!"%line)

        return

    #-----------------------------------------------------------------------------------------------
    # generate the file ids that we need to produce
    #
    # - IMPORTANT: if there are not enough events in the last job the events are not used
    #-----------------------------------------------------------------------------------------------
    def makeLfns(self):

        i = 0
        for gF in self.genFiles:
            nSkip = 0
            if DEBUG > 0:
                print(" Processing(%d): %s"%(i,gF.fileName))
            while (nSkip+self.nEventsPerLfn <= gF.nEvents):
                lfn = "%s_%03d_%07d_%05d"%(self.dataset,i,nSkip,self.nEventsPerLfn)
                self.allLfns[lfn] = 0
                nSkip += self.nEventsPerLfn
                if DEBUG > 0:
                    print(' ALL: %s'%(lfn))
            i+=1

    #-----------------------------------------------------------------------------------------------
    # present the current samples
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print('')
        print(' ====  S a m p l e  ====')
        print(' Dataset       : ' + self.dataset)
        for gf in self.genFiles:
            gf.show()

        #for lfn in self.allLfns:
        #    if self.allLfns[lfn] == 0:
        #        print(" -Missing-> %s (%d)"%(lfn,self.allLfns[lfn]))

#---------------------------------------------------------------------------------------------------
"""
Class:  Submitter()

Each sample we are producing can be described by this class.
"""
#---------------------------------------------------------------------------------------------------
class Submitter:
    "Description of a job submitter"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,id):
        self.id = id
        self.submitFile = ""

    def submit(self,request):
        # make the work directory
        penvTgz = "penv_%s_%s.tgz"%(request.tag,request.hash)
        penvBase = "{}".format(os.getenv('PENV_BASE'))
        penvLog = "{}/{}_{}/{}"\
            .format(os.getenv('PENV_LOG'),request.tag,request.hash,request.sample.dataset)
        if not os.path.exists(penvLog):
            os.makedirs(penvLog)
        # move the relevant files if they are not already there
        if not os.path.exists("%s/%s"%(penvLog,penvTgz)):
            os.system("cp %s/../%s %s"%(penvBase,penvTgz,penvLog))
        if not os.path.exists("%s/ecce_simulate.sh"%penvLog):
            os.system("cp %s/extras/ecce_simulate.sh %s"%(penvBase,penvLog))
        self.submitFile = "{}/{}_{}.sub".format(penvLog,request.sample.dataset,self.id)
        (nMissing,nQueued,nDone) = self._writeSubmitFile(request)

        if (nMissing > 0):
            # now push it into condor
            cmd = "cd %s; condor_submit %s"\
                  %("/".join(self.submitFile.split('/')[:-1]),self.submitFile.split('/')[-1])
            print(" --> %s"%(cmd))
            #os.system(cmd)
        else:
            print("\n There are no missing jobs. We are all set.\n")

        return

    #-----------------------------------------------------------------------------------------------
    # -- internal --
    #-----------------------------------------------------------------------------------------------

    def _addJob(self,fileHandle,lfn,argument):
        fileHandle.write("arguments = %s\n"%(argument))
        fileHandle.write("error = {}.err\n".format(lfn))
        fileHandle.write("output = {}.out\n".format(lfn))
        fileHandle.write("queue 1\n\n")
    
        return

    def _writeHeader(self,fileHandle,dataset):
        fileHandle.write("executable = ecce_simulate.sh\n")
        fileHandle.write("request_cpus = 1\n")
        fileHandle.write("request_memory = 2 GB\n")
        fileHandle.write("request_disk = 3 GB\n")
        fileHandle.write("should_transfer_files = YES\n")
        fileHandle.write("transfer_input_files = penv.tgz\n")
        fileHandle.write("#------------------------------------------------------------------\n")
        fileHandle.write("Requirements = ( regexp(\"T3B.*\",MACHINE) || regexp(\"T2.*\",MACHINE) )\n")
        fileHandle.write("use_x509userproxy = True\n")
        fileHandle.write("+SkipAllChecks = True\n")
        fileHandle.write("+ProjectName = \"EIC\"\n")
        fileHandle.write("#+SingularityImage = \"/cvmfs/eic.opensciencegrid.org/singularity/rhic_sl7_ext\"\n")
        fileHandle.write("#+SingularityBindCVMFS = True\n")
        fileHandle.write("#+SingularityAutoLoad  = True\n")
        fileHandle.write("#+DESIRED_Sites=\"JLab-FARM-CE\"\n")
        fileHandle.write("log = {}.log\n\n".format(dataset))
    
        return

    def _writeSubmitFile(self,request):
        print('')
        print(" Submit file: %s"%(self.submitFile))
        with open(self.submitFile,'w') as fH:
            self._writeHeader(fH,request.sample.dataset)
            nMissing = 0
            nDone = 0
            nQueued = 0
            for lfn in sorted(request.sample.allLfns.iterkeys()):
                if request.sample.allLfns[lfn] == 0:
                    # recover pertinent information from the lfn
                    fid = lfn.split("_")[-3]
                    nskip = lfn.split("_")[-2]
                    nevts = lfn.split("_")[-1]
                    nevts.replace(".root","")
                    inputFile = "/tmp/%s"%(request.sample.genFiles[int(fid)].fileName)
                    args = "%s %s %s %s %s %s %s %s %s"%\
                           (request.tag,request.hash,inputFile,nskip,nevts,fid, \
                            request.sample.physicsGroup,request.sample.generator,request.sample.collisions)
#                           from ecce_simulate.sh
#                           export tag="$1"
#                           export hash="$2"
#                           export inputFile="$3"
#                           export nskip="$4"
#                           export nevts="$5"
#                           export fid="$6"
#                           export pwg="$7"
#                           export gen="$8"
#                           export coll="$9"
                    self._addJob(fH,lfn,args)
                    nMissing += 1
                elif request.sample.allLfns[lfn] == 1:
                    nQueued += 1
                elif request.sample.allLfns[lfn] == 2:
                    nDone += 1

        print('')
        print(" ====  J o b   S u m m a r y  ==== ")
        print(" Adding to queue: %d"%(nMissing))
        print(" Queued already:  %d"%(nQueued))
        print(" Done already:    %d"%(nDone))
        print(" Total counts:    %d"%(len(request.sample.allLfns)))

        return (nMissing,nQueued,nDone)

