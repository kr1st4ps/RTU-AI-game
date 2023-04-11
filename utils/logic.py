#   This file contains all the logic behind AIs moves

from collections import Counter

class game_state():
    registry = []
    maximizer = None
    minimizer = None

    def __init__(self, player_score, ai_score, available_numbers, depth, next_move, parents=[]):
        #   Both player scores
        self.player_score = player_score
        self.ai_score = ai_score
        
        #   Numbers yet to be taken by players
        self.available_numbers = available_numbers
        
        #   Depth within the game tree
        self.depth = depth

        #   Which player has the turn
        self.next_move = next_move

        #   List of current states parents
        self.parents = parents

        #   List of current states children and their minimax values
        self.children = []
        self.children_minimax = []

        #   Minimax value
        self.minimax = None

    #   Logic behind how to determine if two objects are equal
    def __eq__(self, other):
        if isinstance(other, game_state):
            return (self.player_score == other.player_score and 
                    self.ai_score == other.ai_score and 
                    sorted(self.available_numbers) == sorted(other.available_numbers) and 
                    self.depth == other.depth and 
                    self.next_move == other.next_move)
        return False
    
    #   Logic behind printing this object
    def __str__(self):
        return f"Player - {self.player_score}\t\t|AI - {self.ai_score}\t\t|Nums - {self.available_numbers}\t\t|MINIMAX - {self.minimax}\t\t|Parents - {len(self.parents)}\t\t|Children{len(self.children)}"
    
    #   Function that adds object to registry
    def add_to_registry(self):
        self.registry.append(self)

    #   Generate next level in the game tree
    def generate_level(self, level):
        #   Boolean to inform when the tree is fully created
        created_new_state = False

        #   Loops through each state in the registry with the given level, and creates their child states
        for state in game_state.registry:
            if state.depth == level:
                #   Creates the child state if the current state is not a terminal one
                if state.player_score > 0 and state.ai_score > 0 and len(state.available_numbers) > 0:
                    created_new_state = True
                    #   Loops through all possible unique moves and creates child states using them
                    combinations = set()
                    for i_index, i_value in enumerate(state.available_numbers):
                        for j_index, j_value in enumerate(state.available_numbers):
                            if i_index != j_index and (i_value, j_value) not in combinations and (j_value, i_value) not in combinations:
                                combinations.add((i_value, j_value))
                                numbers = state.available_numbers.copy()
                                numbers.remove(i_value)
                                numbers.remove(j_value)
                                if state.next_move == "AI":
                                    child = game_state(state.player_score, state.ai_score - i_value * j_value, numbers, state.depth + 1, "Player 1", [state])
                                elif state.next_move == "Player 1":
                                    child = game_state(state.player_score - i_value * j_value, state.ai_score, numbers, state.depth + 1, "AI", [state])

                                #   If the created state already exists, then add the current state to the existing ones parents
                                for newstate in game_state.registry:
                                    if child == newstate:
                                        newstate.parents.append(state)
                                        state.children.append(newstate)
                                #   If created state is a new one, then add it to current states children and add it to the registry
                                if child not in game_state.registry:
                                    state.children.append(child)
                                    child.add_to_registry()

        return created_new_state

    #   Function to create all level and game states of the game tree         
    def generate_tree(self):
        val = 1
        while True:
            test = self.generate_level(val)
            val+=1
            if not test:
                break

    
    #   Function to evaluate all states in the game tree
    def minimax_evaluation(self):
        #   If state has no child states, then it is the end state of the game
        if len(self.children) == 0:
            #   Check winner and add minimax value accordingy
            winner = self.check_winner()
            if winner == game_state.minimizer:
                self.minimax = -1
            elif winner == game_state.maximizer:
                self.minimax = 1
            else:
                self.minimax = 0

            #   Add minimax value to all parents of state
            for parent in self.parents:
                parent.children_minimax.append(self.minimax)
        
        #   Otherwise determine minimax value using child state minimax values
        else:
            #   If any child does not have minimax value, then find it
            if len(self.children) != len(self.children_minimax):
                for child in self.children:
                    if child.minimax == None:
                        child.minimax_evaluation()
            
            #   Check child state minimax values and add minimax value accordingy
            if self.next_move == game_state.maximizer:
                self.minimax = max(self.children_minimax)
            if self.next_move == game_state.minimizer:
                self.minimax = min(self.children_minimax)

            #   Add minimax value to all parents of state
            for parent in self.parents:
                parent.children_minimax.append(self.minimax)
    

    #   Check if there is a winner
    def check_winner(self):
        if self.player_score == 0 or self.ai_score < 0:
            return "Player 1"
        elif self.ai_score == 0 or self.player_score < 0:
            return "AI"
        elif self.player_score < self.ai_score:
            return "Player 1"
        elif self.ai_score < self.player_score:
            return "AI"
        else:
            return "TIE"
        

    #   Set who is the minimizer and who is the maximizer
    def set_mini_maxi_players(self):
        if self.next_move == "Player 1":
            game_state.maximizer = "Player 1"
            game_state.minimizer = "AI"
        else:
            game_state.minimizer = "Player 1"
            game_state.maximizer = "AI"
    

    #   Function to choose the best move of the avaialable
    def ai_choose_move(self):
        #   Find which value is the best AI can choose from
        value = None
        if "AI" == game_state.maximizer:
            value = max(self.children_minimax)
            print(f"AI is maximizer, his best value appereantly is {value}")
        elif "AI" == game_state.minimizer:
            value = min(self.children_minimax)
            print(f"AI is minimizer, his best value appereantly is {value}")

        print(f"AI can choose from {self.children_minimax}")

        #   Find the state with the best possible value and find what move to take to get it
        for state in self.children:
            if state.minimax == value:
                c1 = Counter(self.available_numbers)
                c2 = Counter(state.available_numbers)
                try:
                    v1, v2 = c1 - c2
                except:
                    v1 = v2 = next(iter(c1 - c2))
                
                return v1, v2