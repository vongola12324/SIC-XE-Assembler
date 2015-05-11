import os
import time
import datetime


class Logger():
    __debug_mode = False
    __err = None
    __log = None

    __log_name = "Execution.log"
    __err_name = "Execution-Error.log"
    __lastlog_time = None
    __error_flag = False
    __tstart = None

    def __init__(self, debug_mode=False):
        self.__debug_mode = debug_mode
        if self.__debug_mode:
            if os.access(self.__log_name, os.W_OK):
                self.__log = open(self.__log_name)
                self.__lastlog_time = self.__log.readline()[1:20]
                self.__log.close()
                os.rename(self.__log_name, self.__lastlog_time + "-" + self.__log_name)
            self.__log = open(self.__log_name, "w")
        if os.access(self.__err_name, os.W_OK):
            self.__err = open(self.__err_name)
            self.__lastlog_time = self.__err.readline()[1:20]
            self.__err.close()
            os.rename(self.__err_name, self.__lastlog_time + "-" + self.__err_name)
        self.__err = open(self.__err_name, "w")
        t = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        if self.__debug_mode:
            self.__log.write("[" + t + "]" + "INFO: Assembler Start!")
        self.__err.write("[" + t + "]" + "[INFO] Assembler Start!")
        self.__tstart = datetime.datetime.now()

    def log(self, string, error_flag=False):
        if error_flag:
            self.error(string)
            self.__error_flag = error_flag
        else:
            self.info(string)

    def info(self, string):
        info_str = "[" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + "]INFO: " + string
        if self.__debug_mode:
            self.logInFile(info_str)
            self.logInConsole(info_str)

    def error(self, string):
        error_str = "[" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + "]ERROR: " + string
        self.logInFile(error_str)
        self.logInConsole(error_str)

    def logInFile(self, string):
        if self.__debug_mode:
            self.__log.write(string)
        self.__err.write(string)

    def logInConsole(self, string):
        print(string)

    def getErrorFlag(self):
        return self.__error_flag

    def endLog(self):
        t = (datetime.datetime.now() - self.__tstart).seconds
        if not self.__error_flag:
            self.log("Assembler Finished!" + "(" + t + "s)")
        else:
            self.log("Assembler Stopped!" + "(" + t + "s)")
        if self.__debug_mode:
            self.__log.close()
        self.__err.close()
