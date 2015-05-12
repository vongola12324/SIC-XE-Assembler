from data import *


def pass2(logger, programSize, hrfout, ojfout):
    # Open file
    try:
        fin = open(".pass1.tmp", "r")
    except:
        logger.log("Can not open input file for pass2 with read mode!", error_flag=True)
        return
    try:
        ojout = open(ojfout, "w")
    except:
        logger.log("Can not open output file for pass2 with write mode!", error_flag=True)
        return

    try:
        hrout = open(hrfout, "w")
    except:
        logger.log("Can not open output file for pass2 with write mode!", error_flag=True)
        return

    line = fin.readline()
    word = line.strip().split(" ")
    while word.count("") > 0:
        word.remove("")
    if word[1] == "START":
        ojout.write(line)
    hrout.write("H" + word[1] + " " * (6 - int((len(word[1]) + 1)) % 6 + 1) + "00" + word[3] + "00" + hex(programSize)[2:].upper() + "\n")
    TStart = word[3]
    PgStart = word[3]
    ObjList = []
    objCount = 0
    objsize = 0
    tmp = ""
    newLine = False
    TextRecode = "T00" + TStart
    objLine = ""
    lineLength = 0
    (line, word) = getline(fin)
    while word.get("OPCODE") != "END":
        if word.get("LABEL") != ".":
            if OPTAB.get(word.get("OPCODE")) is not None:
                word.update({"OBJECTCODE":OPTAB.get(word.get("OPCODE"))})
                if word.get("OPER") is not None and word.get("OPER") is not "":
                    if len(word.get("OPER").split(",")) > 1:
                        tmp = word.get("OPER").split(",")[0]
                    else:
                        tmp = word.get("OPER")
                    if SYMTAB.get(tmp) is not None:
                        word.update({"OBJECTCODE":word.get("OBJECTCODE")+hex(SYMTAB.get(tmp)).upper()[2:]})
                        if len(word.get("OPER").split(",")) > 1:
                            tmp = word.get("OBJECTCODE")[:2] + chr(ord(word.get("OBJECTCODE")[2])+8) + word.get("OBJECTCODE")[3:]
                            word.update({"OBJECTCODE":tmp})
                    else:
                        logger.log("Undefined symbol!")
                        return
                else:
                    word.update({"OBJECTCODE":word.get("OBJECTCODE")+"0000"})
            elif word.get("OPCODE") == "BYTE" or word.get("OPCODE") == "WORD":
                tmp = word.get("OPER").split("\'")
                if len(tmp) > 1:
                    if tmp[0] == "C" or tmp[0] == "c":
                        tmp2 = ""
                        for i in tmp[1]:
                            tmp2 += hex(ord(i))[2:].upper()

                        word.update({"OBJECTCODE":tmp2})
                    else:
                        word.update({"OBJECTCODE":tmp[1].upper()})
                else:
                    tmp = hex(int(word.get("OPER")))[2:].upper()
                    while len(tmp) < 6:
                        tmp = "0" + tmp
                    word.update({"OBJECTCODE":tmp})

            if word.get("OPCODE") == "RESW" or word.get("OPCODE") == "RESB":
                newLine = True
            if objCount == 10 or (newLine and objCount != 0):
                # write Text record to object program
                lineLength = ObjSize(TStart, word.get("LOC"))
                if lineLength < 16:
                    tmp = "0" + hex(lineLength)[2:].upper()
                else:
                    tmp = hex(lineLength)[2:].upper()
                TextRecode += tmp
                for i in ObjList:
                    TextRecode += i
                hrout.write(TextRecode+"\n")
                ObjList = []
                TStart = word.get("LOC")
                TextRecode = "T00" + TStart
                newLine = False
                objCount = 0
            if word.get("OPCODE") != "RESB" and word.get("OPCODE") != "RESW":
                ObjList.append(word.get("OBJECTCODE"))
                objCount+=1

        if word.get("LABEL") != ".":
            ojout.write('{0:<4s}    {1:<8s} {2:<5s}  {3:<16s}  '.format(word.get("LOC"), word.get("LABEL") if word.get("LABEL") is not None else " ", word.get("OPCODE"), word.get("OPER") if word.get("OPER") is not None else " "))
        else:
            ojout.write(line)
        if word.get("LABEL") is not "." and word.get("OPCODE") is not "RESB" and word.get("OPCODE") is not "RESW":
            ojout.write('{0:<6s}\n'.format((word.get("OBJECTCODE") if word.get("OBJECTCODE") is not None else " ")))
        (line, word) = getline(fin)

        if objCount == 0 and newLine:
            if word.get("LOC") is not None:
                TStart = word.get("LOC")
                TextRecode = "T00" + word.get("LOC")
                newLine = False
                ObjList = []
    lineLength = ObjSize(TStart, word.get("LOC"))
    if lineLength < 16:
        tmp = "0" + hex(lineLength)[2:].upper()
    else:
        tmp = hex(lineLength)[2:].upper()
    TextRecode = "T00" + TStart + tmp
    for i in ObjList:
        TextRecode += i
    hrout.write(TextRecode+"\n")
    TextRecode = "E00" + hex(SYMTAB.get(word.get("OPER")))[2:].upper()
    hrout.write(TextRecode+"\n")
    ojout.write('{0:<4s}    {1:<8s} {2:<5s}  {3:<16s}  '.format(word.get("LOC"), word.get("LABEL") if word.get("LABEL") is not None else " ", word.get("OPCODE"), word.get("OPER") if word.get("OPER") is not None else " "))

def getline(fin):
    line = fin.readline()
    word = {}

    if line[0] == ".":
        word.update({"LABEL":"."})
        return line, word

    # Get Loc (0:8)
    lnsp = line[0:4].strip()
    if lnsp != "":
        word.update({"LOC": lnsp})

    # Get Label (4:12)
    lnsp = line[8:17].strip()
    if lnsp != "":
        word.update({"LABEL": lnsp})

    # Get Opcode (13:15)
    lnsp = line[17:24].strip()
    word.update({"OPCODE": lnsp})

    # Get Operand (17:35)
    lnsp = line[24:43].strip()
    word.update({"OPER": lnsp})

    # Get Comment (36:66)
    # lnsp = line[44:74].strip()
    # if lnsp != "":
    # word.update({"COMMENT": lnsp})
    return line, word


def writeline(fout, line, objcode):
    fout.write('{0} {1:<6s}\n'.format(line[:len(line)-2], objcode))
