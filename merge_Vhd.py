import os
import sys
import warnings
from time import sleep
import getopt

def merge_MBR(inputBinFile,templeteVhdFile = 'LEECHUNG.vhd',outputVhdFile = 'out.vhd'):
    with open(inputBinFile,"rb+") as bin:
        data = bin.read()

    with open(templeteVhdFile,"rb+") as vhd:
        vhd.seek(512,0)
        old = vhd.read()

    with open(outputVhdFile,"ab+") as out:
        out.write(data)
        out.write(old)

    print("success write MBR")
    return


def merge_UserBinFile(userFile,sourceFile='out.vhd'):
    with open(sourceFile,"rb+") as sr:
        sourceStream = sr.read()
        sizeUserFile = os.path.getsize(userFile)
        print("size:",sizeUserFile)
        sourceBefore = sourceStream[:sector*512]
        sourceAfter = sourceStream[sector*512+sizeUserFile:]

    with open(userFile,"rb+") as ur:
        usrData = ur.read()


    #os.remove(sourceFile)
    with open("out2.vhd","ab+") as op:
        op.write(sourceBefore)
        op.write(usrData)
        op.write(sourceAfter)

    os.remove(sourceFile)   
    print("Writing success! Generated a file : out2.vhd")
    return

def merge(sector,inputBinFile,userFile,templeteVhdFile ,outputVhdFile):
    flag = int(input("flag=2:MBR\nflag=1:MBR+UserFile\nflag=0:UserFile\nplease input a flag:\n"))    
    print("merging...")
   #print("inputBinFile + userFile + templeteVhdFile ----> outputVhdFile")
    if flag == 1:
        merge_MBR(inputBinFile,templeteVhdFile,outputVhdFile)
        merge_UserBinFile(userFile,outputVhdFile)

    if flag == 2:
        merge_MBR(inputBinFile,templeteVhdFile,outputVhdFile)

    if flag == 3:
        warnings.warn("This option may not often use!!")
        merge_UserBinFile(userFile,outputVhdFile)

    if flag not in [1,2,3]:
        print("wrong input!")
        exit(-1)


if __name__ =='__main__':
    userFile=''
    inputBinFile=''
    sector=0
    templeteVhdFile = 'LEECHUNG.vhd' 
    outputVhdFile = 'out.vhd'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:m:u:t:o:")

        for name,value in opts:
            if name in ('-h'):
                print("merge_Vhd.py -s <targetSector> -m <mbrFile> -u <userFile> -t <templeteVhdFile> -o <outputVhdFile>\n")  
                print("The first arguement: the sector that you want to write.")
                print("The second arguement: the MBR file.")
                print("The third arguement: the UserBin file.   (Optional)")
                print("The forth arguement: the templeteVhdFile, and the default file is LEECHUNG.vhd   (Optional)")
                print("The fifth argement: the MBR outputFile, and the default file is out.vhd      (Optional)")
                exit(0)
            elif name in ('-s'):
                sector=int(value)
                print("sector:",sector)
            elif name in ('-m'):
                inputBinFile = value
                print("MBR:",inputBinFile)
            elif name in ('-u'):
                userFile = value
                print("userFile:",userFile)
            elif name in ('-t'):
                templeteVhdFile = value
                print("templeteVhdFile:",templeteVhdFile)
            elif name in ('-o'):
                outputVhdFile = value
                print("outputVhdFile:",outputVhdFile)

    
    except getopt.GetoptError:
        print("python merge_Vhd.py -s <targetSector> -m <mbrile> -u <userFile> -t <templeteVhdFile> -o <outputVhdFile>")    
        exit(2)            
    merge(sector,inputBinFile,userFile,templeteVhdFile ,outputVhdFile)