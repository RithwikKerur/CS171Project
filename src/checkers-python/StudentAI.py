from random import randint
from BoardClasses import Move
from BoardClasses import Board
from math import sqrt
from numpy import log
import sys
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class node:
    #class for nodes in MCTS
    def __init__(self, move, num_simulations, num_parent_wins, parent):
        self.move = move #the move parent made to get to this node
        self.num_simulations: int = num_simulations #si in slides
        self.num_parent_wins: int =  num_parent_wins #wi in slides
        self.children = [] #list of child nodes
        self.parent: node = parent #if root, should be null
 
    
    def get_uct(self, exploration_parameter = 1): 
        return = (exploration_parameter * sqrt(log(self.parent.num_simulations) / self.num_simulations)) + (self.num_parent_wins / self.num_simulations)

    def add_child(self, new_child: node):
        'adds a child to the children list'
        children.append(new_child)

    def back_propogate(self, is_win: bool):
        'adds the result to the stats and propogates it up to the parent'
        self.num_simulations += 1
        if not is_win: # this counts parent wins, so if the current node is a loss, the parent node will have a victory
            self.num_parent_wins += 1
        
        if self.parent:
            self.propogate(not is_win) # it will alternate back and forth if it was a win, since half the nodes will be opponent moves that will count this as a loss
    
    def pick_best_move(self): #this function should only be called by the root node
        'returns the best move'
        return max(self.children, key = lambda x: x.num_parent_wins / x.num_simulations).move
            


class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        print('best move ')
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        print(f'color = {self.color}')
        moves = self.board.get_all_possible_moves(self.color)
        best_move, heuristic = self.recur_best_move(moves, 3, self.color)
        self.board.make_move(best_move, self.color)
        return best_move


    def move_kings(self, move, color) -> bool: # returns a boolean for if the move kings or not
        if color == 2:
            if move[-1][0] == 0:
                return True
            return False
        if color == 1:
            if move[-1][0] == self.board.row - 1:
                return True
            return False

    def get_heuristic(self, color): # returns the piece differential for the selected color
        heuristic = 0
        for row in range(self.board.row):
                for col in range(self.board.col):
                    if self.board.board[row][col].is_king and self.board.board[row][col].color == color:
                        heuristic += 3

        if color == 2: #we are counting the white differential
            return heuristic + self.board.white_count - self.board.black_count

        return heuristic + self.board.black_count - self.board.white_count



    def get_opponent_best_move(self, move): # returns the best move the opponent can make
        opp_color = 1
        if self.color == 1:
            opp_color = 2 #this ensures we always know the opponents color for testing
        self.board.make_move(move, self.color)

        moves = self.board.get_all_possible_moves(opp_color)

        heuristic = None
        best_move = None
        for row in moves:
            for move in row:
                self.board.make_move(move, opp_color) 

                temp = self.get_heuristic(opp_color)
                
                if heuristic == None or temp > heuristic:
                    heuristic = temp
                    best_move = move
                self.board.undo()


        self.board.undo()
        return heuristic



    def find_best_move(self, moves):
        heuristic = None
        best_move = None
        for piece in moves:
            for move in piece:
                if self.move_kings(move, self.color):
                    row, col = move[0]
                    if not self.board.board[row][col].is_king:
                        best_move = move
                        self.board.make_move(best_move, self.color) 
                        return best_move

                
                opp_hueristic = self.get_opponent_best_move(move)
                if heuristic == None or opp_hueristic < heuristic:
                    heuristic = opp_hueristic
                    best_move = move
                

        
        self.board.make_move(best_move, self.color) 
        return best_move


    def recur_best_move(self, moves, depth, color):
        '''
        print(f'depth = {depth} color = {color}')
        print(moves)
        print()
        '''
        if depth == 0:
            return (None, self.get_heuristic(self.color))
        elif len(moves) == 0:
            return (None, float('-inf'))
        heuristic = None
        best_move = None
        for piece in moves:
            for move in piece:
                #print(f'heuristic = {heuristic} depth = {depth}')
                self.board.make_move(move, color)
                #print(move)
                curr_moves = self.board.get_all_possible_moves(self.opponent[color])
                
                
                move1, temp = self.recur_best_move(curr_moves, depth-1, self.opponent[color])
                if color == self.color:
                    #Maximizing
                    if heuristic is None or temp > heuristic:
                        heuristic = temp
                        best_move = move
                else:
                    #Minimizing
                    if heuristic is None or temp < heuristic:
                        heuristic = temp
                        best_move = move

                self.board.undo()
                #print(f'ending heuristic = {heuristic} depth = {depth}')
                

        #print(f'returning {heuristic} depth = {depth}')
        return (best_move, heuristic)



