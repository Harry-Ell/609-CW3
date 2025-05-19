# STOR609 Coursework 3 Reproduction Study
Pig is a simple dice game of chance, widely-studied in academic literature for its interesting probabilistic features. We have re‐examined and reproduced the results of such a paper by Todd W. Neller and Clifton G.M. Presser (2004). The aim of their paper is to find the optimal policy a player of the game Pig should use, calculated using the value iteration algorithm. At the time of publishing, classical value iteration was seen as too slow and states took too long to converge, and hence a ‘layered’ approach of working backwards was used. This works by using value iteration on subsets of the state space, ensuring these converge before moving onto the next subset. The paper found that the optimal policy is non‐smooth and includes unusual and unintuitive features.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10 or higher
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

### Updating available kernels for using Jupyter Notebooks

The submission is given inside of `notebook_writeup/submission.ipynb`. It is possible that the new kernel has not yet been recognised. In this case, you can add it with the below command. 

```bash
python -m ipykernel install --user --name=env --display-name "Python (env)"
```

This may also need to be followed by refreshing the available kernels in the workspace.

### Run Tests

```bash
pytest
```
An error message may follow if you have not ran the command to move one layer down the file path as intended earlier. 
```bash 
cd 609-CW3 
```

To deactivate the environment after use:

```bash
deactivate
```


## Repository Overview

Below is a breakdown of the contents of this repository, including scripts, tests, and supplementary notebooks. The intended point of entry to the repository is our submission notebook,  `notebook_writeup/submission.ipynb`. A brief explanation of all folders and sub files is given below. 

###  `development_steps/`
Contains notebooks used during development and prototyping of various approaches:

- **`layered_value_iteration.ipynb`** - Notebook exploring the logic and performance of the layered value iteration algorithm.
- **`piglet.ipynb`** – Preliminary notebook working through the simplified "Piglet" game logic.

###  `notebook_writeup/`
Houses the final project and data sets used in analysis:

- **`presentation_figs/`** – Any figures included in the final presentation or summary plots.

- **`pickle_and_config_files/`** – Contains configuration files and precomputed data

- `competition.py` - Simulates head-to-head matches between different policies, including opponent strategies.

- `map_reachable_states.py` - Generates reachable state-space data by simulating play using the optimal policy and varied opponents.

- `optimised_layered_vi.py` - Implementation of the layered value iteration algorithm used to solve the full Pig game efficiently.

- `piglet.py` - A simplified value iteration solver for a toy version of the Pig game

- `plotting_tools.py` - Scripts for generating 3D isosurface plots of policy and value functions using Plotly.

- `submission.ipynb` - The final submission notebook, where all figures and analysis given in the paper is reproduced. 

### `papers/` 
- `Optimal_Play_of_the_Dice_Game_Pig.pdf` Original paper whose content we hope to repoduce.
- `Report_on_reproducibility.pdf.pdf` Our outcomes from the application of their methods. 

### `tests/`
Unit tests for ensuring correctness and reproducibility:

- **`data/`** – Contains test fixtures or test-specific data files (e.g., `.pkl` comparisons).
- `test_pig_policy.py` – Tests for the full Pig value iteration strategy.
- `test_piglet_policy.py` – Tests for the simplified Piglet solver.
- `conftest.py` – Ensures tests are run from the repository root and configures shared test logic.
