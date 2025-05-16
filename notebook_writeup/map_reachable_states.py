'''
This script contains our code for mapping all of the reachable states in the space. 

In this script, we take the approach of direct simulation. We simulate playing a 
variety of opponents by playing two optimal policies against each other, and 
forcing player 2 to hold at random points in the game. This fills in the gaps in 
the state space. 
'''
import random, sys, pickle
import numpy as np 

# This makes imports around a directory a bit easier usually
sys.path.append('..')

def roll_die() -> int:
    '''
    Helper function to conduct a dice roll for us 
    '''
    return random.randint(1,6)

def game_pig(policy_player_1:np.ndarray, 
             policy_player_2:np.ndarray, 
             reachable:np.ndarray, 
             hold_probability:float) -> np.array:
    '''
    Function to conduct a game of pig for us. 
    
    Arguments:
        policy_player_1:np.array = numpy array containing 0s (do not roll) and 1s (roll) for player 1
        policy_player_2:np.array = numpy array containing 0s (do not roll) and 1s (roll) for player 2
        reachable:np.array = numpy array containing containing 0s (state not reached) and 1s (state reached) for player 2
        hold_probability:float = Probability that player 2 holds at random to simulate variety of opponents.

    Returns: 
        reachable:np.array = Updated array of states that can be reached. 
    '''
    # initialise some variables which are useful for the game
    scores = [0,0]
    player = 0 

    # enter a while loop for each game, set until completion of the game. 
    while max(scores) < 100:
        turn_total = 0
        # turn logic, enter an infinite loop which is broken out of when turn change logic is hit
        while True:
            roll = roll_die()
            if (player == 0 and policy_player_1.get((scores[0], scores[1], turn_total), 0)) or \
               (player == 1 and policy_player_2.get((scores[1], scores[0], turn_total), 0)):
                
                # This makes it bank at random points, simulating a variety of sub optimal opponents 
                if player == 1 and np.random.random() > hold_probability:
                    scores[player] += turn_total
                    break
                # else if you roll a 1, then turn also ends
                elif roll == 1:
                    turn_total = 0
                    break
                # else keep on spinning
                else:
                    turn_total += roll
                    # if you are player 1 (player 0 given 0 indexing), we should add in the state you 
                    # have just reached to this array
                    if player == 0:
                        reachable[min(scores[player], 100), min(scores[player-1], 100), min(turn_total, 100)] = 1
            # this logic is the player saying they do not want to roll. Hence, bank points accured up until now 
            else:
                scores[player] += turn_total
                # again, if you are player 1 (player 0 given 0 indexing), we should add in the state you 
                # have just reached to this array
                if player == 0:
                    reachable[min(scores[player], 100), min(scores[player-1], 100), 0] = 1
                break
        # swap players, return to upper while loop 
        player = 1 - player
    # finally we only return all of the states that have been reached, since this is all we care about here. 
    return reachable


def modelling_state_space(policy:np.array, 
                          reachable:np.array, 
                          iterations:int, 
                          hold_prob:float) -> np.array:
    '''
    Wrapper function to call to interact with the above game code. 
    Recursively reassigns the 'reachable' array with outputs of the function

    Arguments:
        policy:np.array = numpy array containing 0s (do not roll) and 1s (roll) for our players
        reachable:np.array = numpy array containing containing 0s (state not reached) and 1s (state reached) for player 2
        hold_probability:float = Probability that player 2 holds at random to simulate variety of opponents.

    Returns: 
        reachable:np.array = Final updated array of states that can be reached.     
    '''
    for _ in range(iterations):
        reachable = game_pig(policy, policy, reachable, hold_prob)
    return reachable



# Point of entry to script. We load in the policy, and allow population of the state
# space by generating a variety of policies using different hold probabilities
if __name__ == "__main__":
    # read pickle file
    with open('notebook_writeup/pickle_and_config_files/policy_dictionary.pkl', 'rb') as f:
        policy = pickle.load(f)

    # initialising our reachable states array
    reachable_states = np.zeros((101, 101, 101))
    for prob in [0, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5]:
        reachable_states = modelling_state_space(reachable_states, iterations = 10**6, hold_prob = prob)
        print(f'finished looping for p = {prob}', flush = True)

    # write to pickle file in desired location
    with open('notebook_writeup/pickle_and_config_files/reachable_states.pkl', 'wb') as f:
        pickle.dump(reachable_states, f)    