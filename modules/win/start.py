#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import sys
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt6.QtCore import QUrl, Qt
from conf.paths import START_MOVIE_PATH
from modules.win.mainwin import MainWindow

"""
PyQt6 视频播放器样例
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

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)

        self.player.setSource(QUrl.fromLocalFile(START_MOVIE_PATH))
        self.player.play()

    def __init_state(self):
        self.player.playbackStateChanged.connect(self.show_mainwin)

    def show_mainwin(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
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
#     from PyQt6.QtWidgets import QSplashScreen, QProgressBar
#     from PyQt6.QtCore import QDir, Qt
#     from PyQt6.QtGui import QPixmap
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
