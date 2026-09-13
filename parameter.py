from typing import TypedDict


class GAParameters(TypedDict):
    population_size: int
    generations: int
    crossover_probability: float
    mutation_probability: float


PARAMETER_SETS: dict[str, GAParameters] = {

    "1": {
        "population_size": 50,
        "generations": 100,
        "crossover_probability": 0.8,
        "mutation_probability": 0.1,
    },

    "2": {
        "population_size": 100,
        "generations": 200,
        "crossover_probability": 0.9,
        "mutation_probability": 0.05,
    },

    "3": {
        "population_size": 200,
        "generations": 300,
        "crossover_probability": 0.7,
        "mutation_probability": 0.2,
    },
}