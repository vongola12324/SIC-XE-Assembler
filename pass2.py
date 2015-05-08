from data import *

def pass2(logger):
    # Open file
    try:
        fin = open("intermediate", "r")
    except:
        logger.log("Can not open input file for pass2 with read mode!", error_flag=True)
        return
    try:
        fout = open("Output", "w")
    except:
        logger.log("Can not open output file for pass2 with write mode!", error_flag=True)
        return




    pass


def writeHeaderRecord():
    pass