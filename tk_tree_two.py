import random
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

import tk_base_two


@dataclass
class DrawOptions:
    subtree_bounds: bool = False
    node_size: int = 30
    line_color: str = "#FFF"
    oval_color: str = "#FFF"
    text_color: str = "#FFF"
    color_opts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    def rand_oval_color(self):
        self.oval_color =  '#' + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)] + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)] + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)]

    def rand_line_color(self):
        self.line_color =  '#' + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)] + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)] + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)]

    def rand_text_color(self):
        self.text_color =  '#' + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)] + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)] + \
               self.color_opts[random.randint(0,15)] + self.color_opts[random.randint(0,15)]

    def rand_all_color(self):
        self.rand_oval_color()
        self.rand_line_color()
        self.rand_text_color()

    def inc_node_size(self):
        self.node_size += 10

    def dec_node_size(self):
        self.node_size -= 10

    #replace node_size method IN HERE

class TreeNode:

    H_PAD = 5
    V_PAD = 5

    def __init__(self, value, left=None, right=None):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.value = value
        self.count = 1
        self.left = left
        self.right = right
        self.num_test = 1

        ###########

    #sick
    def contains(self, num, guess_entry_label_two):
        subtree = None
        already_true = None
        if num == str(self.value):
            already_true = True
            guess_entry_label_two.config(text="True!")
            guess_entry_label_two.pack()
        elif num < str(self.value):
            subtree = self.left
        else:
            subtree = self.right
        if already_true:
            pass
        elif subtree:
            subtree.contains(num, guess_entry_label_two)
        else:
            guess_entry_label_two.config(text="Fuckin' False!")
            guess_entry_label_two.pack()

    def rotate_left(self):
        old_root = self
        old_right_left = self.right.left 

        root = self.right # B = A

        root.left = old_root 

        root.left.right = old_right_left 

        return root  

    def rotate_right(self):
        old_root = self 
        old_left_right = self.left.right 

        root = self.left # A = B

        root.right = old_root

        root.right.left = old_left_right

        return root 


    
    # def update_verify_label(self):
    #     verified = False
    #     verify_num = int(self.guess_input.get())
    #     if verify_num in self.tree.values: 
    #         verified = True
    #     if self.verify_label == None:
    #         self.verify_label = ttk.Label(main_window, text=verified)
    #         self.verify_label.pack()
    #     else:
    #         self.verify_label.text = verified
    #         self.verify_label.pack()

    # def verify_num(self, num):
    #     return num in self.values

    def draw(self, canvas, opts: DrawOptions):
        self.calculate_size(opts)
        self.calculate_child_positions(opts)
        self._draw(canvas, opts)

    def calculate_child_positions(self, opts: DrawOptions):
        left_offset = self.left.width + self.H_PAD if self.left else opts.node_size
        if self.left:
            self.left.x = self.x
            self.left.y = self.y + opts.node_size + self.V_PAD
            self.left.calculate_child_positions(opts)
        if self.right:
            self.right.x = self.x + left_offset + self.H_PAD/2
            self.right.y = self.y + opts.node_size + self.V_PAD
            self.right.calculate_child_positions(opts)

    def calculate_size(self, opts: DrawOptions):
        if not self.left and not self.right:
            self.width = opts.node_size
            self.height = opts.node_size
        else:
            max_width = 0
            max_height = 0
            if self.left:
                self.left.calculate_size(opts)
                max_width = self.left.width
                max_height = self.left.height
            if self.right:
                self.right.calculate_size(opts)
                max_width = max(max_width, self.right.width)
                max_height = max(max_height, self.right.height)
            # balance the size
            # self.width = max_width * 2 + self.H_PAD
            # minimal size -- kinda broken
            self.width = \
                (self.left.width if self.left else opts.node_size) \
                + (self.right.width if self.right else opts.node_size) \
                + (self.H_PAD if self.left or self.right else 0)
            self.height = opts.node_size + max_height + self.V_PAD

    def _draw(self, canvas, opts: DrawOptions):
        half_width = self.width / 2
        half_size = opts.node_size / 2
        canvas.create_oval(self.x + half_width - half_size, self.y, self.x + half_width + half_size, self.y + opts.node_size, outline=opts.oval_color)
        canvas.create_text(self.x + half_width, self.y + half_size, text=str(self.value), font=('times new roman', 15), fill=opts.text_color)
        #canvas.create_rectangle(self.x + half_width - half_size - 10, self.y, self.x + half_width - 10, self.y + 11, fill='#00F')
        canvas.create_oval(self.x + half_width - half_size - 10, self.y, self.x + half_width - 10, self.y + 11, outline=opts.oval_color)
        canvas.create_oval(self.x + half_width - half_size - 25, self.y, self.x + half_width - 25, self.y + 11, outline=opts.oval_color)
        canvas.create_line(self.x + half_width - half_size - 25, self.y + 20, self.x + half_width - 25, self.y + 31, fill=opts.line_color)
        canvas.create_line(self.x + half_width - half_size + 5, self.y + 20, self.x + half_width - 25, self.y + 31, fill=opts.line_color)
        if self.count > 1:
            canvas.create_text(self.x + half_width, self.y + half_size + 10, text=str(self.count), font=('serif', 8), fill=opts.text_color)
        if opts.subtree_bounds:
            outline_colors = ['#F00', '#F80', '#FF0', '#0F0', '#0F8', '#0FF', '#08F', '#00F']
            outline_color = outline_colors[(self.tree_height() - 1) % len(outline_colors)]
            canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, outline=outline_color)
        if self.left:
            canvas.create_line(self.x + half_width, self.y + opts.node_size, self.left.x + self.left.width / 2, self.left.y, fill=opts.line_color)
            self.left._draw(canvas, opts)
        if self.right:
            canvas.create_line(self.x + half_width, self.y + opts.node_size, self.right.x + self.right.width / 2, self.right.y, fill=opts.line_color)
            self.right._draw(canvas, opts)

    def insert(self, node):
        if node.value == self.value:
            self.count += 1
        elif node.value < self.value:
            if self.left:
                self.left.insert(node)
            else:
                self.left = node
        else:
            if self.right:
                self.right.insert(node)
            else:
                self.right = node

    

    def invert(self):
        def lefty_loosy_righty_tighty():
            self.left, self.right = self.right, self.left
        if self.left and self.right:
            lefty_loosy_righty_tighty()
            self.left.invert()
            self.right.invert()
        elif self.left:
            lefty_loosy_righty_tighty()
            self.right.invert()
        elif self.right:
            lefty_loosy_righty_tighty()
            self.left.invert()

    def tree_height(self):
        return max(
            self.left.tree_height() if self.left else 0,
            self.right.tree_height() if self.right else 0,
        ) + 1

    def clone(self):
        new_left = self.left.clone() if self.left else None
        new_right = self.right.clone() if self.right else None
        new_self = TreeNode(self.value, new_left, new_right)
        new_self.count = self.count 

        return new_self



    #def num_in_tree(self):


class TreeUI:
    def __init__(self):
        self.draw_options = DrawOptions(subtree_bounds=False)
        self.guess_input = None
        #self.guess_input_answer = tk.StringVar(text="Your fuckin' answer here:")
        self.reset()

    def reset(self, app=None):
        #self.tree = TreeNode(50)
        self.tree = TreeNode(10, # B
                TreeNode(5, TreeNode(1), TreeNode(7)), # A + children
                TreeNode(15, TreeNode(12), TreeNode(20))) # B.right
        self.prev_tree = None
        self.tree.x = 5
        self.tree.y = 5
        self.next_value = 1
        self.draw_options.node_size = 30
        if app:
            self.draw(app)

    def toggle_bounds(self, app):
        self.draw_options.subtree_bounds = not self.draw_options.subtree_bounds
        self.draw(app)

    def increase_node_size(self, app):
        self.draw_options.inc_node_size()
        self.draw(app)
    def decrease_node_size(self, app):
        self.draw_options.dec_node_size()
        self.draw(app)

    def add_node(self, app):
        self.tree.insert(TreeNode(random.randint(1, 100)))
        # self.tree.insert(TreeNode(self.next_value))
        self.next_value += 1
        self.draw(app)

    def invert_nodes(self, app):
        self.tree.invert()
        self.draw(app)

    def randomize_oval_color(self, app):
        self.draw_options.rand_oval_color()
        self.draw(app)

    def randomize_line_color(self, app):
        self.draw_options.rand_line_color()
        self.draw(app)

    def randomize_text_color(self, app):
        self.draw_options.rand_text_color()
        self.draw(app)

    def randomize_all_color(self, app):
        self.draw_options.rand_all_color()
        self.draw(app)

    def draw(self, app):
        # tree = TreeNode(
        #     10,
        #     TreeNode(5, None, None),
        #     TreeNode(12, None, TreeNode(20, TreeNode(15), TreeNode(21))))
        # tree.x = 5
        # tree.y = 5
        


        app.canvas.delete("all")

        if self.prev_tree:
            self.prev_tree.draw(app.canvas, self.draw_options)
            self.tree.x = self.prev_tree.width + 25
            self.tree.y = 0
        

        self.tree.draw(app.canvas, self.draw_options)

        app.canvas.create_text(5, 900, anchor=tk.SW, fill="#FFF", text="Height: " + str(self.tree.tree_height()))

    def rotate_right(self, app):
        self.prev_tree = self.tree.clone()
        self.tree = self.tree.rotate_right()
        self.draw(app)

    def rotate_left(self, app):
        self.prev_tree = self.tree.clone()
        self.tree = self.tree.rotate_left()
        self.draw(app)

    def init_ui(self, container_frame):
        guess_entry_frame = ttk.Frame(container_frame)
        guess_entry_frame.pack()

        self.guess_input = tk.StringVar()
         
        guess_entry_label = ttk.Label(guess_entry_frame, text="Is # in tree? ...> ")
        guess_entry_label.pack()

        guess_entry = ttk.Entry(guess_entry_frame, textvariable=self.guess_input, font=('times new roman', 15))
        guess_entry.pack(expand=True)

        guess_entry_label_two = ttk.Label(guess_entry_frame, text="Your Fuckin' Answer Here: ")

        guess_entry_button = ttk.Button(guess_entry_frame, text="Check Guess", command=lambda: self.tree.contains(self.guess_input.get(), guess_entry_label_two)) #command=update_verify_label)
        guess_entry_button.pack(pady=10)
        
        guess_entry_label_two.pack()


tree_ui = TreeUI()
tk_base_two.TkBaseApp({ 
    "Add Node": tree_ui.add_node, 
    "Increase the fuckin' node size": tree_ui.increase_node_size, 
    "Decrease the fuckin' node size": tree_ui.decrease_node_size, 
    "Toggle Bounds": tree_ui.toggle_bounds, 
    "Reset": tree_ui.reset,
    "Invert Tree": tree_ui.invert_nodes,
    "Rotate Left": tree_ui.rotate_left,
    "Rotate Right": tree_ui.rotate_right,
    "R Oval Color": tree_ui.randomize_oval_color,
    "R Line Color": tree_ui.randomize_line_color,
    "R Text Color": tree_ui.randomize_text_color,
    "R All Color": tree_ui.randomize_all_color,
    }, 
    tree_ui.init_ui
    ).run()
