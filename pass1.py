from data import *

def pass1(logger):

    # Open file
    try:
        fin = open("Input", "r")
    except:
        logger.log("Can not open input file for pass1 with read mode!", error_flag=True)
        return
    try:
        fout = open("intermediate", "w")
    except:
        logger.log("Can not open output file for pass1 with write mode!", error_flag=True)
        return

    # Get Start Label
    line = fin.readline()
    linenum = 1
    (line, word) = line.strip().split(" ")
    if word[1]=="START" :
        logger.log("Label \"START\" found at line 0!")
        logger.log("Use " + str(word[2]) + " as default LOCCTR and STARTADDR!")
        STARTADDR = word[2]
        LOCCTR = STARTADDR
        fout.write(line)
    else:
        logger.log("Label \"START\" not found!")
        logger.log("Use 0 as default LOCCTR and STARTADDR!")
        LOCCTR = 0
        STARTADDR = 0

    # Calc LOCCTR for every line excluding comment
    (line,word) = getline(fin)
    linenum += 1
    while word.get("OPCODE")!="END":
        if word.get("LABEL") != "." and word.get("OPCODE") != "." :
            if word.get("LABEL") != None:
                if SYMTAB.get(word.get("LABEL"))== None:
                    SYMTAB.update({word[0]:LOCCTR})
                else:
                    logger.log("Duplicate symbol!", error_flag=True)
                    return
            if opcode.get(word.get("OPCODE")) != None:
                logger.log("Label \"" + word.get("OPCODE") + "\" found at line " + str(linenum) + "! LOCCTR += 3")
                LOCCTR += 3
            elif word.get("OPCODE") == "WORD":
                logger.log("Label \"WORD\" found at line " + str(linenum) + "! LOCCTR += 3")
                LOCCTR += 3
            elif word.get("OPCODE") == "RESW":
                logger.log("Label \"RESW\" found at line " + str(linenum) + "! LOCCTR += " + str( 3 * int(word.get("OPER"))))
                LOCCTR += 3 * int(word.get("OPER"))
            elif word.get("OPCODE") == "RESB":
                logger.log("Label \"RESB\" found at line " + str(linenum) + "! LOCCTR += " + word.get("OPER"))
                LOCCTR += int(word.get("OPER"))
            elif word.get("OPCODE") == "BYTE":
                OPERAND = word.get("OPER").strip().split("\'")
                if OPERAND[0] == 'C' or OPERAND[1] == 'c':
                    LOCCTR += len(OPERAND[1])
                    logger.log("Label \"BYTE\" found at line " + str(linenum) + "! LOCCTR += " + str(len(OPERAND[1])))
                else:
                    LOCCTR += len(OPERAND[1])/2
                    logger.log("Label \"BYTE\" found at line " + str(linenum) + "! LOCCTR += " + str(len(OPERAND[1])/2))

            else:
                logger.log("Invalid operation code!", error_flag=True)
                return
            writeline(fout, LOCCTR, word)
        else:
            fout.write("        " + line)
        (line,word) = getline(fin)
        linenum += 1
    fout.write(toLoc(LOCCTR) + line)
    logger.log("Label \"END\" found at line " + str(linenum) + "!")
    return LOCCTR - STARTADDR

def getline(fin):
    line = fin.readline()
    word = {}

    # Get Label (0:8)
    lnsp = line[0:8].strip().split(" ")
    while lnsp.count("") > 0:
        lnsp.remove("")
    if lnsp != "":
        word.update({"LABEL":lnsp})

    # Get Opcode (9:15)
    lnsp = line[9:15].strip().split(" ")
    while lnsp.count("") > 0:
        lnsp.remove("")
    word.update({"OPCODE":lnsp})

    # Get Operand (17:35)
    lnsp = line[17:35].strip().split(" ")
    while lnsp.count("") > 0:
        lnsp.remove("")
    word.update({"OPER":lnsp})

    # Get Comment (36:66)
    lnsp = line[36:66].strip()
    if lnsp != "":
        word.update({"COMMENT":lnsp})

    return (line, word)

def writeline(fout, locctr, word):
    fout.write('{0:<04d}    {1:<8s} {2:<5s}  {3:<18s}'.format(locctr, word.get("LABEL") if word.get("LABEL")!= None else " ", word.get("OPCODE"), word.get("OPER")))