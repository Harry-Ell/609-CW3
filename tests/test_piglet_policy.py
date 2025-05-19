'''
The content of this test is testing the equality of 
the extracted policy of the game of piglet.

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
from notebook_writeup.piglet import PigletSolver
 

def test_piglet_policy():
    '''
    Standard pig game setup policy generation + test
    '''

    solver = PigletSolver(goal=2, epsilon=1e-5)
    solver()  # runs value iteration

    generated_policy = solver.get_policy()
    
    # read in a pre generated verion of the policy 
    with open('tests/data/full_piglet_policy.pkl', 'rb') as d:
        correct_policy = pickle.load(d)

    # and finally test their equality 
    assert_array_equal(generated_policy, correct_policy)
