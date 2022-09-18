#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from pathlib import Path
import traceback
import datetime
from collections import namedtuple
from PyQt6.QtWidgets import QWidget, QApplication, QDialog, QSizePolicy, QLayout
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor, QCursor
from libs.pyaml import configure
from libs.enums import sensitive_flag_name, SENSITIVE_FLAG
from conf.paths import PRIVATE_RESOURCE_HOME, IMAGE_HOME
from modules.gui.ui_main_window import Ui_MainWindow as UiMainWindow
from modules.interaction.widget import WaitingSpinner
from modules.win.msgbox import QWarnMessageBox
from modules.win.tableview import ProgressDataWindow, ExtractDataWindow, SensitiveDataWindow
from modules.win.settings import SettingsWindow
from modules.win.help import HelpAboutWindow
from modules.interaction.manager import TaskManager
from modules.interaction.metric import AbstractMetric, CrawlMetric, ExtractMetric
from utils.filedir import StyleSheetHelper
from utils.mixed import ssh_accessible, human_timedelta
from tools.license import LicenseHelper
from libs.logger import logger


class MainWindow(UiMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressWindow = None
        self.extractWindow = None
        self.sensitiveWindow = None
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
        #
        self.license = LicenseHelper()

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
        # self.setWindowIcon(QIcon(QPixmap('image:logo.png')))
        # self.setWindowTitle('敏感信息监测系统')
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
                       self.historyBtn, self.detailBtn, self.settingBtnLabel, self.helpBtnLabel,
                       self.minimizeBtnLabel, self.maximizeBtnLabel, self.closeBtnLabel,
                       self.crawledCntLabel, self.hitCntLabel, self.failedCntLabel,
                       self.extUrlCntLabel, self.idcardCntLabel, self.keywordCntLabel,
                       self.crawledCntLabel2, self.hitCntLabel2, self.failedCntLabel2,
                       self.extUrlCntLabel2, self.idcardCntLabel2, self.keywordCntLabel2]:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        for waiting_layout in (self.extUrlWaitingLayout, self.idcardWaitingLayout, self.keywordWaitingLayout):
            spinner = WaitingSpinner(self, lines=16, radius=4, line_length=7, speed=1, color=(35, 88, 222))
            waiting_layout.addWidget(spinner)
            spinner.start()
        # 自动换行
        self.robotTipsLabel.adjustSize()
        self.robotTipsLabel.setWordWrap(True)

    def __init_state(self):
        # 保证Layout隐藏部分组件时,剩余组件能自动移动填充(例如grid layout隐藏前两行,后几行能自动上移)
        # https://stackoverflow.com/questions/2293708/pyqt4-hide-widget-and-resize-window
        self.dynGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        #
        self.minimizeBtnLabel.clicked.connect(self.showMinimized)
        self.maximizeBtnLabel.clicked.connect(self.showMaximized)
        self.maximizeBtnLabel.hide()
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
        self.cancelBtn.clicked.connect(self.cancel)
        self.stopBtn.clicked.connect(lambda: self.terminate(notice=True))
        self.returnBtn.clicked.connect(self.return2main)
        self.detailBtn.clicked.connect(self.show_extract_win)
        self.settingBtnLabel.clicked.connect(self.show_settings_win)
        self.helpBtnLabel.clicked.connect(self.show_help_win)
        self.historyBtn.clicked.connect(self.show_latest_result)
        self.crawledCntLabel.clicked.connect(lambda: self.show_progress_win(target='total'))
        self.crawledCntLabel2.clicked.connect(lambda: self.show_progress_win(target='total'))
        self.failedCntLabel.clicked.connect(lambda: self.show_progress_win(target='failed'))
        self.failedCntLabel2.clicked.connect(lambda: self.show_progress_win(target='failed'))
        self.extUrlCntLabel.clicked.connect(lambda: self.show_sensitive_win(target=SENSITIVE_FLAG.URL))
        self.extUrlCntLabel2.clicked.connect(lambda: self.show_sensitive_win(target=SENSITIVE_FLAG.URL))
        self.idcardCntLabel.clicked.connect(lambda: self.show_sensitive_win(target=SENSITIVE_FLAG.IDCARD))
        self.idcardCntLabel2.clicked.connect(lambda: self.show_sensitive_win(target=SENSITIVE_FLAG.IDCARD))
        self.keywordCntLabel.clicked.connect(lambda: self.show_sensitive_win(target=SENSITIVE_FLAG.KEYWORD))
        self.keywordCntLabel2.clicked.connect(lambda: self.show_sensitive_win(target=SENSITIVE_FLAG.KEYWORD))
        self.hitCntLabel.clicked.connect(self.show_extract_win)
        self.hitCntLabel2.clicked.connect(self.show_extract_win)
        #
        try:
            if not configure['metric']['expend_time']:
                self.historyBtn.setEnabled(False)
        except:
            pass

    def __toggle_sftp(self, visible=False):
        sftp_edits = (self.portLineEdit, self.userLineEdit, self.passwdLineEdit, self.pathLineEdit)
        for line_edit in sftp_edits:
            line_edit.setVisible(visible)

    def _robot_tips(self, tips='', label_id=1):
        label = self.robotTipsLabel2 if label_id == 2 else self.robotTipsLabel
        if not tips or tips == 'default':
            if label_id == 2:
                label.setStyleSheet('color: black; font-weight:400;')
                tips = '恭喜您，已完成信息监测！'
            else:
                label.setStyleSheet('color: black; font-weight:400;')
                tips = '您好，欢迎使用敏感信息监测系统！'
        else:
            if label_id == 2:
                label.setStyleSheet('color: gray;')
            else:
                label.setStyleSheet('color: red; font-weight: bold;')
        label.setText('    %s' % tips)

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
            self._robot_tips(tips='SFTP' + '/'.join(empty) + '内容为空！')
            return False
        if not self.portLineEdit.text().strip().isdigit():
            self._robot_tips(tips='SFTP端口格式错误！')
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

    def _init_sensitive_layout(self):
        for layout in (self.extUrlGridLayout, self.idcardGridLayout, self.keywordGridLayout):
            for ix in range(layout.count()):
                child = layout.itemAt(ix).widget()
                child.setVisible(True)
        self.extUrlTextEdit.setText('')
        self.idcardTextEdit.setText('')
        self.keywordTextEdit.setText('')
        self._set_crawl_metric(CrawlMetric())
        self._set_extract_metric(ExtractMetric())
        self._set_expend_time(0)

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
        # expend_time = '{:0>8}'.format(str(datetime.timedelta(seconds=seconds)))
        expend_time = human_timedelta(seconds)
        self.expendTimeLabel.setText(expend_time)
        self.expendTimeLabel2.setText(expend_time)

    def _set_crawl_metric(self, metric):
        self.crawledCntLabel.setText(str(metric.crawl_total))
        self.failedCntLabel.setText(str(metric.crawl_failed))
        self.crawledCntLabel2.setText(str(metric.crawl_total))
        self.failedCntLabel2.setText(str(metric.crawl_failed))

    def _set_extract_metric(self, metric):
        self.extUrlCntLabel.setText('%s' % metric.exturl_count)
        self.extUrlCntLabel2.setText('%s' % metric.exturl_count)
        # if metric.idcard_count > 0:
        #     self.idcardCntLabel.setText('%s/%s' % (metric.idcard_count, metric.idcard_find))
        #     self.idcardCntLabel2.setText('%s/%s' % (metric.idcard_count, metric.idcard_find))
        self.idcardCntLabel.setText('%s' % metric.idcard_count)
        self.idcardCntLabel2.setText('%s' % metric.idcard_count)
        self.keywordCntLabel.setText('%s' % metric.keyword_find)
        self.keywordCntLabel2.setText('%s' % metric.keyword_find)
        #
        self.hitCntLabel.setText(str(metric.origin_hit))
        self.hitCntLabel2.setText(str(metric.origin_hit))

    def _set_metric(self, metric=None):
        if not metric:
            metric = AbstractMetric()
            for key, value in configure['metric'].items():
                setattr(metric, key, value)
        if hasattr(metric, 'expend_time'):
            seconds = 0
            items = re.findall(r'\d+', metric.expend_time)
            bases = [1, 60, 3600, 86400]
            for i, item in enumerate(reversed(items)):
                seconds += int(item) * bases[i]
            self._set_expend_time(seconds)
        self._set_crawl_metric(metric)
        self._set_extract_metric(metric)

    def _save_metric(self):
        configure['metric']['expend_time'] = self.expendTimeLabel.text()
        configure['metric']['crawl_total'] = self.crawledCntLabel.text()
        configure['metric']['crawl_failed'] = self.failedCntLabel.text()
        configure['metric']['exturl_count'] = self.extUrlCntLabel.text()
        configure['metric']['idcard_count'] = self.idcardCntLabel.text()
        configure['metric']['keyword_find'] = self.keywordCntLabel.text()
        configure['metric']['origin_hit'] = self.hitCntLabel.text()
        configure.save()

    def start(self):
        lic_check_result = self.license.check()
        if lic_check_result != 'OK':
            QWarnMessageBox(lic_check_result).exec()
            return
        if not self._check_inputs():
            return
        if self.protocol == 'sftp' and not self._check_ssh_accessible():
            return
        box = QWarnMessageBox('开始监测将清除历史数据！')
        if box.exec() == QDialog.DialogCode.Rejected:
            return
        # 捕获启动时的错误
        try:
            TaskManager.clear()
            self.task_manager = TaskManager(self.target,
                                            flags=self.sensitive_flags,
                                            protocol=self.protocol,
                                            keywords=self._keywords,
                                            auth_config=self.auth_config)
            self.task_manager.start()
        except Exception as e:
            self._robot_tips(tips=str(e))
            logger.error(traceback.format_exc())
            return
        # 恢复默认提示
        self._robot_tips(tips='default')
        # 隐藏没有选中的监控内容
        self._init_sensitive_layout()
        self._hide_sensitive_layout()
        #
        self.historyBtn.setEnabled(True)
        configure['metric']['start_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        configure['target'] = self.target
        #
        self.task_manager.expend_time_signal.connect(self._set_expend_time)
        self.task_manager.extractor.finished.connect(self.terminate)
        self.task_manager.extractor.cur_result.connect(self._log_extractor_result)
        self.task_manager.crawler.metrics.connect(self._set_crawl_metric)
        self.task_manager.extractor.metrics.connect(self._set_extract_metric)
        # 显示下一个Tab页
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.monitTab, '')

    def return2main(self):
        # 返回主页面
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.mainTab, '')

    def cancel(self):
        box = QWarnMessageBox("请确认是否取消目前任务！")
        if box.exec() == QDialog.DialogCode.Rejected:
            return
        self.task_manager.terminate()
        del self.task_manager
        #
        self.historyBtn.setEnabled(False)
        self.return2main()

    def terminate(self, notice=False):
        if notice:
            box = QWarnMessageBox("请确认是否终止目前任务。任务终止后需重新开始！")
            if box.exec() == QDialog.DialogCode.Rejected:
                return
        self.task_manager.terminate()
        del self.task_manager
        #
        self._save_metric()
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.finishTab, '')
        self._robot_tips(tips='default', label_id=2)

    def show_latest_result(self):
        self._set_metric()
        tips = '最近监控对象：%s\n    任务开始时间：%s' % (configure['target'], configure['metric']['start_time'])
        self._robot_tips(tips=tips, label_id=2)
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.finishTab, '')

    def show_progress_win(self, target='total'):
        if target == 'failed':
            self.progressWindow = ProgressDataWindow(resp_code='resp_code>=400 OR resp_code=-1')
        else:
            self.progressWindow = ProgressDataWindow()
        self.progressWindow.show()

    def show_extract_win(self, target=None):
        if isinstance(target, SENSITIVE_FLAG):
            self.extractWindow = ExtractDataWindow(sensitive_type=target.value)
        else:
            self.extractWindow = ExtractDataWindow()
        self.extractWindow.show()

    def show_sensitive_win(self, target=None):
        if isinstance(target, SENSITIVE_FLAG):
            self.sensitiveWindow = SensitiveDataWindow(sensitive_type=target.value)
        else:
            self.sensitiveWindow = SensitiveDataWindow()
        self.sensitiveWindow.show()

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
            for win in (self.helpAboutWindow, self.settingsWindow,
                        self.extractWindow, self.progressWindow, self.sensitiveWindow):
                if win:
                    win.close()
        else:
            event.ignore()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
