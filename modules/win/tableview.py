#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QHeaderView, QMessageBox, QSizePolicy, QGraphicsDropShadowEffect
from PyQt6.QtWidgets import QCalendarWidget, QFileDialog, QApplication, QTableView
from libs.enums import TABLES, SENSITIVE_NAME, tables_cn_name
from conf.paths import DUMP_HOME, PRIVATE_RESOURCE_HOME, IMAGE_HOME
from utils.filedir import StyleSheetHelper
from modules.interaction.widget import QTimeLineEdit
from modules.gui.ui_tableview import Ui_Form
from modules.interaction.dbmodel import TablePageModel


class DataGridWindow(TablePageModel, Ui_Form, QWidget):

    # https://stackoverflow.com/questions/4466797/how-to-remove-focus-from-a-qlineedit-when-anyplace-else-on-the-window-is-clicked
    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QTimeLineEdit):
            focused_widget.clearFocus()
        super().mousePressEvent(event)

    def __init__(self, table, columns, db_where=None, column_modes=None):
        TablePageModel.__init__(self, table, columns, db_where=db_where)
        Ui_Form.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)
        self.__init_ui()
        self.custom_ui()
        self.tableView.setModel(self.query_model)
        header = self.tableView.horizontalHeader()
        if column_modes is not None:
            for i, mode in enumerate(column_modes):
                header.setSectionResizeMode(i, mode)

        self.__init_state()
        self.update_ui_state()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def __init_ui(self):
        QDir.addSearchPath("image", os.path.join(PRIVATE_RESOURCE_HOME, "image"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)           # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.tableView.setAlternatingRowColors(True)    # 开启奇偶行交替背景色
        self.tableView.setShowGrid(False)               # 隐藏网格
        self.tableView.verticalHeader().hide()          # 隐藏行号
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        self.closeBtnLabel.setText('')
        label_images = zip([self.timeIconLabel], ['icon/calendar.png'])
        for label, img in label_images:
            label.setPixmap(QPixmap('image:%s' % img))
            # https://stackoverflow.com/questions/5653114/display-image-in-qt-to-fit-label-size
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.timeWidget.hide()
        self.timeWidget.setWindowFlag(self.timeWidget.windowFlags() | Qt.WindowType.SubWindow)
        self.calendarWidgetFrom.setFirstDayOfWeek(Qt.DayOfWeek.Sunday)
        # 隐藏左侧当前第几周
        self.calendarWidgetFrom.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendarWidgetTo.setFirstDayOfWeek(Qt.DayOfWeek.Sunday)
        self.calendarWidgetTo.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        #
        win_sheet = StyleSheetHelper.load_qss(name='tableview').replace('IMAGE_HOME', IMAGE_HOME)
        self.setStyleSheet(win_sheet)
        # 设置PlaceholderText样式(必须在setStyleSheet后设置)
        palette = self.timeLineEdit.palette()
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 100))
        self.timeLineEdit.setPalette(palette)
        #
        for button in [self.closeBtnLabel, self.calendarWidgetFrom, self.calendarWidgetTo,
                       self.searchBtn, self.dumpBtn, self.refreshBtn, self.timeOkBtn,
                       self.prePageBtn, self.nextPageBtn, self.switchPageBtn,
                       self.pageRecordComboBox, self.searchCodeComboBox]:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # 窗体自定义阴影
        self.render_shadow()

    def custom_ui(self):
        pass

    def __init_state(self):
        self.prePageBtn.clicked.connect(self.on_prev_page)
        self.nextPageBtn.clicked.connect(self.on_next_page)
        self.switchPageBtn.clicked.connect(self.go_switch_page)
        self.searchBtn.clicked.connect(self.go_search)
        self.refreshBtn.clicked.connect(self.refresh)
        self.dumpBtn.clicked.connect(self.dump)
        self.closeBtnLabel.clicked.connect(self.close)
        self.timeLineEdit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.timeLineEdit.calendar_focus_in.connect(self.timeWidget.show)
        # self.timeLineEdit.calendar_focus_out.connect(self.timeWidget.hide)
        self.timeCloseBtn.clicked.connect(self.timeWidget.hide)

    def update_ui_state(self):
        self.totalRecordLabel.setText('共%s条' % self.total_record)
        if self.cur_page <= 1:
            self.prePageBtn.setEnabled(False)
        else:
            self.prePageBtn.setEnabled(True)

        if self.cur_page >= self.total_page:
            self.nextPageBtn.setEnabled(False)
        else:
            self.nextPageBtn.setEnabled(True)

    def go_switch_page(self):
        page = self.switchPageLineEdit.text().strip()
        if page == "":
            QMessageBox.information(self, "提示", "请输入跳转页面")
            return
        if not page.isdigit():
            QMessageBox.information(self, "提示", "请输入数字")
            return
        page_idx = int(page)
        if page_idx > self.total_page or page_idx < 1:
            QMessageBox.information(self, "提示", "没有指定的页，清重新输入")
            return
        self.switch_page = page_idx
        self.on_switch_page()

    def go_search(self):
        # origin = self.originLineEidt.text().strip()
        # if origin == "":
        #     QtWidgets.QMessageBox.information(self, "提示", "请输入查询内容")
        #     return
        code = self.searchCodeComboBox.currentText()
        if code.upper() == 'ALL':
            self.db_where = None
        else:
            if self.table == TABLES.CrawlStat.value:
                self.db_where = 'resp_code=%s' % code
            elif self.table == TABLES.Extractor.value or self.table == TABLES.Sensitives.value:
                self.db_where = 'sensitive_name="%s"' % code

        self.update_total_count()
        self.cur_page = 1
        self.query_page(page=1)

    def refresh(self):
        self.cur_page = 1
        self.query_page(page=1)
        self.update_total_count()

    def dump(self):
        filepath, ok = QFileDialog.getSaveFileName(
            self, "保存文件", os.path.join(DUMP_HOME, "%s.csv" % tables_cn_name.get(self.table, self.table))
        )
        if ok:
            try:
                self.sqlite.dump(self.table, filepath, columns=self.columns)
                QMessageBox.information(self, "提示", "保存成功. 文件路径: " + filepath)
            except Exception as e:
                QMessageBox.warning(self, "提示", "保存失败. 错误原因: " + str(e))

    def closeEvent(self, event):
        self.close_db()

    def render_shadow(self):
        """
        https://blog.csdn.net/mahuatengmmp/article/details/113772969
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # 偏移
        shadow.setBlurRadius(12)  # 阴影半径
        shadow.setColor(QColor(128, 128, 255))  # 阴影颜色
        self.centralWidget.setGraphicsEffect(shadow)  # 将设置套用到widget窗口中


class ProgressDataWindow(DataGridWindow):
    def __init__(self,  resp_code=None):
        columns = dict(zip(
            ['id', 'origin', 'resp_code', 'desc', 'create_time'],
            ['ID', 'URL/FILE路径', '状态码', '描述', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents,
                        QHeaderView.ResizeMode.ResizeToContents]
        db_where = ''
        if resp_code is not None:
            if ' ' in resp_code:
                # 有空格，是完整的查询语句
                db_where += resp_code
            else:
                # 没有空格，只是一个值
                db_where += 'resp_code=%s' % resp_code
        super().__init__(table=TABLES.CrawlStat.value, columns=columns, column_modes=column_modes,  db_where=db_where)

    def custom_ui(self):
        if not self.db_where:
            self.searchCodeLabel.setText('状态码')
            codes = self.sqlite.select('SELECT DISTINCT resp_code FROM %s ORDER BY resp_code' % self.table)
            codes = [item[0] for item in codes]
            for i, code in enumerate(codes):
                self.searchCodeComboBox.insertItem(i+1, str(code))
        else:
            self.searchCodeLabel.hide()
            self.searchCodeComboBox.hide()


class ExtractDataWindow(DataGridWindow):
    def __init__(self, sensitive_type=None):
        columns = dict(zip(
            ['id', 'origin', 'sensitive_name', 'content', 'count', 'create_time'],
            ['ID', 'URL/FILE路径', '敏感类型', '敏感内容', '数量', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        db_where = ''
        if sensitive_type is not None:
            db_where += 'sensitive_type=%s' % sensitive_type
        super().__init__(table=TABLES.Extractor.value, columns=columns, column_modes=column_modes, db_where=db_where)

    def custom_ui(self):
        if not self.db_where:
            self.searchCodeLabel.setText('敏感类型')
            names = [SENSITIVE_NAME.URL.value, SENSITIVE_NAME.IDCARD.value, SENSITIVE_NAME.KEYWORD.value]
            for i, name in enumerate(names):
                self.searchCodeComboBox.insertItem(i + 1, name)
        else:
            self.searchCodeLabel.hide()
            self.searchCodeComboBox.hide()


class SensitiveDataWindow(DataGridWindow):
    def __init__(self, sensitive_type=None):
        columns = dict(zip(
            ['id',  'sensitive_name', 'content', 'origin', 'create_time'],
            ['ID',  '敏感类型', '敏感内容', 'URL/FILE来源', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents,
                        QHeaderView.ResizeMode.Stretch, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents]
        db_where = ''
        if sensitive_type is not None:
            db_where += 'sensitive_type=%s' % sensitive_type
        super().__init__(table=TABLES.Sensitives.value, columns=columns, column_modes=column_modes,  db_where=db_where)

    def custom_ui(self):
        if not self.db_where:
            self.searchCodeLabel.setText('敏感类型')
            names = [SENSITIVE_NAME.URL.value, SENSITIVE_NAME.IDCARD.value, SENSITIVE_NAME.KEYWORD.value]
            for i, name in enumerate(names):
                self.searchCodeComboBox.insertItem(i + 1, name)
        else:
            self.searchCodeLabel.hide()
            self.searchCodeComboBox.hide()


class WhiteListDataWindow(DataGridWindow):
    def __init__(self, white_type='domain'):
        columns = dict(zip(
            ['id', 'ioc', 'desc', 'create_time'],
            ['ID', '内容', '描述', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        db_where = 'white_type="%s"' % white_type
        super().__init__(table=TABLES.WhiteList.value, columns=columns, db_where=db_where, column_modes=column_modes)

    def custom_ui(self):
        self.searchCodeLabel.hide()
        self.searchCodeComboBox.hide()
        self.dumpBtn.hide()
