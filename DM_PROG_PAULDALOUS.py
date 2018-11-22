#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 12:34:58 2018
@author: paul

### README ###
This program aims to create a maze with an interface where user visualizes a red circle into a maze and tries to reach the end.
Thus, we defined a class Caneva which aims to create the Canvas object (from the Tkinter library) representing the maze.
The Maze class inherits Caneva class and handles the event up, down right and left from the user, trigered by the keyboard.
"""

# Import de Tkinter - Python 3
from tkinter import *


class Caneva():
    '''
    Caneva CLass which creates the Canvas object (from the Tinter python library)
    '''

    def __init__(self):

        FO = open('oeuvres.txt', "r+")
        self.FILE = self.extract_structure_from_file(FO.readlines())
        print(self.FILE)
        # Creating the main window
        self.WINDOW = Tk()
        self.WINDOW.title('Pion')

        # Canvas parameters definition
        #self.X = 25
        #self.Y = 50
        self.SQUARE_SIZE = 50 # Size of the SQUAREs representing the unit block for building the maze = side of a square in pixels
        self.WIDTH = len(self.FILE[0])*self.SQUARE_SIZE # Width of the window
        self.HEIGHT = len(self.FILE)*self.SQUARE_SIZE # Height of the window
        self.LIST_SQUARE_CENTERS, self.DEPARTURE_X, self.DEPARTURE_Y, self.ARRIVE_X, self.ARRIVE_Y = self.create_list_of_square_centers(self.FILE) # List containing the (x,y) of each black squares to build the maze
        self.X, self.Y = self.DEPARTURE_X, self.DEPARTURE_Y
        #print(self.LIST_SQUARE_CENTERS)
        self.LIST_SQUARE_EDGES = self.center_to_edges_squares(self.LIST_SQUARE_CENTERS) # List containing the (x1,y1,x2,y2) quadruples for two edges of each square. Useful for drawing the squares with Tkinter

        # Canvas definition
        self.CANEVAS = Canvas(self.WINDOW, width = self.WIDTH, height = self.HEIGHT, bg ='white')
        self.PAWN = self.CANEVAS.create_oval(self.X-0.5*self.SQUARE_SIZE,self.Y-0.5*self.SQUARE_SIZE,self.X+0.5*self.SQUARE_SIZE,self.Y+0.5*self.SQUARE_SIZE,width=2,outline='black',fill='red')
        self.CANEVAS.focus_set()
        self.create_maze(self.LIST_SQUARE_EDGES)

    # Function definition section

    def extract_structure_from_file(self, list_of_lines):
        '''
        Extract a matrix - in a form of a list of lists - taking the lines such as 0010111\n as argument
        '''
        matrix = []
        for line in list_of_lines:
            vector = []
            for caracter in line:
                if (caracter!='\n'):
                    vector = vector + [caracter]
            matrix = matrix + [vector]
        return(matrix)

    def create_list_of_square_centers(self, a_file):
        '''
        Create the list of squares' center, initial position of the pawn X and Y, and arrival position ArriveX and ArriveY
        '''

        list_of_square_centers = []
        column_counter = 0

        for a_line in a_file:
            line_counter = 0
            list_builder = []

            for a_caracter in a_line:

                if a_caracter=='1':
                    list_builder = list_builder + [[0.5*self.SQUARE_SIZE + line_counter*self.SQUARE_SIZE, 0.5*self.SQUARE_SIZE + column_counter*self.SQUARE_SIZE]]
                elif a_caracter=='i':
                    X = 0.5*self.SQUARE_SIZE + line_counter * self.SQUARE_SIZE
                    Y = 0.5*self.SQUARE_SIZE + column_counter * self.SQUARE_SIZE
                elif a_caracter=='o':
                    ArriveX = 0.5*self.SQUARE_SIZE + line_counter * self.SQUARE_SIZE
                    ArriveY = 0.5*self.SQUARE_SIZE + column_counter * self.SQUARE_SIZE
                line_counter += 1

            list_of_square_centers = list_of_square_centers + list_builder
            column_counter +=1

        return(list_of_square_centers, X, Y, ArriveX, ArriveY)

    def center_to_edges_squares(self, list_of_center):
        '''
        Create the list of squares' edges from the list of squares' center
        '''
        liste_of_edges = []
        for center_coords in list_of_center:
            liste_of_edges = liste_of_edges + [[float(center_coords[0] - 0.5*self.SQUARE_SIZE), float(center_coords[1] - 0.5 * self.SQUARE_SIZE), float(center_coords[0] + 0.5 * self.SQUARE_SIZE), float(center_coords[1] + 0.5 * self.SQUARE_SIZE)]]
        return (liste_of_edges)

    def create_maze(self, list_of_edges):
        '''
        Draw the squares in the canvas taking the list of square edges as argument
        '''
        for edges in list_of_edges:
            self.CANEVAS.create_rectangle(edges[0], edges[1], edges[2], edges[3], fill='black')


#Caneva('oeuvres.txt')

class Maze(Caneva):
    '''
    Maze CLass which creates the Cthe maze. Inherits the Caneva class.
    '''
    def __init__(self):
        self.NUMBER_OF_MOVE = 0
        Caneva.__init__(self)
        self.CANEVAS.bind('<Key>',self.keyboard)
        self.CANEVAS.pack(padx =5, pady =5)
        Button(self.WINDOW, text ='Quitter', command = self.WINDOW.destroy).pack(side=LEFT,padx=5,pady=5)
        Button(self.WINDOW, text ='Recommencer', command = self.restart).pack(side=LEFT,padx=5,pady=5)
        self.WINDOW.mainloop()
        
    def keyboard(self, event):
        '''
        Upload the position of the pawn for each action of the user
        '''
        self.touche = event.keysym
        print(self.touche) 
        if (self.X, self.Y) == (self.ARRIVE_X, self.ARRIVE_Y) and (self.NUMBER_OF_MOVE>0):
            self.win()

        if self.touche == 'Up' :
            if [self.X, self.Y-self.SQUARE_SIZE] not in self.LIST_SQUARE_CENTERS:
                self.Y -= self.SQUARE_SIZE
                self.NUMBER_OF_MOVE +=1
            else:
                print('Déplacement impossible')
        if self.touche == 'Down':
            if [self.X, self.Y+self.SQUARE_SIZE] not in self.LIST_SQUARE_CENTERS:
                self.Y += self.SQUARE_SIZE
                self.NUMBER_OF_MOVE +=1
            else:
                print('Déplacement impossible')
        if self.touche == 'Right':
            if [self.X+self.SQUARE_SIZE, self.Y] not in self.LIST_SQUARE_CENTERS:
                self.X += self.SQUARE_SIZE
                self.NUMBER_OF_MOVE +=1
            else:
                print('Déplacement impossible')
        if self.touche == 'Left':
            if [self.X-self.SQUARE_SIZE, self.Y] not in self.LIST_SQUARE_CENTERS:
                self.X -= self.SQUARE_SIZE
                self.NUMBER_OF_MOVE +=1
            else:
                print('Déplacement impossible')

        # Draw the pawn at its new position
        self.CANEVAS.coords(self.PAWN,self.X -0.5*self.SQUARE_SIZE, self.Y -0.5*self.SQUARE_SIZE, self.X +0.5*self.SQUARE_SIZE, self.Y +0.5*self.SQUARE_SIZE)

    def restart(self):
        '''
        Restart the game
        '''
        self.X, self.Y = self.DEPARTURE_X, self.DEPARTURE_Y
        self.CANEVAS.coords(self.PAWN,self.DEPARTURE_X-0.5*self.SQUARE_SIZE,self.DEPARTURE_Y-0.5*self.SQUARE_SIZE,self.DEPARTURE_X+0.5*self.SQUARE_SIZE,self.DEPARTURE_Y+0.5*self.SQUARE_SIZE)
    
    def win(self):
        '''
        Print a window with a winning message
        '''
        win_window = Tk()
        win_window['bg']='white'
        p = PanedWindow(win_window, orient=HORIZONTAL)
        p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
        p.add(Label(p, text='Felicitation, Vous avez gagné', background='blue', anchor=CENTER))
        p.pack()
        win_window.mainloop()

# Instanciation of the Maze class 
Maze()
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
