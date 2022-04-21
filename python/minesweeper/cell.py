from tkinter import Button, Label
import random   #used in randomizedMines
import settings #used in randomizedMines
import ctypes   #used in leftClickActions & showMines
import sys      #used in leftClickActions & showMines

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    flag_count = settings.FLAG_COUNT
    start_time = -1
    cell_count_flag_object = None
    cell_timer_object = None

    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_flagged = False
        self.cell_button_object = None,
        self.x = x
        self.y = y

        #Append the object to the Cell.all list
        Cell.all.append(self)

    #A function that creates the buttons for the game
    def createButtonObject(self, location):
        #Button object
        button = Button(
            location,
            width  = 3, #1:3 ratio?
            height = 1,
            font   = ('', 20)
        )

        #Assigns an action when left clicked
        button.bind(
            "<Button-1>",
            self.leftClickActions)

        #Assigns an action when right clicked
        button.bind(
            "<Button-3>",
            self.rightClickActions)

        self.cell_button_object = button

    #A function that tells what the button does when left clicked
    def leftClickActions(self, event):
        #If player clicked on mine
        if self.is_mine:
            self.showMine()
        #If player clicked on normal cell
        else:
            #Reveals its own cell
            self.showCell()

            #Reveals other adjacent cells if the opened cell has 0 mines
            self.showAllAdjacent()
            
            #If Mine Count == Cells Left Count, player wins
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "You win!", "Congratulations", 0)
                sys.exit()

    #Recursion function that uses DFS to look for adjacent cells with 0 adjacent mines, and opens their adjacent cells
    def showAllAdjacent(self):
        if self.getNumberOfMines == 0:
                for cell_obj in self.findAdjacentCells:
                    if cell_obj.is_opened == False:
                        cell_obj.showCell()
                        cell_obj.showAllAdjacent()

    #Interrupts the game and displays a message that the game is over
    def showMine(self):
        self.cell_button_object.configure(bg = "red")

        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine!", "Game Over", 0)
        sys.exit()

    #Shows the number of cells that potentially has mines
    def showCell(self):
        if not self.is_opened:
            #Makes sure that the non-mine cell are in the right button color
            self.cell_button_object.configure(bg = "#BDBDBD")

            if self.getNumberOfMines != 0:
                #Get the number of mines that could be adjacent (cell's with zero adj mines doesnt get '0"
                self.cell_button_object.configure(text = self.getNumberOfMines)
                #Change color of the text according to the number of mines
                if self.getNumberOfMines == 1:
                    self.cell_button_object.configure(fg = "#0000F2")
                elif self.getNumberOfMines == 2:
                    self.cell_button_object.configure(fg = "#007B00")
                elif self.getNumberOfMines == 3:
                    self.cell_button_object.configure(fg = "#F20000")
                elif self.getNumberOfMines == 4:
                    self.cell_button_object.configure(fg = "#00007D")
                elif self.getNumberOfMines == 5:
                    self.cell_button_object.configure(fg = "grey16") #was #B0B0B0 but it's hard to see on the cell
                elif self.getNumberOfMines == 6:
                    self.cell_button_object.configure(fg = "#007B7D")
                elif self.getNumberOfMines == 7:
                    self.cell_button_object.configure(fg = "#7D007D")
                elif self.getNumberOfMines == 8:
                    self.cell_button_object.configure(fg = "#6F6F6F")

                #Prevents opened cell from being clicked
                self.cell_button_object.unbind("<Button-1>")
                self.cell_button_object.unbind("<Button-3>")

            #Replace the text of cell count label with updated count
            Cell.cell_count -= 1

            #If the flagged non-mine cell is revealed, give the number of flags back to the counter
            if self.is_flagged == True:
                Cell.flag_count += 1
                if Cell.cell_count_flag_object:
                    Cell.cell_count_flag_object.configure(
                        text = f"Flags: {Cell.flag_count}"
                    )
        
        #Mark the cell as opened
        self.is_opened = True
    
    #Counts the number of cells with mines
    @property
    def getNumberOfMines(self):
        counter = 0
        for cell in self.findAdjacentCells:
            if cell.is_mine:
                counter += 1
        return counter

    #Finds all surrounding cells of a clicked cell
    @property
    def findAdjacentCells(self):
        adjacent_cells = [
            self.getCellByAxis(self.x - 1, self.y - 1),  #top    left
            self.getCellByAxis(self.x - 1, self.y),      #center left
            self.getCellByAxis(self.x - 1, self.y + 1),  #bottom left
            self.getCellByAxis(self.x, self.y - 1),      #top    center
            self.getCellByAxis(self.x + 1, self.y - 1),  #top    right
            self.getCellByAxis(self.x + 1, self.y),      #center right
            self.getCellByAxis(self.x + 1, self.y + 1),  #bottom right
            self.getCellByAxis(self.x, self.y + 1),      #bottom center
        ]

        #Takes account "out of bound" cells and are removed from the list
        adjacent_cells = [cell for cell in adjacent_cells if cell is not None]

        return adjacent_cells

    #Return a cell object based on the value of x, y
    def getCellByAxis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    #A function that tells what the button does when right clicked
    def rightClickActions(self, event):
        #Toggle color ON
        if not self.is_flagged:
            #If the number of flags is equal to zero, do not allow right clicks
            if Cell.flag_count == 0:
                self.cell_button_object.unbind("<Button-3>")    #it was on Button-1 (left click)
            else:
                self.cell_button_object.configure(bg = "yellow")
                self.is_flagged = True

                #Replace the text of flag count label with updated count (decrement)
                Cell.flag_count -= 1
                if Cell.cell_count_flag_object:
                    Cell.cell_count_flag_object.configure(
                        text = f"Flags: {Cell.flag_count}"
                    )

                #Unbinds left click when flagged to prevent being accidentally clicked
                self.cell_button_object.unbind("<Button-1>")

        #Toggle color OFF
        else:
            self.cell_button_object.configure(bg = "SystemButtonFace")
            self.is_flagged = False

            #Replace the text of flag count label with updated count (increment)
            Cell.flag_count += 1
            if Cell.cell_count_flag_object:
                Cell.cell_count_flag_object.configure(
                    text = f"Flags: {Cell.flag_count}"
                )

            #Binds the left click back to the unmarked cell
            self.cell_button_object.bind(
                "<Button-1>",
                self.leftClickActions)

    #A function that chooses random cells to become mines
    @staticmethod
    def randomizedMines():
        cells_as_mines = random.sample(
            Cell.all, 
            settings.MINES_COUNT
        )

        #change the attributes of randomly chosen cell's is_mine to true
        for cell in cells_as_mines:
            cell.is_mine = True
        
    #Prints out xy-coordinates of each cell by using print(Cell.all) in main.py
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
    
    @staticmethod
    #A function that creates flag count label for the game
    def createFlagCountLabel(location):
        Cell.cell_count_flag_object = Label(
            location,
            bg     = "grey8",
            fg     = "#FF0000",
            text   = f"Flags: {Cell.flag_count}",
            width  = 8,
            height = 1,
            font   = ("", 20)
        )
    
    #A function that creates tinmer label for the game
    @staticmethod
    def createTimerLabel(location):
        Cell.cell_timer_object = Label(
            location,
            bg     = "grey8",
            fg     = "#FF0000",
            text   = f"Time: {Cell.start_time}",
            width  = 8,
            height = 1,
            font   = ("", 20)
        )
    
    def gameTimer():
        Cell.start_time += 1
        Cell.cell_timer_object.config(
            text   = f"Time: {Cell.start_time}"
        )
        Cell.cell_timer_object.after(1000, Cell.gameTimer)

#BUG?:  a zero cell that's diagonal to another zero cell causes to expand to other cells
#BUG:  FIXED right clicking a normal cell after the number of flags go down to zero will not let you left click it
#BUG:  FIXED if a flagged non-mine cell gets revealed, it doesn't give the remaining amount of flags back
#TODO: add game menu bar using Menu(root). Add functionality of Reset, Quit, Change Difficulty, etc.