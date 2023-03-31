import time
import sys

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

"""
This module defines a base class for a TK canvas in a window for easy drawing without boilerplate.
See examples at bottom.
"""

class TkBaseApp:

    def __init__(self, funcs: dict, ui_init=None):
        self.funcs = funcs
        self.canvas = None
        self.ui_init = ui_init
        self.container_frame = None
        #self.butt_func = butt_func

    def run(self):
        # Define the GUI and various widgets
        main_window = Tk()
        # Create a container that belongs to the main window
        container_frame = ttk.Frame(main_window, padding=10)
        container_frame.pack()

        button_container_frame = ttk.Frame(container_frame)
        button_container_frame.pack()

        ttk.Button(button_container_frame, text="Quit", command=main_window.destroy).pack(side=RIGHT)
        for label, func in self.funcs.items():
            def wrap(fn):
                return lambda: fn(self)
            ttk.Button(button_container_frame, text=label, command=wrap(func)).pack(side=LEFT)
        self.canvas = Canvas(container_frame, bg="#000000", height=900, width=1200)
        #canvas.pack(fill=BOTH, expand=1)
        self.canvas.pack()

        self.ui_init(container_frame)

        # guess_input = StringVar()
        
        # #entry label
        # guess_entry_label = ttk.Label(main_window, text="Is # in tree? ...> ")
        # guess_entry_label.pack()

        # #input entry
        # guess_entry = ttk.Entry(main_window, textvariable=guess_input, font=('times new roman', 15))
        # guess_entry.pack(expand=True)
        # #guess_entry.focus()

        # print_label = ttk.Label(main_window, text=guess_input)
        # print_label.pack()

        # def update_print_label():
        #     print_label.config(text=guess_input.get())
        #     print_label.pack()


        # #input button
        # guess_entry_button = ttk.Button(main_window, text="Check Guess", command=update_print_label)
        # guess_entry_button.pack(pady=10)


        

        
        
        #def check_guess(self)




        #entry_button_container_frame = ttk.Frame(container_frame)
        #entry_button_container_frame.pack()

        #def wrap_again(fn):
         #   return lambda: fn(self)
        #entry_w_button = ttk.Button(entry_button_container_frame, text="# in Tree? Click to verify", command=wrap_again(self.butt_func))
        #entry_w_button.pack()

        # Start the GUI application!
        main_window.mainloop()

# TkBaseApp({"lol": lambda x: print(x, x.canvas), "foo": lambda x: print("foo!")}).run()

# pos = 0
# def draw(app):
#     global pos
#     pos += 10
#     app.canvas.create_rectangle(pos, pos, pos+10, pos+10, fill="#FFF", outline="#F00")
# TkBaseApp({"draw": draw}).run()
