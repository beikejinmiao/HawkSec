# Form implementation generated from reading ui file 'ui_help_settings.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(696, 504)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 50, 55, 16))
        self.label_3.setObjectName("label_3")
        self.timeoutLineEdit = QtWidgets.QLineEdit(Form)
        self.timeoutLineEdit.setGeometry(QtCore.QRect(100, 50, 71, 21))
        self.timeoutLineEdit.setObjectName("timeoutLineEdit")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(180, 50, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.whiteDomTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.whiteDomTextEdit.setGeometry(QtCore.QRect(40, 130, 521, 131))
        self.whiteDomTextEdit.setObjectName("whiteDomTextEdit")
        self.builtinAlexaEnableBox = QtWidgets.QCheckBox(Form)
        self.builtinAlexaEnableBox.setGeometry(QtCore.QRect(570, 130, 111, 20))
        self.builtinAlexaEnableBox.setChecked(True)
        self.builtinAlexaEnableBox.setObjectName("builtinAlexaEnableBox")
        self.checkWhiteDomBtn = QtWidgets.QPushButton(Form)
        self.checkWhiteDomBtn.setGeometry(QtCore.QRect(130, 100, 41, 24))
        self.checkWhiteDomBtn.setObjectName("checkWhiteDomBtn")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(20, 290, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.whiteFileTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.whiteFileTextEdit.setGeometry(QtCore.QRect(40, 320, 521, 131))
        self.whiteFileTextEdit.setObjectName("whiteFileTextEdit")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(20, 80, 651, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(20, 270, 651, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.saveBtn = QtWidgets.QPushButton(Form)
        self.saveBtn.setGeometry(QtCore.QRect(210, 470, 61, 24))
        self.saveBtn.setObjectName("saveBtn")
        self.exitBtn = QtWidgets.QPushButton(Form)
        self.exitBtn.setGeometry(QtCore.QRect(290, 470, 61, 24))
        self.exitBtn.setObjectName("exitBtn")
        self.checkWhiteFileBtn = QtWidgets.QPushButton(Form)
        self.checkWhiteFileBtn.setGeometry(QtCore.QRect(210, 290, 41, 24))
        self.checkWhiteFileBtn.setObjectName("checkWhiteFileBtn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "????????????"))
        self.label.setText(_translate("Form", "???????????????"))
        self.label_3.setText(_translate("Form", "????????????"))
        self.label_4.setText(_translate("Form", "??????:???"))
        self.label_5.setText(_translate("Form", "?????????????????????"))
        self.whiteDomTextEdit.setPlaceholderText(_translate("Form", "????????????,?????????????????????????????????????????????; ??????????????????????????????"))
        self.builtinAlexaEnableBox.setText(_translate("Form", "?????????????????????"))
        self.checkWhiteDomBtn.setText(_translate("Form", "??????"))
        self.label_7.setText(_translate("Form", "??????URL????????????????????????"))
        self.whiteFileTextEdit.setPlaceholderText(_translate("Form", "????????????,????????????URL??????????????????????????????????????????; ?????????????????????"))
        self.saveBtn.setText(_translate("Form", "??????"))
        self.exitBtn.setText(_translate("Form", "??????"))
        self.checkWhiteFileBtn.setText(_translate("Form", "??????"))
