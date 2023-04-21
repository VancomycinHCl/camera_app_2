import logging
import os

import PyQt5.QtCore, PyQt5.QtWidgets

from record import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
import driver.camera_test as A
import log_generate
from datetime import datetime
try:
    from recorder_pi.event_table.timetable import TimeTable
except:
    from event_table.timetable import TimeTable

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.recordImme_flag = False
        self.showPreview_flag = False
        self.autoConversion_flag = False
        self.logger = log_generate.logger
        self.settings = {
            "H264_Folder": None,
            "MP4_Folder": None,
            "width": None,
            "height": None,
            "duration": "0",
            "iniFile": None,
            "framerate": None,
            "lens-position":None
        }
        self.actionOpen_Setting_File.triggered.connect(lambda: self.Open_Setting_File())
        self.actionSave_Settings.triggered.connect(lambda: self.Save_Setting_File())
        self.Open_Setting_File_init("../config.ini")
        self.timeTable_cusMod = TimeTable()
        self.qtableClipboard = []
        #这里是自制模型与UI刷新的槽函数绑定，逻辑是一旦文件读取完成就emit信号驱使UI刷新
        self.timeTable_cusMod.enableUIRefresh.connect(self.refreshUIFromModel)
        self.timeTable_cusMod.ReadTableFromJson()
        self.refreshUIFromModel()
        # self.tableWidget_timeTable.setCellWidget(0,0,)

    @property
    def Setting(self) -> dict:
        return self.settings

    @Setting.setter
    def Setting(self, dictIn) -> None:
        self.settings = dictIn

    def applySettings(self) -> bool:
        logging.info("Apply Setting Function Executed!")
        print(self.WeightBox.text())
        time_min = int(self.timeEdit_duration.time().toPyTime().minute)
        time_sec = int(self.timeEdit_duration.time().toPyTime().second)
        fps = int(self.FPS.value())
        width = int(self.WeightBox.value())
        height = int(self.HeightBox.value())
        filePath = self.filePath_H264.text()
        print(width, height, fps, filePath)
        self.settings["width"] = width
        self.settings["height"] = height
        self.settings["framerate"] = fps
        self.settings["H264_folder"] = filePath
        if (time_min * 60 + time_sec) >= 59 * 60:
            QMessageBox.warning(self,
                                "Time Out Warning!",
                                "Your time setting has Larger than potential recording period, which will cause access conflict on the device. Please set the video duration smaller than 1 hour")
            logging.warning("An Unsuitable Time Duration was set! Please set another proper duration!")
            return False
        else:
            self.settings["duration"] = str((time_sec + time_min * 60) * 1000)
        print(self.settings["duration"])
        return True

    def openOutputH264File(self):
        self.settings['H264_Folder'] = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        if self.settings['H264_Folder'] != '':
            self.filePath_H264.setText(self.settings['H264_Folder'])
        print(self.settings['H264_Folder'])

    def openOutputMP4File(self):
        self.settings['MP4_Folder'] = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        if self.settings['MP4_Folder'] != "":
            self.filePath_MP4.setText(self.settings['MP4_Folder'])
        print(self.settings['MP4_Folder'])

    def Open_Setting_File(self):
        self.settings["iniFile"] = QtWidgets.QFileDialog.getOpenFileName()[0]
        camera_config, path_config, other_config = A.readConfig(self.settings["iniFile"])
        self.settings = self.settings | camera_config
        self.HeightBox.setValue(int(self.settings["height"]))
        self.WeightBox.setValue(int(self.settings["width"]))
        self.FPS.setValue(int(self.settings["framerate"]))
        self.filePath_H264.setText(path_config["root_path"] + path_config["raw_path"])
        self.filePath_MP4.setText(path_config["root_path"] + path_config["mp4_path"])
        self.filePath_H264.home(False)
        self.filePath_MP4.home(False)
        print(camera_config, path_config, other_config)
        print(self.settings["iniFile"], self.settings)
        pass

    def Open_Setting_File_init(self, filePath):
        camera_config, path_config, other_config = A.readConfig(filePath)
        self.settings = self.settings | camera_config
        self.settings = self.settings | other_config
        self.settings = self.settings | path_config
        self.HeightBox.setValue(int(self.settings["height"]))
        self.WeightBox.setValue(int(self.settings["width"]))
        self.FPS.setValue(int(self.settings["framerate"]))
        self.spinBox_cameraDistance.setValue(float(self.settings["lens-position"]))
        self.filePath_H264.setText(path_config["root_path"] + "/" + path_config["raw_path"])
        self.filePath_H264.home(False)


    def Save_Setting_File(self):
        self.settings["iniFile"] = QtWidgets.QFileDialog.getOpenFileName()
        logging.debug('Init file saved as %s' % (self.settings["iniFile"][0]))

    def MergeSettingsFromEvent(self,eventReference_dict:dict):
        # print(eventReference_dict)
        H264_event = eventReference_dict["H264_Folder"]
        width_event = eventReference_dict["width"]
        height_event = eventReference_dict["height"]
        duration_event = eventReference_dict["duration"]
        type_event   = eventReference_dict["type"]
        if "framerate" in eventReference_dict.keys() and type_event == "libcamera-vid":
            framerate_event = eventReference_dict["framerate"]
            self.settings["framerate"] = framerate_event
        if H264_event == "" or H264_event == None:
            pass
        else:
            self.settings["H264_folder"] = H264_event
        self.settings["width"] = width_event
        self.settings["height"] = height_event
        self.settings["duration"] = duration_event
        self.settings["type"] = type_event
        print("Merge setting dict:",self.settings)


    # 这个函数负责定时检查事件，如果今天还有事儿就自动装载表格事件进左边面板，并且把设置立即应用过来
    # 如果今天没事儿了就启动每天一次的定时检查分支，该分支只负责检查下一天凌晨开始有没有事件，没有重新装订每天一次的检查
    # 接上面那句话，如果有事，就把信息装订进左面面板伺机而动
    def CheckScheduludeAndExecute(self):
        self.genTimer()
        self.genTimerCheckNextDayEvent()
        if self.recordImme_flag == True:
            eventReference,timeRemain_s = self.timeTable_cusMod.GetNextEvent()
            if eventReference == None:
                timeRemain_s = datetime(datetime.now().year,datetime.now().month,datetime.now().day,23,59,59) - datetime.now()
                timeRemain_s = timeRemain_s.total_seconds()
                timeRemain_ms = timeRemain_s * 1000
                self.threadTimer_checkNextDay.start(timeRemain_ms)
                return
            else:
                timeRemain_ms = timeRemain_s * 1000
                self.threadTimer.start(timeRemain_ms)
                self.MergeSettingsFromEvent(eventReference)
                self.applySettings()
                return
        else:
            self.threadTimer_checkNextDay.stop()


    def recordEachHour_disableImmeButton(self):
        self.recordImme_flag = not self.recordImme_flag
        self.pushButton_recordImme.setDisabled(self.recordImme_flag)
        self.genTimer()
        self.genTimerCheckNextDayEvent()
        if self.recordImme_flag == True:
            self.applySettings()
            self.CheckScheduludeAndExecute()
            # timePast_minute = datetime.now().minute
            # timeRemain_msec = (59 - timePast_minute) * 60 * 1000
            # self.threadTimer.start(timeRemain_msec)
        else:
            try:
                self.threadTimer.stop()
            except Exception as E:
                logging.info(E)
                logging.info("The timer is not started, so there is no necessary to stop.")

    def openOutputFolder(self):
        pass

    def recordImme(self):
        if self.recordImme_flag == True:
            self.settings["type"] = "libcamera-vid"
        os.system("sudo rm /home/pi/camera_app/output/raw_video/*.h264")
        self.applySettings()
        a1 = self.genCmdInstance()
        print(a1.payload)
        # rawFileName, rawFilePath = 
        A.CaptureVideo(a1)
        if self.recordImme_flag == True:
            # timePast_minute = datetime.now().minute
            # timeRemain_msec = (59 - timePast_minute) * 60 * 1000
            # self.threadTimer.start(timeRemain_msec)
            self.CheckScheduludeAndExecute()
        else:
            try:
                self.threadTimer.stop()
            except Exception as E:
                print(E)
        os.system("sudo cp -r " + "/home/pi/camera_app/output/raw_video/*.h264" + " /media/pi/CFBA-4424/")

    def applyTable(self):
        self.timeTable_cusMod.RefreshFromUI(self.tableWidget_timeTable.model())

    def readTableFromFile(self):
        # self.tableWidget_timeTable.item(1,1).setData()
        # idx = self.tableWidget_timeTable.model().index(1,1)
        # self.tableWidget_timeTable.model().setData(idx,QtCore.QTime.fromString("10:20:10"))
        # self.tableWidget_timeTable.setData(idx,"10:20:10",PyQt5.EditRole)
        self.timeTable_cusMod.ReadTableFromJson()
        pass



    def generateMenu(self,pos:QtCore.QPoint):
        tableModel = self.tableWidget_timeTable.model()
        # tableModel.blockSignals(True)
        pos.setX(pos.x()+35)
        pos.setY(pos.y()+35)
        idx_list = self.tableWidget_timeTable.selectedItems()
        menu = QtWidgets.QMenu()
        item_insert = menu.addAction("Insert")
        item_delete = menu.addAction("Delete")
        item_copy = menu.addAction("Copy Line")
        item_cut = menu.addAction("Cut Line")
        item_paste = menu.addAction("Paste Line")
        action = menu.exec_(self.tableWidget_timeTable.mapToGlobal(pos))

        if action == item_insert:
            print("Insert")
            if not idx_list:
                self.qtable_insert(0)
            else:
                idx = idx_list[0]
                print(idx.row(),idx.column())
                # tableModel.beginInsertRows(tableModel.index(idx.row(),idx.column()),idx.row(),idx.row()+1)
                self.qtable_insert(idx.row())
                # tableModel.endInsertRows()
            self.tableWidget_timeTableRowNumber_int = tableModel.rowCount()

        elif action == item_delete:
            print("Delete")
            for idx in idx_list:
                print(idx.row(),idx.column(),len(idx_list))
                self.qtable_delete(idx.row())
            self.tableWidget_timeTableRowNumber_int = tableModel.rowCount()

        elif action == item_copy:
            self.qtableClipboard = []
            idx_int_list = self.qtable_getRowFromSelection(idx_list=idx_list)
            for i in idx_int_list:
                clip_row = self.qtable_row2list(i)
                self.qtableClipboard.append(clip_row)
                print(clip_row)
            print("Copy")

        elif action == item_cut:
            self.qtableClipboard = []
            idx_int_list = self.qtable_getRowFromSelection(idx_list=idx_list)
            for i in idx_int_list:
                clip_row = self.qtable_row2list(i)
                self.qtableClipboard.append(clip_row)
                print(clip_row)
            for j in idx_int_list:
                self.qtable_delete(j)
            print("Cut")
        elif action == item_paste:
            clipboard_rowcnt = len(self.qtableClipboard)
            paste_baseAddr = 0
            if idx_list:
                idx_int_list = self.qtable_getRowFromSelection(idx_list=idx_list)
                paste_baseAddr = idx_int_list[0]
            else:
                pass
            for i in range(0, clipboard_rowcnt, 1):
                self.qtable_insert(paste_baseAddr)
                self.qtable_list2row(paste_baseAddr,self.qtableClipboard[i*-1-1])
        else:
            pass
        # tableModel.blockSignals(False)
        self.refreshModelFromUI()
        pass

    def refreshModelFromUI(self):
        model = self.tableWidget_timeTable.model()
        self.timeTable_cusMod.RefreshFromUI(model)

    def refreshUIFromModel(self):
        model = self.tableWidget_timeTable.model()
        model.blockSignals(True)
        # self.timeTable_cusMod.enableUIRefresh
        model_idx = model.index(0,0)
        model_row_idx = model.rowCount()
        model.removeRows(0,model_row_idx)
        # self.timeTable_cusMod.ReadTableFromJson()
        len_table = len(self.timeTable_cusMod)
        for i in range(0,len_table,1):
            model.insertRow(i)
            event_table_qtDict = self.timeTable_cusMod[i].infoDict_qtComplete
            startTime_qt     = event_table_qtDict["startTime"]
            duration_qt      = event_table_qtDict["duration"]
            enable_qt        = event_table_qtDict["enable"]
            configuration_qt = event_table_qtDict["configuration"]
            event_qt         = event_table_qtDict["event"]
            model_idx = model.index(i, 0)
            model.setData(model_idx,event_qt)
            model_idx = model.index(i, 1)
            model.setData(model_idx, startTime_qt)
            model_idx = model.index(i, 2)
            model.setData(model_idx, duration_qt)
            model_idx = model.index(i, 3)
            model.setData(model_idx, enable_qt)
            model_idx = model.index(i, 4)
            model.setData(model_idx, configuration_qt)
        model.blockSignals(False)
        pass

    def saveTableToFile(self):
        self.timeTable_cusMod.SaveTableToJson()
        pass

    def genCmdInstance(self):
        a = self.settings
        a1 = A.generateCommand_str(a)
        logging.info(a1.payload)
        return a1
        pass

    def autoConversion(self):
        self.autoConversion_flag = not self.autoConversion_flag
        # os.system("ffmpeg -r 80 -i 05_43_11.h264 output.mp4")
        pass

    def genTimer(self):
        self.threadTimer = QTimer()
        self.threadTimer.timeout.connect(self.recordImme)
        self.threadTimer.setSingleShot(True)
        return

    def genTimerCheckNextDayEvent(self):
        self.threadTimer_checkNextDay = QTimer()
        self.threadTimer_checkNextDay.timeout.connect(self.CheckScheduludeAndExecute)
        self.threadTimer.setSingleShot(True)
        return

    def manualFocusTrig(self):
        print(self.checkBox_manualFocus.isChecked())
        if self.checkBox_manualFocus.isChecked():
            logging.debug("Manual focus status changed into True! Manually Focus!")
            camera_distance = self.spinBox_cameraDistance.value()
            lens_distance = A.cameraDist2lensDist(camera_distance)
            logging.debug("lens distance=%f"%(lens_distance))
            self.settings['lens-position'] = lens_distance
        elif not self.checkBox_manualFocus.isChecked():
            logging.debug("Manual focus status changed into False! Auto Focus!")
            self.settings['lens-position'] = None


if __name__ == "__main__":
    import sys

    sys.path.append('../')
    #import FTP_service.server

    try:
        #server = FTP_service.server.Server_start
        #ftpThread = threading.Thread(target=server)
        #ftpThread.start()
        pass
    except Exception as E:
        logging.error(E)

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
