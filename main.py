from tkinter import *
from tkinter import ttk

from scripts.gameover import GameOver
from scripts.start import StartGame
from scripts.game import RenderEvent

if __name__ == "__main__":
    root = Tk()
    sg = StartGame(root, RenderEvent, GameOver)
    root.mainloop()