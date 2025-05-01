'''
Heavily trimmed submission from cw2, should be lightweight 
'''

import numpy as np 
import matplotlib.pyplot as plt


class GenericMDP:
    '''
    Trimmed implementation of my value iteration solver submitted for the earlier coursework. 
    '''
    def __init__(self, 
                 states:list[tuple], 
                 actions:list[tuple], 
                 probabilities:dict[dict[dict]], 
                 rewards:dict[dict[dict]], 
                 discount_rate:float, 
                 max_iterations:int,
                 tolerance:float = 1e-6):

        self.tolerance = tolerance
        self.goal_state = 100
        self.states = states
        self.actions = actions
        self.probabilities = probabilities
        self.discount_rate = discount_rate
        self.max_iter = max_iterations
        self.rewards_dict = rewards



    def __bellmans_eq(self, state:tuple, values_dict:dict, extract_policy:bool = False)->float:
        '''
        This is a generic implementation of the Bellmans equation as found in textbook 
        linked in the repository. 

        Args:
            state (tuple): Current state for which we are updating the value of .
            values_dict (dict): Dictionary of all of the current values.
            extract_policy (bool): Flag to determine if you are ready to learn the policy. 
                this is only called at the end of the process to minimise wasted computation. 

        Returns:
            V_k (float): Updated value of V_k

        '''

        action_space = len(self.actions)
        V_k = np.zeros(action_space) 

        for action in range(action_space):
            # this must be one scary looking summation
            V_k[action] = sum(self.probabilities[state][action][s_prime] * \
                              (self.rewards_dict.get(state, {}).get(action, {}).get(s_prime,0) + \
                              self.discount_rate * values_dict.get(s_prime, 0)) \
                              for s_prime in self.probabilities[state][action])
        if extract_policy == False:
            return max(V_k)
        else:
            return np.where(V_k == max(V_k))

    def _bellmans_eq(self, state: tuple, values_dict: dict, extract_policy=False) -> float:
        i, j, k = state
        V = values_dict
        if self._is_terminal(state):
            return self._terminal_value(state)

        action_space = len(self.actions)
        Q = np.zeros(action_space)

        for a in range(action_space):
            ev = 0.0
            for s_prime, prob in self.probabilities[state][a].items():
                reward = self.rewards_dict.get(state, {}).get(a, {}).get(s_prime, 0)

                # ---------- did the turn pass? ----------
                turn_passes = (
                    (a == 0)                                    # stick
                    or (a == 1 and s_prime[2] == 0)             # hit & rolled a 1
                )

                if self._is_terminal(s_prime):
                    next_val = self._terminal_value(s_prime)

                elif turn_passes:
                    # mirror the board: it’s now opponent’s turn
                    mirror = self._swap(s_prime)
                    next_val = 1.0 - V.get(mirror, 0.0)         # zero-sum complement
                else:
                    next_val = V.get(s_prime, 0.0)              # still my turn

                ev += prob * (reward + self.discount_rate * next_val)

            Q[a] = ev

        return np.argmax(Q) if extract_policy else np.max(Q)


    def _value_iteration(self)-> dict:
        '''
        Value iteration algorithm. 

        Hacky implementation of tolerance going in to this. 

        Returns:
            V_k (dict): Final array of values for all the states
        '''

        V_k = {}   
        k = 0
        while k < self.max_iter:
            V_k_minus_1 = V_k.copy()
            for state in self.states:
                V_k[state] = self._bellmans_eq(state = state, values_dict = V_k_minus_1)
            k += 1
            # lets see if we have reached tolerance, only after doing multiple iterations through incase of a slow start 
            if k > 10:
                value_change = max(abs(V_k[sub_state] - V_k_minus_1[sub_state]) for sub_state in V_k)
                if value_change < self.tolerance:
                    print(f'Tolerance of {self.tolerance} was met after {k} iterations. Terminating now.')
                    return V_k
        print(f'Tolerance of {self.tolerance} was not met after {self.max_iter} iterations. Terminating now.')
        return V_k
    
    def _extract_policy(self):
        '''
        We will only do this once as to reduce computational load on the solver. 
        Depending on whether we have a generic problem or a large, grid based one, we 
        will or will not decide to print all the actions.  

        Args: 
            self: all objects attributes stored in self
        Returns: 
            Policy: rule for every state
        '''
        Values = self.values
        policy = {}
        for state in self.states:
            policy[state] = self._bellmans_eq(state = state, values_dict = Values, extract_policy=True)
            #print(f'If in state: {state}, the optimal action is: {self.actions[int(policy[state])]}')
        return policy
    
    def _is_terminal(self, s: tuple) -> bool:
        goal = self.goal_state        
        return s[1] >= goal or s[0] >= goal   # j (my score) or i (opp score)

    def _terminal_value(self, s: tuple) -> float:
        # value is 1 if I’ve already won, 0 if opponent has
        return 1.0 if s[1] >= self.goal_state else 0.0

    def _swap(self, s: tuple) -> tuple:
        i, j, k = s
        return (j, i, k)                      # swap scores, leave turn-total

    def __call__(self):
        '''
        Call funciton, allowing us to interact with instances of the class like a function. 
        '''

        self.values = self._value_iteration()
        self.policy = self._extract_policy()

        return self.policy, self.values
