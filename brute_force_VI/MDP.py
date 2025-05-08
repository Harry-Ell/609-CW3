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

    def _bellmans_eq(self, state: tuple, values_dict: dict, extract_policy=False) -> float:
        i, j, k = state
        # start by checking if we have already finished, if so the value should be 1 if we won
        # and 0 if we have lost
        if state[1] >= self.goal_state or state[0] >= self.goal_state:
            return 1.0 if state[1] >= self.goal_state else 0.0

        # as before 
        action_space = len(self.actions)
        V_k = np.zeros(action_space)

        # outer loop takes us through all actions (roll, dont roll)
        for a in range(action_space):
            ev = 0.0
            for s_prime, prob in self.probabilities[state][a].items():
                # Reward is only defined at certain states. Incase it isnt, we will stack .get methods 
                reward = self.rewards_dict.get(state, {}).get(a, {}).get(s_prime, 0)

                # logic to passover the turn. Do we choose to not roll, or do we roll and end up with 
                # 0 points unbanked, which corresponds to having rolled a 1 due to the structure of 
                # the probabilities dict 
                turn_passes = ((a == 0) or (a == 1 and s_prime[2] == 0))
                
                ##############################################################################
                ##################### LOGIC FOR FINDING VALUE OF NEXT STATES #################
                ##############################################################################

                # Again, we check if the game is over. if it is, then the next value we should see is the 
                # reward for winning, or 0 
                if state[1] >= self.goal_state or state[0] >= self.goal_state:
                    next_val = 1.0 if state[1] >= self.goal_state else 0.0

                elif turn_passes:
                # if the game is not over, but the turns swap, then the value of the state you end up 
                # in should (probably!) be the compliment of what your opponent would have been on?
                    i, j, k = s_prime
                    mirrored_state = (j, i, k)  # Should k be 0 here? I do not know. 
                    next_val = 1.0 - values_dict.get(mirrored_state, 0.0)         
                else:
                    next_val = values_dict.get(s_prime, 0.0)              # still my turn
                
                # standard weighted average. 
                ev += prob * (reward + self.discount_rate * next_val)

            # update value with ev of being in that state
            V_k[a] = ev

        # some simple logic which is only triggered after tolerance has been obtained. 
        if extract_policy == False:
            return max(V_k)
        else:
            return np.where(V_k == max(V_k))


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
            print(f'now on iteration {k}', flush = True)
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
                else:
                    print(f'On iteration {k}, current tolerance is {value_change}', flush = True)
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
        return policy

    def __call__(self):
        '''
        Call funciton, allowing us to interact with instances of the class like a function. 
        '''

        self.values = self._value_iteration()
        self.policy = self._extract_policy()

        return self.policy, self.values
