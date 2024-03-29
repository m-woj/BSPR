import tkinter as tk
import tkinter.ttk as ttk
import math


def check_option(func):
    def func_wrapper(self, *args, **kwargs):
        if not self.CHECK_OPTION:
            raise AttributeError("Check option is disabled.")
        return func(self, *args, **kwargs)
    return func_wrapper


class TreeList(tk.Frame):
    CHECK_OPTION = False
    AUTO_NUMBERING = False

    def __init__(self, top, dm_index=1):
        super().__init__(top)
        container = tk.Frame(self)
        scroll = tk.Scrollbar(container)
        tree = ttk.Treeview(container)
        scroll.config(command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        tree.config(yscrollcommand=scroll.set)
        container.pack(fill="both", expand=1)
        self.tree = tree
        self.dm_index = dm_index
        if self.CHECK_OPTION:
            self.checked_img = tk.PhotoImage(file='app/graphic/checked.gif')
            self.unchecked_img = tk.PhotoImage(file='app/graphic/unchecked.gif')
            self.chosen_items_ids = []
            tree.bind("<Button-1>", self._toggle_item)

    def set_data(self, data):
        self.chosen_items_ids = []
        self.clean()
        self.add_to_list(data)

    def add_to_list(self, data):
        i = self.dm_index
        if self.CHECK_OPTION:
            image = {"image": self.unchecked_img}
        else:
            image = {}

        min_precision = 0
        if i >= 0:
            for row in data:
                dm = str(row[i])
                if "." in dm:
                    prec = len(dm) - dm.index(".") - 1
                    min_precision = max(min_precision, prec)

        for n, row in enumerate(data):
            if i >= 0:
                row = list(row)
                row[i] = format(row[i], f'.{min_precision}f')

            if self.AUTO_NUMBERING:
                text = n + 1
                vals = row
            else:
                text = row[0]
                vals = row[1:]
            self.tree.insert(
                '', "end", text=text, values=vals, **image)

    def clean(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.CHECK_OPTION:
            self.chosen_items_ids = []

    def set_columns(self, columns):
        if self.AUTO_NUMBERING:
            if not isinstance(columns, list):
                columns = list(columns)
            columns = ["Lp."] + columns

        tree = self.tree
        tree['columns'] = columns[1:]
        tree['displaycolumns'] = columns[1:]

        tree.heading('#0', text=columns[0])
        for num, column in enumerate(columns[1:]):
            tree.heading(num, text=column)

    def set_columns_width(self, tree_width: int, widths):
        if self.AUTO_NUMBERING:
            if not isinstance(widths, list):
                widths = list(widths)
            widths = [0.1] + widths

        widths = [int(width * tree_width) for width in widths]
        self.tree.column('#0', minwidth=widths[0]//2, width=widths[0])
        for num, width in enumerate(widths[1:]):
            self.tree.column(num, width=width,
                             minwidth=width//2,
                             stretch=1)

    @check_option
    def get_chosen_ids(self):
        return sorted(self.chosen_items_ids)

    @check_option
    def toggle_all(self):
        tree = self.tree
        items = tree.get_children()

        def set_checkout_img(img):
            for item in items:
                tree.item(item, image=img)

        if len(self.chosen_items_ids) != len(items):
            set_checkout_img(self.checked_img)
            self.chosen_items_ids = [i for i in range(0, len(items))]
        else:
            set_checkout_img(self.unchecked_img)
            self.chosen_items_ids = []

    @check_option
    def _toggle_item(self, event):
        row_id = self.tree.identify("item", event.x, event.y)
        if not row_id:
            return
        index = self.tree.index(row_id)
        if index in self.chosen_items_ids:
            self.chosen_items_ids.remove(index)
            self.tree.item(row_id, image=self.unchecked_img)
        else:
            self.chosen_items_ids.append(index)
            self.tree.item(row_id, image=self.checked_img)
