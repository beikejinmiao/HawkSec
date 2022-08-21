import os
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QWidget, QSizePolicy
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from utils.filedir import StyleSheetHelper
from modules.gui.ui_help import Ui_Form


class HelpAboutWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #
        self.__init_ui()
        self.__init_state()

    def __init_ui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        label_images = zip([self.companyLogoLabel, self.appIconLabel], ['company.png', 'app_logo_blue.png'])
        for label, img in label_images:
            label.setPixmap(QPixmap('image:%s' % img))
            # https://stackoverflow.com/questions/5653114/display-image-in-qt-to-fit-label-size
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        #
        win_sheet = StyleSheetHelper.load_qss(name='help').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        #
        self.closeBtnLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def __init_state(self):
        self.closeBtnLabel.clicked.connect(self.close)

