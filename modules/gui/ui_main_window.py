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
        MainWindow.resize(1035, 777)
        MainWindow.setMinimumSize(QtCore.QSize(960, 680))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.helpLabel = QtWidgets.QLabel(self.centralwidget)
        self.helpLabel.setGeometry(QtCore.QRect(20, 700, 18, 18))
        self.helpLabel.setMinimumSize(QtCore.QSize(18, 18))
        self.helpLabel.setObjectName("helpLabel")
        self.settingLabel = QtWidgets.QLabel(self.centralwidget)
        self.settingLabel.setGeometry(QtCore.QRect(20, 730, 17, 17))
        self.settingLabel.setMinimumSize(QtCore.QSize(17, 17))
        self.settingLabel.setObjectName("settingLabel")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 146, 24))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.logoLabel = QtWidgets.QLabel(self.layoutWidget)
        self.logoLabel.setMinimumSize(QtCore.QSize(26, 22))
        self.logoLabel.setObjectName("logoLabel")
        self.gridLayout.addWidget(self.logoLabel, 0, 0, 1, 1)
        self.sysNameLabel = QtWidgets.QLabel(self.layoutWidget)
        self.sysNameLabel.setStyleSheet("font-size: 14px;")
        self.sysNameLabel.setObjectName("sysNameLabel")
        self.gridLayout.addWidget(self.sysNameLabel, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(50, 70, 991, 711))
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.mainFrame = QtWidgets.QFrame(self.mainTab)
        self.mainFrame.setGeometry(QtCore.QRect(10, 100, 951, 581))
        self.mainFrame.setMinimumSize(QtCore.QSize(883, 514))
        self.mainFrame.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.startBtn = QtWidgets.QPushButton(self.mainFrame)
        self.startBtn.setGeometry(QtCore.QRect(380, 490, 137, 50))
        self.startBtn.setMinimumSize(QtCore.QSize(137, 50))
        self.startBtn.setObjectName("startBtn")
        self.addressLineEdit = QtWidgets.QLineEdit(self.mainFrame)
        self.addressLineEdit.setGeometry(QtCore.QRect(210, 160, 500, 40))
        self.addressLineEdit.setMinimumSize(QtCore.QSize(500, 40))
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.layoutWidget_2 = QtWidgets.QWidget(self.mainFrame)
        self.layoutWidget_2.setGeometry(QtCore.QRect(210, 110, 301, 24))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.protoHLayout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.protoHLayout.setContentsMargins(0, 0, 0, 0)
        self.protoHLayout.setObjectName("protoHLayout")
        self.protoLabel = QtWidgets.QLabel(self.layoutWidget_2)
        self.protoLabel.setStyleSheet("font-size: 14px;")
        self.protoLabel.setObjectName("protoLabel")
        self.protoHLayout.addWidget(self.protoLabel)
        self.httpsRadioBtn = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.httpsRadioBtn.setObjectName("httpsRadioBtn")
        self.protoHLayout.addWidget(self.httpsRadioBtn)
        self.httpRadioBtn = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.httpRadioBtn.setObjectName("httpRadioBtn")
        self.protoHLayout.addWidget(self.httpRadioBtn)
        self.sftpRadioBtn = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.sftpRadioBtn.setObjectName("sftpRadioBtn")
        self.protoHLayout.addWidget(self.sftpRadioBtn)
        self.layoutWidget_3 = QtWidgets.QWidget(self.mainFrame)
        self.layoutWidget_3.setGeometry(QtCore.QRect(210, 225, 502, 231))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.dynGridLayout = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.dynGridLayout.setContentsMargins(0, 0, 0, 0)
        self.dynGridLayout.setHorizontalSpacing(12)
        self.dynGridLayout.setVerticalSpacing(30)
        self.dynGridLayout.setObjectName("dynGridLayout")
        self.portLineEdit = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.portLineEdit.setMinimumSize(QtCore.QSize(158, 40))
        self.portLineEdit.setObjectName("portLineEdit")
        self.dynGridLayout.addWidget(self.portLineEdit, 0, 0, 1, 1)
        self.userLineEdit = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.userLineEdit.setMinimumSize(QtCore.QSize(158, 40))
        self.userLineEdit.setObjectName("userLineEdit")
        self.dynGridLayout.addWidget(self.userLineEdit, 0, 1, 1, 1)
        self.passwdLineEdit = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.passwdLineEdit.setMinimumSize(QtCore.QSize(158, 40))
        self.passwdLineEdit.setObjectName("passwdLineEdit")
        self.dynGridLayout.addWidget(self.passwdLineEdit, 0, 2, 1, 1)
        self.pathLineEdit = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.pathLineEdit.setMinimumSize(QtCore.QSize(500, 40))
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.dynGridLayout.addWidget(self.pathLineEdit, 1, 0, 1, 3)
        self.sensiTypeFrame = QtWidgets.QFrame(self.layoutWidget_3)
        self.sensiTypeFrame.setMinimumSize(QtCore.QSize(500, 87))
        self.sensiTypeFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sensiTypeFrame.setStyleSheet("#sensiTypeFrame {\n"
"    background: #FFFFFF;\n"
"    border: 1px solid #C6CCD6;\n"
"}")
        self.sensiTypeFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sensiTypeFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sensiTypeFrame.setObjectName("sensiTypeFrame")
        self.sensiTypeLabel = QtWidgets.QLabel(self.sensiTypeFrame)
        self.sensiTypeLabel.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.sensiTypeLabel.setStyleSheet("font-size: 14px;")
        self.sensiTypeLabel.setObjectName("sensiTypeLabel")
        self.extUrlCheckBox = QtWidgets.QCheckBox(self.sensiTypeFrame)
        self.extUrlCheckBox.setGeometry(QtCore.QRect(100, 10, 80, 20))
        self.extUrlCheckBox.setObjectName("extUrlCheckBox")
        self.idcardCheckBox = QtWidgets.QCheckBox(self.sensiTypeFrame)
        self.idcardCheckBox.setGeometry(QtCore.QRect(190, 10, 80, 20))
        self.idcardCheckBox.setObjectName("idcardCheckBox")
        self.keywordCheckBox = QtWidgets.QCheckBox(self.sensiTypeFrame)
        self.keywordCheckBox.setGeometry(QtCore.QRect(100, 50, 80, 20))
        self.keywordCheckBox.setObjectName("keywordCheckBox")
        self.keywordLineEdit = QtWidgets.QLineEdit(self.sensiTypeFrame)
        self.keywordLineEdit.setGeometry(QtCore.QRect(190, 50, 271, 21))
        self.keywordLineEdit.setStyleSheet("border: #000000;")
        self.keywordLineEdit.setObjectName("keywordLineEdit")
        self.line = QtWidgets.QFrame(self.sensiTypeFrame)
        self.line.setGeometry(QtCore.QRect(190, 60, 261, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.dynGridLayout.addWidget(self.sensiTypeFrame, 2, 0, 1, 3)
        self.robotTipsLabel = QtWidgets.QLabel(self.mainTab)
        self.robotTipsLabel.setGeometry(QtCore.QRect(270, 70, 474, 60))
        self.robotTipsLabel.setMinimumSize(QtCore.QSize(474, 60))
        self.robotTipsLabel.setObjectName("robotTipsLabel")
        self.robotLabel = QtWidgets.QLabel(self.mainTab)
        self.robotLabel.setGeometry(QtCore.QRect(100, 40, 129, 115))
        self.robotLabel.setMinimumSize(QtCore.QSize(129, 115))
        self.robotLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.robotLabel.setObjectName("robotLabel")
        self.tabWidget.addTab(self.mainTab, "")
        self.monitTab = QtWidgets.QWidget()
        self.monitTab.setObjectName("monitTab")
        self.progressFrame = QtWidgets.QFrame(self.monitTab)
        self.progressFrame.setGeometry(QtCore.QRect(10, 10, 951, 136))
        self.progressFrame.setMinimumSize(QtCore.QSize(883, 136))
        self.progressFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.progressFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.progressFrame.setObjectName("progressFrame")
        self.waitforGifLabel = QtWidgets.QLabel(self.progressFrame)
        self.waitforGifLabel.setGeometry(QtCore.QRect(20, 20, 94, 94))
        self.waitforGifLabel.setMinimumSize(QtCore.QSize(94, 94))
        self.waitforGifLabel.setObjectName("waitforGifLabel")
        self.monitTipsLabel = QtWidgets.QLabel(self.progressFrame)
        self.monitTipsLabel.setGeometry(QtCore.QRect(150, 20, 141, 31))
        self.monitTipsLabel.setStyleSheet("font-size: 24px;color: #000000;")
        self.monitTipsLabel.setObjectName("monitTipsLabel")
        self.stopBtn = QtWidgets.QPushButton(self.progressFrame)
        self.stopBtn.setGeometry(QtCore.QRect(730, 20, 93, 40))
        self.stopBtn.setMinimumSize(QtCore.QSize(93, 40))
        self.stopBtn.setObjectName("stopBtn")
        self.cancelBtn = QtWidgets.QPushButton(self.progressFrame)
        self.cancelBtn.setGeometry(QtCore.QRect(830, 20, 93, 40))
        self.cancelBtn.setMinimumSize(QtCore.QSize(93, 40))
        self.cancelBtn.setObjectName("cancelBtn")
        self.progressBar = QtWidgets.QProgressBar(self.progressFrame)
        self.progressBar.setGeometry(QtCore.QRect(150, 110, 771, 10))
        self.progressBar.setMinimumSize(QtCore.QSize(10, 2))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 10))
        self.progressBar.setProperty("value", 2)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.layoutWidget_9 = QtWidgets.QWidget(self.progressFrame)
        self.layoutWidget_9.setGeometry(QtCore.QRect(380, 30, 149, 20))
        self.layoutWidget_9.setObjectName("layoutWidget_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget_9)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.expendTimeTipsLabel = QtWidgets.QLabel(self.layoutWidget_9)
        self.expendTimeTipsLabel.setStyleSheet("font-size: 14px;color: #8B8B8B;")
        self.expendTimeTipsLabel.setObjectName("expendTimeTipsLabel")
        self.horizontalLayout_5.addWidget(self.expendTimeTipsLabel)
        self.expendTimeLabel = QtWidgets.QLabel(self.layoutWidget_9)
        self.expendTimeLabel.setStyleSheet("font-size: 14px;color: #8B8B8B;")
        self.expendTimeLabel.setObjectName("expendTimeLabel")
        self.horizontalLayout_5.addWidget(self.expendTimeLabel)
        self.layoutWidget_10 = QtWidgets.QWidget(self.progressFrame)
        self.layoutWidget_10.setGeometry(QtCore.QRect(320, 71, 114, 20))
        self.layoutWidget_10.setObjectName("layoutWidget_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_10)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget_10)
        self.label_7.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_7.setStyleSheet("font-size: 14px;")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.hitCntLabel = QtWidgets.QLabel(self.layoutWidget_10)
        self.hitCntLabel.setStyleSheet("font-size: 14px;color:#FE8D08;")
        self.hitCntLabel.setObjectName("hitCntLabel")
        self.horizontalLayout.addWidget(self.hitCntLabel)
        self.layoutWidget_11 = QtWidgets.QWidget(self.progressFrame)
        self.layoutWidget_11.setGeometry(QtCore.QRect(150, 71, 96, 20))
        self.layoutWidget_11.setObjectName("layoutWidget_11")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget_11)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget_11)
        self.label_8.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_8.setStyleSheet("font-size: 14px;")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.crawledCntLabel = QtWidgets.QLabel(self.layoutWidget_11)
        self.crawledCntLabel.setStyleSheet("font-size: 14px;color:#2358DE;")
        self.crawledCntLabel.setObjectName("crawledCntLabel")
        self.horizontalLayout_7.addWidget(self.crawledCntLabel)
        self.layoutWidget_12 = QtWidgets.QWidget(self.progressFrame)
        self.layoutWidget_12.setGeometry(QtCore.QRect(510, 71, 114, 20))
        self.layoutWidget_12.setObjectName("layoutWidget_12")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget_12)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_12)
        self.label_9.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_9.setStyleSheet("font-size: 14px;")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.faieldCntLabel = QtWidgets.QLabel(self.layoutWidget_12)
        self.faieldCntLabel.setStyleSheet("font-size: 14px;color:#F41717;")
        self.faieldCntLabel.setObjectName("faieldCntLabel")
        self.horizontalLayout_8.addWidget(self.faieldCntLabel)
        self.detailWidget = QtWidgets.QWidget(self.monitTab)
        self.detailWidget.setGeometry(QtCore.QRect(10, 160, 951, 521))
        self.detailWidget.setMinimumSize(QtCore.QSize(883, 453))
        self.detailWidget.setObjectName("detailWidget")
        self.layoutWidget_13 = QtWidgets.QWidget(self.detailWidget)
        self.layoutWidget_13.setGeometry(QtCore.QRect(30, 10, 901, 501))
        self.layoutWidget_13.setObjectName("layoutWidget_13")
        self.detailVLayout = QtWidgets.QVBoxLayout(self.layoutWidget_13)
        self.detailVLayout.setContentsMargins(0, 0, 0, 0)
        self.detailVLayout.setSpacing(20)
        self.detailVLayout.setObjectName("detailVLayout")
        self.extUrlGridLayout = QtWidgets.QGridLayout()
        self.extUrlGridLayout.setHorizontalSpacing(1)
        self.extUrlGridLayout.setVerticalSpacing(2)
        self.extUrlGridLayout.setObjectName("extUrlGridLayout")
        self.extUrlTextEdit = QtWidgets.QTextEdit(self.layoutWidget_13)
        self.extUrlTextEdit.setObjectName("extUrlTextEdit")
        self.extUrlGridLayout.addWidget(self.extUrlTextEdit, 1, 0, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget_13)
        self.label_10.setMinimumSize(QtCore.QSize(70, 0))
        self.label_10.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_10.setStyleSheet("font-size: 16px;")
        self.label_10.setObjectName("label_10")
        self.extUrlGridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.extUrlCntLabel = QtWidgets.QLabel(self.layoutWidget_13)
        self.extUrlCntLabel.setStyleSheet("font-size: 20px;color: #2358DE;")
        self.extUrlCntLabel.setObjectName("extUrlCntLabel")
        self.extUrlGridLayout.addWidget(self.extUrlCntLabel, 0, 1, 1, 1)
        self.detailVLayout.addLayout(self.extUrlGridLayout)
        self.idcardGridLayout = QtWidgets.QGridLayout()
        self.idcardGridLayout.setHorizontalSpacing(3)
        self.idcardGridLayout.setVerticalSpacing(2)
        self.idcardGridLayout.setObjectName("idcardGridLayout")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget_13)
        self.label_12.setMinimumSize(QtCore.QSize(80, 0))
        self.label_12.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_12.setStyleSheet("font-size: 16px;")
        self.label_12.setObjectName("label_12")
        self.idcardGridLayout.addWidget(self.label_12, 0, 0, 1, 1)
        self.idcardTextEdit = QtWidgets.QTextEdit(self.layoutWidget_13)
        self.idcardTextEdit.setObjectName("idcardTextEdit")
        self.idcardGridLayout.addWidget(self.idcardTextEdit, 1, 0, 1, 2)
        self.idcardCntLabel = QtWidgets.QLabel(self.layoutWidget_13)
        self.idcardCntLabel.setStyleSheet("font-size: 20px;color: #2358DE;")
        self.idcardCntLabel.setObjectName("idcardCntLabel")
        self.idcardGridLayout.addWidget(self.idcardCntLabel, 0, 1, 1, 1)
        self.detailVLayout.addLayout(self.idcardGridLayout)
        self.keywordGridLayout = QtWidgets.QGridLayout()
        self.keywordGridLayout.setSpacing(2)
        self.keywordGridLayout.setObjectName("keywordGridLayout")
        self.label_17 = QtWidgets.QLabel(self.layoutWidget_13)
        self.label_17.setMinimumSize(QtCore.QSize(115, 0))
        self.label_17.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_17.setStyleSheet("font-size: 16px;")
        self.label_17.setObjectName("label_17")
        self.keywordGridLayout.addWidget(self.label_17, 0, 0, 1, 1)
        self.keywordCntLabel = QtWidgets.QLabel(self.layoutWidget_13)
        self.keywordCntLabel.setStyleSheet("font-size: 20px;color: #2358DE;")
        self.keywordCntLabel.setObjectName("keywordCntLabel")
        self.keywordGridLayout.addWidget(self.keywordCntLabel, 0, 1, 1, 1)
        self.keywordTextEdit = QtWidgets.QTextEdit(self.layoutWidget_13)
        self.keywordTextEdit.setObjectName("keywordTextEdit")
        self.keywordGridLayout.addWidget(self.keywordTextEdit, 1, 0, 1, 2)
        self.detailVLayout.addLayout(self.keywordGridLayout)
        self.tabWidget.addTab(self.monitTab, "")
        self.finishTab = QtWidgets.QWidget()
        self.finishTab.setObjectName("finishTab")
        self.mainFrame2 = QtWidgets.QFrame(self.finishTab)
        self.mainFrame2.setGeometry(QtCore.QRect(10, 100, 951, 581))
        self.mainFrame2.setMinimumSize(QtCore.QSize(883, 514))
        self.mainFrame2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.mainFrame2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mainFrame2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mainFrame2.setObjectName("mainFrame2")
        self.finishIconLabel = QtWidgets.QLabel(self.mainFrame2)
        self.finishIconLabel.setGeometry(QtCore.QRect(410, 70, 77, 77))
        self.finishIconLabel.setMinimumSize(QtCore.QSize(77, 77))
        self.finishIconLabel.setObjectName("finishIconLabel")
        self.label_2 = QtWidgets.QLabel(self.mainFrame2)
        self.label_2.setGeometry(QtCore.QRect(370, 160, 161, 41))
        self.label_2.setStyleSheet("font-size: 24px; color: #000000;")
        self.label_2.setObjectName("label_2")
        self.extUrlFrame = QtWidgets.QFrame(self.mainFrame2)
        self.extUrlFrame.setGeometry(QtCore.QRect(230, 330, 134, 101))
        self.extUrlFrame.setMinimumSize(QtCore.QSize(134, 75))
        self.extUrlFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.extUrlFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.extUrlFrame.setObjectName("extUrlFrame")
        self.extUrlIconLabel = QtWidgets.QLabel(self.extUrlFrame)
        self.extUrlIconLabel.setGeometry(QtCore.QRect(10, 10, 14, 14))
        self.extUrlIconLabel.setMinimumSize(QtCore.QSize(14, 14))
        self.extUrlIconLabel.setMaximumSize(QtCore.QSize(14, 14))
        self.extUrlIconLabel.setObjectName("extUrlIconLabel")
        self.label_13 = QtWidgets.QLabel(self.extUrlFrame)
        self.label_13.setGeometry(QtCore.QRect(40, 10, 71, 20))
        self.label_13.setStyleSheet("font-size: 16px; color: #000000;")
        self.label_13.setObjectName("label_13")
        self.extUrlCntLabel2 = QtWidgets.QLabel(self.extUrlFrame)
        self.extUrlCntLabel2.setGeometry(QtCore.QRect(20, 70, 55, 16))
        self.extUrlCntLabel2.setStyleSheet("font-size: 20px;color: #2358DE;")
        self.extUrlCntLabel2.setObjectName("extUrlCntLabel2")
        self.idcardFrame = QtWidgets.QFrame(self.mainFrame2)
        self.idcardFrame.setGeometry(QtCore.QRect(390, 330, 134, 101))
        self.idcardFrame.setMinimumSize(QtCore.QSize(134, 75))
        self.idcardFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.idcardFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.idcardFrame.setObjectName("idcardFrame")
        self.idcardIconLabel = QtWidgets.QLabel(self.idcardFrame)
        self.idcardIconLabel.setGeometry(QtCore.QRect(10, 10, 15, 15))
        self.idcardIconLabel.setMinimumSize(QtCore.QSize(15, 15))
        self.idcardIconLabel.setMaximumSize(QtCore.QSize(15, 15))
        self.idcardIconLabel.setObjectName("idcardIconLabel")
        self.label_14 = QtWidgets.QLabel(self.idcardFrame)
        self.label_14.setGeometry(QtCore.QRect(40, 10, 91, 20))
        self.label_14.setStyleSheet("font-size: 16px; color: #000000;")
        self.label_14.setObjectName("label_14")
        self.idcardCntLabel2 = QtWidgets.QLabel(self.idcardFrame)
        self.idcardCntLabel2.setGeometry(QtCore.QRect(20, 70, 55, 16))
        self.idcardCntLabel2.setStyleSheet("font-size: 20px;color: #2358DE;")
        self.idcardCntLabel2.setObjectName("idcardCntLabel2")
        self.keywordFrame = QtWidgets.QFrame(self.mainFrame2)
        self.keywordFrame.setGeometry(QtCore.QRect(580, 330, 134, 101))
        self.keywordFrame.setMinimumSize(QtCore.QSize(134, 75))
        self.keywordFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.keywordFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.keywordFrame.setObjectName("keywordFrame")
        self.keywordIconLabel = QtWidgets.QLabel(self.keywordFrame)
        self.keywordIconLabel.setGeometry(QtCore.QRect(10, 10, 12, 12))
        self.keywordIconLabel.setMinimumSize(QtCore.QSize(12, 12))
        self.keywordIconLabel.setMaximumSize(QtCore.QSize(12, 12))
        self.keywordIconLabel.setObjectName("keywordIconLabel")
        self.label_15 = QtWidgets.QLabel(self.keywordFrame)
        self.label_15.setGeometry(QtCore.QRect(40, 10, 81, 20))
        self.label_15.setStyleSheet("font-size: 16px; color: #000000;")
        self.label_15.setObjectName("label_15")
        self.keywordCntLabel2 = QtWidgets.QLabel(self.keywordFrame)
        self.keywordCntLabel2.setGeometry(QtCore.QRect(20, 70, 55, 16))
        self.keywordCntLabel2.setStyleSheet("font-size: 20px;color: #2358DE;")
        self.keywordCntLabel2.setObjectName("keywordCntLabel2")
        self.layoutWidget_14 = QtWidgets.QWidget(self.mainFrame2)
        self.layoutWidget_14.setGeometry(QtCore.QRect(410, 280, 114, 20))
        self.layoutWidget_14.setObjectName("layoutWidget_14")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.layoutWidget_14)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_18 = QtWidgets.QLabel(self.layoutWidget_14)
        self.label_18.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_18.setStyleSheet("font-size: 14px;")
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_9.addWidget(self.label_18)
        self.hitCntLabel2 = QtWidgets.QLabel(self.layoutWidget_14)
        self.hitCntLabel2.setStyleSheet("font-size: 14px;color:#FE8D08;")
        self.hitCntLabel2.setObjectName("hitCntLabel2")
        self.horizontalLayout_9.addWidget(self.hitCntLabel2)
        self.layoutWidget_15 = QtWidgets.QWidget(self.mainFrame2)
        self.layoutWidget_15.setGeometry(QtCore.QRect(600, 280, 114, 20))
        self.layoutWidget_15.setObjectName("layoutWidget_15")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.layoutWidget_15)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_19 = QtWidgets.QLabel(self.layoutWidget_15)
        self.label_19.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_19.setStyleSheet("font-size: 14px;")
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_10.addWidget(self.label_19)
        self.faieldCntLabel2 = QtWidgets.QLabel(self.layoutWidget_15)
        self.faieldCntLabel2.setStyleSheet("font-size: 14px;color:#F41717;")
        self.faieldCntLabel2.setObjectName("faieldCntLabel2")
        self.horizontalLayout_10.addWidget(self.faieldCntLabel2)
        self.layoutWidget_16 = QtWidgets.QWidget(self.mainFrame2)
        self.layoutWidget_16.setGeometry(QtCore.QRect(260, 280, 96, 20))
        self.layoutWidget_16.setObjectName("layoutWidget_16")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.layoutWidget_16)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_20 = QtWidgets.QLabel(self.layoutWidget_16)
        self.label_20.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_20.setStyleSheet("font-size: 14px;")
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_11.addWidget(self.label_20)
        self.crawledCntLabel2 = QtWidgets.QLabel(self.layoutWidget_16)
        self.crawledCntLabel2.setStyleSheet("font-size: 14px;color:#2358DE;")
        self.crawledCntLabel2.setObjectName("crawledCntLabel2")
        self.horizontalLayout_11.addWidget(self.crawledCntLabel2)
        self.layoutWidget_17 = QtWidgets.QWidget(self.mainFrame2)
        self.layoutWidget_17.setGeometry(QtCore.QRect(360, 220, 181, 20))
        self.layoutWidget_17.setObjectName("layoutWidget_17")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.layoutWidget_17)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.expendTimeTipsLabel2 = QtWidgets.QLabel(self.layoutWidget_17)
        self.expendTimeTipsLabel2.setStyleSheet("font-size: 14px; color: #8B8B8B;")
        self.expendTimeTipsLabel2.setObjectName("expendTimeTipsLabel2")
        self.horizontalLayout_12.addWidget(self.expendTimeTipsLabel2)
        self.expendTimeLabel2 = QtWidgets.QLabel(self.layoutWidget_17)
        self.expendTimeLabel2.setStyleSheet("font-size: 14px; color: #8B8B8B;")
        self.expendTimeLabel2.setObjectName("expendTimeLabel2")
        self.horizontalLayout_12.addWidget(self.expendTimeLabel2)
        self.layoutWidget_18 = QtWidgets.QWidget(self.mainFrame2)
        self.layoutWidget_18.setGeometry(QtCore.QRect(260, 490, 441, 41))
        self.layoutWidget_18.setObjectName("layoutWidget_18")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.layoutWidget_18)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.detailBtn = QtWidgets.QPushButton(self.layoutWidget_18)
        self.detailBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.detailBtn.setMaximumSize(QtCore.QSize(120, 40))
        self.detailBtn.setObjectName("detailBtn")
        self.horizontalLayout_13.addWidget(self.detailBtn)
        self.dumpBtn = QtWidgets.QPushButton(self.layoutWidget_18)
        self.dumpBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.dumpBtn.setMaximumSize(QtCore.QSize(120, 40))
        self.dumpBtn.setObjectName("dumpBtn")
        self.horizontalLayout_13.addWidget(self.dumpBtn)
        self.returnBtn = QtWidgets.QPushButton(self.layoutWidget_18)
        self.returnBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.returnBtn.setMaximumSize(QtCore.QSize(120, 40))
        self.returnBtn.setObjectName("returnBtn")
        self.horizontalLayout_13.addWidget(self.returnBtn)
        self.robotTipsLabel2 = QtWidgets.QLabel(self.finishTab)
        self.robotTipsLabel2.setGeometry(QtCore.QRect(270, 70, 474, 60))
        self.robotTipsLabel2.setMinimumSize(QtCore.QSize(474, 60))
        self.robotTipsLabel2.setStyleSheet("")
        self.robotTipsLabel2.setObjectName("robotTipsLabel2")
        self.robotLabel2 = QtWidgets.QLabel(self.finishTab)
        self.robotLabel2.setGeometry(QtCore.QRect(100, 40, 129, 115))
        self.robotLabel2.setMinimumSize(QtCore.QSize(129, 115))
        self.robotLabel2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.robotLabel2.setObjectName("robotLabel2")
        self.tabWidget.addTab(self.finishTab, "")
        # MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.helpLabel.setText(_translate("MainWindow", "help"))
        self.settingLabel.setText(_translate("MainWindow", "set"))
        self.logoLabel.setText(_translate("MainWindow", "logo"))
        self.sysNameLabel.setText(_translate("MainWindow", "敏感信息监测系统"))
        self.startBtn.setText(_translate("MainWindow", "开始监测"))
        self.addressLineEdit.setPlaceholderText(_translate("MainWindow", " 请输入监控地址"))
        self.protoLabel.setText(_translate("MainWindow", "访问协议"))
        self.httpsRadioBtn.setText(_translate("MainWindow", "HTTPS"))
        self.httpRadioBtn.setText(_translate("MainWindow", "HTTP"))
        self.sftpRadioBtn.setText(_translate("MainWindow", "SFTP"))
        self.portLineEdit.setPlaceholderText(_translate("MainWindow", " 请输入端口"))
        self.userLineEdit.setPlaceholderText(_translate("MainWindow", " 请输入用户名"))
        self.passwdLineEdit.setPlaceholderText(_translate("MainWindow", " 请输入密码"))
        self.pathLineEdit.setPlaceholderText(_translate("MainWindow", " 请输入路径"))
        self.sensiTypeLabel.setText(_translate("MainWindow", "监控内容"))
        self.extUrlCheckBox.setText(_translate("MainWindow", "外链"))
        self.idcardCheckBox.setText(_translate("MainWindow", "身份证"))
        self.keywordCheckBox.setText(_translate("MainWindow", "关键词"))
        self.robotTipsLabel.setText(_translate("MainWindow", "    您好，欢迎使用敏感信息监测系统！"))
        self.robotLabel.setText(_translate("MainWindow", "robot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), _translate("MainWindow", "Tab 1"))
        self.waitforGifLabel.setText(_translate("MainWindow", "waitforgif"))
        self.monitTipsLabel.setText(_translate("MainWindow", "信息监测中..."))
        self.stopBtn.setText(_translate("MainWindow", "停止"))
        self.cancelBtn.setText(_translate("MainWindow", "取消"))
        self.expendTimeTipsLabel.setText(_translate("MainWindow", "已监测时间 :"))
        self.expendTimeLabel.setText(_translate("MainWindow", "00::00:00"))
        self.label_7.setText(_translate("MainWindow", "含有监控内容:"))
        self.hitCntLabel.setText(_translate("MainWindow", "0"))
        self.label_8.setText(_translate("MainWindow", "已爬取:"))
        self.crawledCntLabel.setText(_translate("MainWindow", "0"))
        self.label_9.setText(_translate("MainWindow", "访问异常数量:"))
        self.faieldCntLabel.setText(_translate("MainWindow", "0"))
        self.label_10.setText(_translate("MainWindow", "外链数量"))
        self.extUrlCntLabel.setText(_translate("MainWindow", "0"))
        self.label_12.setText(_translate("MainWindow", "身份证数量"))
        self.idcardCntLabel.setText(_translate("MainWindow", "0"))
        self.label_17.setText(_translate("MainWindow", "关键字出现次数"))
        self.keywordCntLabel.setText(_translate("MainWindow", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.monitTab), _translate("MainWindow", "Tab 2"))
        self.finishIconLabel.setText(_translate("MainWindow", "finish icon"))
        self.label_2.setText(_translate("MainWindow", "信息监测完成"))
        self.extUrlIconLabel.setText(_translate("MainWindow", "pic"))
        self.label_13.setText(_translate("MainWindow", "外链数量"))
        self.extUrlCntLabel2.setText(_translate("MainWindow", "0"))
        self.idcardIconLabel.setText(_translate("MainWindow", "pic"))
        self.label_14.setText(_translate("MainWindow", "身份证数量"))
        self.idcardCntLabel2.setText(_translate("MainWindow", "0"))
        self.keywordIconLabel.setText(_translate("MainWindow", "pic"))
        self.label_15.setText(_translate("MainWindow", "关键词次数"))
        self.keywordCntLabel2.setText(_translate("MainWindow", "0"))
        self.label_18.setText(_translate("MainWindow", "含有监控内容:"))
        self.hitCntLabel2.setText(_translate("MainWindow", "0"))
        self.label_19.setText(_translate("MainWindow", "访问异常数量:"))
        self.faieldCntLabel2.setText(_translate("MainWindow", "0"))
        self.label_20.setText(_translate("MainWindow", "已爬取:"))
        self.crawledCntLabel2.setText(_translate("MainWindow", "0"))
        self.expendTimeTipsLabel2.setText(_translate("MainWindow", "监测总时长："))
        self.expendTimeLabel2.setText(_translate("MainWindow", "0小时0分0秒"))
        self.detailBtn.setText(_translate("MainWindow", "查看详情"))
        self.dumpBtn.setText(_translate("MainWindow", "导出文档"))
        self.returnBtn.setText(_translate("MainWindow", "返回主页面"))
        self.robotTipsLabel2.setText(_translate("MainWindow", "  恭喜您，已完成信息监测！"))
        self.robotLabel2.setText(_translate("MainWindow", "robot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.finishTab), _translate("MainWindow", "Tab 3"))
