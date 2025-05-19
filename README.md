# STOR609 Coursework 3 Reproduction Study
Pig is a simple dice game of chance, widely-studied in academic literature for its interesting probabilistic features. We have re‐examined and reproduced the results of such a paper by Todd W. Neller and Clifton G.M. Presser (2004). The aim of their paper is to find the optimal policy a player of the game Pig should use, calculated using the value iteration algorithm. At the time of publishing, classical value iteration was seen as too slow and states took too long to converge, and hence a ‘layered’ approach of working backwards was used. This works by using value iteration on subsets of the state space, ensuring these converge before moving onto the next subset. The paper found that the optimal policy is non‐smooth and includes unusual and unintuitive features.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- `git`
- `pip`

### Clone the Repository

```bash
git clone https://github.com/Harry-Ell/609-CW3.git
cd 609-CW3
```

### Set Up a Virtual Environment

#### (Windows, PowerShell)
```powershell
python -m venv env
.\env\Scripts\activate
```

#### (Unix)
```bash
python3 -m venv env
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### (Optional) Using Jupyter Notebooks

If you're working in Jupyter notebooks, you may want to register this virtual environment as a kernel:

```bash
pip install ipykernel
python -m ipykernel install --user --name=env --display-name "Python (env)"
```

This may also need to be followed by refreshing the available kernels in the workspace.

### Run Tests

```bash
pytest
```

To deactivate the environment after use:

```bash
deactivate
```


## Repository Overview

### notebook_writeup
This contains the finalised figures and the report in submission.ipynb. All work from the other folders have been reproduced in a final form in this folder.
#### Submission.ipynb
This is the final notebook submission for the coursework.
#### optimised_layered_vi.py
Implementation of the layered value iteration approach found in the paper
#### map_reachable_states.py
Code for finding all possible reachable states when using the optimal policy.
#### plotting_tools
General plotting code for generates plots for the report.
#### Competition.py
Class for simulation to reproduce metrics on winning probabilities.
#### Piglet.py
Class for value iteration for Piglet game to reproduce the convergence graph.

### layered_VI
This contains layered value iteration code and files for the solution generated used during the coursework.

### plots_and_graphs
Reproduction of reachable states plot.

### simulation_study
A simulation approach for reproducing metrics on winning probabilities for the optimal solution of Pig and reproducing Piglet results.

