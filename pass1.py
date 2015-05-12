from data import *

def pass1(logger, filename):
    # Open file
    try:
        fin = open(filename, "r")
    except:
        logger.log("Can not open input file for pass1 with read mode!", error_flag=True)
        return
    try:
        fout = open(".pass1.tmp", "w")
    except:
        logger.log("Can not open output file for pass1 with write mode!", error_flag=True)
        return

    # Get Start Label
    line = fin.readline()
    linenum = 1
    LOCCTR = 0
    nextLOC = LOCCTR
    word = line.strip().split(" ")
    while word.count("") > 0:
        word.remove("")
    if word[1] == "START":
        logger.log("Label \"START\" found at line 0!")
        logger.log("Use " + str(word[2]) + " as default LOCCTR and STARTADDR!")
        STARTADDR = int(word[2], 16)
        LOCCTR = STARTADDR
        fout.write("{0:04X}    {1:<8s} {2:<5s}  {3:<18s}".format(int(word[2], 16), word[0], word[1], str(word[2])) + "\n")
    else:
        logger.log("Label \"START\" not found!")
        logger.log("Use 0 as default LOCCTR and STARTADDR!")
        LOCCTR = 0
        STARTADDR = 0

    # Calc LOCCTR for every line excluding comment
    nextLOC = LOCCTR
    (line, word) = getline(fin)
    linenum += 1
    logger.log("Line \"" + str(linenum) + "\" loaded. ")
    while word.get("OPCODE") != "END":
        if word.get("LABEL") != "." and word.get("OPCODE") != ".":
            if word.get("LABEL") is not None:
                if SYMTAB.get(word.get("LABEL")) is None:
                    SYMTAB.update({word.get("LABEL"): LOCCTR})
                else:
                    logger.log("Duplicate symbol!", error_flag=True)
                    return
            if OPTAB.get(word.get("OPCODE")) is not None:
                logger.log("OpCode \"" + word.get("OPCODE") + "\" found at line " + str(linenum) + "! LOCCTR += 3")
                nextLOC += 3
            elif word.get("OPCODE") == "WORD":
                logger.log("OpCode \"WORD\" found at line " + str(linenum) + "! LOCCTR += 3")
                nextLOC += 3
            elif word.get("OPCODE") == "RESW":
                logger.log("OpCode \"RESW\" found at line " + str(linenum) + "! LOCCTR += " + str(3 * int(word.get("OPER"))))
                nextLOC += 3 * int(word.get("OPER"))
            elif word.get("OPCODE") == "RESB":
                logger.log("OpCode \"RESB\" found at line " + str(linenum) + "! LOCCTR += " + word.get("OPER"))
                nextLOC += int(word.get("OPER"))
            elif word.get("OPCODE") == "BYTE":
                operand = word.get("OPER").strip().split("\'")
                if operand[0] == 'C' or operand[1] == 'c':
                    nextLOC += len(operand[1])
                    logger.log("OpCode \"BYTE\" found at line " + str(linenum) + "! LOCCTR += " + str(len(operand[1])))
                else:
                    nextLOC += int(len(operand[1])/ 2)
                    logger.log("OpCode \"BYTE\" found at line " + str(linenum) + "! LOCCTR += " + str(len(operand[1]) / 2))

            else:
                logger.log("Invalid operation code!", error_flag=True)
                return
            writeline(fout, LOCCTR, word)
            LOCCTR = nextLOC
        else:
            fout.write(line)
        (line, word) = getline(fin)
        linenum += 1
    fout.write("{0:04X}    {1:<8s} {2:<5s}  {3:<18s}".format(LOCCTR, " ", word.get("OPCODE"), word.get("OPER")) + "\n")
    logger.log("Label \"END\" found at line " + str(linenum) + "!")
    return LOCCTR - STARTADDR


def getline(fin):
    line = fin.readline()
    word = {}
    if line[0] is ".":
        word.update({"LABEL":"."})
        return line, word

    # Get Label (0:8)
    lnsp = line[0:8].strip()
    if lnsp != "":
        word.update({"LABEL": lnsp})

    # Get Opcode (8:15)
    lnsp = line[8:16].strip()
    word.update({"OPCODE": lnsp})

    # Get Operand (17:35)
    lnsp = line[16:35].strip()
    word.update({"OPER": lnsp})

    # # Get Comment (36:66)
    # lnsp = line[36:66].strip()
    # if lnsp != "":
    # word.update({"COMMENT": lnsp})
    return line, word

def writeline(fout, locctr, word):
    fout.write('{0:<04X}    {1:<8s} {2:<5s}  {3:<18s}\n'.format(locctr, word.get("LABEL") if word.get("LABEL") is not None else " ",  word.get("OPCODE"), word.get("OPER")))
