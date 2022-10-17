from tkinter import *
from tkinter import ttk

class GameOver():
    def __init__(self, root, start_fn, game_fn, message):
        self.root = root
        self.root.geometry("300x200")
        self.start_fn = start_fn
        self.game_fn = game_fn
        self.root.title("GAME OVER")
        self.mainframe = ttk.Frame(root, padding="8 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        L = ttk.Label(self.mainframe, text=message)
        L.grid(column=1, row=1, columnspan=2, sticky=N)
        L.config(wrap=250)
        ttk.Button(self.mainframe, text="Restart", command=self.restart).grid(column=1, row=2, sticky=W  )
        ttk.Button(self.mainframe, text="End", command=self.end).grid(column=2, row=2, sticky=E)

    def end(self, *args):
        self.root.destroy()
    
    def restart(self, *args):
        self.mainframe.destroy()
        self.start_fn(self.root, self.game_fn, GameOver)