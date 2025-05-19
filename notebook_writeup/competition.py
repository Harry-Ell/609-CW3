'''
Collection of the code which was originally written by Billie and Jasmine which 
can return all of the relevant analytics to us regarding any instance of the contest. 
'''

import numpy as np
from typing import Tuple


class Competition:
    def __init__(self, player1: np.ndarray, player2: np.ndarray, replications: int, seed: int) -> None:
        """
        Initializes a Competition instance for simulating contests between two policies.

        Args:
            player1: A 3D numpy array representing player 1's policy.
            player2: A 3D numpy array representing player 2's policy.
            replications: Number of independent games to simulate.
            seed: Random seed for reproducibility.
        """
        self.player1_policy = player1  # Policy array of shape (101, 101, 101)
        self.player2_policy = player2
        self.reps = replications
        self.start_seed = seed

    def _turn(self, state: Tuple[int, int, int], pol: np.ndarray) -> Tuple[int, int, int]:
        """
        Simulates a single player's turn based on the given policy.

        Args:
            state: Tuple containing (score_player, score_opponent, turn_total).
            pol: A 3D numpy array policy of shape (101, 101, 101) indicating whether to roll (1) or hold (0).

        Returns:
            Tuple[int, int, int]: The new state after the player's turn, with roles swapped for the next player.
        """
        roll = 0
        while roll != 1 and pol[min(state[0], 100), min(state[1], 100), min(state[2], 100)] == 1:
            roll = np.random.randint(1, 7)
            if roll != 1:
                state = (state[0], state[1], state[2] + roll)

        if roll == 1:
            state = (state[0], state[1], 0)  # Turn lost, no points added
        else:
            state = (state[0] + state[2], state[1], 0)  # Bank the turn total

        return (state[1], state[0], 0)  # Swap turns

    def _game(self, policy1: np.ndarray, policy2: np.ndarray) -> int:
        """
        Simulates a full game between two policies.

        Args:
            policy1: The policy used by player 1.
            policy2: The policy used by player 2.

        Returns:
            int: 1 if player 1 wins, 0 if player 2 wins.
        """
        state = (0, 0, 0)
        turn_counter = 0
        while True:
            state = self._turn(state, policy1)
            turn_counter += 1
            if state[1] >= 100:
                return 1
            state = self._turn(state, policy2)
            turn_counter += 1
            if state[1] >= 100:
                return 0

    def __call__(self) -> float:
        """
        Runs the simulation and computes the win rate for player 1.

        Returns:
            float: The win proportion for player 1 over the specified number of replications.
        """
        np.random.seed(self.start_seed)
        win_sum = 0
        for i in range(self.reps):
            win_sum += self._game(self.player1_policy, self.player2_policy)
        return win_sum / self.reps


class Opponents:
    '''
    A collection of predefined opponent strategies.

    Note:
        This class is used as a container and does not require initialisation.
    '''

    @staticmethod
    def hold_at_n(n: int) -> np.ndarray:
        """
        Generates a simple policy that holds once the turn total reaches n,
        or earlier if the player can win by holding.

        Args:
            n: The minimum turn total at which the player should hold.

        Returns:
            np.ndarray: A 3D policy array where 1 = roll, 0 = hold.
        """
        policy = np.ones((100 + 1, 100 + 1, 100 + 1), np.int64)
        policy[:, :, n:] = 0  # Hold when turn total >= n

        for i in range(101):
            for k in range(101):
                if i + k >= 100:
                    policy[i, :, k] = 0  # Also hold if the player can win

        return policy
