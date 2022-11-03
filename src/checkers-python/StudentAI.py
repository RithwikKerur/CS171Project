from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
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
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        print(move)
        print(self.color)
        print()
        #self.board.make_move(move,self.color)
        return self.find_best_move(moves)


    def find_best_move(self, moves):

        heuristic = None
        best_move = None
        print("AI")
        for row in moves:
            for move in row:
                print(move)
                self.board.make_move(move, self.color)

                
                if self.color == 2:
                    temp = self.board.white_count - self.board.black_count
                    if heuristic == None:
                        heuristic = temp
                        best_move= move
                    elif temp > heuristic:
                        heuristic = temp
                        best_move = move
                else:
                    temp = self.board.black_count - self.board.white_count
                    if heuristic == None:
                        heuristic = temp
                        best_move= move
                    elif temp > heuristic:
                        heuristic = temp
                        best_move = move
                self.board.undo()

        print("best move")
        print(best_move)
        self.board.make_move(best_move, self.color) 
        return best_move



