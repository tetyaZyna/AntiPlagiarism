import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.entry_text = None
        self.entry_pdf = None
        self.entry_docx = None
        self.input_prompt_text = "Введіть або виберіть шлях до файлу"
        self.controller = controller
        self.title("AntiPlagiat")
        self.geometry("500x340+0+0")
        self.minsize(width=500, height=340)
        self.resizable(width=False, height=False)

        self.label_1 = ttk.Label(self, text="Завантажте файл або введіть текст\n для початку аналізу",
                                 font="{Open Sans} 14 {}", anchor="center", justify="center")
        self.label_1.pack(ipadx=12, pady=30, anchor='n')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        self.create_tabs()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.start_button = ttk.Button(self, text="Почати аналіз", command=controller.read_pdf)
        self.start_button.pack(side=tk.RIGHT, anchor=tk.SE, padx=20, pady=20)

        # # Створення бокового меню
        # self.treeview = ttk.Treeview(self)
        # self.treeview.pack(side="left", fill="y")
        #
        # # Додавання елементів у бокове меню
        # self.treeview.insert("", "end", text="Елемент 1")
        # self.treeview.insert("", "end", text="Елемент 2")
        # self.treeview.insert("", "end", text="Елемент 3")
        #
        # # Прив'язка події до вибору елемента в боковому меню
        # self.treeview.bind("<<TreeviewSelect>>", self.on_item_selected)

    def create_tabs(self):
        tab_pdf = ttk.Frame(self.notebook)
        tab_docx = ttk.Frame(self.notebook)
        tab_text = ttk.Frame(self.notebook)

        self.notebook.add(tab_pdf, text="PDF")
        self.notebook.add(tab_docx, text="DOCX")
        self.notebook.add(tab_text, text="Text")

        self.fill_tab_pdf(tab_pdf)
        self.fill_tab_docx(tab_docx)
        self.fill_tab_text(tab_text)

    def fill_tab_pdf(self, tab):
        input_frame_pdf = ttk.Frame(tab)
        input_frame_pdf.pack(anchor="center", pady=20)

        self.entry_pdf = ttk.Entry(input_frame_pdf, foreground='grey', width=50)
        self.entry_pdf.pack(side='left', padx=(0, 10))
        self.entry_pdf.insert(0, self.input_prompt_text)
        self.entry_pdf.bind("<FocusIn>", self.on_focus_in)
        self.entry_pdf.bind("<FocusOut>", self.on_focus_out)

        button = ttk.Button(input_frame_pdf, text="Обрати файл", command=self.select_file_pdf)
        button.pack(side='left')

    def fill_tab_docx(self, tab):
        input_frame_docx = ttk.Frame(tab)
        input_frame_docx.pack(anchor="center", pady=20)

        self.entry_docx = ttk.Entry(input_frame_docx, foreground='grey', width=50)
        self.entry_docx.pack(side='left', padx=(0, 10))
        self.entry_docx.insert(0, self.input_prompt_text)
        self.entry_docx.bind("<FocusIn>", self.on_focus_in)
        self.entry_docx.bind("<FocusOut>", self.on_focus_out)

        button_1 = ttk.Button(input_frame_docx, text="Обрати файл", command=self.select_file_docx)
        button_1.pack(side='left')

    def fill_tab_text(self, tab):
        input_frame_text = ttk.Frame(tab)
        input_frame_text.pack(anchor="center", pady=10)

        self.entry_text = tk.Text(input_frame_text, height=6, width=40)
        self.entry_text.pack(side='left')
        scroll_bar = tk.Scrollbar(input_frame_text, command=self.entry_text.yview)
        scroll_bar.pack(side="right", fill="y")
        self.entry_text.config(yscrollcommand=scroll_bar.set)

    def on_tab_change(self, event):
        current_tab = self.notebook.index("current")
        if current_tab == 0:
            self.start_button.config(command=self.controller.read_pdf)
        if current_tab == 1:
            self.start_button.config(command=self.controller.read_docx)
        if current_tab == 2:
            self.start_button.config(command=self.controller.read_text)

    def on_focus_in(self, event):
        if self.entry_pdf.get() == self.input_prompt_text:
            self.entry_pdf.delete(0, tk.END)
            self.entry_pdf.config(foreground='black')
        if self.entry_docx.get() == self.input_prompt_text:
            self.entry_docx.delete(0, tk.END)
            self.entry_docx.config(foreground='black')

    def on_focus_out(self, event):
        if self.entry_pdf.get() == '':
            self.entry_pdf.insert(0, self.input_prompt_text)
            self.entry_pdf.config(foreground='grey')
        if self.entry_docx.get() == '':
            self.entry_docx.insert(0, self.input_prompt_text)
            self.entry_docx.config(foreground='grey')

    def select_file_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.entry_pdf.delete(0, tk.END)
        self.entry_pdf.insert(0, file_path)
        self.entry_pdf.config(foreground='black')

    def select_file_docx(self):
        file_path = filedialog.askopenfilename(filetypes=[("DOCX files", "*.docx")])
        self.entry_docx.delete(0, tk.END)
        self.entry_docx.insert(0, file_path)
        self.entry_docx.config(foreground='black')

    # def on_item_selected(self, event):
    #     item = self.treeview.focus()  # Отримання вибраного елемента
    #     if item:  # Перевірка, чи був вибраний елемент
    #         print("Вибрано:", self.treeview.item(item, "text"))  # Виведення тексту вибраного елемента

