#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QSizePolicy, QLayout
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor
from modules.gui.ui_finish_window import Ui_MainWindow as UiMainWindow
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from pathlib import Path
from utils.filedir import StyleSheetHelper


IMAGE_HOME = Path(IMAGE_HOME).as_posix()


class MainWindow(UiMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.__init_gui()
        self.__init_state()

    def __init_gui(self):
        bg_pic_path = Path(os.path.join(IMAGE_HOME, 'bg.png')).as_posix()
        self.centralwidget.setStyleSheet('#centralwidget {border-image: url(%s);}' % bg_pic_path)
        label_images = zip([self.logoLabel, self.helpLabel, self.settingLabel, self.robotLabel,
                            self.finishIconLabel, self.extUrlIconLabel, self.idcardIconLabel, self.keywordIconLabel],
                           ['logo.png', 'icon/help.png', 'icon/setting.png', 'robot.png',
                            'icon/finish.png', 'icon/exturl.png', 'icon/idcard.png', 'icon/keyword.png'])
        for label, img in label_images:
            label.setPixmap(QPixmap('image:%s' % img))
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        win_sheet = StyleSheetHelper.finish_win().replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)

    def __init_state(self):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
