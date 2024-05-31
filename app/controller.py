import sys
from difflib import SequenceMatcher

import PyPDF2
import docx
from PyQt5.QtWidgets import QApplication

from app.models.plagiarism_case import PlagiarismCase
from app.config.config_manager import ConfigManager
from views import *
from utils import *


class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow(self)
        self.text_processor = TextProcessor()
        self.search_engine = GoogleSearch()
        self.search_result_processor = SearchResultProcessor()
        self.config_manager = ConfigManager()
        self.init_app_settings()

    def init_app_settings(self):
        config = self.config_manager.read_config()
        self.view.settings_entry_save_path.setText(config.get("path_to_save"))

    def update_settings(self, path_to_save=''):
        self.config_manager.write_config(path_to_save)

    def read_pdf(self):
        file_path = self.view.entry_pdf.text()
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        print("===================Original===================\n\n\n")
        print(text)
        self.get_sentences(text)

    def read_docx(self):
        file_path = self.view.entry_docx.text()
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        print("===================Original===================\n\n\n")
        print(text)
        self.get_sentences(text)

    def read_text(self):
        text = self.view.entry_text.toPlainText().strip() + '.'
        print("===================Original===================\n\n\n")
        print(text)
        self.get_sentences(text)

    def get_sentences(self, text):
        sentences = self.text_processor.get_sentences(text)
        print("\n\n\n===================Cleaned sentences===================\n\n\n")
        print(sentences)
        self.search_plagiat(sentences)

    def search_plagiat(self, sentences):
        found_plagiarism = []
        for sentence in sentences:
            results = self.search_engine.search(sentence)
            if results != 0:
                max_percentage = 0
                max_result = {}
                for result in results:
                    if result.get('snippet'):
                        search_text = self.text_processor.get_cleaned_text(result.get('snippet'))
                        percentage = SequenceMatcher(None, search_text, sentence).ratio()
                        if max_percentage < percentage:
                            max_percentage = percentage
                            max_result = result
                if max_percentage > 0.5:
                    found_plagiarism.append(PlagiarismCase(sentence, max_percentage, max_result.get('link')))

                    # found_plagiarism.append({"sentence": sentence,
                    #                          "plagiarism_rate": max_percentage,
                    #                          "link": max_result.get('link')})

                print("\n")
                print(sentence)
                print(max_result.get('link'))
                print(self.text_processor.get_cleaned_text(max_result.get('snippet')))
                print(f"{max_percentage * 100:.2f}%")
                print("\n")
        self.process_search_result(found_plagiarism, len(sentences))

    def process_search_result(self, found_plagiarism, sentences_count):
        self.search_result_processor.get_report_data(found_plagiarism, sentences_count)

    def run(self):
        # self.view.mainloop()
        self.view.show()
        self.app.exec()





