# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(944, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.targetLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.targetLineEdit.setGeometry(QtCore.QRect(90, 40, 281, 21))
        self.targetLineEdit.setObjectName("targetLineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 40, 55, 16))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 55, 16))
        self.label_4.setObjectName("label_4")
        self.verticalGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalGroupBox.setGeometry(QtCore.QRect(30, 400, 251, 151))
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.metricVerticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.metricVerticalLayout.setObjectName("metricVerticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_17 = QtWidgets.QLabel(self.verticalGroupBox)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 0, 0, 1, 1)
        self.crawledCntLabel = QtWidgets.QLabel(self.verticalGroupBox)
        self.crawledCntLabel.setObjectName("crawledCntLabel")
        self.gridLayout.addWidget(self.crawledCntLabel, 0, 1, 1, 1)
        self.faieldCntLabel = QtWidgets.QLabel(self.verticalGroupBox)
        self.faieldCntLabel.setObjectName("faieldCntLabel")
        self.gridLayout.addWidget(self.faieldCntLabel, 2, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.verticalGroupBox)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 2, 0, 1, 1)
        self.hitCntLabel = QtWidgets.QLabel(self.verticalGroupBox)
        self.hitCntLabel.setObjectName("hitCntLabel")
        self.gridLayout.addWidget(self.hitCntLabel, 1, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.verticalGroupBox)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 1, 0, 1, 1)
        self.metricVerticalLayout.addLayout(self.gridLayout)
        self.checkProgressBtn = QtWidgets.QPushButton(self.verticalGroupBox)
        self.checkProgressBtn.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkProgressBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.checkProgressBtn.setObjectName("checkProgressBtn")
        self.metricVerticalLayout.addWidget(self.checkProgressBtn)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 580, 267, 26))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.operHLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.operHLayout.setContentsMargins(0, 0, 0, 0)
        self.operHLayout.setSpacing(20)
        self.operHLayout.setObjectName("operHLayout")
        self.startBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.startBtn.setObjectName("startBtn")
        self.operHLayout.addWidget(self.startBtn)
        self.stopBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stopBtn.setObjectName("stopBtn")
        self.operHLayout.addWidget(self.stopBtn)
        self.exitBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exitBtn.setObjectName("exitBtn")
        self.operHLayout.addWidget(self.exitBtn)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(630, 400, 231, 151))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)
        self.extUrlCntLabel = QtWidgets.QLabel(self.groupBox)
        self.extUrlCntLabel.setObjectName("extUrlCntLabel")
        self.gridLayout_2.addWidget(self.extUrlCntLabel, 0, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 1, 0, 1, 1)
        self.idcardCntLabel = QtWidgets.QLabel(self.groupBox)
        self.idcardCntLabel.setObjectName("idcardCntLabel")
        self.gridLayout_2.addWidget(self.idcardCntLabel, 1, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 2, 0, 1, 1)
        self.keywordCntLabel = QtWidgets.QLabel(self.groupBox)
        self.keywordCntLabel.setObjectName("keywordCntLabel")
        self.gridLayout_2.addWidget(self.keywordCntLabel, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.checkExtractBtn = QtWidgets.QPushButton(self.groupBox)
        self.checkExtractBtn.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkExtractBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.checkExtractBtn.setObjectName("checkExtractBtn")
        self.verticalLayout.addWidget(self.checkExtractBtn)
        self.mtypeGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mtypeGroupBox.setGeometry(QtCore.QRect(630, 40, 231, 111))
        self.mtypeGroupBox.setObjectName("mtypeGroupBox")
        self.layoutWidget = QtWidgets.QWidget(self.mtypeGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 211, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.mtypeGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.mtypeGridLayout.setContentsMargins(0, 0, 0, 0)
        self.mtypeGridLayout.setObjectName("mtypeGridLayout")
        self.extUrlCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.extUrlCheckBox.setObjectName("extUrlCheckBox")
        self.mtypeGridLayout.addWidget(self.extUrlCheckBox, 0, 0, 1, 1)
        self.idcardCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.idcardCheckBox.setObjectName("idcardCheckBox")
        self.mtypeGridLayout.addWidget(self.idcardCheckBox, 1, 0, 1, 1)
        self.keywordCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.keywordCheckBox.setObjectName("keywordCheckBox")
        self.mtypeGridLayout.addWidget(self.keywordCheckBox, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.mtypeGridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.protocolGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.protocolGroupBox.setGeometry(QtCore.QRect(430, 40, 131, 111))
        self.protocolGroupBox.setObjectName("protocolGroupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.protocolGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 71, 81))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.protocolVLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.protocolVLayout.setContentsMargins(0, 0, 0, 0)
        self.protocolVLayout.setObjectName("protocolVLayout")
        self.httpsRadioBtn = QtWidgets.QRadioButton(self.layoutWidget1)
        self.httpsRadioBtn.setObjectName("httpsRadioBtn")
        self.protocolVLayout.addWidget(self.httpsRadioBtn)
        self.httpRadioBtn = QtWidgets.QRadioButton(self.layoutWidget1)
        self.httpRadioBtn.setObjectName("httpRadioBtn")
        self.protocolVLayout.addWidget(self.httpRadioBtn)
        self.sftpRadioBtn = QtWidgets.QRadioButton(self.layoutWidget1)
        self.sftpRadioBtn.setObjectName("sftpRadioBtn")
        self.protocolVLayout.addWidget(self.sftpRadioBtn)
        self.logTextBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.logTextBox.setGeometry(QtCore.QRect(30, 170, 831, 211))
        self.logTextBox.setReadOnly(True)
        self.logTextBox.setObjectName("logTextBox")
        # MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 22))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        # MainWindow.setMenuBar(self.menubar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menuActionGeneral = QtGui.QAction(MainWindow)
        self.menuActionGeneral.setObjectName("menuActionGeneral")
        self.menuSettings.addAction(self.menuActionGeneral)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "敏感信息监控系统"))
        self.label.setText(_translate("MainWindow", "监控地址"))
        self.label_4.setText(_translate("MainWindow", "监控日志"))
        self.verticalGroupBox.setTitle(_translate("MainWindow", "进度状态统计"))
        self.label_17.setText(_translate("MainWindow", "         已爬取数量:"))
        self.crawledCntLabel.setText(_translate("MainWindow", "0     "))
        self.faieldCntLabel.setText(_translate("MainWindow", "0     "))
        self.label_20.setText(_translate("MainWindow", "      访问失败数量:"))
        self.hitCntLabel.setText(_translate("MainWindow", "0     "))
        self.label_19.setText(_translate("MainWindow", "含有监控内容数量:"))
        self.checkProgressBtn.setText(_translate("MainWindow", "查看"))
        self.startBtn.setText(_translate("MainWindow", "开始"))
        self.stopBtn.setText(_translate("MainWindow", "停止"))
        self.exitBtn.setText(_translate("MainWindow", "退出"))
        self.groupBox.setTitle(_translate("MainWindow", "监控内容统计"))
        self.label_14.setText(_translate("MainWindow", "        外链数量: "))
        self.extUrlCntLabel.setText(_translate("MainWindow", "0     "))
        self.label_15.setText(_translate("MainWindow", "      身份证数量:"))
        self.idcardCntLabel.setText(_translate("MainWindow", "0     "))
        self.label_16.setText(_translate("MainWindow", "关键字发现次数:"))
        self.keywordCntLabel.setText(_translate("MainWindow", "0     "))
        self.checkExtractBtn.setText(_translate("MainWindow", "查看"))
        self.mtypeGroupBox.setTitle(_translate("MainWindow", "监控内容"))
        self.extUrlCheckBox.setText(_translate("MainWindow", "外链"))
        self.idcardCheckBox.setText(_translate("MainWindow", "身份证"))
        self.keywordCheckBox.setText(_translate("MainWindow", "关键字"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "逗号,分割多个关键字"))
        self.protocolGroupBox.setTitle(_translate("MainWindow", "访问协议"))
        self.httpsRadioBtn.setText(_translate("MainWindow", "HTTPS"))
        self.httpRadioBtn.setText(_translate("MainWindow", "HTTP"))
        self.sftpRadioBtn.setText(_translate("MainWindow", "SFTP"))
        self.menuSettings.setTitle(_translate("MainWindow", "设置"))
        self.menuHelp.setTitle(_translate("MainWindow", "帮助"))
        self.action.setText(_translate("MainWindow", "网站网页"))
        self.action_2.setText(_translate("MainWindow", "服务器文件"))
        self.menuActionGeneral.setText(_translate("MainWindow", "通用"))
