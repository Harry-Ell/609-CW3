'''
This script contains our code for mapping all of the reachable states in the space.

We take the approach of direct simulation: two optimal policies play against each other,
but player 2 is forced to hold at random points in order to fill in gaps in the reachable state space.
'''

import random
import sys
import pickle
import numpy as np
from typing import Any

# This makes imports around a directory a bit easier usually
sys.path.append('..')


def roll_die() -> int:
    """
    Helper function to simulate a fair 6-sided die roll.

    Returns:
        int: A random integer from 1 to 6.
    """
    return np.random.randint(1, 7)


def game_pig(policy_player_1: np.ndarray,
             policy_player_2: np.ndarray,
             reachable: np.ndarray,
             hold_probability: float) -> np.ndarray:
    """
    Simulates one game of Pig and updates reachable states for player 1.

    Args:
        policy_player_1 (np.ndarray): A 3D array [i][j][k] with 1 = roll, 0 = hold for player 1.
        policy_player_2 (np.ndarray): A 3D array with the same structure for player 2.
        reachable (np.ndarray): A 3D array tracking which states are reached (1) or not (0).
        hold_probability (float): Probability that player 2 randomly decides to hold, simulating varied opponents.

    Returns:
        np.ndarray: The updated reachable array after one simulated game.
    """
    scores = [0, 0]
    player = 0

    while max(scores) < 100:
        turn_total = 0
        while True:
            roll = roll_die()

            if (player == 0 and policy_player_1[scores[0], scores[1], turn_total]) or \
               (player == 1 and policy_player_2[scores[1], scores[0], turn_total]):

                # Player 2 randomly chooses to hold (to simulate suboptimality)
                if player == 1 and np.random.random() > hold_probability:
                    scores[player] += turn_total
                    break

                elif roll == 1:
                    turn_total = 0
                    break

                else:
                    turn_total += roll
                    if player == 0:
                        # Record the reached state for player 1
                        reachable[min(scores[player], 100), min(scores[player - 1], 100), min(turn_total, 100)] = 1

            else:
                scores[player] += turn_total
                if player == 0:
                    reachable[min(scores[player], 100), min(scores[player - 1], 100), 0] = 1
                break

        # Swap players
        player = 1 - player

    return reachable


def modelling_state_space(policy: np.ndarray,
                          reachable: np.ndarray,
                          iterations: int,
                          hold_prob: float) -> np.ndarray:
    """
    Simulates many games to explore reachable state space under stochastic variation.

    Args:
        policy (np.ndarray): A 3D policy array [i][j][k] for both players (shared policy).
        reachable (np.ndarray): The running reachable-state map to update.
        iterations (int): Number of game simulations to perform.
        hold_prob (float): Probability player 2 will hold at random during their turn.

    Returns:
        np.ndarray: The updated reachable state space after simulation.
    """
    for _ in range(iterations):
        reachable = game_pig(policy, policy, reachable, hold_prob)
    return reachable


# Brute-force mapping of reachable states
if __name__ == "__main__":
    # Generate the optimal policy 
    from optimised_layered_vi import pig_layered_value_iteration

    die_size = 6
    target_score = 100
    max_turn = 100

    _, policy = pig_layered_value_iteration(target_score=target_score,
                                            die_sides=die_size,
                                            max_turn=max_turn,
                                            epsilon=1e-6)

    # Initialise 3D array to track which (i, j, k) states are reached by player 1
    reachable_states = np.zeros((101, 101, 101))

    for prob in [0, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        reachable_states = modelling_state_space(policy, reachable_states, iterations=10**6, hold_prob=prob)
        print(f'finished looping for p = {prob}', flush=True)

    with open('notebook_writeup/pickle_and_config_files/reachable_states.pkl', 'wb') as f:
        pickle.dump(reachable_states, f)
