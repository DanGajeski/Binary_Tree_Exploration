import time
import sys

from tkinter import *
from tkinter import ttk

"""
This module defines a base class for a TK canvas in a window for easy drawing without boilerplate.
See examples at bottom.
"""

class TkBaseApp:

    def __init__(self, funcs: dict):
        self.funcs = funcs
        self.canvas = None

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
        self.canvas = Canvas(container_frame, bg="#000000", height=800, width=1200)
        #canvas.pack(fill=BOTH, expand=1)
        self.canvas.pack()

        # Start the GUI application!
        main_window.mainloop()

# TkBaseApp({"lol": lambda x: print(x, x.canvas), "foo": lambda x: print("foo!")}).run()

# pos = 0
# def draw(app):
#     global pos
#     pos += 10
#     app.canvas.create_rectangle(pos, pos, pos+10, pos+10, fill="#FFF", outline="#F00")
# TkBaseApp({"draw": draw}).run()
