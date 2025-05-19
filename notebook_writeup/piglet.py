'''
Billie's code for the simplified game of Piglet.

This class solves a simplified variant of the dice game Pig using value iteration.
At each state, the agent chooses whether to "flip" (roll) or "hold" (bank points).
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
import sys
from typing import List

# Enable relative imports when running from different entry points
sys.path.append('..')


class PigletSolver:
    """
    Solves a simplified version of Pig using tabular value iteration.
    Tracks convergence history and allows policy extraction for testing.
    """

    def __init__(self, goal: int, epsilon: float) -> None:
        """
        Initialises the solver with a win condition and convergence tolerance.

        Args:
            goal (int): Score required to win the game.
            epsilon (float): Threshold for value iteration convergence.
        """
        self.goal: int = goal
        self.epsilon: float = epsilon
        self.p: List[List[List[float]]] = [[[0.0 for _ in range(goal)] for _ in range(goal)] for _ in range(goal)]
        self.flip: List[List[List[bool]]] = [[[False for _ in range(goal)] for _ in range(goal)] for _ in range(goal)]
        self.iteration_logs: List[List[List[List[float]]]] = []  # list of snapshots of `p` across iterations

    def _value_iterate(self) -> None:
        """
        Runs value iteration until the value function converges.
        Updates both the value estimates `p` and the action decisions `flip`.
        """
        max_change = float('inf')
        while max_change >= self.epsilon:
            max_change = 0.0
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

    def _p_win(self, i: int, j: int, k: int) -> float:
        """
        Computes the probability of winning from a given state.

        Args:
            i (int): Player 1's score.
            j (int): Player 2's score.
            k (int): Unbanked turn total for Player 1.

        Returns:
            float: Estimated win probability for the current state.
        """
        if i + k >= self.goal:
            return 1.0
        elif j >= self.goal:
            return 0.0
        else:
            return self.p[i][j][k]

    def _return_convergence_plots(self) -> None:
        """
        Plots the win probability values for all reachable states over iterations.
        Only called if `convergence_plots=True` is passed to the solver.
        """
        valid_states = [(i, j, k) for i in range(self.goal)
                        for j in range(self.goal)
                        for k in range(self.goal - i)]

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

        if self.savefig:
            plt.savefig('piglet_convergence_plot.png')

        plt.show()

    def __call__(self, convergence_plots: bool = False, savefig: bool = False) -> None:
        """
        Solves the game by running value iteration, optionally plotting convergence.

        Args:
            convergence_plots (bool): Whether to generate convergence plots.
            savefig (bool): Whether to save the plot as a PNG file.
        """
        self.savefig = savefig
        self._value_iterate()
        if convergence_plots:
            mpl.rc_file('pickle_and_config_files/matplotlibrc')
            self._return_convergence_plots()

    def get_policy(self) -> List[List[List[bool]]]:
        """
        Returns:
            List[List[List[bool]]]: The optimal policy as a 3D array of booleans.
                                    True = roll, False = hold.
        """
        return self.flip
