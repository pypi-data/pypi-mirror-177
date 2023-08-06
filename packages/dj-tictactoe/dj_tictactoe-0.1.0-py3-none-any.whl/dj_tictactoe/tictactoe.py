# TODO: 5. draw
# TODO: 6. check if any player has won
# TODO: 7. print win
import sys
class Tic_Tac_Toe:
    def __init__(self):
        self.grid = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.empty_cell = ["1", "2", "3", "4", "5" ,"6", "7", "8", "9"] 
        self.win_pattern = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]
        self.turn = True

    def Draw_Board(self): 
        print("{} | {} | {}".format(self.grid[0], self.grid[1], self.grid[2]))
        print("----------")
        print("{} | {} | {}".format(self.grid[3], self.grid[4], self.grid[5]))
        print("----------")
        print("{} | {} | {}\n".format(self.grid[6], self.grid[7], self.grid[8]))

    def UI(self):
        if self.turn:
            print("It's o's turn")
        else:
            print("It's x's turn")
        return input("Enter the number: ")
    
    def Check_Valid(self):
        self.user_input = self.UI()
        if self.user_input in self.empty_cell:
            self.empty_cell.remove(self.user_input)
            return True
        else:
            return False

    def Turn(self):
        if self.Check_Valid:
            if self.turn:
                 return "o"
            else:
                 return "x"
    
    def Draw(self):
        shape = self.Turn()
        if self.Check_Valid():
            self.grid[int(self.user_input) - 1] = shape
            if shape == "o":
                self.turn = False
            else:
                self.turn = True
        else:
            print("Invalid Number!!")
    
    def Win_Lose(self):
        for items in self.win_pattern:
            if self.grid[items[0] - 1] == "o" and self.grid[items[1] - 1] == "o" and self.grid[items[2] -1] == "o":
                print("o won")
                return True
            elif self.grid[items[0] - 1] == "x" and self.grid[items[1] - 1] == "x" and self.grid[items[2] -1] == "x":
                print("x won")
                return True
            else:
                if len(self.empty_cell) == 0:
                    print("It's draw")
                
            
    
    def Run(self):
        while True:
            self.Draw_Board()
            self.Draw()
            if self.Win_Lose():
                sys.exit()
                
    
