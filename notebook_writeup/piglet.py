'''
Billies code for the simplified game of piglet. 
'''

import matplotlib.pyplot as plt
import copy

class PigletSolver:
    '''
    
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

    def _output_hold_values(self):
        for i in range(self.goal):
            row = []
            for j in range(self.goal):
                k = 0
                while k < self.goal - i and self.flip[i][j][k]:
                    k += 1
                row.append(str(k))
            print(' '.join(row))
            
    # def _print_state(self):
    #     '''
    #     is this a redundant function? 
    #     '''
    #     print("Current state probabilities (p[i][j][k]):")
    #     for i in range(self.goal):
    #         for j in range(self.goal):
    #             for k in range(self.goal - i):
    #                 print(f"p[{i}][{j}][{k}] = {self.p[i][j][k]:.4f}")
    #     print("-" * 40)

    def _return_convergence_plots(self):
        pass


    def __call__(self, ):
        solved_game = self.value_iterate()
        self._return_convergence_plots()