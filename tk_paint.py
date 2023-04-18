import tkinter as tk 
from tkinter import ttk
from tkinter import ACTIVE, NORMAL 
from dataclasses import dataclass

import tk_base_two

#ui framework -- generally inherit the look and feel of parent OS

class PaintUI:
    def __init__(self):
        pass

    #bind to canvas instead of frame that holds canvas and buttons?
    def init_ui(self, frame, canvas):
        self.frame = frame
        self.canvas = canvas
        self.frame.master.title("The Diddler")
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-1>', self.mouse_down)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
        self.canvas.bind('<Double-Button-1>', self.double_click)
        self.mouse_down_pos = [0,0]
        self.motion_line = None
        self.motion_rectangle = None
        self.mouse_down_pressed = False
        self.set_draw_type = "None"

    def draw_straight_line(self, app):
        if self.set_draw_type != "STRAIGHT":
            self.set_draw_type = "STRAIGHT"
            #app.my_buttons['Draw']['state'] = ACTIVE
            app.my_buttons['Draw Straight Line'].config(text="Draw Straight Line")
            app.my_buttons['Draw Curvy Line'].config(text="No Draw Curvy line")
            app.my_buttons['Draw Rectangle'].config(text="No Draw Rectangle")
            self.reset_buttons_check(app)
        else:
            self.set_draw_type = "None"
            #app.my_buttons['Draw']['state'] = NORMAL
            app.my_buttons['Draw Straight Line'].config(text="No Draw Straight Line")
            self.reset_buttons_check(app)

    def draw_curvy_line(self, app):
        if self.set_draw_type != "GAY":
            self.set_draw_type = "GAY"
            app.my_buttons['Draw Curvy Line'].config(text="Draw Curvy Line")
            app.my_buttons['Draw Straight Line'].config(text="No Draw Straight Line")
            app.my_buttons['Draw Rectangle'].config(text="No Draw Rectangle")
            self.reset_buttons_check(app)
        else:
            self.set_draw_type = "None"
            app.my_buttons['Draw Curvy Line'].config(text="No Draw Curvy Line")
            self.reset_buttons_check(app)

    def draw_rectangle(self, app):
        if self.set_draw_type != "RECTANGLE":
            self.set_draw_type = "RECTANGLE"
            app.my_buttons['Draw Rectangle'].config(text="Draw Rectangle")
            app.my_buttons['Draw Straight Line'].config(text="No Draw Straight Line")
            app.my_buttons['Draw Curvy Line'].config(text="No Draw Curvy Line")
            self.reset_buttons_check(app)
        else:
            self.set_draw_type = "None"
            app.my_buttons['Draw Rectangle'].config(text="No Draw Rectangle")
            self.reset_buttons_check(app)

    def reset_buttons_check(self, app):
        if app.my_buttons['Draw Straight Line'].cget('text') == "No Draw Straight Line" and \
        app.my_buttons['Draw Curvy Line'].cget('text') == "No Draw Curvy Line" and \
        app.my_buttons['Draw Rectangle'].cget('text') == "No Draw Rectangle":
            app.my_buttons['Draw Straight Line'].config(text="Draw Straight Line")
            app.my_buttons['Draw Curvy Line'].config(text="Draw Curvy Line")
            app.my_buttons['Draw Rectangle'].config(text="Draw Rectangle")



    def motion(self, event):
        #x, y = self.mouse_down_pos[0], self.mouse_down_pos[1]
        #self.canvas.create_line(self.mouse_down_pos[0], self.mouse_down_pos[1], x, y, fill='#00F')
        #self.canvas.delete(self.motion_line)
        x, y = event.x, event.y
        if self.set_draw_type == "STRAIGHT":
            if self.mouse_down_pressed == True:
                self.canvas.delete(self.motion_line)
                self.motion_line = self.canvas.create_line(self.mouse_down_pos[0], self.mouse_down_pos[1], x, y, fill='#00F')
        elif self.set_draw_type == "GAY":
            if self.mouse_down_pressed == True:
                self.motion_line = self.canvas.create_line(self.mouse_down_pos[0], self.mouse_down_pos[1], x, y, fill='#0F0')
                self.mouse_down_pos[0] = x
                self.mouse_down_pos[1] = y
        elif self.set_draw_type == "RECTANGLE":
            if self.mouse_down_pressed == True:
                self.canvas.delete(self.motion_rectangle)
                self.motion_rectangle = self.canvas.create_rectangle(self.mouse_down_pos[0], self.mouse_down_pos[1], x, y, outline='#F00')
            #self.canvas.delete(motion_line)
        print('{}, {}'.format(x, y))

    def mouse_down(self, event):
        x, y = event.x, event.y
        self.mouse_down_pos = [x, y]
        self.mouse_down_pressed = True
        print('Mouse Down: {}, {}'.format(x, y))

    def mouse_up(self, event):
        x, y = event.x, event.y
        if self.set_draw_type == "STRAIGHT":
            self.canvas.create_line(self.mouse_down_pos[0], self.mouse_down_pos[1], x, y, fill='#00F')
        elif self.set_draw_type == "RECTANGLE":
            self.canvas.create_rectangle(self.mouse_down_pos[0], self.mouse_down_pos[1], x, y, outline='#F00')
        print('Mouse Up: {}, {}'.format(x, y))
        self.mouse_down_pressed = False

    def double_click(self, event):
        x, y = event.x, event.y
        print('Double Click: {}, {}'.format(x, y))

    def reset_canvas(self, app):
        self.canvas.delete('all')
        self.set_draw_type = "None"
        app.my_buttons['Draw Straight Line'].config(text="Draw Straight Line")
        app.my_buttons['Draw Curvy Line'].config(text="Draw Curvy line")
        app.my_buttons['Draw Rectangle'].config(text="Draw Rectangle")

        # click draw_line() to enable line drawing... then click(and-hold) on canvas to draw line from origin to where
        # user releases mouse-click1
    
    


paint_ui = PaintUI()
tk_base_two.TkBaseApp(
    { 
    "Draw Straight Line": ("<Control-a>", paint_ui.draw_straight_line),
    "Draw Curvy Line" :("<Control-b>", paint_ui.draw_curvy_line),
    "Draw Rectangle" :("<Control-r>", paint_ui.draw_rectangle),
    "Reset Canvas" :("<Control-z>", paint_ui.reset_canvas),
    }, 
    paint_ui.init_ui
    ).run()

#funciton stands alone
#method has object parameter baked into it
#   self parameter is already filled 