import main
import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo

class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title('DnD Converter')
        self.geometry('300x50')

        self.build_interface()

    def build_interface(self):
        pass


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()