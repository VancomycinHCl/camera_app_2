# -*- coding: utf-8 -*-
# import PyQt5.QtWidgets.QGridLayout
# Form implementation generated from reading ui file 'record_new.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

# import PyQt5.QtWidgets.QGridLayout


#lkdsjfl;kasdjf;lkjasd;lfkjas;dlkjf;lsdkajf;lksdvc;lknds;fj;sdalkjfl;ksdajflksdajfoi
#kasdjhfl;jjsdhalfkjsdlk;jflsdjflkjhasdlfkh;sldkajflsdajhfkljhsdlkfjhasdlkjfhlaksjdhf

class DelegateTimeEdit_startTimeBox(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(DelegateTimeEdit_startTimeBox, self).__init__()
    def createEditor(self, parent:QtWidgets.QTableWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtWidgets:
        if index.column() == 1:
            timeEdit = QtWidgets.QTimeEdit(parent)
            timeEdit.setDisplayFormat("HH:mm:ss")
            return timeEdit

    def displayText(self, value: QtCore.QDateTime, locale: QtCore.QLocale) -> str:
        return locale.toString(value,"HH:mm:ss")

    def setEditorData(self, editor: QtWidgets.QTimeEdit, index: QtCore.QModelIndex) -> None:
        if index.column() == 1:
            t = QtCore.QTime.fromString("12:30:30")
            editor.setTime(t)
            pass

class DelegateQSpinBox_durationBox(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(DelegateQSpinBox_durationBox,self).__init__()
    def createEditor(self, parent: QtWidgets, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtWidgets:
        if index.column() == 2:
            spinbox = QtWidgets.QSpinBox(parent=parent)
            spinbox.setMaximum(86400)
            spinbox.setMinimum(0)
            spinbox.setValue(60)
            # spinbox.customContextMenuRequested.connect(self.test)
            return spinbox
    def displayText(self, value: int, locale: QtCore.QLocale) -> str:
        return locale.toString(value)
    def setEditorData(self, editor: QtWidgets.QSpinBox, index: QtCore.QModelIndex) -> None:
            if index.column() == 2:
                editor.setValue(0)
            return

class DelegateQComboBox_eventBox(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(DelegateQComboBox_eventBox,self).__init__()
        pass
    def createEditor(self, parent: QtWidgets, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtWidgets.QComboBox:
        if index.column() == 0:
            combobox = QtWidgets.QComboBox(parent=parent)
            combobox.insertItem(0,"libcamera-still")
            combobox.insertItem(0,"libcamera-vid")
            return combobox
    def displayText(self, value: str, locale: QtCore.QLocale) -> str:
        return value

class DelegateQCheckBox_enableBox(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(DelegateQCheckBox_enableBox,self).__init__()

    def createEditor(self, parent: QtWidgets.QCheckBox, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtWidgets.QCheckBox:
        checkbox = QtWidgets.QCheckBox(parent)
        checkbox.setText("")
        checkbox.setChecked(True)
        return checkbox

    def setModelData(self, editor: QtWidgets.QCheckBox, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        if editor.isChecked():
            model.setData(index, "On",QtCore.Qt.DisplayRole)
        else:
            model.setData(index,"Off",QtCore.Qt.DisplayRole)

# class TimeTable_Qtable(QtWidgets.QTableWidget):
#     def __init__(self, rowNum:int=24, columnNum:int=5,MainWindow_parent:QtWidgets.QMainWindow=None,parent=None):
#         super(TimeTable_Qtable,self).__init__(parent=parent)
#         self.rowNum = rowNum
#         self.columnNum = columnNum
#         self.setRowCount(rowNum)
#         self.setColumnCount(columnNum)
#         self.setObjectName("tableWidget_timeTable")
#         item = QtWidgets.QTableWidgetItem()
#         self.setHorizontalHeaderItem(0, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.setHorizontalHeaderItem(1, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.setHorizontalHeaderItem(2, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.setHorizontalHeaderItem(3, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.setHorizontalHeaderItem(4, item)
#         self.horizontalHeader().setCascadingSectionResizes(False)
#
#         timeTableModel = self.model()
#         self.delegate_duration = DelegateQSpinBox_durationBox()
#         self.delegate_event = DelegateQComboBox_eventBox()
#         self.delegate_time = DelegateTimeEdit_startTimeBox()
#         self.delegate_enable = DelegateQCheckBox_enableBox()
#
#         self.setItemDelegateForColumn(0, self.delegate_event)
#         self.setItemDelegateForColumn(1, self.delegate_time)
#         self.setItemDelegateForColumn(2, self.delegate_duration)
#         self.setItemDelegateForColumn(3, self.delegate_enable)
#
#         self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#         self.customContextMenuRequested.connect(MainWindow_parent.generateMenu)
#
#         for i in range(0, self.rowNum):
#             self.qtable_RowInit(i)
#
#     def qtable_RowInit(self,index:int=0):
#         model = self.model()
#         m_index = model.index(index, 0)
#         model.setItemData(m_index, {0: "libcamera-still"})
#         m_index = model.index(index, 1)
#         model.setItemData(m_index, {0: QtCore.QTime.fromString("11:56:30")})
#         m_index = model.index(index, 2)
#         model.setItemData(m_index, {0: 10})
#         m_index = model.index(index, 3)
#         model.setItemData(m_index, {0: "On"})
#
#     def qtable_insert(self,index:int=0):
#         self.insertRow(index)
#         self.qtable_RowInit(index)
#
#     def qtable_delete(self,index:int=0):
#         model = self.model()
#         model.removeRow(index)
#
#     def keyPressEvent(self,event):
#         print(event)
#         idx_list = self.selectedItems()
#         if event.key() == QtCore.Qt.Key_Delete:
#             for i in idx_list:
#                 self.qtable_delete(i.row())
#         elif event.key() == QtCore.Qt.Key_Enter:
#             pass

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1253, 464)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setDocumentMode(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_duration = QtWidgets.QLabel(self.centralwidget)
        self.label_duration.setGeometry(QtCore.QRect(20, 60, 131, 16))
        self.label_duration.setObjectName("label_duration")
        self.label_weight = QtWidgets.QLabel(self.centralwidget)
        self.label_weight.setGeometry(QtCore.QRect(240, 60, 48, 16))
        self.label_weight.setObjectName("label_weight")
        self.WeightBox = QtWidgets.QSpinBox(self.centralwidget)
        self.WeightBox.setGeometry(QtCore.QRect(310, 50, 81, 31))
        self.WeightBox.setMaximum(5000)
        self.WeightBox.setObjectName("WeightBox")
        self.label_height = QtWidgets.QLabel(self.centralwidget)
        self.label_height.setGeometry(QtCore.QRect(240, 100, 48, 16))
        self.label_height.setObjectName("label_height")
        self.HeightBox = QtWidgets.QSpinBox(self.centralwidget)
        self.HeightBox.setGeometry(QtCore.QRect(310, 95, 81, 31))
        self.HeightBox.setMaximum(5000)
        self.HeightBox.setObjectName("HeightBox")
        self.label_fps = QtWidgets.QLabel(self.centralwidget)
        self.label_fps.setGeometry(QtCore.QRect(20, 100, 72, 16))
        self.label_fps.setObjectName("label_fps")
        self.FPS = QtWidgets.QSpinBox(self.centralwidget)
        self.FPS.setGeometry(QtCore.QRect(150, 90, 71, 31))
        self.FPS.setMinimum(0)
        self.FPS.setMaximum(100)
        self.FPS.setObjectName("FPS")
        self.label_filepath = QtWidgets.QLabel(self.centralwidget)
        self.label_filepath.setGeometry(QtCore.QRect(20, 146, 141, 31))
        self.label_filepath.setObjectName("label_filepath")
        self.filePath_H264 = QtWidgets.QLineEdit(self.centralwidget)
        self.filePath_H264.setGeometry(QtCore.QRect(160, 144, 221, 31))
        self.filePath_H264.setText("")
        self.filePath_H264.setMaxLength(32767)
        self.filePath_H264.setFrame(True)
        self.filePath_H264.setDragEnabled(False)
        self.filePath_H264.setReadOnly(False)
        self.filePath_H264.setClearButtonEnabled(False)
        self.filePath_H264.setObjectName("filePath_H264")
        self.pushButton_Apply = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Apply.setGeometry(QtCore.QRect(210, 366, 211, 28))
        self.pushButton_Apply.setObjectName("pushButton_Apply")
        self.pushButton_Preview = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Preview.setGeometry(QtCore.QRect(210, 326, 211, 28))
        self.pushButton_Preview.setObjectName("pushButton_Preview")
        self.pushButton_recordImme = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_recordImme.setGeometry(QtCore.QRect(10, 326, 191, 28))
        self.pushButton_recordImme.setObjectName("pushButton_recordImme")
        self.checkBox_launchPreview = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_launchPreview.setGeometry(QtCore.QRect(20, 270, 351, 19))
        self.checkBox_launchPreview.setObjectName("checkBox_launchPreview")
        self.timeEdit_duration = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_duration.setGeometry(QtCore.QRect(150, 52, 71, 31))
        self.timeEdit_duration.setTime(QtCore.QTime(0, 20, 0))
        self.timeEdit_duration.setObjectName("timeEdit_duration")
        self.pushButton_H264File = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_H264File.setGeometry(QtCore.QRect(390, 146, 41, 31))
        self.pushButton_H264File.setObjectName("pushButton_H264File")
        self.label_filepath_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_filepath_2.setGeometry(QtCore.QRect(20, 198, 131, 31))
        self.label_filepath_2.setObjectName("label_filepath_2")
        self.pushButton_MP4File = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_MP4File.setGeometry(QtCore.QRect(390, 196, 41, 31))
        self.pushButton_MP4File.setObjectName("pushButton_MP4File")
        self.filePath_MP4 = QtWidgets.QLineEdit(self.centralwidget)
        self.filePath_MP4.setGeometry(QtCore.QRect(150, 196, 231, 31))
        self.filePath_MP4.setText("")
        self.filePath_MP4.setMaxLength(32767)
        self.filePath_MP4.setFrame(True)
        self.filePath_MP4.setDragEnabled(False)
        self.filePath_MP4.setReadOnly(False)
        self.filePath_MP4.setClearButtonEnabled(False)
        self.filePath_MP4.setObjectName("filePath_MP4")
        self.checkBox_autoConvert = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_autoConvert.setGeometry(QtCore.QRect(20, 246, 381, 19))
        self.checkBox_autoConvert.setCheckable(True)
        self.checkBox_autoConvert.setChecked(False)
        self.checkBox_autoConvert.setTristate(False)
        self.checkBox_autoConvert.setObjectName("checkBox_autoConvert")
        self.checkBox_recoedEachHour = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_recoedEachHour.setGeometry(QtCore.QRect(20, 296, 241, 19))
        self.checkBox_recoedEachHour.setObjectName("checkBox_recoedEachHour")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 366, 191, 28))
        self.pushButton.setObjectName("pushButton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(430, 30, 20, 381))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_timetable = QtWidgets.QLabel(self.centralwidget)
        self.label_timetable.setGeometry(QtCore.QRect(460, 20, 72, 15))
        self.label_timetable.setObjectName("label_timetable")
        self.pushButton_ApplyTable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ApplyTable.setGeometry(QtCore.QRect(750, 370, 131, 31))
        self.pushButton_ApplyTable.setObjectName("pushButton_ApplyTable")
        self.pushButton_tableClear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tableClear.setGeometry(QtCore.QRect(750, 330, 131, 31))
        self.pushButton_tableClear.setObjectName("pushButton_tableClear")
        self.pushButton_saveTable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_saveTable.setGeometry(QtCore.QRect(470, 370, 131, 31))
        self.pushButton_saveTable.setObjectName("pushButton_saveTable")
        self.pushButton_readTable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_readTable.setGeometry(QtCore.QRect(610, 370, 131, 31))
        self.pushButton_readTable.setObjectName("pushButton_readTable")



        self.tableWidget_timeTableColumnNumber_int = 5
        self.tableWidget_timeTableRowNumber_int    = 24
        # self.tableWidget_timeTable = TimeTable_Qtable( self.tableWidget_timeTableColumnNumber_int,
        #                                                self.tableWidget_timeTableRowNumber_int,
        #                                                MainWindow,
        #                                                parent=self.centralwidget)
        # self.setCentralWidget(self.tableWidget_timeTable)
        # self.tableWidget_timeTable.setGeometry(QtCore.QRect(460, 50, 581, 271))
        # self.tableWidget_timeTable.setFrameShadow(QtWidgets.QFrame.Sunken)


        self.tableWidget_timeTable = QtWidgets.QTableWidget(self.centralwidget)
        # super(QtWidgets.QTableWidget, self.tableWidget_timeTable).__init__(self.centralwidget)
        self.tableWidget_timeTable.setGeometry(QtCore.QRect(460, 50, 781, 271))
        self.tableWidget_timeTable.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget_timeTable.setRowCount(self.tableWidget_timeTableRowNumber_int)
        self.tableWidget_timeTable.setColumnCount(self.tableWidget_timeTableColumnNumber_int)
        self.tableWidget_timeTable.setObjectName("tableWidget_timeTable")
        self.tableWidget_timeTable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_timeTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_timeTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_timeTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_timeTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_timeTable.setHorizontalHeaderItem(4, item)
        self.tableWidget_timeTable.setColumnWidth(4,300)
        self.tableWidget_timeTable.horizontalHeader().setCascadingSectionResizes(False)

        timeTableModel = self.tableWidget_timeTable.model()
        self.delegate_duration = DelegateQSpinBox_durationBox()
        self.delegate_event = DelegateQComboBox_eventBox()
        self.delegate_time = DelegateTimeEdit_startTimeBox()
        self.delegate_enable = DelegateQCheckBox_enableBox()

        self.tableWidget_timeTable.setItemDelegateForColumn(0, self.delegate_event)
        self.tableWidget_timeTable.setItemDelegateForColumn(1, self.delegate_time)
        self.tableWidget_timeTable.setItemDelegateForColumn(2, self.delegate_duration)
        self.tableWidget_timeTable.setItemDelegateForColumn(3, self.delegate_enable)

        self.tableWidget_timeTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_timeTable.customContextMenuRequested.connect(MainWindow.generateMenu)

        for i in range(0,self.tableWidget_timeTableRowNumber_int):
            self.qtable_RowInit(i)
            # timeTableItem_idx = timeTableModel.index(i,0)
            # timeTableItem = timeTableModel.setItemData(timeTableItem_idx, {0: "libcamera-vid"})
            # timeTableItem_idx = timeTableModel.index(i,1)
            # timeTableItem = timeTableModel.setItemData(timeTableItem_idx,{0:QtCore.QTime.fromString("11:45:14")})
            # timeTableItem_idx = timeTableModel.index(i,2)
            # timeTableItem = timeTableModel.setItemData(timeTableItem_idx, {0:0})
            # # timeTableItem.
            # print(timeTableItem)







        self.pushButton_AddRecord = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_AddRecord.setGeometry(QtCore.QRect(470, 330, 131, 31))
        self.pushButton_AddRecord.setObjectName("pushButton_AddRecord")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 330, 131, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_statusTitile = QtWidgets.QLabel(self.centralwidget)
        self.label_statusTitile.setGeometry(QtCore.QRect(910, 340, 72, 15))
        self.label_statusTitile.setObjectName("label_statusTitile")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(930, 370, 111, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 72, 15))
        self.label_2.setObjectName("label_2")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(90, 20, 331, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(540, 20, 501, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1053, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Recording = QtWidgets.QAction(MainWindow)
        self.actionOpen_Recording.setObjectName("actionOpen_Recording")
        self.actionOpen_Setting_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Setting_File.setObjectName("actionOpen_Setting_File")
        self.actionSave_Settings = QtWidgets.QAction(MainWindow)
        self.actionSave_Settings.setObjectName("actionSave_Settings")
        self.menuFile.addAction(self.actionOpen_Recording)
        self.menuFile.addAction(self.actionOpen_Setting_File)
        self.menuFile.addAction(self.actionSave_Settings)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.pushButton_Apply.clicked.connect(MainWindow.applySettings)
        self.pushButton_Preview.clicked.connect(MainWindow.previewImme)
        self.pushButton_H264File.clicked.connect(MainWindow.openOutputH264File)
        self.pushButton_recordImme.clicked.connect(MainWindow.recordImme)
        self.pushButton_MP4File.clicked.connect(MainWindow.openOutputMP4File)
        self.pushButton.clicked.connect(MainWindow.openOutputFolder)
        self.checkBox_recoedEachHour.clicked.connect(MainWindow.recordEachHour_disableImmeButton)
        self.pushButton_ApplyTable.clicked.connect(MainWindow.applyTable)
        self.pushButton_readTable.clicked.connect(MainWindow.readTableFromFile)
        self.pushButton_saveTable.clicked.connect(MainWindow.saveTableToFile)
        self.pushButton_tableClear.clicked.connect(MainWindow.saveTableToFile)
        self.pushButton_2.clicked.connect(MainWindow.deleteEventFromTable)
        self.pushButton_AddRecord.clicked.connect(MainWindow.addEventToTable)
        # self.tableWidget_timeTable.model().dataChanged.connect(MainWindow.refreshModelFromUI)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.HeightBox, self.WeightBox)
        MainWindow.setTabOrder(self.WeightBox, self.pushButton_Preview)
        MainWindow.setTabOrder(self.pushButton_Preview, self.filePath_H264)
        MainWindow.setTabOrder(self.filePath_H264, self.FPS)
        MainWindow.setTabOrder(self.FPS, self.pushButton_Apply)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Brief Video Controller"))
        self.label_duration.setText(_translate("MainWindow", "Video Duration"))
        self.label_weight.setText(_translate("MainWindow", "Weight"))
        self.label_height.setText(_translate("MainWindow", "Height"))
        self.label_fps.setText(_translate("MainWindow", "Framerate"))
        self.label_filepath.setText(_translate("MainWindow", "H.264 Output Path"))
        self.pushButton_Apply.setText(_translate("MainWindow", "Apply Settings"))
        self.pushButton_Preview.setText(_translate("MainWindow", "Preview"))
        self.pushButton_recordImme.setText(_translate("MainWindow", "Record Immediately"))
        self.checkBox_launchPreview.setText(_translate("MainWindow", "Launch Preview In Recording"))
        self.pushButton_H264File.setText(_translate("MainWindow", "..."))
        self.label_filepath_2.setText(_translate("MainWindow", "MP4 Output Path"))
        self.pushButton_MP4File.setText(_translate("MainWindow", "..."))
        self.checkBox_autoConvert.setText(_translate("MainWindow", "Convrt Videos Automatically After Recording"))
        self.checkBox_recoedEachHour.setText(_translate("MainWindow", "Recording each hour"))
        self.pushButton.setText(_translate("MainWindow", "Open Output Folder"))
        self.label_timetable.setText(_translate("MainWindow", "TimeTable"))
        self.pushButton_ApplyTable.setText(_translate("MainWindow", "Apply Table"))
        self.pushButton_tableClear.setText(_translate("MainWindow", "Clear Table"))
        self.pushButton_saveTable.setText(_translate("MainWindow", "Save Table"))
        self.pushButton_readTable.setText(_translate("MainWindow", "Read Table"))
        item = self.tableWidget_timeTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Event"))
        item = self.tableWidget_timeTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Time(H:M:S)"))
        item = self.tableWidget_timeTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Duration(sec)"))
        item = self.tableWidget_timeTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Enable"))
        item = self.tableWidget_timeTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Configuration"))
        self.pushButton_AddRecord.setText(_translate("MainWindow", "Add Event"))
        self.pushButton_2.setText(_translate("MainWindow", "Delete Event"))
        self.label_statusTitile.setText(_translate("MainWindow", "Status:"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "Settings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_Recording.setText(_translate("MainWindow", "Open Recording"))
        self.actionOpen_Setting_File.setText(_translate("MainWindow", "Open Settings"))
        self.actionSave_Settings.setText(_translate("MainWindow", "Save Settings"))

    def qtable_RowInit(self,index:int=0):
        model = self.tableWidget_timeTable.model()
        m_index = model.index(index, 0)
        model.setItemData(m_index, {0: "libcamera-still"})
        m_index = model.index(index, 1)
        model.setItemData(m_index, {0: QtCore.QTime.fromString("11:56:30")})
        m_index = model.index(index, 2)
        model.setItemData(m_index, {0: 10})
        m_index = model.index(index, 3)
        model.setItemData(m_index, {0: "On"})

    def qtable_insert(self,index:int=0):
        self.tableWidget_timeTable.insertRow(index)
        self.qtable_RowInit(index)

    def qtable_delete(self,index:int=0):
        model = self.tableWidget_timeTable.model()
        model.removeRow(index)

    def qtable_getRowFromSelection(self,idx_list:list) -> list:
        idx_list_int = []
        for idx in idx_list:
            idx_list_int.append(idx.row())
        idx_list_int = set(idx_list_int)
        idx_list_int = list(idx_list_int)
        print(idx_list_int)
        return idx_list_int

    def qtable_row2list(self,rowIdx:int) -> tuple:
        model = self.tableWidget_timeTable.model()
        column_cnt = model.columnCount()
        clipboard = []
        for i in range(0,column_cnt,1):
            idx = model.index(rowIdx,i)
            clipboard.append(model.data(idx))
        clipboard = tuple(clipboard)
        return clipboard

    def qtable_list2row(self,rowIdx:int,clipboard:tuple) -> None:
        model = self.tableWidget_timeTable.model()
        column_cnt = model.columnCount()
        idx = model.index(rowIdx,0)
        if len(clipboard) != column_cnt:
            raise ValueError
        else:
            for i in range(0,column_cnt,1):
                idx = model.index(rowIdx,i)
                model.setData(idx,clipboard[i])
        return

    def keyPressEvent(self,event):
        print(event)
        idx_list = self.tableWidget_timeTable.selectedItems()
        if event.key() == QtCore.Qt.Key_Delete:
            for i in idx_list:
                self.qtable_delete(i.row())
        elif event.key() == QtCore.Qt.Key_Enter:
            pass
