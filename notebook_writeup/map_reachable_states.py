'''
This is an experimental approach to the problem of mapping all reachable states. 

We put the optimal strategy against its self, forcing it to hold at random points 
to help fill in any gaps which may crop up in the space.  


'''
import random
import sys
import pickle
from numba import njit
import numpy as np 
import plotly.graph_objects as go 


sys.path.append('..')

with open('notebook_writeup/pickle_and_config_files/policy_dictionary.pkl', 'rb') as f:
    policy = pickle.load(f)


#dice roll
@njit
def roll_die():
    return random.randint(1,6)

# @njit
def game_pig(policy_player_1, policy_player_2, reachable, hold_probability):
    scores = [0,0]
    player = 0 

    while max(scores) < 100:
        turn_total = 0
        while True:
            # i would rather have this inside but it does not work there 
            roll = roll_die()
            if (player == 0 and policy_player_1.get((scores[0], scores[1], turn_total), 0)) or \
               (player == 1 and policy_player_2.get((scores[1], scores[0], turn_total), 0)):
                # i think this logic will just make it bank at random. 
                if player == 1 and np.random.random() > hold_probability:
                    # then we will bank at random
                    scores[player] += turn_total
                    break
                elif roll == 1:
                    turn_total = 0
                    break
                else:
                    turn_total += roll
                    if player == 0:
                        reachable[min(scores[player], 100), min(scores[player-1], 100), min(turn_total, 100)] = 1
            else:
                scores[player] += turn_total
                if player == 0:
                    reachable[min(scores[player], 100), min(scores[player-1], 100), 0] = 1
                break

        player = 1 - player
    return reachable


def modelling_state_space(reachable, iterations, hold_prob):
    # reachable = np.zeros((101, 101, 101))
    for i in range(iterations):
        reachable = game_pig(policy, policy, reachable, hold_prob)
    return reachable


# creating a function to plot our results as a decision surface



if __name__ == "__main__":
    reachable_states = np.zeros((101, 101, 101))
    for prob in [0, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5]:
        reachable_states = modelling_state_space(reachable_states, iterations = 10**6, hold_prob = prob)
        print(f'finished looping for p = {prob}')

