import numpy as np

from JSSP import JSSP


def tournament_selection(JSSP_cur):
    candidates = JSSP_cur.rng.choice(
        JSSP_cur.population.shape[0],
        size=2,
        replace=False
    )

    if JSSP_cur.population_fitness[candidates[0]] <= JSSP_cur.population_fitness[candidates[1]]:
        return JSSP_cur.population[candidates[0]]

    return JSSP_cur.population[candidates[1]]


def GA_run(JSSP_cur: JSSP):
    num_population = JSSP_cur.get_population_num()
    num_generation = JSSP_cur.get_generation_num()
    crossover_rate = JSSP_cur.get_crossover_rate()
    mutation_rate = JSSP_cur.get_mutation_rate()
    schedule_length = JSSP_cur.jobs_num * JSSP_cur.machines_num

    generation_log_points = {
        max(1, (checkpoint * num_generation + 9) // 10)
        for checkpoint in range(1, 11)
    }

    (
        individual_best_makespan,
        individual_best,
        individual_worst_makespan,
        individual_worst
    ) = JSSP_cur.calculate_population_fitness()

    generation_converge = 0
    generation_results = []

    current_average_fitness = float(
        np.mean(JSSP_cur.population_fitness)
    )

    current_standard_deviation = float(
        np.std(JSSP_cur.population_fitness)
    )

    for generation in range(1, num_generation + 1):
        new_population = np.zeros(
            (num_population, schedule_length),
            dtype=int
        )

        index_to_add = 0

        while index_to_add < num_population:

            # -----------------------------------------------
            # Selection
            # -----------------------------------------------
            parent1 = tournament_selection(JSSP_cur).copy()
            parent2 = tournament_selection(JSSP_cur).copy()

            # -----------------------------------------------
            # Crossover
            # -----------------------------------------------
            crossover_probability = JSSP_cur.rng.random()

            if crossover_probability < crossover_rate:
                child1, child2 = JSSP_cur.jox_crossover(
                    parent1,
                    parent2
                )
            else:
                child1 = parent1.copy()
                child2 = parent2.copy()

            # -----------------------------------------------
            # Mutation
            # -----------------------------------------------
            mutation_probability1 = JSSP_cur.rng.random()

            if mutation_probability1 < mutation_rate:
                child1 = JSSP_cur.mutation_swap(child1)

            mutation_probability2 = JSSP_cur.rng.random()

            if mutation_probability2 < mutation_rate:
                child2 = JSSP_cur.mutation_swap(child2)

            # -----------------------------------------------
            # Add children
            # -----------------------------------------------
            new_population[index_to_add] = child1
            index_to_add += 1

            if index_to_add < num_population:
                new_population[index_to_add] = child2
                index_to_add += 1

        JSSP_cur.population = new_population

        (
            generation_best_makespan,
            generation_best,
            generation_worst_makespan,
            generation_worst
        ) = JSSP_cur.calculate_population_fitness()

        # Store generation statistics for experiment results
        current_average_fitness = float(
            np.mean(JSSP_cur.population_fitness)
        )

        current_standard_deviation = float(
            np.std(JSSP_cur.population_fitness)
        )

        generation_results.append({
            "generation": generation,
            "best": int(generation_best_makespan),
            "worst": int(generation_worst_makespan),
            "average": current_average_fitness,
            "standard_deviation": current_standard_deviation
        })

        if generation in generation_log_points:
            print(
                f"Generation {generation} average makespan: "
                f"{current_average_fitness}"
            )

            print(
                f"Generation {generation} average std dev.: "
                f"{current_standard_deviation}"
            )

        if generation_best_makespan < individual_best_makespan:
            individual_best = generation_best.copy()
            individual_best_makespan = generation_best_makespan
            generation_converge = generation

        if generation_worst_makespan > individual_worst_makespan:
            individual_worst = generation_worst.copy()
            individual_worst_makespan = generation_worst_makespan

    return (
        individual_best_makespan,
        individual_best,
        generation_converge,
        current_average_fitness,
        current_standard_deviation,
        individual_worst_makespan,
        generation_results
    )