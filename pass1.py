from Table import *

def pass1():
    fin = open("Input", "r")
    fout = open("intermediate", "w")

    line = fin.readline()
    (line, word) = line.strip().split(" ")
    if word[1]=="START" :
        STARTADDR = word[2]
        LOCCTR = STARTADDR
        fout.write(line)
    else:
        LOCCTR = 0

    (line,word) = getline(fin)
    while word.get("OPCODE")!="END":
        if word.get("LABEL") != "." and word.get("OPCODE") != "." :
            if word.get("LABEL") != None:
                if SYMTAB.get(word.get("LABEL"))== None:
                    SYMTAB.update({word[0]:LOCCTR})
                else:
                    print("Error: Duplicate symbol!")
                    # Exit
            if opcode.get(word.get("OPCODE")) != None:
                LOCCTR += 3
            elif word.get("OPCODE") == "WORD":
                LOCCTR += 3
            elif word.get("OPCODE") == "RESW":
                LOCCTR += 3 * int(word.get("OPER"))
            elif word.get("OPCODE") == "RESB":
                LOCCTR += int(word.get("OPER"))
            elif word.get("OPCODE") == "BYTE":
                OPERAND = word.get("OPER").strip().split("\'")
                if OPERAND[0] == 'C' or OPERAND[1] == 'c':
                    LOCCTR += len(OPERAND[1])
                else:
                    LOCCTR += len(OPERAND[1])/2
            else:
                print("Error: Invalid operation code!")
        fout.write(toLoc(LOCCTR) + line)
        (line,word) = getline(fin)
    fout.write(toLoc(LOCCTR) + line)
    return LOCCTR - STARTADDR

def getline(fin):
    line = fin.readline()
    lnsp = line[:36].strip().split(" ")
    while lnsp.count("")>0 :
        lnsp.remove("")
    if len(lnsp) > 2:
        word = {"LABEL":lnsp[0], "OPCODE":lnsp[1], "OPER":lnsp[2]}
    else:
        word = {"OPCODE":lnsp[0], "OPER":lnsp[1]}
    return (line, word)
