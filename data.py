HexDig = {"0": 0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15}
DecDig = {0: "0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
OPTAB = {"ADD":"18", "ADDF":"58", "ADDR":"90", "AND":"40", "CLEAR":"B4", "COMP":"28", "COMPF":"88", "COMPR":"A0", "DIV":"24",
          "DIVF":"64", "DIVR":"9C", "FIX":"C4", "FLOAT":"C0", "HIO":"F4", "J":"3C", "JEQ":"30", "JGT":"34", "JLT":"38", "JSUB":"48",
          "LDA":"00", "LDB":"68", "LDCH":"50", "LDF":"70", "LDL":"08", "LDS":"6C", "LDT":"74", "LDX":"04", "LPS":"D0", "MUL":20,
          "MULF":"60", "MULR":"98", "NORM":"C8", "OR":"44", "RD":"D8", "RMO":"AC", "RSUB":"4C", "SHIFTL":"A4", "SHIFTR":"A8",
          "SIO":"F0", "SSK":"EC", "STA":"0C", "STB":"78", "STCH":"54", "STF":"80", "STI":"D4", "STL":"14", "STS":"7C", "STSW":"E8",
          "STT":"84", "STX":"10", "SUB":"1C", "SUBF":"5C", "SUBR":"94", "SVC":"B0", "TD":"E0", "TIO":"F8", "TIX":"2C", "TIXR":"B8",
          "WD":"DC"}

SYMTAB = {}

def toLoc(LOCCTR):
    string = ""
    loc = LOCCTR
    while loc > 15 :
        print("loc = " + str(loc) + " str = " + string)
        string += DecDig.get(loc%16)
        loc = int((loc-loc%16)/16)
    string = DecDig.get(LOCCTR) + string
    while len(string) < 4:
        string = "0" + string
    return string

def ObjSize(Tstart, NowObj):
    start = int(Tstart, 16)
    end = int(NowObj, 16)
    return end - start

def toDec(HexStr):
    ans = 0
    for i in HexStr:
        ans = ans * 16 + HexDig.get(i)
    return ans

def toHex(DecStr):
    hexstr = ""
    while DecStr > 16:
        hexstr += DecDig.get(DecStr%16)
        DecStr = (DecStr - DecStr%16)/16
    hexstr += DecDig.get(DecStr%16)
    return hexstr
