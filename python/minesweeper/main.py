from tkinter import *

import settings
import utils
from cell import Cell

root = Tk()     #instantiate the window

#Override the settings of the the window
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')       #change size of window
root.title("Minesweeper")       #title of the window
root.resizable(False, False)    #prevents from resizing the window
root.configure(bg="black")      #changes the background color (black)

#Title Frame
top_frame = Frame(
    root,
    bg     = "black",
    width  = settings.WIDTH,
    height = utils.height_percent(25)
)
top_frame.place(
    x = 0,
    y = 0
)

game_title = Label(
    top_frame,
    bg   = "black",
    fg   = "white",
    text = "Minesweeper",
    font = ('', 48)
)

#TODO: polish game title
game_title.place(
    x = utils.width_percent(25),
    y = 0
)

#Game Info Frame
left_frame = Frame(
    root,
    bg     = "black",
    width  = utils.width_percent(25),
    height = utils.height_percent(75)
)
left_frame.place(
    x = 0, 
    y = utils.height_percent(25)
)

#TODO: polish label
#TODO: add counter for flags
#Call the label from Cell class
Cell.createCellCountLabel(left_frame)
Cell.cell_count_label_object.place(
    x = 0,
    y = 0
)

#Actual Game Frame
center_frame = Frame(
    root,
    bg     = "black",
    width  = utils.width_percent(75),
    height = utils.height_percent(75)
)
center_frame.place(
    x = utils.width_percent(25),
    y = utils.height_percent(25)
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