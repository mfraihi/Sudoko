#!/usr/bin/env python
import random
board = [None] * 81

def display():
    for x in range(0, len(board)):
        print board[x],
        if (x+1)%3 == 0 and x > 0 and (x+1)%9 != 0:
            print " | ",
        if (x+1)%27 == 0:
            print "\n--------------------------"
        elif (x+1)%9 == 0:
            print

def init_board():
    while None in board:
        for location in range(0, len(board)):
            invalid_number = True
            while(invalid_number):
                new_numb = random.randint(1, 9)
                
                if determine_box(board, new_numb, location)  and determine_col(board, new_numb, location) and determine_row(board, new_numb, location):
                    invalid_number = False
                
            board[location] = new_numb
            invalid_number = True
            display()
    display()
        

def determine_box(board, new_numb, location):
    boxes = [
                [0, 1, 2, 9, 10, 11, 18, 19, 20],     #box1
                [3, 4, 5, 12, 13, 14, 21, 22, 23],    #box2
                [6, 7, 8, 15, 16, 17, 24, 25, 26],    #box3
                
                [27, 28, 29, 36, 37, 38, 45, 46, 47], #box4
                [30, 31, 32, 39, 40, 41, 48, 49, 50], #box5
                [33, 34, 35, 42, 43, 44, 51, 52, 53], #box6
                
                [54, 55, 56, 62, 63, 64, 72, 73, 74], #box7
                [57, 58, 59, 65, 66, 67, 75, 76, 77], #box8
                [60, 61, 62, 68, 69, 70, 78, 79, 80]  #box9
        ]
    
    #print "location = ", location
    for box_num in range(0, len(boxes)):
        if location in boxes[box_num]:
            location_list = boxes[box_num]
            
            break
    
    #print "location list = ", location_list
    for loc in location_list:
        if board[loc] == new_numb:
            #print board[loc], " && ", new_numb
            #print False
            return False
    return True
        
def determine_row(board, new_numb, location):
    
    while(location % 9 != 0):
        location-=1
    location = (location/9)
    location_list =  range(9*(location), (9*location)+9)

    print "row list = ", location_list
    for loc in location_list:
        if board[loc] == new_numb:
            return False
    
    return True
    
def determine_col(board, new_numb, location):
    
    while(location>9):
       location = location - 9
    
    if(location%9==0): location=location-9 #exception for cols multiple of 9
    
    location_list = range(location, 90, 9)[:9]
    #print "new num = ", new_numb
    #print "col list = ", location_list
    for loc in location_list:
        if board[loc] == new_numb:
            return False
        
    return True
    
init_board()
display()

#print "Box: ", determine_box()

#location = 9

#print "Row: ",
#determine_row(board, 4, location)
#print "Col: ", 
#determine_col(location)