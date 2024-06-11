import os
import sys
import threading
import traceback
from datetime import datetime

import PyPDF2
import docx
from PyQt5.QtWidgets import QApplication

from config.config_manager import ConfigManager
from views import *
from utils import *


class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow(self)
        self.text_processor = TextProcessor()
        self.search_engine = DuckDuckGoSearch()
        self.search_result_processor = SearchResultProcessor()
        self.config_manager = ConfigManager()
        self.report_generator = ReportGenerator()
        self.init_app_settings()

    def init_app_settings(self):
        config = self.config_manager.read_config()
        self.view.settings_entry_save_path.setText(config.get("path_to_save"))

    def update_settings(self, path_to_save=''):
        self.config_manager.write_config(path_to_save)

    def read_pdf(self):
        file_path = self.view.entry_pdf.text()
        if not os.path.exists(file_path):
            self.view.update_info_label("Path doesn't exist", 'red')
            return
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.get_sentences(text, file_name)

    def read_docx(self):
        file_path = self.view.entry_docx.text()
        if not os.path.exists(file_path):
            self.view.update_info_label("Path doesn't exist", 'red')
            return
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.get_sentences(text, file_name)

    def read_text(self):
        text = self.view.entry_text.toPlainText().strip() + '.'
        self.get_sentences(text)

    def get_sentences(self, text, filename='entered_text'):
        self.view.update_progress_bar()
        self.view.update_start_button(False)
        sentences = self.text_processor.get_sentences(text)
        try:
            thread = threading.Thread(target=self.search_plagiat, args=(sentences, filename))
            thread.start()
        except Exception as e:
            print("An error occurred:", e)
            print("Full traceback:")
            traceback.print_exc()

    def search_plagiat(self, sentences, filename):
        found_plagiarism = []
        sentences_count = len(sentences)
        current_sentence = 1
        for sentence in sentences:
            try:
                results = self.search_engine.search(sentence)
            except Exception as e:
                print("An error occurred:", e)
                print("Full traceback:")
                traceback.print_exc()
                results = None
            if results is not None:
                plagiarism_case = self.search_result_processor.get_plagiarism_case(results, sentence)
                if plagiarism_case is not None:
                    found_plagiarism.append(plagiarism_case)
                self.view.update_progress_bar(self.calculate_progress_percentage(sentences_count, current_sentence))
                current_sentence += 1
        self.process_search_result(found_plagiarism, sentences_count, filename)
        self.view.update_info_label("Done")
        self.view.update_start_button(True)

    @staticmethod
    def calculate_progress_percentage(sentences_count, current_sentence):
        return int((current_sentence/sentences_count) * 100)

    def process_search_result(self, found_plagiarism, sentences_count, filename):
        plagiarism_percentages = self.search_result_processor.get_report_data(found_plagiarism, sentences_count)
        self.generate_report(found_plagiarism, plagiarism_percentages, filename)

    def generate_report(self, found_plagiarism, plagiarism_percentages, filename):
        save_path = self.config_manager.read_config().get("path_to_save")
        self.report_generator.generate_document(found_plagiarism, plagiarism_percentages, filename, save_path)

    def run(self):
        self.view.show()
        self.app.exec()
