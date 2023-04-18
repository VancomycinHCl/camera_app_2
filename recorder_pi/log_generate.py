#!/bin/python3
import logging
from colorama import Fore,Style
import colorlog

class CameraException(Exception):
    def __init__(self,msg):
        super(CameraException, self).__init__(msg)
        self.__str__ = msg


def Log_Init() ->  None:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %a %H:%M:%S',
                        filename='../log/test.log',
                        filemode='a')



    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.debug(Fore.GREEN+'Log System Started'+Fore.RESET)
    return console




if __name__ == "__main__":
    #logging.critical('Hwloooo')
    Log_Init()
    logging.debug(Fore.GREEN+'This is debug message'+Fore.RESET)
    logging.info('This is info message')
    logging.warning('This is warning message')
    #logging.critical("Programme Stopped!")