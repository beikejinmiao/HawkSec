# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created by: PyQt5 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from modules.interaction.widget import QClickLabel


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(872, 553)
        Form.setMinimumSize(QtCore.QSize(860, 510))
        Form.setStyleSheet("")
        self.centralWidget = QtWidgets.QWidget(Form)
        self.centralWidget.setGeometry(QtCore.QRect(10, 10, 851, 531))
        self.centralWidget.setObjectName("centralWidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 120, 101, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.importDomLabel = QClickLabel(self.layoutWidget)
        self.importDomLabel.setStyleSheet("font-size: 14px; color: #2358DE;")
        self.importDomLabel.setObjectName("importDomLabel")
        self.horizontalLayout_3.addWidget(self.importDomLabel)
        self.checkWhiteDomBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.checkWhiteDomBtn.setMinimumSize(QtCore.QSize(40, 24))
        self.checkWhiteDomBtn.setMaximumSize(QtCore.QSize(40, 16777215))
        self.checkWhiteDomBtn.setObjectName("checkWhiteDomBtn")
        self.horizontalLayout_3.addWidget(self.checkWhiteDomBtn)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(41, 121, 80, 21))
        self.label_3.setStyleSheet("font-size: 16px;")
        self.label_3.setObjectName("label_3")
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(160, 310, 101, 26))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.importFileLabel = QClickLabel(self.layoutWidget_2)
        self.importFileLabel.setStyleSheet("font-size: 14px; color: #2358DE;")
        self.importFileLabel.setObjectName("importFileLabel")
        self.horizontalLayout_2.addWidget(self.importFileLabel)
        self.checkWhiteFileBtn = QtWidgets.QPushButton(self.layoutWidget_2)
        self.checkWhiteFileBtn.setMinimumSize(QtCore.QSize(40, 24))
        self.checkWhiteFileBtn.setMaximumSize(QtCore.QSize(40, 16777215))
        self.checkWhiteFileBtn.setObjectName("checkWhiteFileBtn")
        self.horizontalLayout_2.addWidget(self.checkWhiteFileBtn)
        self.whiteDomTextEdit = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.whiteDomTextEdit.setGeometry(QtCore.QRect(160, 150, 591, 131))
        self.whiteDomTextEdit.setObjectName("whiteDomTextEdit")
        self.cancelBtn = QtWidgets.QPushButton(self.centralWidget)
        self.cancelBtn.setGeometry(QtCore.QRect(390, 490, 61, 30))
        self.cancelBtn.setMinimumSize(QtCore.QSize(60, 30))
        self.cancelBtn.setObjectName("cancelBtn")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(40, 300, 81, 41))
        self.label_4.setStyleSheet("font-size: 16px;")
        self.label_4.setObjectName("label_4")
        self.saveBtn = QtWidgets.QPushButton(self.centralWidget)
        self.saveBtn.setGeometry(QtCore.QRect(310, 490, 61, 30))
        self.saveBtn.setMinimumSize(QtCore.QSize(60, 30))
        self.saveBtn.setObjectName("saveBtn")
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(160, 60, 222, 32))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_5.setStyleSheet("font-size: 14px; color: #666666;")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.timeoutComboBox = QtWidgets.QComboBox(self.layoutWidget_3)
        self.timeoutComboBox.setMinimumSize(QtCore.QSize(138, 30))
        self.timeoutComboBox.setObjectName("timeoutComboBox")
        self.timeoutComboBox.addItem("")
        self.timeoutComboBox.addItem("")
        self.timeoutComboBox.addItem("")
        self.timeoutComboBox.addItem("")
        self.horizontalLayout.addWidget(self.timeoutComboBox)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_8.setStyleSheet("font-size: 14px; color: #666666;")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.builtinAlexaEnableBox = QtWidgets.QCheckBox(self.centralWidget)
        self.builtinAlexaEnableBox.setGeometry(QtCore.QRect(630, 125, 121, 20))
        self.builtinAlexaEnableBox.setStyleSheet("font-size: 14px; color: #666666;")
        self.builtinAlexaEnableBox.setChecked(True)
        self.builtinAlexaEnableBox.setObjectName("builtinAlexaEnableBox")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(40, 60, 71, 31))
        self.label.setStyleSheet("font-size: 16px;")
        self.label.setObjectName("label")
        self.titleFrame = QtWidgets.QFrame(self.centralWidget)
        self.titleFrame.setGeometry(QtCore.QRect(-20, -10, 881, 61))
        self.titleFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.titleFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.titleFrame.setObjectName("titleFrame")
        self.label_2 = QtWidgets.QLabel(self.titleFrame)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 51, 16))
        self.label_2.setStyleSheet("font-size: 16px;")
        self.label_2.setObjectName("label_2")
        self.closeBtnLabel = QClickLabel(self.titleFrame)
        self.closeBtnLabel.setGeometry(QtCore.QRect(850, 30, 10, 10))
        self.closeBtnLabel.setMaximumSize(QtCore.QSize(10, 10))
        self.closeBtnLabel.setObjectName("closeBtnLabel")
        self.whiteFileTextEdit = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.whiteFileTextEdit.setGeometry(QtCore.QRect(160, 340, 591, 131))
        self.whiteFileTextEdit.setObjectName("whiteFileTextEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "详情页"))
        self.importDomLabel.setText(_translate("Form", "导入TXT"))
        self.checkWhiteDomBtn.setText(_translate("Form", "查看"))
        self.label_3.setText(_translate("Form", "域名白名单"))
        self.importFileLabel.setText(_translate("Form", "导入TXT"))
        self.checkWhiteFileBtn.setText(_translate("Form", "查看"))
        self.whiteDomTextEdit.setPlaceholderText(_translate("Form", "新加域名,多个域名请以逗号或者换行符分割; 格式错误域名将被忽略"))
        self.cancelBtn.setText(_translate("Form", "取消"))
        self.label_4.setText(_translate("Form", "文件白名单"))
        self.saveBtn.setText(_translate("Form", "保存"))
        self.label_5.setText(_translate("Form", "超时时间"))
        self.timeoutComboBox.setItemText(0, _translate("Form", "1"))
        self.timeoutComboBox.setItemText(1, _translate("Form", "2"))
        self.timeoutComboBox.setItemText(2, _translate("Form", "4"))
        self.timeoutComboBox.setItemText(3, _translate("Form", "8"))
        self.label_8.setText(_translate("Form", "秒"))
        self.builtinAlexaEnableBox.setText(_translate("Form", "启用内置白名单"))
        self.label.setText(_translate("Form", "客户端"))
        self.label_2.setText(_translate("Form", "设置"))
        self.closeBtnLabel.setText(_translate("Form", "x"))
        self.whiteFileTextEdit.setPlaceholderText(_translate("Form", "新加路径,多个文件URL和路径请以逗号或者换行符分割; 不校验输入内容"))
