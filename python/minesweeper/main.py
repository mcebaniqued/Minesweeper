from tkinter import *
import ctypes   #used in leftClickActions & showMines
import sys      #used in leftClickActions & showMines

import settings
import utils
from cell import Cell

root = Tk()     #instantiate the window

#Override the settings of the the window
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')       #change size of window
root.title("Minesweeper")       #title of the window
root.resizable(False, False)    #prevents from resizing the window
root.configure(bg = "#D3D3D3")      #changes the background color (black)

#Top Frame
top_frame = Frame(
    root,
    bg     = "#3C4143",
    width  = settings.WIDTH,
    height = utils.height_percent(25)
)
top_frame.place(
    x = 0,
    y = 0
)

#Call the flag count label from Cell class
Cell.createFlagCountLabel(top_frame)
Cell.cell_count_flag_object.place(
    x = utils.height_percent(10),
    y = utils.height_percent(10)
)

#Call the flag count label from Cell class
Cell.createTimerLabel(top_frame)
Cell.cell_timer_object.place(
    x = utils.height_percent(70),
    y = utils.height_percent(10)
)

#Actual Game Frame
center_frame = Frame(
    root,
    bg     = "red",    #CHANGE BACK LATER
    width  = settings.WIDTH,
    height = utils.height_percent(75)
)
center_frame.place(
    x = utils.height_percent(20),
    y = utils.height_percent(30)
)

#Instantiate Buttons in the Game Frame
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.createButtonObject(center_frame)
        c.cell_button_object.grid(
            column = x,
            row    = y
        )

#Choose random buttons to become mines
Cell.randomizedMines()

#Run the window
root.mainloop()