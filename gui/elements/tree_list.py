import tkinter as tk
import tkinter.ttk as ttk


class TreeList(tk.Frame):
    def __init__(self, top):
        tk.Frame.__init__(self, top)
        self.checked_img = tk.PhotoImage(file='graphic/checked.gif')
        self.unchecked_img = tk.PhotoImage(file='graphic/unchecked.gif')

        scroll = tk.Scrollbar(self)
        tree = ttk.Treeview(self)
        scroll.config(command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        tree.bind('<<TreeviewSelect>>', self.__select)
        tree.config(yscrollcommand=scroll.set)

        self.tree = tree
        self.top = top

    def set_columns(self, columns):
        tree = self.tree

        tree['columns'] = columns[1:]
        tree['displaycolumns'] = columns[1:]

        tree.heading('#0', text=columns[0])
        for num, column in enumerate(columns[1:]):
            tree.heading(num, text=column)

    def set_columns_width(self, tree_width, widths):
        widths = [int(width * tree_width) for width in widths]
        self.tree.column('#0', minwidth=widths[0]//2, width=widths[0])
        for num, width in enumerate(widths[1:]):
            self.tree.column(num, width=width,
                             minwidth=width//2,
                             stretch=1)

    def __select(self):
        pass
