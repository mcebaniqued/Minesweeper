from tkinter import Button, Label
import random   #used in randomizedMines
import settings #used in randomizedMines
import ctypes   #used in leftClickActions & showMines
import sys      #used in leftClickActions & showMines

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

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
            width  = 6, #width must be double the height to create a square button
            height = 3,
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

    @staticmethod
    def createCellCountLabel(location):
        label = Label(
            location,
            bg      = "black",
            fg      = "white",
            text    = f"Cells Left: {Cell.cell_count}",
            width   = 12,
            height  = 4,
            font    = ("", 30)
        )
        Cell.cell_count_label_object = label

    #A function that tells what the button does when left clicked
    def leftClickActions(self, event):
        #If player clicked on mine
        if self.is_mine:
            self.showMine()
        #If player clicked on normal cell
        else:
            if self.getNumberOfMines == 0:
                #TODO: open other cells with 0 instead of just adjacent cells
                for cell_obj in self.findAdjacentCells:
                    cell_obj.showCell()
            self.showCell()
            
            #If Mine Count == Cells Left Count, player wins
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "You win!", "Congratulations", 0)
                sys.exit()
        
        #TODO: prevent clicking on cells that are marked candidate mines

    #Interrupts the game and displays a message that the game is over
    def showMine(self):
        self.cell_button_object.configure(bg = "red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine!", "Game Over", 0)
        sys.exit()

    #Shows the number of cells that potentially has mines
    def showCell(self):
        if not self.is_opened:
            #Get the number of mines that could be adjacent
            self.cell_button_object.configure(text = self.getNumberOfMines)

            #Makes sure that the non-mine cell are in the right button color
            self.cell_button_object.configure(bg = "SystemButtonFace")

            #Prevents opened cell from being clicked
            self.cell_button_object.unbind("<Button-1>")
            self.cell_button_object.unbind("<Button-3>")

            #Replace the text of cell count label with updated count
            Cell.cell_count -= 1
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text = f"Cells Left: {Cell.cell_count}"
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
            self.cell_button_object.configure(bg = "yellow")
            self.is_flagged = True
        #Toggle color OFF
        else:
            self.cell_button_object.configure(bg = "SystemButtonFace")
            self.is_flagged = False

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