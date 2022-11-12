#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import math
from collections import OrderedDict
from PyQt5.QtCore import QDir, Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QPalette, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QHeaderView, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QCalendarWidget, QFileDialog, QApplication, QTableView, QPushButton
from libs.enums import TABLES, SENSITIVE_FLAG, SENSITIVE_NAME, sensitive_flag_name
from conf.paths import DUMP_HOME, PRIVATE_RESOURCE_HOME, IMAGE_HOME
from utils.filedir import StyleSheetHelper
from modules.interaction.widget import QTimeLineEdit
from modules.gui.ui_tableview import Ui_Form
from modules.interaction.dbmodel import TablePageModel
from modules.win.msgbox import QWarnMessageBox, QInfoMessageBox, QFileSaveMessageBox


class DataGridWindow(TablePageModel, Ui_Form, QWidget):

    # https://stackoverflow.com/questions/4466797/how-to-remove-focus-from-a-qlineedit-when-anyplace-else-on-the-window-is-clicked
    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QTimeLineEdit):
            focused_widget.clearFocus()
        super().mousePressEvent(event)

    def __init__(self, table, columns, db_where=None, column_modes=None, title='监测详情'):
        TablePageModel.__init__(self, table, columns, db_where=db_where)
        Ui_Form.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)
        self.titleLabel.setText(title)
        self.__init_ui()
        self.modify_ui()
        #
        self.page_buttons = (self.pageOneBtn, self.pageTwoBtn, self.pageThreeBtn, self.pageFourBtn, self.pageFiveBtn)
        self.page_btn_ix_range = [1, 5]
        #
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
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.tableView.setAlternatingRowColors(True)  # 开启奇偶行交替背景色
        self.tableView.setShowGrid(False)  # 隐藏网格
        self.tableView.verticalHeader().hide()  # 隐藏行号
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.closeBtnLabel.setText('')
        label_images = zip([self.timeIconLabel], ['icon/calendar.png'])
        for label, img in label_images:
            label.setPixmap(QPixmap('image:%s' % img))
            # https://stackoverflow.com/questions/5653114/display-image-in-qt-to-fit-label-size
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.timeWidget.hide()
        # TypeError: setWindowFlag(self, Qt.WindowType, on: bool = True): argument 1 has unexpected type 'WindowFlags'
        # self.timeWidget.setWindowFlag(self.timeWidget.windowFlags() | Qt.WindowType.SubWindow)
        self.timeWidget.setWindowFlag(Qt.WindowType.SubWindow)
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
        # 时间选择弹窗阴影
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # 偏移
        shadow.setBlurRadius(6)  # 阴影半径
        shadow.setColor(QColor(128, 128, 255))  # 阴影颜色
        self.timeWidget.setGraphicsEffect(shadow)  # 将设置套用到widget窗口中

    def modify_ui(self):
        pass

    def __init_state(self):
        self.prePageBtn.clicked.connect(self.on_prev_page)
        self.nextPageBtn.clicked.connect(self.on_next_page)
        self.switchPageBtn.clicked.connect(self.on_switch_page)
        # for btn in self.page_buttons:
        #     page_ix = int(btn.text())
        #     btn.clicked.connect(lambda: self.on_switch_page(page=page_ix))
        self._set_page_btn_event()
        self.searchBtn.clicked.connect(self.go_search)
        self.refreshBtn.clicked.connect(self.refresh)
        self.dumpBtn.clicked.connect(self.dump)
        self.closeBtnLabel.clicked.connect(self.close)
        self.timeLineEdit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.timeLineEdit.calendar_focus_in.connect(self.timeWidget.show)
        # self.timeLineEdit.calendar_focus_out.connect(self.timeWidget.hide)
        self.calendarWidgetFrom.selectionChanged.connect(self._update_time)
        self.calendarWidgetTo.selectionChanged.connect(self._update_time)
        self.timeEditFrom.timeChanged.connect(lambda: self._update_time(operation='change'))
        self.timeEditTo.timeChanged.connect(lambda: self._update_time(operation='change'))
        self.timeOkBtn.clicked.connect(lambda: self._update_time(operation='ok'))
        self.timeCloseBtn.clicked.connect(lambda: self._update_time(operation='clear'))
        self.pageRecordComboBox.currentTextChanged.connect(self._update_page_record)

    def _update_time(self, operation='change'):
        if operation == 'clear':
            self.timeLineEdit.setText('')
        elif operation == 'change' or (operation == 'ok' and not self.timeLineEdit.text()):
            date_from = str(self.calendarWidgetFrom.selectedDate().toPyDate())
            date_to = str(self.calendarWidgetTo.selectedDate().toPyDate())
            time_from = str(self.timeEditFrom.time().toPyTime())
            time_to = str(self.timeEditTo.time().toPyTime())
            self.timeLineEdit.setText('{date_from} {time_from} - {date_to} {time_to}'.format(
                date_from=date_from, time_from=time_from, date_to=date_to, time_to=time_to))
        if operation == 'ok' or operation == 'clear':
            self.timeWidget.hide()

    def _update_page_record(self):
        self.page_record = int(self.pageRecordComboBox.currentText()[:2])
        self.total_page = math.ceil(self.total_record / self.page_record)
        self.cur_page = min(self.cur_page, self.total_page)

        if self.total_page <= 0:
            return
        if self.total_page >= 5 and self.cur_page >= 5:
            for i, btn in enumerate(self.page_buttons):
                btn.setText(str(self.cur_page - 5 + (i + 1)))
            self.page_btn_ix_range = [int(self.page_buttons[0].text()), int(self.page_buttons[-1].text())]
        elif self.total_page >= 5 and self.cur_page < 5:
            for i, btn in enumerate(self.page_buttons):
                btn.setText(str(i + 1))
            self.page_btn_ix_range = [int(self.page_buttons[0].text()), int(self.page_buttons[-1].text())]
        elif 0 < self.total_page < 5:
            for i, btn in enumerate(self.page_buttons[:self.total_page]):
                btn.setText(str(i + 1))
            self.page_btn_ix_range = [int(self.page_buttons[0].text()), int(self.page_buttons[self.total_page].text())]

        start_index = (self.cur_page - 1) * self.page_record
        self.limit_query(start_index=start_index)
        self.update_ui_state()
        self._set_page_btn_event()

    def update_ui_state(self):
        self.totalRecordLabel.setText('共%s条' % self.total_record)
        # 判断是否可以操作上一页、下一页
        if self.page_btn_ix_range[0] > 1:
            self.prePageBtn.setEnabled(True)
        else:
            self.prePageBtn.setEnabled(False)

        if self.page_btn_ix_range[1] < self.total_page:
            self.nextPageBtn.setEnabled(True)
        else:
            self.nextPageBtn.setEnabled(False)
        # 当总页数不足5个时，需判断隐藏多余按钮
        buttons = self.page_buttons[1:]
        if 0 < self.total_page < 5:
            for btn in buttons[:self.total_page - 1]:
                btn.show()
            for btn in buttons[self.total_page - 1:]:
                btn.hide()
        elif self.total_page >= 5:
            for btn in buttons:
                btn.show()
        if self.total_page > 0:
            self.pageOneBtn.setEnabled(True)
        else:
            self.pageOneBtn.setEnabled(False)
        # 高亮显示当前页面按钮
        for btn in self.page_buttons:
            if int(btn.text()) == self.cur_page:
                btn.setStyleSheet('color: #2358DE; background: #FFFFFF; border: 1px solid #2358DE;')
            else:
                btn.setStyleSheet('color: #5C5C5C; background: #FFFFFF; border: 1px solid #C6CCD6;')

    def _set_page_btn_event(self):
        self.pageOneBtn.clicked.connect(lambda: self.on_switch_page(page=int(self.pageOneBtn.text())))
        self.pageTwoBtn.clicked.connect(lambda: self.on_switch_page(page=int(self.pageTwoBtn.text())))
        self.pageThreeBtn.clicked.connect(lambda: self.on_switch_page(page=int(self.pageThreeBtn.text())))
        self.pageFourBtn.clicked.connect(lambda: self.on_switch_page(page=int(self.pageFourBtn.text())))
        self.pageFiveBtn.clicked.connect(lambda: self.on_switch_page(page=int(self.pageFiveBtn.text())))

    def on_next_page(self):
        for btn in self.page_buttons:
            btn.clicked.disconnect()
            page_ix = int(btn.text()) + 1
            btn.setText(str(page_ix))
            # 无法生效....
            # btn.clicked.connect(lambda: self.on_switch_page(page=page_ix))
        self._set_page_btn_event()
        self.page_btn_ix_range = [int(self.page_buttons[0].text()), int(self.page_buttons[-1].text())]
        super().on_next_page()

    def on_prev_page(self):
        for btn in self.page_buttons:
            btn.clicked.disconnect()
            page_ix = int(btn.text()) - 1
            btn.setText(str(page_ix))
            # btn.clicked.connect(lambda: self.on_switch_page(page=page_ix))
        self._set_page_btn_event()
        self.page_btn_ix_range = [int(self.page_buttons[0].text()), int(self.page_buttons[-1].text())]
        super().on_prev_page()

    @pyqtSlot()
    # 不添加@pyqtSlot()，page参数会被设置为False
    # https://stackoverflow.com/questions/56422246/function-call-through-signal-changes-default-keyed-arguments-to-false-why
    # https://stackoverflow.com/questions/53110309/qpushbutton-clicked-fires-twice-when-autowired-using-ui-form/53110495
    def on_switch_page(self, page=None):
        if page is None:
            page = self.switchPageLineEdit.text().strip()
            if page == '':
                QWarnMessageBox('请输入跳转页面').exec()
                return
            if not page.isdigit():
                QWarnMessageBox('请输入数字').exec()
                return
            page = int(page)
        elif not (isinstance(page, int) and page > 0):
            raise ValueError('跳转页面必须是正整数')
        #
        if page > self.total_page or page < 1:
            QWarnMessageBox('没有指定的页: %s' % page).exec()
            return
        if page == self.cur_page:
            return

        if page < self.page_btn_ix_range[0] or page > self.page_btn_ix_range[-1]:
            offset = max(0, page - 5)
            for i, btn in enumerate(self.page_buttons):
                btn.setText(str(offset + (i + 1)))
            self.page_btn_ix_range = [int(self.page_buttons[0].text()), int(self.page_buttons[-1].text())]
        #
        self.cur_page = page
        self.query_page()

    def go_search(self):
        # origin = self.originLineEidt.text().strip()
        # if origin == "":
        #     QtWidgets.QMessageBox.information(self, "提示", "请输入查询内容")
        #     return
        self.db_where = self._db_where
        if self.searchCodeComboBox.isVisible():
            code = self.searchCodeComboBox.currentText()
            if not (code == '' or code.upper() == 'ALL'):
                _db_where = ''
                if self.table == TABLES.CrawlStat.value:
                    self.db_where = 'resp_code=%s' % code
                elif self.table == TABLES.Extractor.value or self.table == TABLES.Sensitives.value:
                    _db_where = 'sensitive_name="%s"' % code
                    self.db_where = _db_where + ('' if not self.db_where else ' AND ' + self.db_where)
        if self.timeLineEdit.text():
            time_range = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', self.timeLineEdit.text())
            if len(time_range) != 2:
                QWarnMessageBox("查询日期格式错误，请重新输入").exec()
                return
            _db_where = 'create_time>= "%s" AND create_time<="%s"' % (time_range[0], time_range[1])
            self.db_where = _db_where + ('' if not self.db_where else ' AND ' + self.db_where)

        self.update_total_count()
        # 重新计算分页数量
        self._update_page_record()
        self.cur_page = 1
        self.query_page(page=1)

    def refresh(self):
        self.cur_page = 1
        self.query_page(page=1)
        self.update_total_count()

    def dump(self):
        filepath, ok = QFileDialog.getSaveFileName(
            self, "保存文件", os.path.join(DUMP_HOME, "%s.csv" % self.titleLabel.text())
        )
        if ok:
            try:
                self.sqlite.dump(self.table, filepath, columns=self.columns, where=self.db_where)
                QFileSaveMessageBox("保存成功. 文件路径:\n" + filepath, path=filepath).exec()
            except Exception as e:
                QWarnMessageBox("保存失败. 错误原因:\n" + str(e)).exec()

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
    def __init__(self, title='URL文件爬取列表', resp_code=None):
        columns = OrderedDict(zip(
            ['id', 'origin', 'origin_name', 'resp_code', 'desc', 'create_time'],
            ['ID', 'URL/FILE路径', 'URL/FILE名称', '状态码', '描述', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.Stretch, QHeaderView.ResizeMode.ResizeToContents,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        db_where = ''
        if resp_code is not None:
            if ' ' in resp_code:
                # 有空格，是完整的查询语句
                db_where += resp_code
            else:
                # 没有空格，只是一个值
                db_where += 'resp_code=%s' % resp_code
        super().__init__(table=TABLES.CrawlStat.value,
                         columns=columns, column_modes=column_modes,
                         db_where=db_where, title=title)

    def modify_ui(self):
        self.searchCodeLabel.setText('状态码')
        codes = self.sqlite.select('SELECT DISTINCT resp_code FROM {table} {where} ORDER BY resp_code'.format(
            table=self.table, where='' if not self.db_where else 'WHERE ' + self.db_where))
        codes = [item[0] for item in codes]
        for i, code in enumerate(codes):
            self.searchCodeComboBox.insertItem(i + 1, str(code))


class ExtractDataWindow(DataGridWindow):
    def __init__(self, title='URL文件解析结果'):
        columns = OrderedDict(zip(
            ['id', 'origin', 'sensitive_name', 'content', 'count', 'create_time'],
            ['ID', 'URL/FILE路径', '敏感类型', '敏感内容', '数量', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        super().__init__(table=TABLES.Extractor.value,
                         columns=columns, column_modes=column_modes,
                         db_where=None, title=title)

    def modify_ui(self):
        self.searchCodeLabel.setText('敏感类型')
        names = [SENSITIVE_NAME.URL.value, SENSITIVE_NAME.IDCARD.value, SENSITIVE_NAME.KEYWORD.value]
        for i, name in enumerate(names):
            self.searchCodeComboBox.insertItem(i + 1, name)


class SensitiveDataWindow(DataGridWindow):
    def __init__(self, title='敏感内容', sensitive_type=None):
        columns = OrderedDict(zip(
            ['id', 'sensitive_name', 'content', 'content_name', 'desc', 'origin', 'create_time'],
            ['ID', '敏感类型', '敏感内容', '内容名称', '描述', '发现地址', '发现时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents,
                        QHeaderView.ResizeMode.Stretch, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents]
        db_where = ''
        if sensitive_type in sensitive_flag_name:
            db_where += 'sensitive_type=%s' % sensitive_type
            title = sensitive_flag_name[sensitive_type].value
        title += '列表'
        # 外链表格添加标题描述，其他移除描述
        if sensitive_type != SENSITIVE_FLAG.URL:
            del columns['content_name']
            del columns['desc']
            column_modes.pop(3)
            column_modes.pop(3)
        #
        super().__init__(table=TABLES.Sensitives.value,
                         columns=columns, column_modes=column_modes,
                         db_where=db_where, title=title)

    def modify_ui(self):
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
        columns = OrderedDict(zip(
            ['id', 'ioc', 'desc', 'create_time'],
            ['ID', '内容', '描述', '创建时间']
        ))
        column_modes = [QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.Stretch,
                        QHeaderView.ResizeMode.ResizeToContents, QHeaderView.ResizeMode.ResizeToContents]
        db_where = 'white_type="%s"' % white_type
        super().__init__(table=TABLES.WhiteList.value, columns=columns, db_where=db_where, column_modes=column_modes)

    def modify_ui(self):
        self.searchCodeLabel.hide()
        self.searchCodeComboBox.hide()
        self.dumpBtn.hide()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    extractWindow = ExtractDataWindow()
    extractWindow.show()
    sys.exit(app.exec())
