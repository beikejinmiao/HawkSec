#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import sys
from PyQt5.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt5.QtCore import QUrl, Qt
from conf.paths import START_MOVIE_PATH
from modules.win.mainwin import MainWindow

"""
PyQt5 视频播放器样例
https://doc.qt.io/qtforpython/examples/example_multimedia__player.html
"""


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.mainWindow = None
        self.__init_ui()
        self.__init_state()

    def __init_ui(self):
        layout = QHBoxLayout()
        # https://stackoverflow.com/questions/47852697/how-to-make-layout-automatically-fill-window-size
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.player = QMediaPlayer()
        # AttributeError: 'QMediaPlayer' object has no attribute 'setAudioOutput'
        # self.audio_output = QAudioOutput()
        # self.player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)

        # AttributeError: 'QMediaPlayer' object has no attribute 'setSource'
        # self.player.setSource(QUrl.fromLocalFile(START_MOVIE_PATH))

        # https://stackoverflow.com/questions/60585605/why-media-player-pyqt5-is-not-working-on-windows-10-python
        # 需安装https://files2.codecguide.com/K-Lite_Codec_Pack_1725_Basic.exe，否则无法解码视频文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(START_MOVIE_PATH)))
        self.player.play()

    def __init_state(self):
        # AttributeError: 'QMediaPlayer' object has no attribute 'playbackStateChanged'
        self.player.stateChanged.connect(self.show_mainwin)

    def show_mainwin(self):
        # AttributeError: 'QMediaPlayer' object has no attribute 'playbackState'
        # AttributeError: type object 'QMediaPlayer' has no attribute 'PlaybackState'
        if self.player.state() == QMediaPlayer.StoppedState:
            self.mainWindow = MainWindow()      # 该变量必须定义在self下,否则动画结束后会主页窗口莫名其妙的退出
            self.mainWindow.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.setMinimumSize(960, 680)
    splash.show()
    sys.exit(app.exec())

# def default_splash():
#     import os
#     import time
#     from conf.paths import PRIVATE_RESOURCE_HOME
#     from PyQt5.QtWidgets import QSplashScreen, QProgressBar
#     from PyQt5.QtCore import QDir, Qt
#     from PyQt5.QtGui import QPixmap
#
#     app = QApplication(sys.argv)
#     QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
#     pixmap = QPixmap("image:bg.png")
#     splash = QSplashScreen(pixmap)
#     # splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
#     # splash.setEnabled(False)
#
#     progressBar = QProgressBar(splash)
#     progressBar.setMaximum(10)
#     progressBar.setGeometry(0, pixmap.height() - 50, pixmap.width(), 20)
#
#     splash.show()
#     splash.showMessage("<h1><font color='gray'>Welcome HawkEye!</font></h1>",
#                        Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
#     for i in range(1, 11):
#         progressBar.setValue(i)
#         t = time.time()
#         while time.time() < t + 0.1:
#             app.processEvents()
#
#     # time.sleep(1)
#
#     window = MainWindow()
#     window.show()
#     splash.finish(window)
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     default_splash()
#
#
