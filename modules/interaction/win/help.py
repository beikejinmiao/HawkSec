import os
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QCursor, QColor
from PyQt6.QtWidgets import QWidget, QSizePolicy, QGraphicsDropShadowEffect
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
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)           # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.closeBtnLabel.setText('')
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
        # 窗体自定义阴影
        self.render_shadow()

    def __init_state(self):
        self.closeBtnLabel.clicked.connect(self.close)

    def render_shadow(self):
        """
        https://blog.csdn.net/mahuatengmmp/article/details/113772969
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # 偏移
        shadow.setBlurRadius(12)  # 阴影半径
        shadow.setColor(QColor(128, 128, 255))  # 阴影颜色
        self.centralWidget.setGraphicsEffect(shadow)  # 将设置套用到widget窗口中

