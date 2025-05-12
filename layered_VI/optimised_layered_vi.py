'''
This is an implementation of the layered value iteration approach found in 
the paper. We make use of numba to precompile for loops and eliminate any 
python overhead for the loop computations
'''

import pickle
import numpy as np
from numba import njit


@njit
def _init_V_policy(target_score, max_turn):
    V      = np.zeros((target_score+1, target_score+1, max_turn+1))
    policy = np.ones((target_score+1, target_score+1, max_turn+1), np.int64)

    for ps in range(target_score+1):
        for os in range(target_score+1):
            for t in range(max_turn+1):
                if ps + t >= target_score:
                    V[ps, os, t]      = 1.0
                    policy[ps, os, t] = 0
                elif os >= target_score:
                    V[ps, os, t] = 0.0
    return V, policy

# Core layered value-iteration
@njit
def _layered_vi(V, policy, target_score, die_sides, max_turn, epsilon):
    # small fixed array rather than Python list
    roll_values = np.arange(1, die_sides+1)
    roll_prob   = 1.0 / die_sides

    # we go from high sums to low
    for score_sum in range(2*target_score-1, -1, -1):
        converged = False
        while not converged:
            max_diff = 0.0

            # loop over all (ps, os) with ps+os == score_sum
            p_min = max(0, score_sum - target_score + 1)
            p_max = min(target_score, score_sum)
            for ps in range(p_min, p_max+1):
                os = score_sum - ps
                if ps >= target_score or os >= target_score:
                    continue

                for t in range(max_turn+1):
                    if ps + t >= target_score or os >= target_score:
                        continue

                    # --- ROLL value ---
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

                    # --- HOLD value ---
                    if ps + t >= target_score:
                        hold_value = 1.0
                    elif os >= target_score:
                        hold_value = 0.0
                    elif os + ps + t > score_sum:
                        hold_value = 1.0 - V[os, ps + t, 0]
                    else:
                        hold_value = 0.0

                    # choose best
                    if roll_value >= hold_value:
                        new_v      = roll_value
                        policy_val = 1
                    else:
                        new_v      = hold_value
                        policy_val = 0

                    # update & track convergence
                    diff = abs(V[ps, os, t] - new_v)
                    if diff > max_diff:
                        max_diff = diff

                    V[ps, os, t]      = new_v
                    policy[ps, os, t] = policy_val

            if max_diff < epsilon:
                converged = True

# wrapper function to call precompiled other functions
def pig_layered_value_iteration_numba(
    target_score=15,
    die_sides=6,
    max_turn=15,
    epsilon=1e-6
):
    V, policy = _init_V_policy(target_score, max_turn)
    _layered_vi(V, policy, target_score, die_sides, max_turn, epsilon)
    return V, policy

if __name__ == "__main__":
    # running the layered value iteration function
    die_size = 6
    target_score = 100
    max_turn = 100
    V, policy = pig_layered_value_iteration_numba(target_score=target_score, 
                                                  die_sides=die_size, 
                                                  max_turn=max_turn, 
                                                  epsilon=1e-6)
    policy_dict = {}
    for player_score in range(0,101):
        for opponent_score in range(0,101):
            for turn_total in range(0,101):
                policy_dict[(player_score, opponent_score, turn_total)] = policy[player_score, opponent_score, turn_total]
    with open('layered_VI/policy_dictionary.pkl', 'wb') as f:
        pickle.dump(policy, f)