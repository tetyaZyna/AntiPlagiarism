import tkinter
from tkinter import filedialog
from difflib import SequenceMatcher

import PyPDF2

from views import MainWindow
from utils import TextProcessor
from utils import GoogleSearch


class MainController:
    def __init__(self):
        self.view = MainWindow(self)
        self.search_engine = GoogleSearch()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.view.entry_1.delete(0, tkinter.END)
        self.view.entry_1.insert(0, file_path)
        self.view.entry_1.config(foreground='black')

    def read_pdf(self):
        file_path = self.view.entry_1.get()
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        # print("===================Original===================\n\n\n")
        # print(text)
        self.get_sentences(text)

    def get_sentences(self, text):
        text_processor = TextProcessor(text)
        sentences = text_processor.get_sentences()
        # print("\n\n\n===================Cleaned sentences===================\n\n\n")
        # print(sentences)
        self.search_plagiat(sentences)

    def search_plagiat(self, sentences):
        for sentence in sentences:
            results = self.search_engine.search(sentence)
            if results != 0:
                max_percentage = 0
                max_result = {}
                for result in results:
                    if result.get('snippet'):
                        search_text = TextProcessor(result.get('snippet')).get_cleaned_text()
                        percentage = SequenceMatcher(None, search_text, sentence).ratio() * 100
                        if max_percentage < percentage:
                            max_percentage = percentage
                            max_result = result
                print("\n")
                print(sentence)
                print(max_result.get('link'))
                print(max_result.get('snippet').get_cleaned_text())
                print(f"{max_percentage:.2f}%")
                print("\n")

    def run(self):
        self.view.mainloop()
