'''
Script for making up the rewards arrays which will be needed

Far from a lightweight implementation, however this should be as customisable as possible
'''

class Probability_Generator:

    def __init__(self, dice_size:int, game_size:int):
        self.dice_size:int = dice_size
        self.game_size:int = game_size
        self.actions:list[int, int] = [0,1] # 0 means stick, 1 means hit 

    def _upper_dict_generator(self):
        upper_dictionary = {}
        for i in range(self.game_size+1):
            for j in range(self.game_size+1):
                for k in range(self.game_size+1):
                    upper_dictionary[(i,j,k)] = self._lower_dict_generator(i,j,k)
        return upper_dictionary

    def _lower_dict_generator(self, 
                              i:int, # opponents score
                              j:int, # player score  
                              k:int  # players unbanked points
                              ):
        lower_dictionary = {}
        temp1, temp2 = {}, {}
        for action in self.actions:
            if action == 0: # if we are sticking, gaurenteed to happen
                temp1[(i, min(self.game_size, j+k), 0)] = 1 
            elif action == 1: # we are hitting,
                temp2[(i, j, 0)] = 1 / self.dice_size 
                for roll_outcome in range(2, self.dice_size + 1):
                    temp2[(i, j, k + roll_outcome)] = 1 / self.dice_size 
                 

        lower_dictionary[0] = temp1
        lower_dictionary[1] = temp2
        return lower_dictionary
    
    def __call__(self):
        return self._upper_dict_generator()