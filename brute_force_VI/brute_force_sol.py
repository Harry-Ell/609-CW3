import sys 
import pickle
sys.path.append('..')

# my packages
from probability_generator import Probability_Generator
from rewards_generator import Rewarder
from MDP import GenericMDP



# we could tidy up the api a lot to make it so that we dont have to define all these extra things 
game_size = 100
dice_size = 6
states = [(i, j, k) for i in range(game_size) for j in range(game_size) for k in range(game_size)]
actions = [0, 1]
discount_rate = 1
max_iterations = 1000


ps = Probability_Generator(dice_size, game_size)()
rs = Rewarder(dice_size, game_size)()

value_iteration = GenericMDP(states=states, 
                 actions = actions,
                 probabilities=ps, 
                 rewards=rs, 
                 discount_rate=discount_rate, 
                 max_iterations=max_iterations, 
                 tolerance = 1e-6)()

policy = value_iteration[0]
with open('brute_force_solution_3.pkl', 'wb') as f:
    pickle.dump(policy, f)