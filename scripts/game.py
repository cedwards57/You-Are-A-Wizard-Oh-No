from tkinter import *
from tkinter import ttk
from scripts.gamedata import GameData
import json
import os

class RenderEvent():
    def __init__(self, root, start_fn, end_fn):
        self.root = root
        self.root.geometry("500x700")
        self.root.title("You Are A Wizard (Oh No!)")
        self.start_fn = start_fn
        self.end_fn = end_fn
        self.data = GameData()
        self.event_key = "event1_1"
        self.i = 0
        self.wrap=400
        project_root = os.path.dirname(os.path.dirname(__file__))
        self.content = json.load(open(f"{project_root}/src/content.json"))

        self.img_style = ttk.Style()
        self.img_style.configure("img.TFrame", background="black")
        self.txt_fr_style = ttk.Style()
        self.txt_fr_style.configure("txt.TFrame", background="#AFD6C3")
        self.txt_style = ttk.Style()
        self.txt_style.configure("txt.TLabel", font="Helvetica 12", background=ttk.Style().lookup('txt.TFrame', 'background'))
        self.btn_style = ttk.Style()
        self.btn_style.configure("TButton", padding="4")

        self.frame = ttk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.img_frame = ttk.Frame(self.frame, padding="0", style="img.TFrame")
        self.img_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.txt_frame = ttk.Frame(self.frame, padding="20", style="txt.TFrame")
        self.txt_frame.grid(column=0, row=1, columnspan=5, sticky=(N, W, E, S))
        
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)
        self.img_frame.rowconfigure(0, weight=1)
        self.img_frame.columnconfigure(1, weight=2)
        self.img_frame.columnconfigure(2, weight=1, minsize=100)
        self.img_frame.columnconfigure(3, weight=2)
        self.txt_frame.rowconfigure(0, weight=1, minsize=150)
        self.txt_frame.rowconfigure(1, weight=1)
        self.txt_frame.columnconfigure(0, weight=1)
        self.txt_frame.columnconfigure(1, weight=1)

        
        self.sprite_style = ttk.Style()
        self.sprite_style.configure("spr.TLabel", background="black")
        self.left_sprite_img = PhotoImage(file="img/placeholder_1.png")
        self.left_sprite = ttk.Label(self.img_frame, image=self.left_sprite_img, borderwidth=0, style="spr.TLabel")
        self.left_sprite.grid(column=1, row=0, sticky=SW)
        self.right_sprite_img = PhotoImage(file="img/placeholder_2.png")
        self.right_sprite = ttk.Label(self.img_frame, image=self.right_sprite_img, borderwidth=0, style="spr.TLabel")
        self.right_sprite.grid(column=3, row=0, sticky=SE)
        

        self.dialogue = StringVar(self.txt_frame, value="Placeholder")
        self.dialabel = ttk.Label(self.txt_frame, textvariable=self.dialogue, borderwidth=0, style="txt.TLabel",)
        self.dialabel.grid(column=0, row=0, sticky=NW, columnspan=2)
        self.dialabel.config(wrap=self.wrap)
        self.next_btn = ttk.Button(self.txt_frame, text="Next", command=lambda:self.render_dialogue(self.event_key))
        self.next_btn.grid(column=0, row=1, sticky=SW)
        self.option_btns = []

        self.render_dialogue(self.event_key)

    def render_dialogue(self, line):
        for btn in self.option_btns: btn.grid_remove()
        self.next_btn.grid(column=0, row=1, sticky=SW)
        if not isinstance(line, dict):
            line = self.content[line][self.i]

        if isinstance(line,str):
            self.i += 1
            self.dialogue.set(line)

        elif list(line.keys())[0] == "JUMP":
            self.i = 0
            self.event_key = line["JUMP"]
            self.render_dialogue(line["JUMP"])

        elif list(line.keys())[0] == "GAMEOVER":
            self.i = 0
            self.end_fn(self.root, self.start_fn, RenderEvent, line["GAMEOVER"])

        elif list(line.keys())[0] == "PROMPT":
            self.i = 0
            self.next_btn.grid_remove()
            self.render_options(line)
        
        elif list(line.keys())[0] == "GET":
            self.i += 1
            self.data.add(line["GET"].lower())
            self.render_dialogue(self.event_key)
        
        elif list(line.keys())[0] == "LOSE":
            self.i += 1
            self.data.remove(line["LOSE"].lower())
            self.render_dialogue(self.event_key)

        elif list(line.keys())[0] == "SPRITES":
            self.i += 1
            self.render_sprites(line)
            self.render_dialogue(self.event_key)  

    def render_options(self, line):
        self.dialogue.set(line["PROMPT"])
        self.option_btns = []
        options = line["OPTIONS"]
        for option in options:
            key = list(option.keys())[0]
            #print(options, option, key)
            if self.data.meets_requirement(option[key][1]):
                self.option_btns.append(ttk.Button(self.txt_frame, text=option[key][0], command=lambda key=key, option=option:self.render_dialogue({key: option[key][2]})))
        for i, button in enumerate(self.option_btns):
            button.grid(column=0, row=1+i, sticky=SW, pady=4)
    
    def render_sprites(self, line):
        if line["SPRITES"][0] is not None:
            self.left_sprite.grid_remove()
            self.left_sprite_img = PhotoImage(file=self.data.sprites[line["SPRITES"][0]])
            self.left_sprite = ttk.Label(self.img_frame, image=self.left_sprite_img, borderwidth=0, style="spr.TLabel")
            self.left_sprite.grid(column=1, row=0, sticky=SW)
        
        if line["SPRITES"][1] is not None:
            self.right_sprite.grid_remove()
            self.right_sprite_img = PhotoImage(file=self.data.sprites[line["SPRITES"][1]])
            self.right_sprite = ttk.Label(self.img_frame, image=self.right_sprite_img, borderwidth=0, style="spr.TLabel")
            self.right_sprite.grid(column=3, row=0, sticky=SE)