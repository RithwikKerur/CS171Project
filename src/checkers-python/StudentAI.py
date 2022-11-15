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


    def move_kings(self, move, color):
        if color == 2:
            if move[-1][0] == 0:
                return True
            return False
        if color == 1:
            if move[-1][0] == self.board.row - 1:
                return True
            return False

    def get_heuristic(self, color): # returns the piece differential for the selected color
        if color == 2: #we are counting the white differential
            return self.board.white_count - self.board.black_count
        return self.board.black_count - self.board.white_count



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