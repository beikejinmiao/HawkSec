#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import datetime
from pathlib import Path
from collections import namedtuple
from PyQt6.QtWidgets import QWidget, QApplication, QDialog, QSizePolicy, QLayout
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor, QCursor
from libs.enums import sensitive_flag_name, SENSITIVE_FLAG, QMSG_BOX_REPLY_NO, QMSG_BOX_REPLY_YES
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from modules.gui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.interaction.widget import WaitingSpinner
from modules.interaction.win.msgbox import QWarnMessageBox
from modules.interaction.win.tableview import ExtractDataWindow
from modules.interaction.win.settings import SettingsWindow
from modules.interaction.win.help import HelpAboutWindow
from modules.action.manager import TaskManager
from utils.filedir import StyleSheetHelper
from utils.mixed import ssh_accessible


class MainWindow(UiMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.extractWindow = None
        self.settingsWindow = None
        self.helpAboutWindow = None
        #
        self.__init_gui()
        self.__init_state()
        #
        self.target = ''
        self.protocol = 'https'
        self.sensitive_flags = list()
        self.ssh_accessible = False
        self.auth_config = None
        self._keywords = None
        self.task_manager = None
        self._move_flag = False

    # https://blog.csdn.net/QW1540235670/article/details/111028331
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() < self.dragWidget.height():
            self._move_flag = True
            self._move_position = event.pos() - self.pos()                      # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))              # 更改鼠标图标

    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self._move_flag:
            self.move(event.pos() - self._move_position)                        # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event):
        self._move_flag = False
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def __init_gui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabBarAutoHide(True)
        # StyleSheet中文件路径必须使用posix格式
        # https://stackoverflow.com/questions/51750501/do-not-insert-a-background-picture-into-widget-setstylesheet
        bg_pic_path = Path(os.path.join(IMAGE_HOME, 'bg.png')).as_posix()
        self.centralwidget.setStyleSheet('#centralwidget {border-image: url(%s);}' % bg_pic_path)
        # 使用border-image而不是background-image会让图片自适应widget大小
        # self.centralwidget.setStyleSheet(
        #     '#centralwidget {background-image: url(%s); background-repeat: no-repeat}' % bg_pic_path)
        self.closeBtnLabel.setText('')
        self.helpBtnLabel.setText('')
        self.settingBtnLabel.setText('')
        label_images = zip([self.logoLabel, self.robotLabel, self.robotLabel2,
                            self.waitforGifLabel, self.finishIconLabel,
                            self.extUrlIconLabel, self.idcardIconLabel, self.keywordIconLabel,
                            self.minimizeBtnLabel, self.maximizeBtnLabel],
                           ['logo.png', 'robot.png', 'robot.png',
                            'icon/waitfor.png', 'icon/finish.png',
                            'icon/exturl.png', 'icon/idcard.png', 'icon/keyword.png',
                            'icon/minimize.png', 'icon/maximize.png'])
        for label, img in label_images:
            label.setPixmap(QPixmap('image:%s' % img))
            # https://stackoverflow.com/questions/5653114/display-image-in-qt-to-fit-label-size
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # 设置整体样式
        win_sheet = StyleSheetHelper.load_qss(name='mainwin').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        # 设置PlaceholderText字体颜色和透明度
        self.line_edits = (self.addressLineEdit, self.portLineEdit,
                           self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in self.line_edits:
            palette = line_edit.palette()
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 100))
            line_edit.setPalette(palette)
        # 设置可点击组件悬浮手型按钮
        for button in [self.startBtn, self.cancelBtn, self.stopBtn, self.returnBtn,
                       self.dumpBtn, self.detailBtn, self.settingBtnLabel, self.helpBtnLabel,
                       self.minimizeBtnLabel, self.maximizeBtnLabel, self.closeBtnLabel,
                       self.crawledCntLabel, self.hitCntLabel, self.faieldCntLabel,
                       self.extUrlCntLabel, self.idcardCntLabel, self.keywordCntLabel,
                       self.crawledCntLabel2, self.hitCntLabel2, self.faieldCntLabel2,
                       self.extUrlCntLabel2, self.idcardCntLabel2, self.keywordCntLabel2]:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        for waiting_layout in (self.extUrlWaitingLayout, self.idcardWaitingLayout, self.keywordWaitingLayout):
            spinner = WaitingSpinner(self, lines=16, radius=4, line_length=7, speed=1, color=(35, 88, 222))
            waiting_layout.addWidget(spinner)
            spinner.start()

    def __init_state(self):
        # 保证Layout隐藏部分组件时,剩余组件能自动移动填充(例如grid layout隐藏前两行,后几行能自动上移)
        # https://stackoverflow.com/questions/2293708/pyqt4-hide-widget-and-resize-window
        self.dynGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        #
        self.minimizeBtnLabel.clicked.connect(self.showMinimized)
        self.maximizeBtnLabel.clicked.connect(self.showFullScreen)
        self.closeBtnLabel.clicked.connect(self.close)
        #
        self.__toggle_sftp()
        self.httpsRadioBtn.setChecked(True)
        self.extUrlTextEdit.setReadOnly(True)
        self.idcardTextEdit.setReadOnly(True)
        self.keywordTextEdit.setReadOnly(True)
        self.httpRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=False))
        self.httpsRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=False))
        self.sftpRadioBtn.clicked.connect(lambda: self.__toggle_sftp(visible=True))
        self.startBtn.clicked.connect(self.start)
        self.cancelBtn.clicked.connect(self.terminate)
        self.stopBtn.clicked.connect(lambda: self.terminate(notice=True))
        self.returnBtn.clicked.connect(self.cancel)
        self.detailBtn.clicked.connect(self.show_extract_win)
        self.settingBtnLabel.clicked.connect(self.show_settings_win)
        self.helpBtnLabel.clicked.connect(self.show_help_win)

    def __toggle_sftp(self, visible=False):
        sftp_edits = (self.portLineEdit, self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in sftp_edits:
            line_edit.setVisible(visible)

    def _robot_tips(self, tips=''):
        if not tips or tips == 'default':
            self.robotTipsLabel.setStyleSheet('color: black; font-weight:400;')
            tips = '您好，欢迎使用敏感信息监测系统！'
        else:
            self.robotTipsLabel.setStyleSheet('color: red; font-weight: bold;')
        self.robotTipsLabel.setText('    %s' % tips)

    def _check_inputs(self):
        self.target = self.addressLineEdit.text().strip()
        if len(self.target) <= 0:
            self._robot_tips(tips='请输入监控地址')
            return False
        # 访问协议
        for radio in (self.httpRadioBtn, self.httpsRadioBtn, self.sftpRadioBtn):
            if radio.isChecked():
                self.protocol = radio.text().lower()
        # 监控内容/敏感类型
        self.sensitive_flags = list()
        for ix, check_box in enumerate([self.extUrlCheckBox, self.idcardCheckBox, self.keywordCheckBox]):
            if check_box.isChecked():
                self.sensitive_flags.append(ix)
        if SENSITIVE_FLAG.KEYWORD in self.sensitive_flags:
            self._keywords = [item.strip() for item in self.keywordLineEdit.text().split(',')]
        if len(self.sensitive_flags) <= 0:
            self._robot_tips(tips='请选择监控内容：外链/身份证/关键字')
            return False
        return True

    SSH_CONFIG = namedtuple('SSH_CONFIG', ['host', 'port', 'username', 'password', 'path'])

    def get_ssh_config(self):
        return self.SSH_CONFIG(
            host=self.addressLineEdit.text().strip(),
            port=int(self.portLineEdit.text().strip()),
            username=self.userLineEdit.text().strip(),
            password=self.passwdLineEdit.text().strip(),
            path=self.pathLineEdit.text().strip()
        )

    def _check_ssh_input(self):
        self.elements = ('host', '地址', self.addressLineEdit), ('port', '端口', self.portLineEdit), \
                        ('username', '用户名', self.userLineEdit), ('password', '密码', self.passwdLineEdit), \
                        ('path', '路径', self.pathLineEdit)
        empty = []
        for field, name, ele in self.elements:
            if len(ele.text().strip()) <= 0:
                empty.append(name)
        if len(empty) > 0:
            self._robot_tips('SFTP' + '/'.join(empty) + '内容为空！')
            return False
        if not self.portLineEdit.text().strip().isdigit():
            self._robot_tips('SFTP端口格式错误！')
            return False
        return True

    def _check_ssh_accessible(self):
        if not self._check_ssh_input():
            self.accessible = False
            return None
        #
        config = self.get_ssh_config()
        try:
            ssh_accessible(config.host, port=config.port, username=config.username, password=config.password)
        except Exception as e:
            self.accessible = False
            QWarnMessageBox('访问SSH服务器错误！原因: ' + str(e)).exec()
            return None
        self.accessible = True      # 在已校验访问成功后,保存配置时无需再次校验
        self.auth_config = config._asdict()
        return self.auth_config

    def _hide_sensitive_layout(self):
        sensitive_layouts = {
            SENSITIVE_FLAG.URL: self.extUrlGridLayout,
            SENSITIVE_FLAG.IDCARD: self.idcardGridLayout,
            SENSITIVE_FLAG.KEYWORD: self.keywordGridLayout,
        }
        for flag in set(list(sensitive_layouts.keys())) - set(self.sensitive_flags):
            layout = sensitive_layouts[flag]
            for ix in range(layout.count()):
                child = layout.itemAt(ix).widget()
                child.setVisible(False)

    def _log_extractor_result(self, result):
        flag = result.flag
        if flag == SENSITIVE_FLAG.URL:
            text_edit = self.extUrlTextEdit
        elif flag == SENSITIVE_FLAG.IDCARD:
            text_edit = self.idcardTextEdit
        elif flag == SENSITIVE_FLAG.KEYWORD:
            text_edit = self.keywordTextEdit
        else:
            raise ValueError('不支持敏感内容Flag: %s' % flag)
        text_edit.append('来源：{origin}\t{name}：{content}'.format(
            origin=result.origin, name=sensitive_flag_name[flag].value, content=result.content))

    def _set_expend_time(self, seconds):
        seconds = int(seconds)
        # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
        expend_time = '{:0>8}'.format(str(datetime.timedelta(seconds=seconds)))
        self.expendTimeLabel.setText(expend_time)
        self.expendTimeLabel2.setText(expend_time)
        self.progressBar.setValue(min(2+int(seconds/240), 99))

    def _set_crawl_metric(self, metric):
        self.crawledCntLabel.setText(str(metric.crawl_total))
        self.faieldCntLabel.setText(str(metric.crawl_failed))
        self.crawledCntLabel2.setText(str(metric.crawl_total))
        self.faieldCntLabel2.setText(str(metric.crawl_failed))

    def _set_extract_metric(self, metric):
        self.extUrlCntLabel.setText('%s' % metric.external_url_count)
        self.extUrlCntLabel2.setText('%s' % metric.external_url_count)
        if metric.idcard_count > 0:
            self.idcardCntLabel.setText('%s/%s' % (metric.idcard_count, metric.idcard_find))
            self.idcardCntLabel2.setText('%s/%s' % (metric.idcard_count, metric.idcard_find))
        self.keywordCntLabel.setText('%s' % metric.keyword_find)
        self.keywordCntLabel2.setText('%s' % metric.keyword_find)
        #
        self.hitCntLabel.setText(str(metric.origin_hit))
        self.hitCntLabel2.setText(str(metric.origin_hit))

    def start(self):
        if not self._check_inputs():
            return
        if self.protocol == 'sftp' and not self._check_ssh_accessible():
            return
        box = QWarnMessageBox('开始监测将清除历史数据！')
        if box.exec() == QDialog.DialogCode.Rejected:
            return
        # 恢复默认提示
        self._robot_tips(tips='default')
        # 隐藏没有选中的监控内容
        self._hide_sensitive_layout()
        #
        TaskManager.clear()
        self.task_manager = TaskManager(self.target,
                                        flags=self.sensitive_flags,
                                        protocol=self.protocol,
                                        keywords=self._keywords,
                                        auth_config=self.auth_config)
        self.task_manager.start()
        self.task_manager.expend_time_signal.connect(self._set_expend_time)
        self.task_manager.extractor.finished.connect(self.terminate)
        self.task_manager.extractor.cur_result.connect(self._log_extractor_result)
        self.task_manager.crawler.metrics.connect(self._set_crawl_metric)
        self.task_manager.extractor.metrics.connect(self._set_extract_metric)
        # 显示下一个Tab页
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.monitTab, '')

    def cancel(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.mainTab, '')

    def terminate(self, notice=False):
        if notice:
            box = QWarnMessageBox("请确认是否终止目前任务。\n任务终止后需重新开始！")
            if box.exec() == QDialog.DialogCode.Rejected:
                return
        self.task_manager.terminate()
        del self.task_manager
        #
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.finishTab, '')

    def show_extract_win(self):
        self.extractWindow = ExtractDataWindow()        # 窗口关闭后销毁对象
        self.extractWindow.show()

    def show_settings_win(self):
        self.settingsWindow = SettingsWindow()        # 窗口关闭后销毁对象
        self.settingsWindow.show()

    def show_help_win(self):
        self.helpAboutWindow = HelpAboutWindow()
        self.helpAboutWindow.show()

    def closeEvent(self, event):
        box = QWarnMessageBox("确认退出！")
        if box.exec() == QDialog.DialogCode.Accepted:
            event.accept()
            if self.helpAboutWindow:
                self.helpAboutWindow.close()
            if self.settingsWindow:
                self.settingsWindow.close()
            if self.extractWindow:
                self.extractWindow.close()
        else:
            event.ignore()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
