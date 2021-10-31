import main
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo

class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title('DnD Converter')
        self.geometry('300x150')

        s = ttk.Style()
        s.theme_use('vista')
        print(s.theme_use())

        self.build_interface()

    def build_interface(self):
        self.input_file = tkinter.StringVar()
        self.output_file = tkinter.StringVar()

        self.input_frame = tkinter.LabelFrame(self, text='Input file')
        self.input_frame.grid(row=0, column=0, padx=2, pady=(2,0))

        self.input_box = ttk.Entry(self.input_frame, textvariable=self.input_file)
        self.input_box.grid(row=0, column=0, padx=2, pady=(2,0))

        self.input_browse_button = ttk.Button(self.input_frame, 
            text='Browse...', 
            command=lambda: self.input_file.set(filedialog.askopenfilename(filetypes=[("eXtensible Markup Language", "*.xml")])))
        self.input_browse_button.grid(row=0, column=1, padx=2, pady=(2,0))

        self.output_frame = tkinter.LabelFrame(self, text='Output file')
        self.output_frame.grid(row=1, column=0, padx=2, pady=(2,0))

        self.output_box = ttk.Entry(self.output_frame, textvariable=self.output_file)
        self.output_box.grid(row=0, column=0, padx=2, pady=(2,0))

        self.output_browse_button = ttk.Button(self.output_frame, 
            text='Browse...', 
            command=lambda: self.output_file.set(filedialog.asksaveasfilename(filetypes=[("Comma-separated values", "*.csv")])))
        self.output_browse_button.grid(row=0, column=1, padx=2, pady=(2,0))

        self.convert_button = ttk.Button(self, text='Convert', command=self.convert_command)
        self.convert_button.grid(row=2, column=0, padx=2, pady=5)

    def convert_command(self):
        main.convert_xml_to_csv(self.input_file.get(), self.output_file.get())


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()