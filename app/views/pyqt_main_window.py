from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.info_label = None
        self.progressBar = None
        self.input_prompt_text = "Введіть або виберіть шлях до файлу"
        self.controller = controller
        self.setWindowTitle("AntiPlagiat")
        self.setMinimumSize(550, 340)
        self.setGeometry(0, 0, 550, 340)
        self._move_to_center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.main_widget = QWidget()
        self.settings_widget = QWidget()

        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.settings_widget)

        self._fill_main_page()
        self._fill_settings_page()

    def _fill_main_page(self):
        label_1 = QLabel("Завантажте файл або введіть текст\n для початку аналізу")
        label_1.setFont(QFont("Open Sans", 14))
        label_1.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(label_1)

        self.tab_widget = QTabWidget(self)
        self.main_layout.addWidget(self.tab_widget)
        self._create_tabs()
        self.tab_widget.currentChanged.connect(self.tab_changed)

        control_button_layout = QHBoxLayout()
        self.main_layout.addLayout(control_button_layout)

        self.start_button = QPushButton("Почати аналіз")
        self.start_button.clicked.connect(self._start_analysis)
        self.start_button.setEnabled(False)
        control_button_layout.addWidget(self.start_button)

        settings_button = QPushButton()
        settings_button.clicked.connect(self._open_settings)
        settings_button.setIcon(QIcon("views/icons/settings.ico"))
        settings_button.setFixedWidth(30)
        control_button_layout.addWidget(settings_button)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(separator)

        self.status_bar = self.statusBar()
        self.main_layout.addWidget(self.status_bar)

    def _fill_settings_page(self):
        settings_field_layout = QVBoxLayout()
        self.settings_layout.addLayout(settings_field_layout)

        section_label_1 = QLabel("Місце зберігання файлів звітів")
        section_label_1.setStyleSheet("font-weight: bold; font-size: 16px;")
        section_label_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        settings_field_layout.addWidget(section_label_1)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        settings_field_layout.addWidget(separator)

        save_place_setting_layout = QHBoxLayout()
        settings_field_layout.addLayout(save_place_setting_layout)

        self.settings_entry_save_path = QLineEdit()
        self.settings_entry_save_path.setPlaceholderText("Введіть або виберіть шлях")
        save_place_setting_layout.addWidget(self.settings_entry_save_path)

        button_1 = QPushButton("Обрати")
        button_1.clicked.connect(self._path_select)
        save_place_setting_layout.addWidget(button_1)

        spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        settings_field_layout.addItem(spacer)

        control_button_layout = QHBoxLayout()
        self.settings_layout.addLayout(control_button_layout)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        control_button_layout.addItem(spacer)

        cancel_button = QPushButton("Скасувати")
        cancel_button.clicked.connect(self._cancel)
        cancel_button.setFixedWidth(100)
        control_button_layout.addWidget(cancel_button)

        save_button = QPushButton("Зберегти")
        save_button.setDefault(True)
        save_button.clicked.connect(self._save_settings)
        save_button.setFixedWidth(100)
        control_button_layout.addWidget(save_button)

    def _create_tabs(self):
        tab_pdf = QWidget()
        tab_docx = QWidget()
        tab_text = QWidget()

        self.tab_widget.addTab(tab_pdf, "PDF")
        self.tab_widget.addTab(tab_docx, "DOCX")
        self.tab_widget.addTab(tab_text, "Text")

        self._fill_tab_pdf(tab_pdf)
        self._fill_tab_docx(tab_docx)
        self._fill_tab_text(tab_text)

    def _fill_tab_pdf(self, tab):
        input_layout_pdf = QHBoxLayout(tab)

        self.entry_pdf = QLineEdit(tab)
        self.entry_pdf.setPlaceholderText(self.input_prompt_text)
        self.entry_pdf.textChanged.connect(self.check_empty)
        input_layout_pdf.addWidget(self.entry_pdf)

        button = QPushButton("Обрати файл", tab)
        button.clicked.connect(self._select_file_pdf)
        input_layout_pdf.addWidget(button)

    def _fill_tab_docx(self, tab):
        input_layout_docx = QHBoxLayout(tab)

        self.entry_docx = QLineEdit(tab)
        self.entry_docx.setPlaceholderText(self.input_prompt_text)
        self.entry_docx.textChanged.connect(self.check_empty)
        input_layout_docx.addWidget(self.entry_docx)

        button_1 = QPushButton("Обрати файл", tab)
        button_1.clicked.connect(self._select_file_docx)
        input_layout_docx.addWidget(button_1)

    def _fill_tab_text(self, tab):
        input_layout_text = QHBoxLayout(tab)
        self.entry_text = QPlainTextEdit(tab)
        self.entry_text.textChanged.connect(self.check_empty)
        input_layout_text.addWidget(self.entry_text)

    @pyqtSlot(int)
    def tab_changed(self, index):
        if index == 0:
            self.update_start_button(self.entry_pdf.text().strip() != "")
        elif index == 1:
            self.update_start_button(self.entry_docx.text().strip() != "")
        elif index == 2:
            self.update_start_button(self.entry_text.toPlainText().strip() != "")

    @pyqtSlot()
    def check_empty(self):
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            self.update_start_button(self.entry_pdf.text().strip() != "")
        elif current_tab == 1:
            self.update_start_button(self.entry_docx.text().strip() != "")
        elif current_tab == 2:
            self.update_start_button(self.entry_text.toPlainText().strip() != "")

    def _start_analysis(self):
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            self.controller.read_pdf()
        elif current_tab == 1:
            self.controller.read_docx()
        elif current_tab == 2:
            self.controller.read_text()

    def _select_file_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Обрати файл", "", "PDF files (*.pdf)")
        if file_path:
            self.entry_pdf.setText(file_path)
            self.update_start_button(True)

    def _select_file_docx(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Обрати файл", "", "DOCX files (*.docx)")
        if file_path:
            self.entry_docx.setText(file_path)
            self.update_start_button(True)

    def update_start_button(self, enabled):
        self.start_button.setEnabled(enabled)

    def _path_select(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Обрати папку", "")
        if folder_path:
            self.settings_entry_save_path.setText(folder_path)

    def _open_settings(self):
        self.controller.init_app_settings()
        self.stacked_widget.setCurrentIndex(1)

    def _cancel(self):
        self.stacked_widget.setCurrentIndex(0)

    def _save_settings(self):
        self.controller.update_settings(self.settings_entry_save_path.text())
        self.stacked_widget.setCurrentIndex(0)

    def _move_to_center(self):
        window_rect = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_rect.moveCenter(screen_center)
        self.move(window_rect.topLeft())

    def start_progress_bar(self):
        self.clear_status_bar()
        self.progressBar = QProgressBar(self)
        self.progressBar.setFixedHeight(20)
        self.status_bar.addWidget(self.progressBar)
        self.progressBar.setValue(0)

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)
        if value >= 100:
            self._remove_progress_bar()

    def add_info_label(self, text, color='green'):
        self.clear_status_bar()
        self.info_label = QLabel(self)
        self.info_label.setText(text)
        self.info_label.setFixedHeight(20)
        self.info_label.setStyleSheet(f"color: {color};")
        self.status_bar.addWidget(self.info_label)

    def _remove_progress_bar(self):
        if self.progressBar is not None:
            self.status_bar.removeWidget(self.progressBar)
            self.progressBar.deleteLater()
            self.progressBar = None

    def _remove_info_label(self):
        if self.info_label is not None:
            self.status_bar.removeWidget(self.info_label)
            self.info_label.deleteLater()
            self.info_label = None

    def clear_status_bar(self):
        self._remove_info_label()
        self._remove_progress_bar()
