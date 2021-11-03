"""Manage the GUI portion of the application"""
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import main


class GUI(tkinter.Tk):
    """GUI manager"""

    #pylint: disable=too-many-instance-attributes
    #The amount of instance attributes are reasonable

    def __init__(self):
        super().__init__()

        self.title('DnD Converter')
        self.geometry('295x150')
        self.iconbitmap('dnd-icon-22.ico')

        style = ttk.Style()
        style.theme_use('vista')

        self.build_interface()

    def build_interface(self):
        """Logic for building the graphical interface"""
        self.input_file = tkinter.StringVar()
        self.output_file = tkinter.StringVar()
        self.statusbar_text = tkinter.StringVar()

        self.reset_status_bar()

        self.input_frame = tkinter.LabelFrame(self, text='Input file')
        self.input_frame.grid(row=0, column=0, padx=2, pady=(2, 0))

        self.input_box = ttk.Entry(
            self.input_frame,
            width=33,
            textvariable=self.input_file
        )
        self.input_box.grid(row=0, column=0, padx=2, pady=(2, 0))

        self.input_browse_button = ttk.Button(
            self.input_frame,
            text='Browse...',
            command=lambda: self.input_file.set(
                filedialog.askopenfilename(
                    filetypes=[("eXtensible Markup Language", "*.xml")]
                )
            )
        )
        self.input_browse_button.grid(row=0, column=1, padx=2, pady=(2, 0))

        self.output_frame = tkinter.LabelFrame(self, text='Output file')
        self.output_frame.grid(row=1, column=0, padx=2, pady=(2, 0))

        self.output_box = ttk.Entry(
            self.output_frame,
            width=33,
            textvariable=self.output_file
        )
        self.output_box.grid(row=0, column=0, padx=2, pady=(2, 0))

        self.output_browse_button = ttk.Button(
            self.output_frame,
            text='Browse...',
            command=lambda: self.output_file.set(
                filedialog.asksaveasfilename(
                    filetypes=[("Comma-separated values", "*.csv")]
                )
            )
        )
        self.output_browse_button.grid(row=0, column=1, padx=2, pady=(2, 0))

        self.convert_button = ttk.Button(
            self,
            text='Convert',
            command=self.convert_command
        )
        self.convert_button.grid(row=2, column=0, padx=2, pady=5)

        self.statusbar = tkinter.Label(
            self,
            textvariable=self.statusbar_text,
            bd=1,
            relief=tkinter.SUNKEN,
            anchor=tkinter.W
        )
        self.statusbar.grid(row=3, column=0, columnspan=2, sticky='sew')

    def convert_command(self):
        """Trigger the conversion from XML to CSV"""
        self.statusbar_text.set("Converting...")
        try:
            items = main.convert_xml_to_csv(
                self.input_file.get(),
                self.output_file.get()
                )
            self.statusbar_text.set(f"Done! Converted {items} items.")
        except AttributeError as atribute_error:
            messagebox.showerror(title='Exception!', message=atribute_error)
            self.statusbar_text.set('Exception!')
        except FileNotFoundError as file_error:
            messagebox.showerror(title='File not found!', message=file_error)
            self.statusbar_text.set('File not found!')

        self.input_file.set('')
        self.output_file.set('')
        self.after(3000, self.reset_status_bar)

    def reset_status_bar(self):
        """Reset the status bar to display further messages"""
        self.statusbar_text.set('Ready')


if __name__ == '__main__':
    gui = GUI()
    gui.resizable(False, False)
    gui.mainloop()
