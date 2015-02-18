#!/usr/bin/env python
import random
import math
import time
import copy
import pygame
import sys
import webcolors
import msvcrt as m
import planes

draw_it = True

def display(board):
    for x in range(0, len(board)):
        for y in range(0, len(board[x])):
            
            print ("*" , end=" ") if board[x][y] is None else print (board[x][y], end=" ")
           # print("[" + str(x) + "][" + str(y) + "]", end=" ")
            if y == math.sqrt(grid)-1 or y == (math.sqrt(grid)*2)-1 and y+1 != grid:
                print (" | ", end="")
            if (y % (grid-1) == 0 and y > 0) and ((x+1) % math.sqrt(grid) == 0 and x > 0) and x < grid-1:
                print ("\n" + ("------" * int(grid/2)))
            elif (y+1)%grid == 0:
                print("\n")

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

class board:
    
    #initialize a new object board
    def __init__(self, grid,  diff):
        self.grid = grid #size of grid
        self.diff = diff #difficulty level
        self.chance = 3; #guess chances
        self.state = "o" #True: game still going, False: game is over (win or loss)
        self.board = [[None] * grid for i in range(0, grid)] #initilize array for board
        
        self.board = self.fill_board(self.board, grid, diff) 
    
    #fill board with numbers based on difficiulty level
    def fill_board(self, board, grid, diff):
        
        #prefill = self.determine_prefill()
        prefill = diff #temporary
        last_row = 0
        last_col = 0
        filled_count = 0
        
        #loop until we reach the targeted prefilled cells
        while filled_count < prefill:
            
            #time.sleep(0.5)
            #self.display()
            #print("\n")
            
            row, col = random.randint(0, grid-1), random.randint(0, grid-1) #pick random row, col on the board
            
            while board[row][col] is not None:
                row, col = random.randint(0, grid-1), random.randint(0, grid-1) #loop until finding an empty cell
            #else: print(self.board[x][y])
            
            board_to_validate = [row[:] for row in board]
            random_value = random.randint(1, grid)

            if self.validate(random_value, row, col):
                
                board_to_validate[row][col] = random_value 

                if(self.is_solvable(board_to_validate)):
                    board[row][col] = random_value
                    last_row = row
                    last_col = col
                    filled_count += 1
                else:
                    #if last initilization made board unsolvable, revert
                    board[last_row][last_col] = None
                    filled_count -= 1
        
        if draw_it:
            self.draw()
        else:
            self.display()
        return board
                        
    def determine_prefill(self):
        if self.diff == 1:
            return random.randint(35, 45)
        
        elif self.diff == 2:
            return random.randint(20, 30)
        
        else:
            return random.randint(2, 2)
    
    #displays the board in text to console
    def display(self):
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[x])):
                
                print ("*" , end=" ") if self.board[x][y] is None else print (self.board[x][y], end=" ")
               # print("[" + str(x) + "][" + str(y) + "]", end=" ")
                if y == math.sqrt(self.grid)-1 or y == (math.sqrt(self.grid)*2)-1 and y+1 != self.grid:
                    print (" | ", end="")
                if (y % (self.grid-1) == 0 and y > 0) and ((x+1) % math.sqrt(self.grid) == 0 and x > 0) and x < self.grid-1:
                    print ("\n" + ("------" * int(self.grid/2)))
                elif (y+1)%self.grid == 0:
                    print("\n")
    
    #draws the board using PyGame
    def draw(self):
        pygame.init()
        
        screen_edge = 400
        
        cell_count = self.grid * self.grid
        
        cell_edge = screen_edge / self.grid
        
        screen = pygame.display.set_mode((screen_edge+100, screen_edge))
        myfont = pygame.font.SysFont("calibri", 30)
    
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                #color_input = input("Enter color: ")
                rndm_clr = (255, 255, 255)
                value = str(self.board[row][col]) if self.board[row][col] is not None else "*"
                
                x = col*cell_edge
                y = row*cell_edge
                               
                pygame.draw.rect(screen,rndm_clr,(x, y,cell_edge,cell_edge), 3)          
        
            # render text
                
                if self.board[row][col] is not None:
                    value = str(self.board[row][col])
                    label = myfont.render(value, 1, webcolors.name_to_rgb("white"))
                else:
                    value = "*"
                    label = myfont.render(value, 1, webcolors.name_to_rgb("red"))
                
                
                #draw number on rectangle
                screen.blit(label, (x+(cell_edge/self.grid),y+(cell_edge/self.grid)))

               # pygame.time.wait(40)
        
        small_font = pygame.font.SysFont("calibri", 18)
        label = small_font.render("Chances: " + str(self.chance), 1, webcolors.name_to_rgb("white"))
        screen.blit(label, (screen_edge + 5, 0))
        
        pygame.event.pump()
        pygame.display.flip()

        if self.state ==  "w":
            pygame.display.quit()
    
    #inserts value into cell given row and col
    def insert(self, value, row, col):
        board_to_validate = [row[:] for row in self.board]
        board_to_validate[row][col] = value
        
        if value < 1 or value > self.grid:
            print("Invalid entry.")
            
        if self.is_solvable(board_to_validate) and self.validate(value, row, col):
            self.board[row][col] = value
            
            self.is_solved()
            if self.state ==  "w":
                print("You win!")
            
            if draw_it:
                self.draw()
            else:
                self.display()
             
        else:
            self.chance -= 1
            
            if(self.chance == 0):
                print("Incorrect! You lost")
                self.state = 'l'
                
            else:
                print("INCORRECT, you have " + str(self.chance) + " remaining")
        del board_to_validate
        
    #takes value, row and col and validates if the value exists in ROW, COL and BOX    
    def validate(self, value, row, col):
        #check row
        if value in self.board[row]:
            return False
        
        #check col
    
        for x in range(0, len(self.board)):
            if value == self.board[x][col]:
                return False
        
        
        row_min = int(math.floor(row/math.sqrt(self.grid)) * math.sqrt(self.grid)) if row > 0 else 0
        row_max = row_min + int(math.sqrt(self.grid))
        
        col_min = int(math.floor(col/math.sqrt(self.grid)) * math.sqrt(self.grid)) if col > 0 else 0
        col_max = col_min + int(math.sqrt(self.grid))
        #
        #
        #print(row_min)
        #print(row_max)
        #print(col_min)
        #print(col_max)
        box = []
        
        for x in range(row_min, row_max):
            for y in range(col_min, col_max):
                if self.board[x][y] is not None:
                    box.append(self.board[x][y])
        
       # print("Box = " + str(box))
        if value in box:
            return False
        else:
            return True
    
    #checks if board is solvable (returns solved board) or not solvable (returns FALSE)
    def is_solvable(self, board):
        row, col = find_unassigned_loc(board)
    
        if(row is None and col is None):
            return board
        
        for i in range(1, self.grid+1):
            if(self.validate(i, row, col)):
                board[row][col] = i
                if(self.is_solvable(board)):
                    return board
                
                board[row][col] = None
    
        return False

    #checks if the puzzle has been solved and turns state to 'w' if so
    def is_solved(self):
        flag = True
        for row in range(0, len(self.board)):
            if None in self.board[row]:
                flag = False
                break
                
        if(flag):
            self.state = 'w'
#                
#def generate_board(prefill):
#    board = [[None] * grid for i in range(0, grid)]
#    filled_count = 0
#    
#    
#    while filled_count < prefill:
#        
#        placed = False
#        row, col = random.randint(0, grid-1), random.randint(0, grid-1)
#        
#        while board[row][col] is not None:
#            row, col = random.randint(0, grid-1), random.randint(0, grid-1)
#        #else: print(board[x][y])
#        
#        while not placed:
#            board_to_validate = [row[:] for row in board]
#            random_value = random.randint(1, grid)
#            if validate(board_to_validate, row, col, random_value):
#                
#                board_to_validate[row][col] = random_value 
#
#                if(is_solvable(board_to_validate, 0)):
#                    placed = True
#                    board[row][col] = random_value               
#                    filled_count += 1
#                else:                    
#                    board[row][col] = None
#           
#        
#        #display(board)
#    return board
#
#
##returns the board if it's solv

def find_unassigned_loc(board):
    
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if(board[row][col] is None):
                return row, col
          
    return None, None

if __name__ == "__main__":
   # my_board = generate_board(10)
    
    #print("Initial board:")
    #display(my_board)
        
    #my_board = [[3, 1, 2, 4], [4, 2, 3, 1], [1, 3, 4, 2], [2, 4, 1, 3]]
    #my_board = [[None, 3, 1, None], [1, None, None, None], [None, None, None, 2], [None, 2, 4, None]]
    #
    #solved_board = is_solvable(my_board, True)
    #print(solved_board)
    #draw(my_board)
    
    my_board = board(9, 10)
    
    
    value = 0
    row = 0
    col = 0
    
    small_font = pygame.font.SysFont("calibri", 18)
    
    done = False
        
    while my_board.state == "o":
        
        while done == False:
            #row = int(input("Enter row: "))
            #col = int(input("Enter col: "))
            #value = int(input("Enter value: "))
            
            for event in pygame.event.get():
          
              # handle MOUSEBUTTONUP
              
              if event.type == pygame.QUIT:
                done = True
              if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
            
            my_board.draw()         
            #my_board.insert(value, row-1, col-1)
    
    # solved_board = is_solvable(my_board, True)
    
    #draw(solved_board)