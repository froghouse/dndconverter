"""Manage the GUI portion of the application"""
import os
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import main


def is_windows() -> bool:
    """Return if we are on windows or not"""
    return os.name == 'nt'


class GUI(tkinter.Tk):
    """GUI manager"""

    # pylint: disable=too-many-instance-attributes
    # The amount of instance attributes are reasonable

    def __init__(self):
        super().__init__()

        self.title('DnD Converter')
        self.geometry('367x165')

        if is_windows():
            style = ttk.Style()
            style.theme_use('vista')
            self.iconbitmap('dnd-icon-22.ico')
            self.geometry('295x150')

        self.build_interface()

    def build_interface(self) -> None:
        """Logic for building the graphical interface"""
        self.components = {}
        self.components['input_file'] = tkinter.StringVar()
        self.components['output_file'] = tkinter.StringVar()
        self.components['statusbar_text'] = tkinter.StringVar()

        self.reset_status_bar()

        self.input_field()
        self.output_field()
        self.convert_field()
        self.status_field()

    def input_field(self) -> None:
        """Logic for displaying the input field"""
        self.components['input_frame'] = tkinter.LabelFrame(
            self, text='Input file'
            )
        self.components['input_frame'].grid(
            row=0, column=0, padx=2, pady=(2, 0)
            )

        self.components['input_entry'] = ttk.Entry(
            self.components['input_frame'],
            width=33,
            textvariable=self.components['input_file'],
            state='disabled'
        )
        self.components['input_entry'].grid(
            row=0, column=0, padx=2, pady=(2, 0)
            )

        self.components['input_browse_button'] = ttk.Button(
            self.components['input_frame'],
            text='Browse...',
            command=lambda: self.components['input_file'].set(
                filedialog.askopenfilename(
                    filetypes=[("eXtensible Markup Language", "*.xml")]
                )
            )
        )
        self.components['input_browse_button'].grid(
            row=0, column=1, padx=2, pady=(2, 0)
            )

    def output_field(self) -> None:
        """Logic for displaying the output field"""
        self.components['output_frame'] = tkinter.LabelFrame(
            self, text='Output file'
            )
        self.components['output_frame'].grid(
            row=1, column=0, padx=2, pady=(2, 0)
            )

        self.components['output_entry'] = ttk.Entry(
            self.components['output_frame'],
            width=33,
            textvariable=self.components['output_file'],
            state='disabled'
        )
        self.components['output_entry'].grid(
            row=0, column=0, padx=2, pady=(2, 0)
            )

        self.components['output_browse_button'] = ttk.Button(
            self.components['output_frame'],
            text='Browse...',
            command=lambda: self.components['output_file'].set(
                filedialog.asksaveasfilename(
                    filetypes=[("Comma-separated values", "*.csv")]
                )
            )
        )
        self.components['output_browse_button'].grid(
            row=0, column=1, padx=2, pady=(2, 0)
            )

    def convert_field(self) -> None:
        """Logic for displaying the convert button"""
        self.components['convert_button'] = ttk.Button(
            self,
            text='Convert',
            command=self.convert_command
        )
        self.components['convert_button'].grid(row=2, column=0, padx=2, pady=5)

    def status_field(self) -> None:
        """Logic for displaying the status bar"""
        self.components['statusbar'] = tkinter.Label(
            self,
            textvariable=self.components['statusbar_text'],
            bd=1,
            relief=tkinter.SUNKEN,
            anchor=tkinter.W
        )
        self.components['statusbar'].grid(
            row=3, column=0, columnspan=2, sticky='sew'
            )

    def convert_command(self) -> None:
        """Trigger the conversion from XML to CSV"""
        self.components['statusbar_text'].set("Converting...")
        try:
            items = main.convert_xml_to_csv(
                self.components['input_file'].get(),
                self.components['output_file'].get()
                )
            self.components['statusbar_text'].set(
                f"Done! Converted {items} items."
                )
        except AttributeError as atribute_error:
            messagebox.showerror(title='Exception!', message=atribute_error)
            self.components['statusbar_text'].set('Exception!')
        except FileNotFoundError as file_error:
            messagebox.showerror(title='File not found!', message=file_error)
            self.components['statusbar_text'].set('File not found!')

        self.components['input_file'].set('')
        self.components['output_file'].set('')
        self.after(3000, self.reset_status_bar)

    def reset_status_bar(self) -> None:
        """Reset the status bar to display further messages"""
        self.components['statusbar_text'].set('Ready')


if __name__ == '__main__':
    gui = GUI()
    gui.resizable(False, False)
    gui.mainloop()
