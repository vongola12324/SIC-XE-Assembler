HexDig = {"0": 0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15}
DecDig = {0: "0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
opcode = {"ADD":"18", "ADDF":"58", "ADDR":"90", "AND":"40", "CLEAR":"B4", "COMP":"28", "COMPF":"88", "COMPR":"A0", "DIV":"24",
          "DIVF":"64", "DIVR":"9C", "FIX":"C4", "FLOAT":"C0", "HIO":"F4", "J":"3C", "JEQ":"30", "JGT":"34", "JLT":"38", "JSUB":"48",
          "LDA":"00", "LDB":"68", "LDCH":"50", "LDF":"70", "LDL":"08", "LDS":"6C", "LDT":"74", "LDX":"04", "LPS":"D0", "MUL":20,
          "MULF":"60", "MULR":"98", "NORM":"C8", "OR":"44", "RD":"D8", "RMO":"AC", "RSUB":"4C", "SHIFTL":"A4", "SHIFTR":"A8",
          "SIO":"F0", "SSK":"EC", "STA":"0C", "STB":"78", "STCH":"54", "STF":"80", "STI":"D4", "STL":"14", "STS":"7C", "STSW":"E8",
          "STT":"84", "STX":"10", "SUB":"1C", "SUBF":"5C", "SUBR":"94", "SVC":"B0", "TD":"E0", "TIO":"F8", "TIX":"2C", "TIXR":"B8",
          "WD":"DC"}
format = {"ADD":3, "ADDF":3, "ADDR":2, "AND":3, "CLEAR":2, "COMP":3, "COMPF":3, "COMPR":2, "DIV":3, "DIVF":3, "DIVR":2, "FIX":1,
          "FLOAT":1, "HIO":1, "J":3, "JEQ":3, "JGT":3, "JLT":3, "JSUB":3, "LDA":3, "LDB":3, "LDCH":3, "LDF":3, "LDL":3, "LDL":3,
          "LDS":3, "LDT":3, "LDX":3, "LPS":3, "MUL":3, "MULF":3, "MULR":2, "NORM":1, "OR":3, "RD":3, "RMO":2, "RSUB":3, "SHIFTL":2,
          "SHIFTR":2, "SIO":1, "SSK":3, "STA":3, "STB":3, "STCH":3, "STF":3, "STI":3, "STL":3, "STS":3, "STSW":3, "STT":3, "STX":3,
          "SUB":3, "SUBF":3, "SUBR":2, "SVC":2, "TD":3, "TIO":1, "TIX":3, "TIXR":2, "WD":3}
register = {"A":0, "X":1, "L":2, "B":3, "S":4, "T":5, "F":6, "PC":8, "SW":9}