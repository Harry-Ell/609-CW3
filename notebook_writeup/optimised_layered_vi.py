'''
This is an implementation of the layered value iteration approach found in 
the paper. We make use of numba to precompile for loops and eliminate any 
python overhead for the loop computations.
'''

import numpy as np
from numba import njit
from typing import Tuple


@njit
def _init_V_policy(target_score: int, max_turn: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Initialises the value and policy arrays for all reachable states.

    Args:
        target_score (int): The score required to win the game.
        max_turn (int): Maximum number of unbanked points to track (limits state space).

    Returns:
        Tuple[np.ndarray, np.ndarray]: Zero-initialised value array and default policy (all roll).
    """
    V = np.zeros((target_score + 1, target_score + 1, max_turn + 1))
    policy = np.ones((target_score + 1, target_score + 1, max_turn + 1), np.int64)

    for ps in range(target_score + 1):
        for os in range(target_score + 1):
            for t in range(max_turn + 1):
                if ps + t >= target_score:
                    V[ps, os, t] = 1.0
                    policy[ps, os, t] = 0
                elif os >= target_score:
                    V[ps, os, t] = 0.0
    return V, policy


@njit
def _layered_vi(V: np.ndarray,
                policy: np.ndarray,
                target_score: int,
                die_sides: int,
                max_turn: int,
                epsilon: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Executes layered value iteration over all states using backward induction.

    Args:
        V (np.ndarray): Value function array (updated in place).
        policy (np.ndarray): Policy array (0 = hold, 1 = roll).
        target_score (int): Score threshold to win the game.
        die_sides (int): Number of faces on the die.
        max_turn (int): Max turn total tracked.
        epsilon (float): Convergence threshold for iteration.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The converged value and policy arrays.
    """
    roll_values = np.arange(1, die_sides + 1)
    roll_prob = 1.0 / die_sides

    for score_sum in range(2 * target_score - 1, -1, -1):
        converged = False
        while not converged:
            max_diff = 0.0

            p_min = max(0, score_sum - target_score + 1)
            p_max = min(target_score, score_sum)

            for ps in range(p_min, p_max + 1):
                os = score_sum - ps
                if ps >= target_score or os >= target_score:
                    continue

                for t in range(max_turn + 1):
                    if ps + t >= target_score or os >= target_score:
                        continue

                    # Compute expected value of rolling
                    roll_value = 0.0
                    for k in range(roll_values.shape[0]):
                        r = roll_values[k]
                        if r == 1:
                            roll_value += roll_prob * (1.0 - V[os, ps, 0])
                        else:
                            new_t = t + r
                            if ps + new_t >= target_score:
                                roll_value += roll_prob * 1.0
                            elif new_t <= max_turn:
                                roll_value += roll_prob * V[ps, os, new_t]

                    # Compute value of holding
                    if ps + t >= target_score:
                        hold_value = 1.0
                    elif os >= target_score:
                        hold_value = 0.0
                    elif os + ps + t > score_sum:
                        hold_value = 1.0 - V[os, ps + t, 0]
                    else:
                        hold_value = 0.0

                    # Select better action
                    if roll_value >= hold_value:
                        new_v = roll_value
                        policy_val = 1
                    else:
                        new_v = hold_value
                        policy_val = 0

                    diff = abs(V[ps, os, t] - new_v)
                    if diff > max_diff:
                        max_diff = diff

                    V[ps, os, t] = new_v
                    policy[ps, os, t] = policy_val

            if max_diff < epsilon:
                converged = True

    return V, policy


def pig_layered_value_iteration(target_score: int = 15,
                                die_sides: int = 6,
                                max_turn: int = 15,
                                epsilon: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
    """
    Wrapper to perform layered value iteration from scratch.

    Args:
        target_score (int, optional): Score needed to win. Defaults to 15.
        die_sides (int, optional): Number of sides on the die. Defaults to 6.
        max_turn (int, optional): Maximum turn total to represent. Defaults to 15.
        epsilon (float, optional): Convergence threshold. Defaults to 1e-6.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Final value and policy arrays.
    """
    V, policy = _init_V_policy(target_score, max_turn)
    V, policy = _layered_vi(V, policy, target_score, die_sides, max_turn, epsilon)
    return V, policy
