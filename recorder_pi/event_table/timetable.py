#!/bin/python3
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,QTime
from recorder_pi.event_table.cam_factory import *
from recorder_pi.event_table.table_decoder import  *

"""
这些是您的Dissdafadfcord账号 ********32@**.**.***的备用码。请妥善保管！

hhd5-4cnx 
agop-u5p3 
y2de-syi4 
bj5s-wwh9 
g8ul-o407 
tslx-cvyt 
f73x-sra5 
r0zr-riv7 
vwcc-v3ha 
fz2k-81bx 
"""

CURRENT_COLUM_CNT = 5

TIMEBLOCK_KET_STARTIME = "startTime"
TIMEBLOCK_KET_ENDTIME  = "endTime"
TIMEBLOCK_KET_EVENT    = "type"
TIMEBLOCK_KET_WIDTH    = "width"
TIMEBLOCK_KET_HEIGHT   = "height"
TIMEBLOCK_KET_FRAMERATE = "framerate"
TIMEBLOCK_KET_OUTPUT   = "H264_Folder"
TIMEBLOCK_KET_ENABLE   = "enable"

class TimeBlock():
    __slots__ = ("__startTime", "__endTime", "__event", "__enable", "__configuration","__eventInstanceList")

    def __init__(self):
        factory = CameraFactoryImpl()
        self.__startTime = datetime.now().time()
        self.__endTime = datetime.now().time()
        self.__event = "libcamera-still"
        self.__enable = True
        self.__configuration = "None"
        self.__eventInstanceList = [factory.create_still(),factory.create_vid()]

    # 警告！！这里有个大坑，eventInstance的duration是由UI configuration列决定的！！！而不是由UI的duration列决定的
    # 具体原因是对eventInstance做更新的时候没有修改这里的duration
    # 这里的duration修改的时候也没有通知底下的Instance
    # 现在的应对方法是把这个类的duration在读写时强制更新到eventInstance里去

    @property
    def configuration(self) -> str:
        currentConfigInstance = self.configGetter()
        self.__configuration = currentConfigInstance.__str__()
        return self.__configuration
    @configuration.setter
    def configuration(self,refStr:str) -> None:
        currentConfigInstance = self.configGetter()
        currentConfigInstance.setRefDict(refStr)
        self.__configuration = currentConfigInstance.__str__()

    @property
    def configDict(self) -> dict:
        currentConfigInstance = self.configGetter()
        retDict = currentConfigInstance.RefDict
        retDict["duration"] = str(self.duration)
        return retDict
    @configDict.setter
    def configDict(self,refStr_or_dict:str or dict) -> None:
        if isinstance(refStr_or_dict,str):
            currentConfigInstance = self.configGetter()
            currentConfigInstance.setRefDict(refStr_or_dict)
            return
        elif isinstance(refStr_or_dict,dict):
            currentConfigInstance = self.configGetter()
            currentConfigInstance.RefDict = refStr_or_dict
            return

    @property
    def infoDict_complete(self) -> dict:
        cfgDict = self.configDict
        cfgDict[TIMEBLOCK_KET_STARTIME] = self.startTime
        cfgDict[TIMEBLOCK_KET_ENDTIME]  = self.endTime
        cfgDict[TIMEBLOCK_KET_ENABLE]    = "true" if self.enable else "false"
        return cfgDict

    @property
    def infoDict_qtComplete(self) -> dict:
        cfgDict = self.configDict
        table_startTime = self.startTime
        q_startTime = QTime(table_startTime.hour,table_startTime.minute,table_startTime.second)
        cfgDict["startTime"] =  q_startTime
        cfgDict["duration"] = self.duration
        cfgDict["enable"] = "On" if self.enable else "Off"
        cfgDict["configuration"] = self.configuration
        cfgDict["event"] = self.event
        return cfgDict


    def configIndex(self) -> int:
        if self.__event == "libcamera-still":
            return 0
        elif self.__event == "libcamera-vid":
            return 1

    def configGetter(self) -> LibCameraVid:# or LibCameraStill:
        if self.__event == "libcamera-still":
            return self.__eventInstanceList[0]
        elif self.__event == "libcamera-vid":
            return self.__eventInstanceList[1]

    @property
    def startTime(self) -> datetime.time:
        return self.__startTime
    @startTime.setter
    def startTime(self, startTime: time) -> None:
        self.__startTime = startTime
        return

    @property
    def endTime(self) -> datetime.date:
        return self.__endTime
    @endTime.setter
    def endTime(self, endTime: time) -> None:
        self.__endTime = endTime
        return

    @property
    def duration(self) -> int:
        # dura = datetime.combine(datetime.now().date(),datetime.now().time()) - \
        #        datetime.combine(datetime.now().date(),datetime.now().time())
        # dura = int(dura.seconds)
        dura = datetime.combine(datetime.now().date(),self.endTime) - \
               datetime.combine(datetime.now().date(),self.__startTime)
        dura = int(dura.total_seconds())
        self.__eventInstanceList[0]._duration = dura
        self.__eventInstanceList[1]._duration = dura
        return dura
    @duration.setter
    def duration(self,duration:int) -> None:
        endTime_d = timedelta(seconds=duration)
        endTime = datetime.combine(datetime.now().date(),self.__startTime)
        endTime += endTime_d
        self.__endTime = endTime.time()
        self.__eventInstanceList[0]._duration = duration
        self.__eventInstanceList[1]._duration = duration
        return

    @property
    def event(self) -> str:
        return self.__event
    @event.setter
    def event(self,event:str) -> None:
        if event == "libcamera-still":
            event_i = event
        elif event == "libcamera-vid":
            event_i = event
        else:
            raise ValueError
        self.__event = event_i

    @property
    def enable(self) -> bool:
        return self.__enable
    @enable.setter
    def enable(self,enable:bool) -> None:
        self.__enable = enable

    @property
    def timeleft(self) -> int:
        dura = datetime.combine(datetime.now().date(), self.startTime) - datetime.now()
        dura = int(dura.total_seconds())
        return dura

    def __str__(self):
        return self.__event


# class timeTable():
#     def __init__(self):
#         self.__timeHashTable = {"time":None}
#         self.__timeHashTable.keys()
#
#     def addBlockEvent(self,timeBlock:TimeBlock)->None:
#         self.__timeHashTable[timeBlock.startTime] = timeBlock
#
#     def readTimetableFromFile(self,fileName:str="timetable1.json"):
#         a = None
#         with open("timetable1.json", "r") as fp:
#             a = json.load(fp)
#         print(a.keys())
#
#     def readTimetableFromUi(self):
#         pass
#
#     def timetableIterator(self):
#         pass
#
#     def setTimeTable(self):
#         pass
#
#     def __iter__(self):
#         pass
#
#     def __next__(self):
#         pass

class QTimeTable(QtCore.QObject):
    testSignal1 = QtCore.pyqtSignal(str)
    testSignal2 = QtCore.pyqtSignal(str)
    # 自制控件信号必须是静态成员，要不然不起效
    def __init__(self):
        super(QTimeTable,self).__init__()
        # 这里我们使用QueuedConnection，即事件需要排队被处理而非抢占式中断
        self.testSignal1.connect(self.testSlot1,type=Qt.QueuedConnection)
        self.testSignal2.connect(self.testSlot,type=Qt.QueuedConnection)
        # self.testSignal1.connect(self.testSlot1)
        # self.testSignal2.connect(self.testSlot)
    @pyqtSlot(str)
    def testSlot(self,message:str):
        print(message)
        self.testSignal1.emit(message)
        #return
    @pyqtSlot(str)
    def testSlot1(self,message:str):
        print(message)
        self.testSignal2.emit(message)
        #return

class TimeTable(QtCore.QObject):
    enableUIRefresh = QtCore.pyqtSignal()
    def __init__(self):
        super(TimeTable, self).__init__()
        self.setProperty("eventTable_",[])

    def __RefreshTable(self, qtTableModel:QtCore.QAbstractItemModel) -> None:
        model = qtTableModel
        rowCnt = model.rowCount()
        eventTable_ = []
        for i in range(0,rowCnt,1):
            block1 = TimeBlock()
            rowinfo = {}
            idx_cur = model.index(i, 0)
            data = model.data(idx_cur)
            rowinfo["Event"] = data
            idx_cur = model.index(i, 1)
            data = model.data(idx_cur)
            rowinfo["StartTime_qtime"] = data
            idx_cur = model.index(i, 2)
            data = model.data(idx_cur)
            rowinfo["duration_int"] = data
            print("rowinfo[\"duration_int\"]",rowinfo["duration_int"])
            idx_cur = model.index(i, 3)
            data = model.data(idx_cur)
            rowinfo["Enable_str"] = data
            idx_cur = model.index(i, 4)
            data = model.data(idx_cur)
            rowinfo["Config_str"] = data
            print("rowinfo[\"Config_str\"]=",rowinfo["Config_str"])
            block1.event = rowinfo["Event"] if rowinfo["Event"] != None else "libcamera-still"
            block1.startTime =  rowinfo["StartTime_qtime"].toPyTime()
            block1.configDict = rowinfo["Config_str"] if rowinfo["Config_str"] != None else "libcamera-still"
            block1.enable = True if rowinfo["Enable_str"] == "On" else False
            block1.duration = rowinfo["duration_int"]
            eventTable_.append(block1)
            print(block1.configuration)
            print(block1.duration)
            print(block1.enable)
            print(block1.configDict)
            print(str(block1))
        self.setProperty("eventTable_",eventTable_)
        if len(eventTable_) != 0:
            print("adsfdsf", str(self.property("eventTable_")[0]))
            return
        else:
            print("No event in the new list.")

    def RefreshTableFromFile(self):
        self.enableUIRefresh.emit()
        pass

    def InsertEvent(self,timeBlock:TimeBlock) -> None:
        eventTable_ = self.property("eventTable_")
        eventTable_.append(timeBlock)
        self.setProperty("eventTable_", eventTable_)

    def GetNextEvent(self) -> tuple:#-> tuple[dict,int]:
        sortTimeLeft = []
        eventTable_ = self.property("eventTable_")
        for i in eventTable_:
            # i = TimeBlock()
            enable = i.enable
            timeleft = i.timeleft
            sortTimeLeft.append( (timeleft,enable) )
        nextEventIdx = self.__MinTimeLeft_idx(sortTimeLeft,True)
        if nextEventIdx != -1:
            timeleft = eventTable_[nextEventIdx].timeleft
            nextEventDict = eventTable_[nextEventIdx].configDict
            return (nextEventDict,timeleft)
        else:
            return (None,None)

    def __MinTimeLeft_idx(self, timeList:list, useEnable:bool=False) -> int:
        # 数据结构是 [ (time_int,enable_bool),...... ]
        try:
            min_new_idx,min_new = min(enumerate(filter(lambda x:x[0]>0 and x[1],timeList)),key=lambda x:x[1][0])
            min_new_idx = timeList.index(min_new)
            print(min_new,min_new_idx)
            return min_new_idx
        except Exception as E:
            print(E)
            print("Nothing valid found")
            return -1

    def __getitem__(self, index)-> TimeBlock or None:
        eventTable_ = self.property("eventTable_")
        table_cnt = len(eventTable_)
        try:
            block = eventTable_[index]
            return block
        except Exception as E:
            print(E)
            return None

    def __iter__(self):
        return self

    def __next__(self):
        pass

    def __add__(self, other):
        pass

    def __len__(self) -> int:
        eventTable_ = self.property("eventTable_")
        return len(eventTable_)


    @pyqtSlot()
    def RefreshFromUI(self,model:QtCore.QAbstractItemModel) -> None:
        self.__RefreshTable(model)
        # self.GetNextEvent()

    def SaveTableToJson(self, fileName: str = "timetable1.json") -> None:
        table = self.property("eventTable_")
        table_cnt = len(table)
        blockDict_list = []
        for i in range(0,table_cnt,1):
            block = table[i]
            # block = TimeBlock()
            infoDict = block.infoDict_complete
            infoDict_withJsonKey = timeblock_dict2json_dict(str(i),infoDict)
            # infoDict_withJsonKey = (str(i),infoDict)
            blockDict_list.append( infoDict_withJsonKey )
        blockdict_list_encode_jsonfile(blockDict_list,fileName)


    def ReadTableFromJson( self,fileName:str="timetable1.json") -> None:
        eventDictList_fromFile = jsonfile_decode_blockdict_list(fileName)
        for eventDict in eventDictList_fromFile:
            eventDict_cfgOnly = {}
            # 这里也要改成for循读取源字典然后刷新
            eventDict_keys = eventDict.keys()
            if TIMEBLOCK_KET_FRAMERATE in eventDict_keys:
                eventDict_cfgOnly[TIMEBLOCK_KET_FRAMERATE] = eventDict[TIMEBLOCK_KET_FRAMERATE]
            else:
                pass
            eventDict_cfgOnly[TIMEBLOCK_KET_HEIGHT] = eventDict[TIMEBLOCK_KET_HEIGHT]
            eventDict_cfgOnly[TIMEBLOCK_KET_WIDTH] = eventDict[TIMEBLOCK_KET_WIDTH]
            eventDict_cfgOnly[TIMEBLOCK_KET_OUTPUT] = eventDict[TIMEBLOCK_KET_OUTPUT]
            block = TimeBlock()
            block.event = eventDict[TIMEBLOCK_KET_EVENT]
            block.enable    = eventDict[TIMEBLOCK_KET_ENABLE]
            block.startTime = eventDict[TIMEBLOCK_KET_STARTIME]
            block.endTime   = eventDict[TIMEBLOCK_KET_ENDTIME]
            block.configDict = eventDict_cfgOnly
            self.InsertEvent(block)
        # 去驱动刷新
        self.enableUIRefresh.emit()


from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt

class MyModel(QAbstractItemModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            return QModelIndex()
        return self.createIndex(row, column)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return self._data[row][col]
        return None







if __name__ == "__main__":
    # a = TimeBlock()
    # print(a)
    # print(a.endTime)
    # #a.endTime = 9
    # print(a.endTime)
    # #a.startTime = 10
    # print(a.startTime)
    # print(a.duration)
    a = TimeBlock()
    a.duration = 1000
    print(a.startTime)
    print(a.endTime)
    a.event = "libcamera-vid"
    a.configuration = "libcamera-vid -t 0 --width 1920 --height 1080 --duration 1000"
    print(a.event)
    print(a.configuration)

    data = [[1, 2, 3,4,5],
            [4, 5, 6,7,8],
            [7, 8, 9,10,11]]
    model = MyModel(data)

    b = TimeTable()
    # b.__RefreshTable(model)

    # app = QtWidgets.QApplication([])
    # a = QTimeTable()
    # a.testSignal2.emit("dfsa")
    # app.exec_()


    # a.testSignal.connect(a.testSlot)

