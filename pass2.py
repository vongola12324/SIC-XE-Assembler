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
    PgStart = word[3]
    ObjList = []
    objCount = 0
    objc = ""
    tmp = ""
    newLine = False
    TextRecode = "T00"
    objLine = ""
    (line, word) = getline(fin)
    while word.get("OPCODE") is not "END":
        if word.get("LABEL") is not ".":
            if OPTAB.get(word.get("OPCODE")) is not None:
                objc = "0" + OPTAB.get(word.get("OPCODE"))
                if word.get("OPER") is not None:
                    if len(word.get("OPER").split(",")) > 1:
                        tmp = word.get("OPER").split(",")[0]
                    else:
                        tmp = word.get("OPER")
                    if SYMTAB.get(tmp) is not None:
                        print(SYMTAB.get(tmp))
                        if len(word.get("OPER").split(",")) > 1:
                            word.update({"OPERADDR":hex(SYMTAB.get(tmp) | 32768).upper()})
                        else:
                            word.update({"OPERADDR":hex(SYMTAB.get(tmp)).upper()})
                    else:
                        logger.log("Undefined symbol!")
                        return
                else:
                    word.update({"OPERADDR":"0000"})
            elif word.get("OPCODE") is "BYTE" or word.get("OPCODE") is "WORD":
                tmp = word.get("OPER").split("\'")
                if len(tmp) > 1:
                    if tmp[0] is "C" or tmp[0] is "c":
                        objc == hex(int(tmp[1])).upper()
                    else:
                        objc = tmp[1]
                else:
                    tmp = hex(int(word.get("OPER"))).upper()
                    if len(tmp) < 6:
                        tmp += "0"
                    objc = tmp
            if word.get("OPCODE") is "RESW" or word.get("OPCODE") is "RESB":
                newLine = True
            if objCount is 10 or (newLine and objCount is not 0):
                # write Text record to object program
                lineLength = ObjSize(TStart, word.get("LOC"))
                if lineLength < 16:
                    tmp = "0" + hex(lineLength).upper()
                else:
                    tmp = hex(lineLength).upper()
                for i in ObjList:
                    TextRecode += i
                hrout.write(TextRecode)
                TextRecode = "T00" + TStart
                TStart = word.get("LOC")
                newLine = False
            elif objCount is 0 and newLine:
                # Next Text Record
                TextRecode = "T00" + TStart
                TStart = word.get("LOC")
                newLine = False
            if word.get("OPCODE") is not "RESB" and word.get("OPCODE") is not "RESW":
                ObjList.append(objc)
                objCount+=1

        ojout.write('{0:<4s}    {1:<8s} {2:<5s}  {3:<16s}  '.format(word.get("LOC"), word.get("LABEL"), word.get("OPCODE"), word.get("OPER")))
        if word.get("LABEL") is not "." and word.get("OPCODE") is not "RESB" and word.get("OPCODE") is not "RESW":
            ojout.write('{0:<6s}\n'.format(objc))
        (line, word) = getline(fin)
    lineLength = ObjSize(TStart, word.get("LOC"))
    if lineLength < 16:
        tmp = "0" + hex(lineLength).upper()
    else:
        tmp = hex(lineLength).upper()
    TextRecode = "T00" + tmp
    for i in ObjList:
        TextRecode += i
    hrout.write(TextRecode)
    TextRecode = "E00" + PgStart + tmp + "\n"
    hrout(TextRecode)
    ojout.write('{0:<4s}    {1:<8s} {2:<5s}  {3:<16s}  '.format(word.get("LOC"), word.get("LABEL"), word.get("OPCODE"), word.get("OPER")))



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
    fout.write('{0} {1:<6s}\n'.format(line[:len(line)-2], objcode))


# if word.get("OPCODE") == "BYTE" or word.get("OPCODE") == "WORD":
#             if word.get("OPER")[0] is "X" or word.get("OPER")[0] is "C" or word.get("OPER")[0] is "x" or word.get("OPER")[0] is "c":
#                 string = word.get("OPER").split("\'")[1]
#             else:
#                 string = word.get("OPER")
#             if word.get("OPER")[0] == "X":
#                 objc = string
#             else:
#                 objc = ""
#                 for i in string:
#                     objc = hex(ord(i))[2:]
#         elif word.get("LOC") != ".":
#             if OPTAB.get(word.get("OPCODE")) is not None:
#                 # print(SYMTAB)
#                 # print(word.get("OPER"))
#                 print(SYMTAB.get(word.get("OPER")))
#                 if SYMTAB.get(word.get("OPER")) is not None:
#                     word.update({"OPERADDR": SYMTAB.get(word.get("OPER"))})
#                 else:
#                     word.update({"OPERADDR": 0})
#             else:
#                 word.update({"OPERADDR": 0})
#             objc = OPTAB.get(word.get("OPCODE")) + str(word.get("OPERADDR"))
#             if len(word.get("OPER").split(",")) > 1:
#                 objca = []
#                 for i in objc:
#                     objca.append(ord(i))
#                 objca[2] += 1
#                 if objca[2] > 9:
#                     objca[2] -= 10
#                     objca[1] += 1
#                 if objca[1] > 9:
#                     objca[1] -= 10
#                     objca[0] += 1
#                 objc = ""
#                 for i in objca:
#                     objc += chr(i)
