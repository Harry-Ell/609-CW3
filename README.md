# 609-CW3
Shared repository for coursework 3 of 609 module 

## Repository Overview
Please add to this section if you include any new features or functionalities 
### brute_force_VI
First pass attempt at solving the full problem without having to partition the space in the same way they did in the paper. 
Files: 
- `MDP.py` Generic Implementation of Value Iteration Algorithm, slightly modified to this case for ease of use.
- `probability_generator.py` Helper function for above script. This populates the probability data structure which the above script uses.
- `rewards_generator.py` Helper function for above script. This populates the rewards data structure which the above script uses.
- `brute_force_sol.py` Calling all the above functions, and saves the output to a .pkl file.
- `brute_force_sol.pkl` Pickle file which contains the optimal policy. 
- `solution_analysis_bf.ipynb` Notebook for performing exploratory data analysis on this solution. 
