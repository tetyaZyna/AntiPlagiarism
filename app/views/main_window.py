import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("AntiPlagiat")
        self.geometry("500x300+0+0")
        self.minsize(width=500, height=300)
        self.resizable(width=False, height=False)

        self.label_1 = ttk.Label(self, text="Завантажте файл для початку аналізу", font="{Open Sans} 14 {}",
                                 anchor="center")
        self.label_1.pack(ipadx=12, pady=40, anchor='n')

        self.horizontal_panedwindow_1 = ttk.Panedwindow(self, orient="horizontal")
        self.horizontal_panedwindow_1.pack()

        self.frame_1 = tk.Frame(self.horizontal_panedwindow_1)
        self.horizontal_panedwindow_1.add(self.frame_1)

        self.placeholder_text = "Введіть або виберіть шлях до файлу"
        self.entry_1 = ttk.Entry(self.frame_1, foreground='grey', width=50)
        self.entry_1.grid(row=0, column=0, sticky='ew')
        self.entry_1.insert(0, self.placeholder_text)
        self.entry_1.bind("<FocusIn>", self.on_focus_in)
        self.entry_1.bind("<FocusOut>", self.on_focus_out)

        self.button_1 = ttk.Button(self.frame_1, text="Обрати файл", command=controller.select_file)
        self.button_1.grid(row=0, column=1, padx=5)

        self.button_2 = ttk.Button(self, text="Почати аналіз", command=controller.read_pdf)
        self.button_2.pack(side=tk.RIGHT, anchor=tk.SE, padx=20, pady=20)

    def on_focus_in(self):
        if self.entry_1.get() == self.placeholder_text:
            self.entry_1.delete(0, tk.END)
            self.entry_1.config(foreground='black')

    def on_focus_out(self):
        if self.entry_1.get() == "":
            self.entry_1.insert(0, self.placeholder_text)
            self.entry_1.config(foreground='grey')
