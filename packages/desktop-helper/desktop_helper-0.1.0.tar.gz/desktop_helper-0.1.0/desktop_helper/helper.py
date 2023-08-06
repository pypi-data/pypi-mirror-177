import sys
from typing import Iterable
from PyQt6.QtWidgets import (QWidget, QApplication, QMainWindow, QFormLayout,
                             QTableWidget, QTableWidgetItem, QDockWidget, QTabWidget, QTextEdit, QToolBar, QFileDialog,
                             QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt, QProcess, QTimer, QSettings
from PyQt6.QtGui import QTextCursor, QAction, QColor, QCloseEvent
import time
import math
import ast
import enum
from typing import Union

ORGANIZATION_NAME = "Desk Helper"
APP_NAME = "Desk Helper"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        This will initiate UI.
        """
        # init statusbar
        status_bar = self.statusBar()
        status_bar.showMessage("Welcome.")

        # central tabs
        central_tabs = QTabWidget(self)
        self.setCentralWidget(central_tabs)
        central_tabs.setTabShape(QTabWidget.TabShape.Triangular)
        central_tabs.setMovable(True)
        central_tabs.setTabsClosable(True)
        central_tabs.tabCloseRequested.connect(self._handle_tab_close)
        self.central_tabs = central_tabs

        # process table
        process_pool = NProcessPool(self, central_tabs)
        # The following line is necessary because otherwise connect() in NProcessPool will not work
        self.process_pool = process_pool
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea, process_pool.table_dock())

        # settings panel
        settings = NSettingsPanel(self)
        self.settings = settings
        settings.register(process_pool.settings())
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea, settings.dock())

        # toolbox
        toolbox_file = process_pool.toolbar()
        self.addToolBar(toolbox_file)

        # general setting
        self.setGeometry(540, 100, 1600, 900)
        self.setWindowTitle('Desk Helper')
        self.show()

    def _handle_tab_close(self, index: int):
        tab_item = self.central_tabs.widget(index)
        if isinstance(tab_item, NProcessPool.NProcessTextEdit):
            tab_item.process().hide_display()

    def closeEvent(self, a0: QCloseEvent):
        self.process_pool.safe_close()


class NProcessPool():
    """
    TODO: Maintain a NProcessTableWidget, a process_list in the instance.
    """

    class ProcessHealth(enum.Enum):
        """
        Init: This is the original state display on the table, meaning script server is somewhere initializing.
        NoError: There is no error during script running, or user has ignored previous error.
        Unknown: The script hasn't run yet. Whether there is an error is not clear.
        Error: Ops. One or more error occur.
        Error now support:
            1. any output in stderr
        """
        Init = -1
        NoError = 0
        Unknown = 1
        Error = 2

    class NProcess(QProcess):
        next_id = 0

        def __init__(self, parent: QWidget, display_tab_widget: QTabWidget, pool: "NProcessPool"):
            super().__init__(parent)
            self._id = NProcessPool.NProcess.next_id
            self._display_tab_widget = display_tab_widget
            self._pool = pool
            NProcessPool.NProcess.next_id += 1
            self._output_text_edit = NProcessPool.NProcessTextEdit(
                "New Process", self, parent)
            self._output_text_edit.setReadOnly(True)
            self.readyReadStandardOutput.connect(self._handle_stdout)
            self.readyReadStandardError.connect(self._handle_stderr)
            self.stateChanged.connect(self._handle_state_changed)
            self.new_paragraph_for_next_print = True
            self.start_time: float = 0.0
            self.stop_time: float = 0.0
            self._timer = QTimer(parent)
            self._health = NProcessPool.ProcessHealth.Unknown
            self._dispaly_health = NProcessPool.ProcessHealth.Init
            self._timer.timeout.connect(self._handle_update_timer_timeout)
            self._timer.start(1000)

        def id(self) -> int:
            return self._id

        def ignore_error(self):
            self._health = NProcessPool.ProcessHealth.NoError

        def health(self) -> "tuple[str, str]":
            """
            return (color_str, health_str)
            """
            if self._health == NProcessPool.ProcessHealth.NoError:
                return "green", "no error"
            elif self._health == NProcessPool.ProcessHealth.Error:
                return "red", "error"
            elif self._health == NProcessPool.ProcessHealth.Unknown:
                return "white", "unknown"
            elif self._health == NProcessPool.ProcessHealth.Init:
                return "white", ""
            else:
                raise ValueError(
                    f"Unsupported NProcessPool.ProcessHealth: {self._health}.")

        def pool(self) -> "NProcessPool":
            return self._pool

        def print(self, text: str, end: str = ""):
            if self.new_paragraph_for_next_print:
                self._output_text_edit.append(text+end)
                self.new_paragraph_for_next_print = False
            else:
                self._output_text_edit.moveCursor(
                    QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
                self._output_text_edit.insertPlainText(text + end)

        def output_text_edit(self) -> QTextEdit:
            return self._output_text_edit

        def show_display(self):
            label = " ".join([self.program(), *self.arguments()])
            self._display_tab_widget.addTab(self.output_text_edit(), label)
            self._display_tab_widget.setCurrentWidget(self.output_text_edit())
            self.output_text_edit().show()

        def hide_display(self):
            index = self._display_tab_widget.indexOf(self.output_text_edit())
            self._display_tab_widget.removeTab(index)
            self.output_text_edit().hide()

        def state_str(self) -> str:
            state = self.state()
            if state == QProcess.ProcessState.Running:
                state_str = "running..."
            elif state == QProcess.ProcessState.NotRunning:
                state_str = "stop"
            elif state == QProcess.ProcessState.Starting:
                state_str = "starting..."
            else:
                raise ValueError(
                    f"Unsupported QProcess.ProcessState: {state}.")
            return state_str

        def running_time(self) -> Union[float, None]:
            if self.start_time:
                if self.stop_time > self.start_time:
                    return self.stop_time-self.start_time
                else:
                    return time.time() - self.start_time

        def running_time_str(self) -> str:
            running_time = self.running_time()
            if running_time:
                day_str = str(math.floor(running_time/(24*60*60))) + "d"
                time_str = time.strftime(
                    "%H:%M:%S", time.gmtime(self.running_time()))
                return " ".join([day_str, time_str])
            else:
                return ""

        def _handle_stdout(self):
            data = self.readAllStandardOutput()
            try:
                stdout = data.data().decode("utf8")
                self.print(stdout)
            except UnicodeDecodeError as error:
                error.args += (error.args[0] +
                               f". Bytes tried to decode were: {data.data()}.",)
                raise

        def _handle_stderr(self):
            self._health = NProcessPool.ProcessHealth.Error
            data = self.readAllStandardError()
            try:
                stderr = data.data().decode("utf8")
                self.print(stderr)
            except UnicodeDecodeError as error:
                error.args += (error.args[0] +
                               f". Bytes tried to decode were: {data.data()}.",)
                raise

        def _handle_state_changed(self, state: QProcess.ProcessState):
            table = self.pool().table()
            if state == QProcess.ProcessState.Running:
                self.start_time = time.time()
                self._health = NProcessPool.ProcessHealth.NoError
                start_time_str = time.strftime(
                    "%Y/%m/%d %H:%M:%S", time.localtime(self.start_time))
                table.set_value_by_column_label(table.get_row_by_process_id(
                    self.id()), "start time", start_time_str)
                table.set_value_by_column_label(table.get_row_by_process_id(
                    self.id()), "stop time", "")
            elif state == QProcess.ProcessState.NotRunning:
                self.stop_time = time.time()
                stop_time_str = time.strftime(
                    "%Y/%m/%d %H:%M:%S", time.localtime(self.stop_time))
                table.set_value_by_column_label(table.get_row_by_process_id(
                    self.id()), "stop time", stop_time_str)
            elif state == QProcess.ProcessState.Starting:
                pass

            state_str = self.state_str()
            self.print(f"Process State: {state_str}\n")

            table.set_value_by_column_label(
                table.get_row_by_process_id(self.id()), "status", str(state_str))

        def _handle_update_timer_timeout(self):
            table = self.pool().table()
            running_time_str = self.running_time_str()
            if running_time_str:
                table.set_value_by_column_label(table.get_row_by_process_id(
                    self.id()), "running time", running_time_str)
            if not self._dispaly_health == self._health:
                color, health = self.health()
                table.set_value_by_column_label(
                    table.get_row_by_process_id(self.id()), "health", health)
                table.set_color_by_column_label(
                    table.get_row_by_process_id(self.id()), "health", color)

                self._dispaly_health = self._health

    class NProcessTextEdit(QTextEdit):
        def __init__(self, text: str, process: "NProcessPool.NProcess",  parent: QWidget):
            super().__init__(text, parent)
            self.hide()
            self._process = process

        def process(self) -> "NProcessPool.NProcess":
            return self._process

    class NProcessTableWidget(QTableWidget):
        def __init__(self, parent: QWidget, process_pool: "NProcessPool") -> None:
            super().__init__(1, 8, parent)
            self._process_pool = process_pool
            self._horizontal_labels = [
                "id", "program", "arguments", "status", "health", "start time", "running time", "stop time"]
            self._column_editable = [False, True,
                                     True, False, False, False, False, False]
            self._column_width = [60, 100, 350, 100, 100, 130, 100, 130]
            self.setHorizontalHeaderLabels(self._horizontal_labels)
            self._update_row_editable(0)
            self._set_columns_width()
            self._last_double_clicked_item_cell = (-1, -1)
            self.itemChanged.connect(self._handle_item_changed)
            self.itemDoubleClicked.connect(self._handle_item_double_clicked)

        def set_items_at_bottom(self, items: Iterable[QTableWidgetItem]):
            row_counts = self.rowCount()
            for column, item in enumerate(items):
                self.setItem(row_counts - 1, column, item)

        def set_strs_at_bottom(self, strs: Iterable[str]):
            row = self.rowCount() - 1
            for column, new_str in enumerate(strs):
                self.item(row, column).setText(str(new_str))

        def get_row_by_process_id(self, process_id: int):
            for row in range(self.rowCount()):
                if self.item(row, self._get_column_by_label("id")).text() == str(process_id):
                    return row
            all_id = ", ".join([str(process.id())
                               for process in self._process_pool.process_list()])
            raise ValueError(
                f'No row with given process_id "{process_id}" found. Id of all processes: {all_id}.')

        def setItem(self, row: int, column: int, item: QTableWidgetItem) -> None:
            super().setItem(row, column, item)

        def get_item_by_column_label(self, row: int, label: str) -> QTableWidgetItem:
            column = self._get_column_by_label(label)
            return self.item(row, column)

        def set_value_by_column_label(self, row: int, label: str, value: str):
            item = self.get_item_by_column_label(row, label)
            item.setText(str(value))

        def set_color_by_column_label(self, row: int, label: str, color: str):
            item = self.get_item_by_column_label(row, label)
            item.setBackground(QColor(color))

        def get_process_by_item(self, item: QTableWidgetItem) -> "NProcessPool.NProcess":
            current_row = item.row()
            id_str = self.item(
                current_row, self._get_column_by_label("id")).text()
            if id_str:
                process_id = int(id_str)
                return self._process_pool._get_process(process_id)
            else:
                raise ValueError("Can't get process of row item.")

        def _get_column_by_label(self, label: str) -> int:
            if not label in self._horizontal_labels:
                raise ValueError(f'Label "{label}" not in _horizontal_labels')
            return self._horizontal_labels.index(label)

        def _is_match_column_label(self, column: int, label: str) -> bool:
            if not label in self._horizontal_labels:
                raise ValueError(f'Label "{label}" not in _horizontal_labels')
            if self._horizontal_labels[column] == label:
                return True
            else:
                return False

        def _update_row_editable(self, row: int):
            for column in range(self.columnCount()):
                if not self.item(row, column):
                    self.setItem(row, column, QTableWidgetItem(""))
                if self._column_editable[column]:
                    self.item(row, column).setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsDropEnabled |
                                                    Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)
                else:
                    self.item(row, column).setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable |
                                                    Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsSelectable)

        def _set_columns_width(self):
            for column in range(self.columnCount()):
                self.setColumnWidth(column, self._column_width[column])

        def _delete_row_if_empty(self, row: int):
            if self._is_empty_row(row):
                self.removeRow(row)

        def _add_new_row_if_needed(self):
            row_count = self.rowCount()
            if not self._is_empty_row(row_count - 1):
                self.insertRow(row_count)
                for column in range(self.columnCount()):
                    new_item = QTableWidgetItem("")
                    self.setItem(row_count, column, new_item)
                self._update_row_editable(row_count)

        def _is_empty_row(self, row: int) -> bool:
            for column in range(self.columnCount()):
                if self._is_empty(self.item(row, column)):
                    pass
                else:
                    return False
            return True

        def _is_empty(self, item: Union[QTableWidgetItem, None]) -> bool:
            if item == None or item.text() == "":
                return True
            else:
                return False

        def _handle_item_changed(self, item: QTableWidgetItem):
            column = item.column()
            row = item.row()
            if not row == self.rowCount() - 1:
                self._delete_row_if_empty(row)
            else:
                self._add_new_row_if_needed()

            # Handle:
            #   1. user modifying "program" and "arguments" parameter of exist process via table;
            #   2. user adding new process via table.
            if self._last_double_clicked_item_cell == (item.row(), item.column()) == (self.currentRow(), self.currentColumn()):
                if self._column_editable[column] == True:
                    id_item = self.item(row, self._get_column_by_label("id"))
                    if not self._is_empty(id_item):  # If this is an exist process
                        id = int(id_item.text())
                        if self._is_match_column_label(column, "program"):
                            self._process_pool._get_process(
                                id).setProgram(item.text())
                        elif self._is_match_column_label(column, "arguments"):
                            try:
                                arguments = ast.literal_eval(
                                    item.text())  # Convert str to list
                                self._process_pool._get_process(
                                    id).setArguments(arguments)
                                item.setBackground(QColor("white"))
                                item.setToolTip("")
                            except SyntaxError:
                                item.setBackground(QColor("red"))
                                item.setToolTip(
                                    "Cannot convert string to list.")
                    else:  # If this is NOT an exist process
                        if self._is_match_column_label(column, "program"):
                            self._process_pool.add_process(
                                item.text(), [], item.row())
                        elif self._is_match_column_label(column, "arguments"):
                            try:
                                arguments = ast.literal_eval(
                                    item.text())  # Convert str to list
                                self._process_pool.add_process(
                                    "", arguments, item.row())
                                item.setBackground(QColor("white"))
                                item.setToolTip("")
                            except SyntaxError:
                                item.setBackground(QColor("red"))
                                item.setToolTip(
                                    "Cannot convert string to list.")
                self._last_double_clicked_item_cell = (-1, -1)

        def _handle_item_double_clicked(self, item: QTableWidgetItem):
            process = self.get_process_by_item(item)
            if process:
                process.show_display()
            self._last_double_clicked_item_cell = (
                item.row(), item.column())  # User may be editing this cell.

    def __init__(self, parent: QWidget, display_tab_widget: QTabWidget) -> None:
        """
        Displat_tab_widget is a QTabWidget where to display information about each process.
        Call table_dock() to get the dock of process table.
        """
        self._parent = parent
        self._display_tab_widget = display_tab_widget
        self._process_list: list[NProcessPool.NProcess] = []
        self._dock = QDockWidget("Process Manager", parent)
        self._dock.setMinimumWidth(200)
        self._dock.setMinimumHeight(200)
        self._table = NProcessPool.NProcessTableWidget(self._dock, self)
        self._dock.setWidget(self._table)
        self._toolbar = QToolBar("Script Server Toolbar")
        self._init_toolbar()
        setting = QSettings(ORGANIZATION_NAME, APP_NAME)
        if setting.value("process manager/load after launch") == "true":
            self.load()
            if setting.value("process manager/start after load") == "true":
                self._start_all_processes()

    def table(self) -> NProcessTableWidget:
        return self._table

    def table_dock(self) -> QDockWidget:
        return self._dock

    def toolbar(self) -> QToolBar:
        return self._toolbar

    def process_list(self) -> "list[NProcess]":
        return self._process_list

    def add_process(self, program: str, arguments: Iterable[str], row: int = -1):
        new_process = NProcessPool.NProcess(
            self._parent, self._display_tab_widget, self)
        new_process.setProgram(program)
        new_process.setArguments(arguments)
        # new_process.show_display()  # show display after init
        self._process_list.append(new_process)
        arguments_str = str(arguments)
        if row == -1:
            process_row = self.table().rowCount() - 1
        else:
            process_row = row
        self.table().set_value_by_column_label(process_row, "id", str(new_process.id()))
        self.table().set_value_by_column_label(process_row, "program", program)
        self.table().set_value_by_column_label(process_row, "arguments", arguments_str)
        self.table().set_value_by_column_label(
            process_row, "status", new_process.state_str())
        color, health = new_process.health()
        self.table().set_value_by_column_label(process_row, "health", health)
        self.table().set_color_by_column_label(process_row, "health", color)

    def remove_process(self, process: NProcess):
        process.hide_display()
        row = self.table().get_row_by_process_id(process.id())
        self._process_list.remove(process)
        self.table().removeRow(row)
        process.deleteLater()

    def save(self):
        self._save_all_processes()
        print("All processes are saved.")

    def load(self):
        result = self._load_all_processes()
        if result:
            print("Previous processes are loaded.")

    def safe_close(self):
        if QSettings(ORGANIZATION_NAME, APP_NAME).value("process manager/save before exit") == "true":
            self.save()

    def settings(self) -> "NSettingsGroupBox":
        group_box = NSettingsGroupBox("process manager")

        group_box.add_setting(
            "process manager/save before exit", "save before exit", False)
        group_box.add_setting(
            "process manager/load after launch", "load after launch", False)
        group_box.add_setting(
            "process manager/start after load", "start after load", False)

        return group_box

    def _init_toolbar(self):
        open_action = QAction("&Open", self._parent)
        open_action.setStatusTip("Open an existing file")
        open_action.triggered.connect(self._handle_open_triggered)
        self.toolbar().addAction(open_action)

        save_action = QAction("&Save", self._parent)
        save_action.triggered.connect(self._save_all_processes)
        self.toolbar().addAction(save_action)

        load_action = QAction("&Load", self._parent)
        load_action.triggered.connect(self._load_all_processes)
        self.toolbar().addAction(load_action)

        self.toolbar().addSeparator()
        label_current = QLabel("Current Process: ", self._parent)
        label_current.setToolTip(
            "action to process currently displayed in working area")
        self.toolbar().addWidget(label_current)

        start_current_action = QAction("Start", self._parent)
        start_current_action.triggered.connect(
            self._handle_start_current_triggered)
        self.toolbar().addAction(start_current_action)

        stop_current_action = QAction("Stop", self._parent)
        stop_current_action.triggered.connect(
            self._handle_stop_current_triggered)
        self.toolbar().addAction(stop_current_action)

        restart_current_action = QAction("Restart", self._parent)
        restart_current_action.triggered.connect(
            self._handle_restart_current_triggered)
        self.toolbar().addAction(restart_current_action)

        ignore_current_error_action = QAction("Ignore Error", self._parent)
        ignore_current_error_action.triggered.connect(
            self._handle_ignore_current_error_triggered)
        self.toolbar().addAction(ignore_current_error_action)

        self.toolbar().addSeparator()
        label_select = QLabel("Select Process: ", self._parent)
        label_select.setToolTip(
            "action to process currently selected in process manager")
        self.toolbar().addWidget(label_select)

        start_select_action = QAction("Start", self._parent)
        start_select_action.triggered.connect(
            self._handle_start_select_triggered)
        self.toolbar().addAction(start_select_action)

        stop_select_action = QAction("Stop", self._parent)
        stop_select_action.triggered.connect(
            self._handle_stop_select_triggered)
        self.toolbar().addAction(stop_select_action)

        restart_select_action = QAction("Restart", self._parent)
        restart_select_action.triggered.connect(
            self._handle_restart_select_triggered)
        self.toolbar().addAction(restart_select_action)

        ignore_select_error_action = QAction("Ignore Error", self._parent)
        ignore_select_error_action.triggered.connect(
            self._handle_ignore_select_error_triggered)
        self.toolbar().addAction(ignore_select_error_action)

        remove_select_action = QAction("Remove", self._parent)
        remove_select_action.triggered.connect(
            self._handle_remove_select_triggered)
        self.toolbar().addAction(remove_select_action)

        self.toolbar().addSeparator()
        label_all = QLabel("All Processes: ", self._parent)
        label_all.setToolTip("action to all processes")
        self.toolbar().addWidget(label_all)

        start_all_action = QAction("Start", self._parent)
        start_all_action.triggered.connect(self._handle_start_all_triggered)
        self.toolbar().addAction(start_all_action)

        stop_all_action = QAction("Stop", self._parent)
        stop_all_action.triggered.connect(self._handle_stop_all_triggered)
        self.toolbar().addAction(stop_all_action)

        restart_all_action = QAction("Restart", self._parent)
        restart_all_action.triggered.connect(
            self._handle_restart_all_triggered)
        self.toolbar().addAction(restart_all_action)

        ignore_all_error_action = QAction("Ignore Error", self._parent)
        ignore_all_error_action.triggered.connect(
            self._handle_ignore_all_error_triggered)
        self.toolbar().addAction(ignore_all_error_action)

    def _get_process(self, id: int) -> NProcess:
        for process in self.process_list():
            if process.id() == id:
                return process
        else:
            raise ValueError("No process has id {id}.")

    def _start_all_processes(self):
        for process in self.process_list():
            process.start()

    def _handle_update_timer_timeout(self):
        for process in self.process_list():
            running_time_str = process.running_time_str()
            if running_time_str:
                self.table().set_value_by_column_label(self.table().get_row_by_process_id(
                    process.id()), "running time", running_time_str)

    def _handle_open_triggered(self):
        file_name = QFileDialog.getOpenFileName(
            self._parent, "Open scripts", "./", "Python Scripts (*.py)")
        if file_name[0]:
            self.add_process("python", [file_name[0]])

    def _save_all_processes(self):
        processes_info = [(process.program(), process.arguments())
                          for process in self.process_list()]
        QSettings(ORGANIZATION_NAME, APP_NAME).setValue(
            "process manager/processes info", processes_info)

    def _load_all_processes(self) -> bool:
        processes_info = QSettings(ORGANIZATION_NAME, APP_NAME).value(
            "process manager/processes info")
        for process in self.process_list().copy():
            self.remove_process(process)
        if processes_info:
            for program, arguments in processes_info:
                self.add_process(program, arguments)
            return True
        else:
            return False

    def _handle_start_current_triggered(self):
        current_widget = self._display_tab_widget.currentWidget()
        if isinstance(current_widget, NProcessPool.NProcessTextEdit):
            current_widget.process().start()

    def _handle_stop_current_triggered(self):
        current_widget = self._display_tab_widget.currentWidget()
        if isinstance(current_widget, NProcessPool.NProcessTextEdit):
            current_widget.process().kill()

    def _handle_restart_current_triggered(self):
        current_widget = self._display_tab_widget.currentWidget()
        if isinstance(current_widget, NProcessPool.NProcessTextEdit):
            current_widget.process().kill()
            current_widget.process().waitForFinished(30000)
            current_widget.process().start()

    def _handle_ignore_current_error_triggered(self):
        current_widget = self._display_tab_widget.currentWidget()
        if isinstance(current_widget, NProcessPool.NProcessTextEdit):
            current_widget.process().ignore_error()

    def _handle_start_select_triggered(self):
        current_process = self.table().get_process_by_item(self.table().currentItem())
        if current_process:
            current_process.start()

    def _handle_stop_select_triggered(self):
        current_process = self.table().get_process_by_item(self.table().currentItem())
        if current_process:
            current_process.kill()

    def _handle_restart_select_triggered(self):
        current_process = self.table().get_process_by_item(self.table().currentItem())
        if current_process:
            current_process.kill()
            current_process.waitForFinished(30000)
            current_process.start()

    def _handle_ignore_select_error_triggered(self):
        current_process = self.table().get_process_by_item(self.table().currentItem())
        if current_process:
            current_process.ignore_error()

    def _handle_remove_select_triggered(self):
        current_process = self.table().get_process_by_item(self.table().currentItem())
        if current_process:
            self.remove_process(current_process)

    def _handle_start_all_triggered(self):
        self._start_all_processes()

    def _handle_stop_all_triggered(self):
        for process in self.process_list():
            process.kill()

    def _handle_restart_all_triggered(self):
        for process in self.process_list():
            process.kill()
            process.waitForFinished(30000)
            process.start()

    def _handle_ignore_all_error_triggered(self):
        for process in self.process_list():
            process.ignore_error()


class NSettingsGroupBox(QGroupBox):
    def __init__(self, title: str, parent: Union[QWidget, None] = ..., setting: Union[QSettings, None] = ...):
        if not isinstance(parent, QWidget):
            super().__init__(title)
        else:
            super().__init__(title, parent)
        if not isinstance(setting, QSettings):
            setting = QSettings(ORGANIZATION_NAME, APP_NAME)
        self._setting = setting

        self._box_layout = QVBoxLayout(self)
        self.setLayout(self._box_layout)

        self._settings_area = QWidget()
        self._box_layout.addWidget(self._settings_area)
        self._settings_layout = QFormLayout(self._settings_area)
        self._settings_area.setLayout(self._settings_layout)
        self._setting_list = []

        self._init_button()
        self._is_setting_changed = False

    def add_setting(self, key: str, label: str, default_value: Union[bool, str, int], type_hint: Union[type, None] = ...):

        value = self._setting.value(key)

        if value == None:
            value = default_value
            self._setting.setValue(key, value)
        if isinstance(value, str):
            if value == "false" or value == "true":
                widget = QCheckBox(self)
                if value == "false":
                    widget.setChecked(False)
                else:
                    widget.setChecked(True)
                widget.stateChanged.connect(self._handle_anything_changed)
            else:
                widget = QLineEdit(value, self)
                widget.textChanged.connect(self._handle_anything_changed)
            self._add_row(label, widget)
        elif isinstance(value, bool):
            widget = QCheckBox(self)
            widget.setChecked(value)
            widget.stateChanged.connect(self._handle_anything_changed)
            self._add_row(label, widget)
        elif isinstance(value, int):
            widget = QSpinBox(self)
            if value:
                widget.setValue(value)
            widget.valueChanged.connect(self._handle_anything_changed)
            self._add_row(label, widget)
        else:
            raise TypeError(f"Type {type(value)} is not yet supported.")
        self._setting_list.append(
            {"key": key, "label": label, "widget": widget, "default value": default_value})

    def _set_setting(self, widget: Union[QCheckBox, QLineEdit, QSpinBox], value: Union[bool, str, int, None]):
        if value == None:
            return
        if isinstance(widget, QCheckBox):
            if isinstance(value, bool):
                pass
            elif isinstance(value, str):
                if value == "true":
                    value = True
                elif value == "false":
                    value = False
                else:
                    raise ValueError(f"Can't convert str {value} to bool literally,\
                                    so it can't be set to {type(widget)}.")
            else:
                raise ValueError(f"Cannt set {type(value)} to {type(widget)}.")
            widget.setChecked(value)
        elif isinstance(widget, QLineEdit):
            assert isinstance(value, str)
            widget.setText(value)
        else:
            assert isinstance(value, int)
            widget.setValue(value)

    def _get_setting(self, widget: Union[QCheckBox, QLineEdit, QSpinBox]) -> Union[bool, str, int]:
        if isinstance(widget, QCheckBox):
            if widget.isChecked():
                return True
            else:
                return False
        elif isinstance(widget, QLineEdit):
            return widget.text()
        else:
            return widget.value()

    def _init_button(self):
        self._button_area = QWidget()
        self._box_layout.addWidget(self._button_area)
        self._button_layout = QHBoxLayout(self._button_area)
        self._button_area.setLayout(self._button_layout)

        save_button = QPushButton("save", self._button_area)
        self._save_button = save_button
        save_button.pressed.connect(self._handle_save_button_pressed)
        self._button_layout.addWidget(save_button)

        cancel_button = QPushButton("cancel", self._button_area)
        self._cancel_button = cancel_button
        cancel_button.pressed.connect(self._handle_cancel_button_pressed)
        self._button_layout.addWidget(cancel_button)

        default_button = QPushButton("default", self._button_area)
        self._default_button = default_button
        default_button.pressed.connect(self._handle_default_button_pressed)
        self._button_layout.addWidget(default_button)

        self._save_button.setEnabled(False)
        self._cancel_button.setEnabled(False)

    def _add_row(self, label: str, field: QWidget):
        self._settings_layout.addRow(label, field)

    def _handle_save_button_pressed(self):
        for setting in self._setting_list:
            key = setting["key"]
            value = self._get_setting(setting["widget"])
            self._setting.setValue(key, value)

        self._is_setting_changed = False
        self._save_button.setEnabled(False)
        self._cancel_button.setEnabled(False)

        # If there are needs when parent class is expected to applied settings at once,
        # parent should have a method like reload_setting(). Relavant logic should also
        # be added here.

    def _handle_cancel_button_pressed(self):
        for setting in self._setting_list:
            key = setting["key"]
            widget = setting["widget"]
            value = self._setting.value(key)
            self._set_setting(widget, value)

        self._is_setting_changed = False
        self._save_button.setEnabled(False)
        self._cancel_button.setEnabled(False)

    def _handle_default_button_pressed(self):
        for setting in self._setting_list:
            widget = setting["widget"]
            value = setting["default value"]
            self._set_setting(widget, value)

    def _handle_anything_changed(self):
        self._is_setting_changed = True
        self._save_button.setEnabled(True)
        self._cancel_button.setEnabled(True)


class NSettingsPanel():
    def __init__(self, parent: QWidget) -> None:
        self._parent = parent
        self._dock = QDockWidget("Settings", parent)
        self._dock.setMinimumWidth(200)
        self._dock.setMinimumHeight(200)

        self._panel = QWidget(self._dock)
        self._panel_layout = QVBoxLayout(self._panel)
        self._panel.setLayout(self._panel_layout)
        self._dock.setWidget(self._panel)

        # uncomment this to see settings demo
        # self.register(self.demo_settings())

    def dock(self) -> QDockWidget:
        return self._dock

    def demo_settings(self) -> NSettingsGroupBox:
        group_box = NSettingsGroupBox("demo settings")

        group_box.add_setting("settings demo/movie", "movie", "Star Trek I")
        group_box.add_setting("settings demo/volume", "volumn", 27)
        group_box.add_setting("settings demo/mute", "mute", False)
        group_box.add_setting("settings demo/scale", "scale", 1)

        return group_box

    def register(self, setting_group: NSettingsGroupBox):
        self._panel_layout.addWidget(setting_group)


def main():
    app = QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec())


main()
