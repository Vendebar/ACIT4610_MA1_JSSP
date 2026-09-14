# ACIT4610_MA1_JSSP Group 5
Job Shop Scheduling with Genetic Algorithms

Authors:

Alex Fathman || Vendebar

Carl Christian Roll-Lund || 99CCC

Anders Jørgensen || AndersJorgensen04

## Installation guide / How to run the program

#### 1. Clone the github repository
    git clone the repository.

### 2.  Install dependencies
    Do "pip install -r requirements.txt".

### 3. Starting the program
    Type "python main.py" into the console.

### 4. Running the GA
    After starting the program you will shortly be prompted 7 options, select the job scheduling problem you want to solve.
    Next step is to select 1 of the parameters sets provided.
    Lastly select how many individual runs you want to do (1-100).
### 5. Results
    Results are saved in files under forexample "results/la01_small/parameter_1", best_gantt for the problem is also saved here.
## Code Flow

The solution uses a simple CLI + Controller design.

`main.py` acts as the entrypoint and starts `cli.py`, where the user selects a test case from `./testCases` and a GA parameter set from `parameter.py`.

The selected file and parameters are then passed to `controller.py`, which handles the execution flow.

`test_case.py` reads the selected `.txt` file and extracts the number of jobs, machines, and the job operation data.

`JSSP.py` uses this data to create the JSSP object and initialize the population.

`ga.py` then runs the genetic algorithm using tournament selection, JOX crossover, and swap mutation.

After the run is complete, the best solution is decoded and sent to `gantt_builder.py` for visualization.

Flow:

`main.py` → `cli.py` → `controller.py` → `test_case.py` → `JSSP.py` → `ga.py` → `gantt_builder.py`

## Specifications

- Selection Strategy: Tournament Selection
- Crossover Strategy: JOX
- Mutation Strategy: Swap Mutation
- Fitness: Makespan
- Goal: Minimize Makespan

# Declaration of AI usage
No artificial intelligence was used in the writing of the report.
Copilot (GPT-5.3 Codex) was used to assist in coding the final solution.
The main GA program code was first developed without assistance, and then AI assistance was used for building out the solution with CLI interaction, reproducibility, logging, and modular architecture.
