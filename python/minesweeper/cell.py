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
    #A function that creates cell count label for the game
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
            #Reveals its own cell
            self.showCell()

            #Reveals other adjacent cells if the opened cell has 0 mines
            self.showAllAdjacent()
            
            #If Mine Count == Cells Left Count, player wins
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "You win!", "Congratulations", 0)
                sys.exit()
        
    #TODO: prevent clicking on cells that are marked candidate mines

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

#TODO: change the behavior of showing zero-mine cells to expand (not just the adjacent of the clicked cell) DONE
#BUG:  a zero cell that's diagonal to another zero cell causes to expand to other cells
#TODO: prevent from left clicking flagged cells
#TODO: change the button color of zero cells DONE
#TODO: add a counter for flagged cell. it should have the same amount of mines. limit the number of cells to be flagged
#TODO: change text size of the button to be a little bit bigger