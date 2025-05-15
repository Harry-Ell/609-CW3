'''
Billies code for the simplified game of piglet. 
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
import sys

# this makes imports more reliable when importing from a variety of places.
sys.path.append('..')

# some nice and optional formatting tools
mpl.rc_file('pickle_and_config_files/matplotlibrc')


class PigletSolver:
    '''
    some exposition here about what this does would be helpful if anyone has the time to do so . 
    '''
    def __init__(self, goal, epsilon):
        self.goal:int = goal
        self.epsilon:float = epsilon
        self.p:list[list[list[float]]] = [[[0.0 for _ in range(goal)] for _ in range(goal)] for _ in range(goal)]
        self.flip:list[list[list[float]]] = [[[False for _ in range(goal)] for _ in range(goal)] for _ in range(goal)]
        self.iteration_logs:list = [] 


    def _value_iterate(self):
        max_change = float('inf')
        while max_change >= self.epsilon:
            max_change = 0.0
            # p_old = copy.deepcopy(self.p)  # Save current state for comparison or logging
            self.iteration_logs.append(copy.deepcopy(self.p))
            for i in range(self.goal):
                for j in range(self.goal):
                    for k in range(self.goal - i):
                        old_prob = self.p[i][j][k]
                        p_flip = (1.0 - self._p_win(j, i, 0) + self._p_win(i, j, k + 1)) / 2
                        p_hold = 1.0 - self._p_win(j, i + k, 0)
                        self.p[i][j][k] = max(p_flip, p_hold)
                        self.flip[i][j][k] = p_flip > p_hold
                        change = abs(self.p[i][j][k] - old_prob)
                        max_change = max(max_change, change)

    def _p_win(self, i, j, k):
        if i + k >= self.goal:
            return 1.0
        elif j >= self.goal:
            return 0.0
        else:
            return self.p[i][j][k]

    def _return_convergence_plots(self):
        '''
        
        '''
        valid_states = [(i, j, k) for i in range(self.goal)
                                for j in range(self.goal)
                                for k in range(self.goal - i)]

        # Create a plot for each state
        plt.figure(figsize=(10, 6))

        for state in valid_states:
            i, j, k = state
            values = [log[i][j][k] for log in self.iteration_logs]
            plt.plot(values, label=f"({i},{j},{k})")

        plt.xlabel("Iteration")
        plt.ylabel("Win Probability")
        plt.title("State Value Convergence in Piglet (goal=2)")
        plt.legend(title="State (i,j,k)", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.grid(True)
        if self.savefig == True:
            plt.savefig('piglet_convergence_plot.png')
        plt.show()


    def __call__(self, convergence_plots = False, savefig = False):
        # self.goal = goal
        # self.epsilon = epsilon
        self.savefig = savefig
        self._value_iterate()
        if convergence_plots:
            self._return_convergence_plots()
