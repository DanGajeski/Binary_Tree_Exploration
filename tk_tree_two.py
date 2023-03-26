import random
import tkinter as tk
from dataclasses import dataclass

import tk_base_two


@dataclass
class DrawOptions:
    subtree_bounds: bool = False
    NODE_SIZE: int = 30


class TreeNode:

    NODE_SIZE = 30
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

    def draw(self, canvas, opts: DrawOptions):
        self.calculate_size(opts)
        self.calculate_child_positions(opts)
        self._draw(canvas, opts)

    def calculate_child_positions(self, opts: DrawOptions):
        left_offset = self.left.width + self.H_PAD if self.left else 0
        if self.left:
            self.left.x = self.x
            self.left.y = self.y + opts.NODE_SIZE + self.V_PAD
            self.left.calculate_child_positions(opts)
        if self.right:
            self.right.x = self.x + left_offset + self.H_PAD/2
            self.right.y = self.y + opts.NODE_SIZE + self.V_PAD
            self.right.calculate_child_positions(opts)

    def calculate_size(self, opts: DrawOptions):
        if not self.left and not self.right:
            self.width = opts.NODE_SIZE
            self.height = opts.NODE_SIZE
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
                (self.left.width if self.left else opts.NODE_SIZE) \
                + (self.right.width if self.right else opts.NODE_SIZE) \
                + (self.H_PAD if self.left or self.right else 0)
            self.height = opts.NODE_SIZE + max_height + self.V_PAD

    def _draw(self, canvas, opts: DrawOptions):
        half_width = self.width / 2
        half_size = opts.NODE_SIZE / 2
        canvas.create_oval(self.x + half_width - half_size, self.y, self.x + half_width + half_size, self.y + opts.NODE_SIZE, outline="#FF0")
        canvas.create_text(self.x + half_width, self.y + half_size, text=str(self.value), font=('times new roman', 15), fill='#fff')
        #canvas.create_rectangle(self.x + half_width - half_size - 10, self.y, self.x + half_width - 10, self.y + 11, fill='#00F')
        canvas.create_oval(self.x + half_width - half_size - 10, self.y, self.x + half_width - 10, self.y + 11, outline='#F00')
        canvas.create_oval(self.x + half_width - half_size - 25, self.y, self.x + half_width - 25, self.y + 11, outline='#F00')
        canvas.create_line(self.x + half_width - half_size - 25, self.y + 20, self.x + half_width - 25, self.y + 31, fill='#F00')
        canvas.create_line(self.x + half_width - half_size + 5, self.y + 20, self.x + half_width - 25, self.y + 31, fill='#F00')
        if self.count > 1:
            canvas.create_text(self.x + half_width, self.y + half_size + 10, text=str(self.count), font=('serif', 8), fill='#fff')
        if opts.subtree_bounds:
            outline_colors = ['#F00', '#F80', '#FF0', '#0F0', '#0F8', '#0FF', '#08F', '#00F']
            outline_color = outline_colors[(self.tree_height() - 1) % len(outline_colors)]
            canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, outline=outline_color)
        if self.left:
            canvas.create_line(self.x + half_width, self.y + opts.NODE_SIZE, self.left.x + self.left.width / 2, self.left.y, fill='#fff')
            self.left._draw(canvas, opts)
        if self.right:
            canvas.create_line(self.x + half_width, self.y + opts.NODE_SIZE, self.right.x + self.right.width / 2, self.right.y, fill='#fff')
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

    def tree_height(self):
        return max(
            self.left.tree_height() if self.left else 0,
            self.right.tree_height() if self.right else 0,
        ) + 1


class TreeUI:
    def __init__(self):
        self.draw_options = DrawOptions(subtree_bounds=False)
        self.reset()

    def reset(self, app=None):
        self.tree = TreeNode(50)
        self.tree.x = 5
        self.tree.y = 5
        self.next_value = 1
        self.draw_options.NODE_SIZE = 30
        if app:
            self.draw(app)

    def toggle_bounds(self, app):
        self.draw_options.subtree_bounds = not self.draw_options.subtree_bounds
        self.draw(app)

    def increase_node_size(self, app):
        self.draw_options.NODE_SIZE += 10
        self.draw(app)

    def add_node(self, app):
        self.tree.insert(TreeNode(random.randint(1, 100)))
        # self.tree.insert(TreeNode(self.next_value))
        self.next_value += 1
        self.draw(app)

    def draw(self, app):
        # tree = TreeNode(
        #     10,
        #     TreeNode(5, None, None),
        #     TreeNode(12, None, TreeNode(20, TreeNode(15), TreeNode(21))))
        # tree.x = 5
        # tree.y = 5

        app.canvas.delete("all")
        self.tree.draw(app.canvas, self.draw_options)

        app.canvas.create_text(5, 800, anchor=tk.SW, fill="#FFF", text="Height: " + str(self.tree.tree_height()))


tree_ui = TreeUI()
tk_base_two.TkBaseApp({"Add Node": tree_ui.add_node, "Increase the fuckin' node size": tree_ui.increase_node_size, "Toggle Bounds": tree_ui.toggle_bounds, "Reset": tree_ui.reset}).run()
