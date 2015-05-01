import os
import platform
import time

ErrName = "Error"
InfoName = "Uasge"
DirName = "Log"
SubName = ".log"

if platform.system() == "Windows":
    PathChar = "\\"
else:
    PathChar = "/"


class Logger:
    def __init__(self):
        if not os.path.exists(DirName):
            os.makedirs(DirName)
        if os.access(DirName + PathChar + ErrName + SubName, os.R_OK):
            self.file = open(DirName + PathChar + ErrName + SubName, "w")
            string = self.file.readline()
            string = string[1:20]
            self.file.close()
            os.rename(DirName + PathChar + ErrName + SubName, ErrName + "-" + string + SubName)
        self.stderr = open(DirName + PathChar + ErrName + SubName, "w")
        if os.access(DirName + PathChar + InfoName + SubName, os.R_OK):
            self.file = open(DirName + PathChar + InfoName + SubName, "w")
            string = self.file.readline()
            string = string[1:20]
            self.file.close()
            os.rename(DirName + PathChar + InfoName + SubName, InfoName + "-" + string + SubName)
        self.stdout = open(DirName + PathChar + InfoName + SubName, "w")

    def warn(self, string):
        t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        self.logInFile("[" + t + "]Warning : " + string)
        pass

    def info(self, string):
        t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        self.logInFile("[" + t + "]Info : " + string)
        pass

    def error(self, string):
        t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        self.logInFile("[" + t + "]Error : " + string, 1)
        pass

    def logInFile(self, string, error=0):
        self.stdout.write(string)
        if error == 1:
            self.stderr.write(string)

    def close(self):
        self.stdout.close()
        self.stderr.close()
