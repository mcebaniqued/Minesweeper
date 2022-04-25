from re import X
import tkinter as tk
import random
import settings
import cell

class Game(tk.Frame):
    cells = []
    matrix = []
    numberList=[1,2,3,4,5,6,7,8,9]

    def __init__(self):
        #Initiate window
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Sudoku")

        self.main_grid = tk.Frame(
            self,
            bg = "gray",
            bd = 2,
            #width = settings.WIDTH,
            #height = settings.HEIGHT
        )
        self.main_grid.grid(pady = (50,0)) #offset of 100 pixels from the top (this is where we put the score, buttons, etc)

        for _ in range(9):
            self.matrix.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        self.make_GUI()
        self.start_game()
        self.update_GUI()
        self.mainloop()
    
    def make_GUI(self):
        #Make the 9x9 grid
        for i in range(9):
            row = []
            for j in range(9):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg = settings.EMPTY_CELL_COLOR,
                    width = 50,
                    height = 50
                )
                cell_frame.grid(row = i, column = j, padx = 1, pady = 1)

                #Create a thicker border for big grids
                if i == 2 or i == 5:
                    cell_frame.grid(row = i, column = j, padx = 1, pady = (1, 2))
                if j == 2 or j == 5:
                    cell_frame.grid(row = i, column = j, padx = (1, 2), pady = 1)

                cell_number = tk.Label(self.main_grid, bg = settings.EMPTY_CELL_COLOR)
                cell_number.grid(row = i, column = j)

                cell_data = {"number": cell_number}
                row.append(cell_data)

                cell_frame.bind("<Button-1>", self.leftClick)
            self.cells.append(row)

        #Make the timer frame and label
        time_frame = tk.Frame(self)
        time_frame.place(relx = 0.9, rely = 0.05, anchor = "center")
        self.time_label = tk.Label(
            time_frame,
            text = "00:00",
            font = ("", 20)
        )
        self.time_label.grid(row = 0)
    
    #Remove the numbers of (81-x) number of cells, where x is number of cells based on difficulty
    def start_game(self):
        self.fill_grid(self.matrix)

        diff = settings.DIFFICULTY[1]
        for _ in range(81-random.choice(diff)):
            row = random.randint(0,8)
            col = random.randint(0,8)
            while(self.matrix[row][col] == 0):
                row = random.randint(0,8)
                col = random.randint(0,8)
            self.matrix[row][col] = 0


    #Randomly populate the grid with a completed game
    def fill_grid(self, grid):
        #Algorithm from https://www.101computing.net/sudoku-generator-algorithm/
        for i in range(0,81):
            row=i//9
            col=i%9
            if grid[row][col]==0:
                random.shuffle(self.numberList)      
                for value in self.numberList:
                    #Check that this value has not already be used on this row
                    if not(value in grid[row]):
                        #Check that this value has not already be used on this column
                        if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                            #Identify which of the 9 squares we are working on
                            square=[]
                            if row<3:
                                if col<3:
                                    square=[grid[i][0:3] for i in range(0,3)]
                                elif col<6:
                                    square=[grid[i][3:6] for i in range(0,3)]
                                else:  
                                    square=[grid[i][6:9] for i in range(0,3)]
                            elif row<6:
                                if col<3:
                                    square=[grid[i][0:3] for i in range(3,6)]
                                elif col<6:
                                    square=[grid[i][3:6] for i in range(3,6)]
                                else:  
                                    square=[grid[i][6:9] for i in range(3,6)]
                            else:
                                if col<3:
                                    square=[grid[i][0:3] for i in range(6,9)]
                                elif col<6:
                                    square=[grid[i][3:6] for i in range(6,9)]
                                else:  
                                    square=[grid[i][6:9] for i in range(6,9)]
                            #Check that this value has not already be used on this 3x3 square
                            if not value in (square[0] + square[1] + square[2]):
                                grid[row][col]=value
                                if self.checkGrid(grid):
                                    return True
                                else:
                                    if self.fill_grid(grid):
                                        return True
                break
        grid[row][col] = 0

    #A function to check if the grid is full
    def checkGrid(self, grid):
        for row in range(0,9):
            for col in range(0,9):
                if grid[row][col]==0:
                    return False

        #We have a complete grid!  
        return True 

    def update_GUI(self):
        for i in range(9):
            for j in range(9):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["number"].configure(
                            fg = settings.DEFAULT_NUMBER_COLOR,
                            font = ("", 25),
                            text = ""
                        )
                else:
                    self.cells[i][j]["number"].configure(
                            fg = settings.DEFAULT_NUMBER_COLOR,
                            font = ("", 25),
                            text = str(cell_value)
                        )

        #TODO: check for valid/invalid inputs and change the colors of numbers/cell accordingly
        
    def leftClick(self, event):
        pass


def main():
    root = tk.Tk()
    root.resizable(False, False)
    Game()

if __name__ == "__main__":
    main()