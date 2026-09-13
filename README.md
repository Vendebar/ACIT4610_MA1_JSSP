# ACIT4610_MA1_JSSP Group 5
Job Shop Scheduling with Genetic Algorithms

Authors:

Alex Fathman || Vendebar

Carl Christian Roll-Lund || 99CCC

Anders

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

Note to self: we only care about the standard deviation of the final generation

For analytical stats: show both for final generation and all generations 