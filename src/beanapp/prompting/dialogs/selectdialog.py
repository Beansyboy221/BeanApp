"""A dialog for selecting one or more items from a list."""

import tkinter.simpledialog
import tkinter
import typing


class SelectDialog(tkinter.simpledialog.Dialog):
    """A dialog for selecting one or more items from a list."""

    def __init__(
        self,
        title: str,
        prompt: str,
        items: typing.Sequence,
        multiselect: bool = False,
        parent=None,
    ):
        self.prompt = prompt
        self.items = items
        self.multiselect = multiselect
        self.result: list | object | None = None
        super().__init__(parent, title)

    def body(self, master):
        tkinter.Label(master, text=self.prompt).pack(pady=5)

        frame = tkinter.Frame(master)
        frame.pack(pady=5, padx=5, fill=tkinter.BOTH, expand=True)

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        self.listbox = tkinter.Listbox(
            master=frame,
            yscrollcommand=scrollbar.set,
            exportselection=False,
            selectmode=tkinter.MULTIPLE if self.multiselect else tkinter.BROWSE,
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        for item in self.items:
            self.listbox.insert(tkinter.END, str(item))

        if self.items:
            self.listbox.selection_set(0)
            self.listbox.activate(0)

        return self.listbox

    def apply(self):
        selection = self.listbox.curselection()
        if self.multiselect:
            self.result = [self.items[i] for i in selection]
        else:
            self.result = self.items[selection[0]] if selection else None
