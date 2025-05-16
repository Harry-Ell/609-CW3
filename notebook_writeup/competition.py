'''
Collection of code written by billie and jasmine which can return all of the relevant analytics to us 
regarding any instance of the contest
'''

import numpy as np

class Competition:

    def __init__(self, player1, player2, replications, seed):
        self.player1_policy = player1 # i think this works for these two being numpy arrays
        self.player2_policy = player2
        self.reps = replications
        self.start_seed = seed

    def _turn(self, state, pol):
        roll = 0
        while roll != 1 and pol[min(state[0], 100), min(state[1], 100), min(state[2], 100)] == 1:
            roll = np.random.randint(1, 7)
            if roll != 1:
                state = (state[0], state[1], state[2] + roll)

        if roll == 1:
            state = (state[0], state[1], 0)  # Turn lost, no points added
        else:
            state = (state[0] + state[2], state[1], 0)  # Bank the turn total

        return (state[1], state[0], 0)  # Swap turns

    def _game(self, policy1, policy2):
        state = (0, 0, 0)
        turn_counter = 0
        while True:
            state = self._turn(state, policy1)
            turn_counter += 1
            if state[1] >= 100:
                return 1
            state = self._turn(state, policy2)
            turn_counter += 1
            if state[1] >= 100:
                return 0
          
    def __call__(self):
        '''
        Call method by which we will interact with the class 
        '''
        np.random.seed(self.start_seed)
        win_sum = 0
        for i in range(self.reps):
            win_sum += self._game(self.player1_policy, self.player2_policy)
        return win_sum/self.reps
    
class Opponents:
    '''
    is a class really needed here? most likely not 
    '''
    def hold_at_n(n):
        policy = np.ones((100+1, 100+1, 100+1), np.int64)
        # basic hold at n aspect of strat
        policy[:, :, n:] = 0

        # supplement to make them hold when they could win 
        for i in range(101):
             for k in range(101):
                 if i + k >= 100:
                     policy[i, :, k] = 0
        return policy


    def sophies_policy(self):
        pass