'''
The content of this test is testing the equality of 
the extracted policy of the game of pig.

This is quite a broad test, and hence we note the 
purpose of this is not intermediate testing, rather 
it checks for a properly configured environment.

This test will be ran once if the instructions in 
`getting started` of the readme are followed. 
'''

import sys
import os
import pickle
import numpy as np
from numpy.testing import assert_array_equal


# coding in relative imports in a flexible manor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Loading in the module to be tested. 
from notebook_writeup.optimised_layered_vi import pig_layered_value_iteration
 

def test_pig_policy():
    '''
    Standard pig game setup policy generation + test
    '''

    TARGET_SCORE = 100
    DICE_SIZE = 6
    MAX_TURN = 100

    # run the module to be tested
    _, generated_policy = pig_layered_value_iteration(target_score=TARGET_SCORE, 
                                            die_sides=DICE_SIZE, 
                                            max_turn=MAX_TURN, 
                                            epsilon=1e-6)
    
    # read in a pre generated verion of the policy 
    with open('tests/data/full_pig_policy.pkl', 'rb') as d:
        correct_policy = pickle.load(d)

    # and finally test their equality 
    assert_array_equal(generated_policy, correct_policy)

