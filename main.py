from pass1 import pass1
from pass2 import pass2
from log import Logger
import sys
import os

# Program Info
__version__ = '1.0'
__author__ = 'vongola12324 <Vongola>'
__license__ = 'GNU General Public License Version 3, 29 June 2007'
__URI__ = 'https://github.com/vongola12324/SIC-XE-Assembler'

programSize = ""


def getArgvValue(key):
    if sys.argv.count(key) > 1:
        return sys.argv[sys.argv.index(key)+1]
    else:
        return None

def showHelp():
    print("SIC Assembler")
    print("-------------------------------------")
    print("main.py [--in filename][--hrout filename][--ojout filename][--debug]")
    print("\t--in\tSet input file")
    print("\t--hrout\tSet output file(Head Record)")
    print("\t--ojout\tSet output file(Object List)")
    print()

# Check Debug Mode
debug_mode = sys.argv.count("--debug")
if debug_mode == 0:
    debug_mode = False
else:
    debug_mode = True

logger = Logger(debug_mode=debug_mode)

if len(sys.argv) < 3:
    showHelp()
    print()

# Input / Output Init
fin = getArgvValue("--in")
if fin == None:
    fin = input("Enter Input Filename[Input.txt]: ")
    if len(fin) < 1:
        fin = "Input.txt"
else:
    logger.log("Input: " + fin)

hrout = getArgvValue("--hrout")
if hrout == None:
    hrout = input("Enter Output Filename[HeadRecord.txt]: ")
    if len(hrout) < 1:
        hrout = "HeadRecord.txt"
else:
    logger.log("HR Out: " + hrout)


ojout = getArgvValue("--ojout")
if ojout == None:
    ojout = input("Enter Output Filename[ObjectList.txt]: ")
    if len(ojout) < 1:
        ojout = "ObjectList.txt"
else:
    logger.log("OJ Out: " + ojout)



# Start

try:
    programSize = pass1(logger=logger, filename=fin)
except:
    logger.log("Pass 1 Failed, view the error log to get error message", error_flag=True)
    logger.endLog()
    sys.exit(1)
else:
    if logger.getErrorFlag():
        logger.log("Pass 1 Failed, view the error log to get error message", error_flag=True)
        logger.endLog()
        sys.exit(1)
    else:
        logger.log("Pass 1 Finished.")

# PASS 2, if pass1 successful
pass2(logger=logger, programSize=programSize, hrfout=hrout, ojfout=ojout)
if logger.getErrorFlag():
    logger.log("Pass 2 Failed, view the error log to get error message", error_flag=True)
    logger.endLog()
    sys.exit(1)
else:
    logger.log("Pass 2 Finished.")

if not logger.getErrorFlag():
    logger.endLog()
