# at start a think do it like a console programm
# but i need scrot for this
# and a can't install it to my Kali Linux XD
# so, let's do a bycycle!
import PIL.ImageDraw as ImageDraw
import pickle
import numpy as np
from neuro_web import img_to_vec
import os
import PIL.ImageOps
from tkinter import *
import PIL.Image as Image
import sh


# frame class

# make "cutting" rectangle

class border_rectangle:
    txt = "Wait..."
    canvas = None
    bord = None
    REV = False
    anim = None
    img = None
    img_start = None
    left_down = (0,0)
    top_right = (0,0)
    def __init__(self,c,i):

        self.canvas = c
        self.bord = canvas.create_rectangle(self.left_down, self.top_right)
        self.canvas.bind("<ButtonPress-1>", self.start)
        self.canvas.bind("<B1-Motion>", self.cont)
        self.canvas.bind("<ButtonRelease-1>", self.end)
        self.img = i
        self.img_start = i


    def start(self,event):
        self.bord = self.canvas.create_rectangle(self.left_down, self.top_right)
        self.left_down = (event.x,event.y)
        self.canvas.delete(self.bord)



    def cont(self,event):
        self.canvas.delete(self.anim)
        self.top_right = (event.x,event.y)
        self.anim = self.canvas.create_rectangle(self.left_down, self.top_right)





    def end(self,event):
        self.top_right = (event.x,event.y)
        self.img_start = self.img_start.convert("L")
        self.img = self.img_start.crop((self.left_down[0],self.left_down[1],self.top_right[0],self.top_right[1]))
        self.img_start = self.img_start.convert("L")
        try:
            os.remove("to_text.gif")
        except:
            pass
        self.img.save("to_text.gif")
        if self.REV:
            img_rev = Image.open("to_text.png")
            img_rev = img_rev.convert("L")
            img_rev = PIL.ImageOps.invert(img_rev)
            img_rev.save("to_text.png")
        r = sh.python("pil_tst.py")
        txt = open("buff.txt")
        self.txt = txt.read()
        lab.insert(END,self.txt)
        self.left_down = (0,0)
        self.top_right = (0,0)
# Exit function
def ex():
    master.destroy()

run = sh.sh("screen.sh")
master = Tk()
master.title("ITT pre-pre-alpha v1.0")
reverse = Image.open("v2.png")
reverse = reverse.resize((reverse.size[0],reverse.size[1]))
reverse.save("v2.gif")
canvas_width = master.winfo_screenwidth()
canvas_height =master.winfo_screenheight()

# Make menu. Now work just "Exit"

m = Menu(master)
master.config(menu=m)
fm = Menu(m)
m.add_cascade(label="File", menu=fm)
fm.add_command(label="Open...")
fm.add_command(label="New")
fm.add_command(label="Save...")

hm = Menu(m)
m.add_cascade(label="Help", menu=hm)
hm.add_command(label="Help")
hm.add_command(label="About")

tm = Menu(m)
m.add_command(label="Exit",command=ex)

# Label with text
lab = Text(master,width=20,height=3,font="12",wrap=WORD)
lab.pack()

# canvas with screenshot

canvas = Canvas(master,
           width=canvas_width,
           height=canvas_height)
canvas.pack()
img = PhotoImage(file="v2.gif")
canvas.create_image(0,0, anchor=NW, image=img)

brd = border_rectangle(canvas,reverse)

mainloop()