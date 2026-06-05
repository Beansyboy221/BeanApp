"""A dialog with a scrolled text widget for multi-line text input."""

import tkinter.scrolledtext
import tkinter.simpledialog
import tkinter


class ScrolledTextDialog(tkinter.simpledialog.Dialog):
    """A dialog with a scrolled text widget for multi-line text input."""

    def __init__(self, title: str, prompt: str, initial_text: str = "", parent=None):
        self.prompt = prompt
        self.initial_text = initial_text
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        tkinter.Label(master, text=self.prompt).pack(pady=5)
        self.text = tkinter.scrolledtext.ScrolledText(
            master, width=50, height=10, wrap=tkinter.WORD
        )
        self.text.pack(pady=5, padx=10, fill=tkinter.BOTH, expand=True)
        if self.initial_text:
            self.text.insert(tkinter.END, self.initial_text)
        return self.text

    def apply(self):
        raw_text = self.text.get("1.0", tkinter.END)
        self.result = raw_text.rstrip("\n")
