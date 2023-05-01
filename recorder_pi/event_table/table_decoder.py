# file: table_decoder.py
# author: 2112484232@qq.com
# version: 0.2.0
# description: File interface between event table and json file

import json
from datetime import datetime,date,timedelta,time
try:
    import recorder_pi.log_generate as log_generate
    # from recorder_pi.log_generate import logger
except:
    import log_generate
    # import log_generate.logger
# local_logger = log_generate.logger
local_logger = log_generate.cameraLogger()

EVENT_KEY = "event"
START_TIME_KEY = "startTime"
END_TIME_KEY = "endTime"

TIMEBLOCK_KET_STARTIME  = "startTime"
TIMEBLOCK_KET_ENDTIME   = "endTime"
TIMEBLOCK_KET_EVENT     = "type"
TIMEBLOCK_KET_WIDTH     = "width"
TIMEBLOCK_KET_HEIGHT    = "height"
TIMEBLOCK_KET_FRAMERATE = "framerate"
TIMEBLOCK_KET_OUTPUT    = "H264_Folder"
TIMEBLOCK_KET_ENABLE    = "enable"

#   警告！ EVENT DICT，即json转进来的数据结构，是需要重新写一个类的！！！！！ 这里没写！！！注意一定要改！！！！
#   我只做了个裸结构一点封装都没有！！！！


class JSONFileFormateError(Exception):
    def __init__(self,msgKey:str):
        super(JSONFileFormateError,self).__init__()
        print("%s is invalid at Key:"%(msgKey),end="  ")

class FileDictHasNoStartTime(JSONFileFormateError):
    def __init__(self,msgKey:str,timeName:str or None):
        super(FileDictHasNoStartTime,self).__init__(msgKey)
        if timeName:
            print("Because it has invalid start time (%s)."%(timeName))
        else:
            print("Because it has no start time given")

class FileDictHasWrongTime(JSONFileFormateError):
    def __init__(self,msgKey:str,timeName:str or None):
        super(FileDictHasWrongTime,self).__init__(msgKey)
        if timeName:
            print("Because it has invalid time (%s)."%(timeName))
        else:
            print("Because it has no time given")

class FileDictHasNoEvent(JSONFileFormateError):
    def __init__(self,msgKey:str,eventName:str or None):
        super(FileDictHasNoEvent,self).__init__(msgKey)
        if eventName:
            print("Because it has invalid Event (%s)."%(eventName))
        else:
            print("Because it has no event")

def timeblock_dict2json_dict(blockKeyVal:str,blockDictVal:dict) -> tuple:
    jsonDict = {}
    # 这里需要改成利用for循环获取字典内键值对然后自动写新字典的函数，以做到不同事件之间的解耦
    startTime = blockDictVal[TIMEBLOCK_KET_STARTIME]
    endTime   = blockDictVal[TIMEBLOCK_KET_ENDTIME]
    height    = blockDictVal[TIMEBLOCK_KET_HEIGHT]
    width     = blockDictVal[TIMEBLOCK_KET_WIDTH]
    enable    = blockDictVal[TIMEBLOCK_KET_ENABLE]
    startTime = startTime.strftime("%H:%M:%S")
    endTime   = endTime.strftime("%H:%M:%S")
    height    = str(height)
    width     = str(width)
    jsonDict[TIMEBLOCK_KET_STARTIME] = startTime
    jsonDict[TIMEBLOCK_KET_ENDTIME]  = endTime
    jsonDict[TIMEBLOCK_KET_HEIGHT]   = height
    jsonDict[TIMEBLOCK_KET_WIDTH]    = width
    jsonDict[TIMEBLOCK_KET_OUTPUT]   = blockDictVal[TIMEBLOCK_KET_OUTPUT]
    jsonDict[TIMEBLOCK_KET_EVENT]    = blockDictVal[TIMEBLOCK_KET_EVENT]
    jsonDict[TIMEBLOCK_KET_ENABLE]   = enable
    return (blockKeyVal,jsonDict)

def blockdict_list_encode_jsonfile(jsonDictList:list,fileName:str="timetable1.json") -> None:
    with open(fileName,"w+") as fp:
        finalJsonDict = {}
        for singleEventDict in jsonDictList:
            singleEventKey   = singleEventDict[0]
            singleEventDict  = singleEventDict[1]
            finalJsonDict[singleEventKey] = singleEventDict
            # print(singleEventDict)
        json.dump(finalJsonDict,fp,indent="    ")

def json_dict2timeblock_dict(jsonKeyVal:str,jsonDictVal:dict) -> dict or None:
    try:
        jsonDictVal_keyList = jsonDictVal.keys()
        # print(jsonDictVal)
        if "type" not in jsonDictVal_keyList:
            raise FileDictHasNoEvent(EVENT_KEY,None)
        elif "startTime" not in jsonDictVal_keyList:
            raise FileDictHasNoStartTime(START_TIME_KEY,None)
    except Exception as E:
        print(E)
        return None
    returnDict = {}
    try:
        timeStr = jsonDictVal["startTime"]
        returnDict[TIMEBLOCK_KET_STARTIME] = datetime.strptime(timeStr, "%H:%M:%S").time()
    except Exception as E:
        print(E)
        return None
    try:
        timeStr = jsonDictVal["endTime"]
        returnDict[TIMEBLOCK_KET_ENDTIME] = datetime.strptime(timeStr, "%H:%M:%S").time()
    except Exception as E:
        print(E)
        return None
    try:
        event = jsonDictVal["type"]
        if event != "libcamera-still" and event != "libcamera-vid":
            raise FileDictHasNoEvent(EVENT_KEY,event)
        returnDict[TIMEBLOCK_KET_EVENT]   = event
    except Exception as E:
        print(E)
        return None
    try:
        width = jsonDictVal["width"]
        returnDict[TIMEBLOCK_KET_WIDTH]   = int(width)
    except Exception as E:
        print(E)
        returnDict[TIMEBLOCK_KET_WIDTH]   = 1920
    try:
        height = jsonDictVal["height"]
        returnDict[TIMEBLOCK_KET_HEIGHT]   = int(height)
    except Exception as E:
        print(E)
        returnDict[TIMEBLOCK_KET_HEIGHT]   = 1080
    try:
        framerate = jsonDictVal["framerate"]
        returnDict[TIMEBLOCK_KET_FRAMERATE]   = int(framerate)
    except Exception as E:
        # print(E)
        local_logger.warning(f"{E} is not found in the key number [{jsonKeyVal}] from json timetable.")#,exc_info=True)
        returnDict[TIMEBLOCK_KET_FRAMERATE]   = 25
    try:
        enable = jsonDictVal["enable"]
        if enable != "true" and enable != "false":
            raise ValueError
        returnDict[TIMEBLOCK_KET_ENABLE] = True if enable == "true" else False
    except Exception as E:
        print(E)
        print("record %s has invalid enable option"%(jsonKeyVal))
        returnDict[TIMEBLOCK_KET_ENABLE] = True
    try:
        output = jsonDictVal[TIMEBLOCK_KET_OUTPUT]
        returnDict[TIMEBLOCK_KET_OUTPUT] = output
    except Exception as E:
        print(E)
        returnDict[TIMEBLOCK_KET_OUTPUT] = ""
    return returnDict

def jsonfile_decode_blockdict_list(fileName:str="timetable1.json") -> list:
    with open(fileName,"r") as fp:
        a = json.load(fp)
        jsonKeyList = a.keys()
        blockList = []
        for i in jsonKeyList:
            block = json_dict2timeblock_dict(i, a[i])
            blockList.append(block)
    return blockList


if __name__ == "__main__":
    a = jsonfile_decode_blockdict_list()
    for i in a:
        print(i)

