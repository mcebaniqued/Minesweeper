from tkinter import *
import os   #used in restartProgram
import sys  #used restartProgram
import settings
import utils
from cell import Cell

root = Tk()     #instantiate the window

#Override the settings of the the window
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')    #change size of window
root.title("Minesweeper")                               #title of the window
root.resizable(False, False)                            #prevents from resizing the window
root.configure(bg = "#D3D3D3")                          #changes the background color (black)

#Top Frame
top_frame = Frame(
    root,
    bg     = "#3C4143",
    width  = settings.WIDTH,
    height = utils.height_percent(10) #600 / 10 = 60 pixels
)
top_frame.place(
    x = 0,
    y = 0
)

#Call the flag count label from Cell class
Cell.createFlagCountLabel(top_frame)
Cell.cell_count_flag_object.place(
    x = 10,
    y = 10
)

#Call the flag count label from Cell class
Cell.createTimerLabel(top_frame)
Cell.cell_timer_object.place(
    x = 455,
    y = 10
)

#Actual Game Frame
center_frame = Frame(
    root,
    bg     = "red",    #CHANGE BACK LATER
    width  = settings.WIDTH,
    height = utils.height_percent(90)
)

#8x8 cell is 464x448
center_frame.place(
    x = (settings.WIDTH - 464) / 2, #centers in the game frame
    y = ((utils.height_percent(90) - 448) / 2) + utils.height_percent(10)   #centers in the game frame
)

#Function used to restart the game
def restartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

#Set up the menu bar for the game
menu_bar = Menu(root)

#File menu
file_menu = Menu(menu_bar, tearoff = 0)
file_menu.add_command(label = "Restart", command = restartProgram)
file_menu.add_command(label = "Quit", command = root.quit)
menu_bar.add_cascade(label = "File", menu = file_menu)

#Difficulty Menu
diff_menu = Menu(menu_bar, tearoff = 0)
diff_menu.add_command(label = "Beginner")
diff_menu.add_command(label = "Intermediate")
diff_menu.add_command(label = "Expert")
diff_menu.add_command(label = "Custom")
#menu_bar.add_cascade(label = "Difficulty", menu = diff_menu)   #implement later

#Display Menu
disp_menu = Menu(menu_bar, tearoff = 0)
disp_menu.add_command(label = "Small (500x500)")
disp_menu.add_command(label = "Medium (600x600)")
disp_menu.add_command(label = "Large (720x720)")
#menu_bar.add_cascade(label = "Display", menu = disp_menu)

#Add menu bar to the window
root.config(menu = menu_bar)

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

#Starts the timer
Cell.gameTimer()

#Run the window
root.mainloop()