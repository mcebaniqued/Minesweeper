from tkinter import *

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

#Title of the game
#game_title = Label(
#    top_frame,
#    bg   = "black",
#    fg   = "white",
#    text = "Minesweeper",
#    font = ('', 48)
#)

#game_title.place(
#    x = utils.width_percent(25),
#    y = 0
#)

#Left Frame
#left_frame = Frame(
#    root,
#    bg     = "red",   #CHANGE BACK LATER
#    width  = utils.width_percent(25),
#    height = settings.HEIGHT
#)
#left_frame.place(
#    x = 0, 
#    y = 0
#)

#Right Frame
#right_frame = Frame(
#    root,
#    bg     = "blue",   #CHANGE BACK LATER
#    width  = utils.width_percent(25),
#    height = settings.HEIGHT
#)
#right_frame.place(
#    x = 0, 
#    y = 0
#)

#Call the cell count label from Cell class
#Cell.createCellCountLabel(left_frame)
#Cell.cell_count_label_object.place(
#    x = 0,
#    y = 0
#)

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

#TODO: move game over/win condition here
#      maybe it will update the game before the window pops up

#Run the window
root.mainloop()