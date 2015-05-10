from pass1 import pass1
from pass2 import pass2
from log import Logger
import sys

# Program Info
__version__ = '1.0'
__author__ = 'vongola12324 <Vongola>'
__license__ = 'GNU General Public License Version 3, 29 June 2007'
__URI__ = 'https://github.com/vongola12324/SIC-XE-Assembler'

programSize = ""


debug_mode = False
logger = Logger(debug_mode)

programSize = pass1(logger=logger)
if logger.getErrorFlag():
    logger.log("Pass 1 Failed, view the error log to get error message", error_flag=True)
    logger.endLog()
    sys.exit(1)
else:
    logger.log("Pass 1 Finished.")

# PASS 2, if pass1 successful
pass2(logger=logger, programSize)
if logger.getErrorFlag():
    logger.log("Pass 2 Failed, view the error log to get error message", error_flag=True)
    logger.endLog()
    sys.exit(1)
else:
    logger.log("Pass 2 Finished.")

if not logger.getErrorFlag():
    logger.endLog()
