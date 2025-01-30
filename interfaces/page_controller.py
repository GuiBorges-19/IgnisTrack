import tkinter as tk
from tkinter import ttk

class PageController:
    def __init__(self, parent):
        self.parent = parent
        self.pages = {}
        
    def add_page(self, page_name, page_instance):
        self.pages[page_name] = page_instance
        page_instance.grid(row=0, column=0, sticky="nsew")
        page_instance.grid_remove()

    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_remove()
        self.pages[page_name].grid()
        