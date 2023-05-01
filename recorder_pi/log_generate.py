#!/bin/python3
import logging
from datetime import datetime
from colorama import Fore,Style
import colorlog

class CameraException(Exception):
    def __init__(self,msg):
        super(CameraException, self).__init__(msg)
        self.__str__ = msg

class ColoredFormatter(logging.Formatter):

    level_color = {
            "DEBUG": Fore.LIGHTGREEN_EX + Style.BRIGHT,
            "INFO": Fore.LIGHTBLUE_EX  + Style.BRIGHT,
            "WARNING": Fore.LIGHTYELLOW_EX  + Style.BRIGHT,
            "ERROR": Fore.RED  + Style.BRIGHT,
            "CRITICAL": Fore.LIGHTRED_EX + Style.BRIGHT,
        }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.level_color:
            levelname_color = self.level_color[levelname] + levelname + Fore.RESET + Style.RESET_ALL
            record.levelname = levelname_color
        return super().format(record)

# def Log_Init(loggerName="default",logName="test",filePath="../log/") ->  logging.StreamHandler:
#     today = datetime.now().date().strftime("%Y-%m-%d")
#     fileName = logName+"_"+today+".log"
#     fileComplete = filePath+fileName
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s %(funcName)20s line:%(lineno)d [%(levelname)s] %(message)s',
#                         datefmt='%Y-%m-%d %a %H:%M:%S',
#                         filename=fileComplete,
#                         filemode='a')
#     console = logging.StreamHandler()
#     console.setLevel(logging.DEBUG)
#     formatter = ColoredFormatter('%(asctime)s %(filename)s %(funcName)s() line:%(lineno)d [%(levelname)s] %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
#     logging.debug(f'Log System Started')
#     return console


class cameraLogger:
    _instance = None
    def __new__(cls, loggerName="", logName="test", filePath="../log/"):
        # print(cls._instance)
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger(loggerName)
            cls._instance.logger.setLevel(logging.DEBUG)
            today = datetime.now().date().strftime("%Y-%m-%d")
            fileName = logName+"_"+today+".log"
            fileComplete = filePath+fileName
            file_handler = logging.FileHandler(fileComplete,mode="a+")
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)20s line:%(lineno)d [%(levelname)s] %(message)s')
            file_handler.setFormatter(formatter)
            console = logging.StreamHandler()
            # console.setLevel(logging.DEBUG)
            colored_formatter = ColoredFormatter('%(asctime)s %(filename)s %(funcName)s() line:%(lineno)d [%(levelname)s] %(message)s')
            console.setFormatter(colored_formatter)
            console.name=""
            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(console)
            cls._instance.logger.info('Log System Started')
            # print(cls._instance)
        else:
            # print("Branch B")
            # print(cls._instance)
            pass
        return cls._instance.logger

# global logger
# logger = cameraLogger()




if __name__ == "__main__":
    logger = cameraLogger()
    logger.critical("dsf")
    logger.error("hjgjh")
    logger.warning("ghhg")
    pass
    # #logging.critical('Hwloooo')
    # logger1 = cameraLogger()
    #
    # logger1.debug('Log1 debug message')
    # logger1.error('Log1 error message')
    #
    # logger2 = cameraLogger()
    # logger2.debug('Log2 debug message')
    # logger2.error('Log2 error message')
    #
    # print(logger1 is logger2)  # True
    # logging.debug(Fore.GREEN+'This is debug message'+Fore.RESET)
    # logging.info('This is info message')
    # logging.warning('This is warning message')
    # def A():
    #     logging.info("dsf",exc_info=True)
    #     return
    # def A1():
    #     A()
    # A1()