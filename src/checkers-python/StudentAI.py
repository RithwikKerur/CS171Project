from random import randint
from BoardClasses import Move
from BoardClasses import Board
from math import sqrt, log
import sys
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class Node():
    #class for nodes in MCTS
    def __init__(self, color, move = None, parent = None):
        self.move = move #the move parent made to get to this node. If None, must be root node
        self.color = color #color of whose move it is. Always inverse to the parents
        self.num_simulations: int = 0 #si in slides
        self.num_parent_wins: int = 0 #wi in slides
        self.children = [] #list of child nodes
        self.parent = parent #if root, should be null
        self.current_child = 0 #index of what child we are currently expanding
        self.uct = 0
 
    
    def get_uct(self) -> float: 
        return self.uct

    def get_current_child(self):
        'returns the current child to be expanded'
        self.current_child += 1
        return self.children[self.current_child - 1]

    def add_children(self, moves: [[Move]], opp_color):
        'extends the list of children when given a list of moves'
        self.children.extend((Node(opp_color, move, self)  for piece in moves for move in piece))

    def back_propogate(self, winning_color): # returns the number of undos that need to be performed
        'adds the result to the stats and propogates it up to the parent'
        self.num_simulations += 1
        if winning_color != self.color: # this is a win for the move made associated with this node
            self.num_parent_wins += 1 #if the node is black, and the winning color is white, it should count as a win since the move associated with this node was made by a white piece



        if self.parent:
            self.uct = (1.4 * sqrt(log(self.parent.num_simulations+1) / self.num_simulations)) + (self.num_parent_wins / self.num_simulations)
            return self.parent.back_propogate(winning_color) + 1 # it will alternate back and forth if it was a win, since half the nodes will be opponent moves that will count this as a loss
        return 0
    
    def pick_best_move(self) -> Move: #this function should only be called by the root node
        'returns the best move'
        return max(self.children, key = lambda x: x.num_parent_wins / x.num_simulations).move
            
    def is_leaf_node(self) -> bool: 
        'returns whether the current node is a leaf node'
        return len(self.children) == 0
    
    def is_fully_expanded(self) -> bool:
        'returns whether all the children of this node have been expanded into'
        return len(self.children) == self.current_child
    



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

        #print(f'color = {self.color}')
        moves = self.board.get_all_possible_moves(self.color)
        #best_move, heuristic = self.recur_best_move(moves, 3, self.color)
        best_move = self.monte_carlo()
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


    def find_next_node(self, root):  # this is selection AND expansion
        'returns the node for MCTS to simulate off of'
        curr_node = root

        while not curr_node.is_leaf_node() and curr_node.is_fully_expanded(): #selection; keeps going till a node is terminal or has unexplored children
            curr_node = self.best_uct(curr_node) # best child UCT
            #print(f"Making Move: {curr_node.move}")
            self.board.make_move(curr_node.move, self.opponent[curr_node.color]) #keeps the board up to date for rollout purposes
            

        if curr_node.is_leaf_node(): #we need to add the children of the current node into the tree if it has no children
            curr_node.add_children(self.board.get_all_possible_moves(curr_node.color), self.opponent[curr_node.color]) # if terminal node, adds the children

        result =  curr_node.get_current_child() # returns new unexplored node 
        #print(f"Making Move: {result.move}")
        self.board.make_move(result.move, self.opponent[result.color])
        return result
            

    def pick_random_move(self, moves):
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        return moves[index][inner_index]

    def simulation(self, node): #rollout for MCTS, random moves
        current_color = self.opponent[node.color]
        num_moves = 0
        while not self.board.is_win(current_color):
            current_color = self.opponent[current_color] # flip color
            moves = self.board.get_all_possible_moves(current_color) 
            self.board.make_move(self.pick_random_move(moves), current_color) #make random move
            num_moves+=1

        for x in range(num_moves):
            self.board.undo()
        return current_color

        

    def best_uct(self, node):
        return max(node.children, key = lambda x: x.get_uct())

    def monte_carlo(self, iterations = 500): 
        
        root = Node(self.color)
        root.add_children(self.board.get_all_possible_moves(self.color), self.opponent[self.color])
        for _x in range(iterations):
            #print(f'mcts loop {_x+1}')
            node = self.find_next_node(root)
            winning_color = self.simulation(node) #do simulation here
            undos = node.back_propogate(winning_color)

            for _x in range(undos):
                self.board.undo()

        return root.pick_best_move()



