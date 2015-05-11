from data import *


def pass2(logger, programSize, hrfout, ojfout):
    # Open file
    try:
        fin = open(".pass1.tmp", "r")
    except:
        logger.log("Can not open input file for pass2 with read mode!", error_flag=True)
        return
    try:
        ojout = open(hrfout, "w")
    except:
        logger.log("Can not open output file for pass2 with write mode!", error_flag=True)
        return

    try:
        hrout = open(ojfout, "w")
    except:
        logger.log("Can not open output file for pass2 with write mode!", error_flag=True)
        return

    line = fin.readline()
    word = line.strip().split(" ")
    while word.count("") > 0:
        word.remove("")
    if word[1] == "START":
        ojout.write(line)
    hrout.write("H" + word[1] + " " * (6 - int((len(word[1]) + 1)) % 6) + "00" + word[3] + "00" + str(programSize) + "\n")
    TStart = word[3]
    ObjList = []
    objc = ""
    (line, word) = getline(fin)
    while word.get("OPCODE") != "END":
        if word.get("LOC") != ".":
            if OPTAB.get(word.get("OPCODE")):
                # print(SYMTAB)
                # print(word.get("OPER"))
                # print(SYMTAB.get(word.get("OPER")))
                if SYMTAB.get(word.get("OPER")) is not None:
                    word.update({"OPERADDR": SYMTAB.get(word.get("OPER"))})
                    objc = OPTAB.get(word.get("OPCODE")) + str(word.get("OPERADDR"))
                    if len(word.get("OPER").split(",")) > 1:
                        objca = []
                        for i in objc:
                            objca.append(ord(i))
                        objca[2] += 1
                        if objca[2] > 9:
                            objca[2] -= 10
                            objca[1] += 1
                        if objca[1] > 9:
                            objca[1] -= 10
                            objca[0] += 1
                        objc = ""
                        for i in objca:
                            objc += chr(i)
                else:
                    word.update({"OPERADDR": 0})
                    logger.log("Undefined symbol!", error_flag=True)
                    return
            else:
                word.update({"OPERADDR": 0})
            pass
        elif word.get("OPCODE") == "BYTE" or word.get("OPCODE") == "WORD":
            if word.get("OPER")[0] == "X":
                string = word.get("OPER").split("\'")[1]
                objc = string
            else:
                string = word.get("OPER").split("\'")[1]
                objc = ""
                for i in string:
                    objc = hex(ord(i))[2:]
        print(TStart)
        print(word.get("LOC"))
        if ObjSize(TStart, word.get("LOC")) > 30:
            TextRecode = "T" + "00" + TStart
            for i in ObjList:
                TextRecode += "00" + i
            hrout.write(TextRecode + "\n")
            ObjList = []
            ObjListSize = 0
            TStart = word.get("LOC")
        ObjList.append(objc)
        writeline(ojout, line, objc)
        (line, word) = getline(fin)
    TEnd = "T"
    for i in ObjList:
        TEnd += "00" + i
    hrout.write(TEnd)
    hrout.write("E" + SYMTAB.get(word.get("OPER")))
    ojout.write(line)


def getline(fin):
    line = fin.readline()
    word = {}
    if line[0] is ".":
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
    print (word)
    return line, word


def writeline(fout, line, objcode):
    fout.write('{0} {1:<6s}'.format(line, objcode))
