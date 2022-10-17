from tkinter import *
from tkinter import ttk

class StartGame():
    def __init__(self, root, game_fn, end_fn):
        self.root = root
        self.game_fn = game_fn
        self.end_fn = end_fn
        self.root.title("GAME START")
        self.root.resizable(FALSE, FALSE)
        self.root.geometry("200x100")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="You are a wizard.").grid(column=1, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Oh No!", command=self.begin).grid(column=2, row=2, sticky=W)

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
    def begin(self, *args):
        self.mainframe.destroy()
        self.game_fn(self.root, StartGame, self.end_fn)