import sys


# Test cases
LA_01 = "/testCases/la01"  # Small
LA_04 = "/testCases/la04"  # Small
LA_17 = "/testCases/la17"  # Medium
LA_20 = "/testCases/la20"  # Medium
LA_32 = "/testCases/la32"  # Large
LA_33 = "/testCases/la33"  # Large


# Three fixed GA parameter sets
PARAMETER_SETS = {
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


def get_valid_input(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()

        if choice in valid_choices:
            return choice

        print(
            f"Invalid choice. Please enter one of these options: "
            f"{', '.join(valid_choices)}"
        )


def choose_file():
    print("\nSelect Job Shop Scheduling Problem:\n")

    print("1) la01 - Small")
    print("2) la04 - Small")
    print("3) la17 - Medium")
    print("4) la20 - Medium")
    print("5) la32 - Large")
    print("6) la33 - Large")
    print("7) Exit")

    file_choice = get_valid_input(
        "\nSelect a file (1-7): ",
        ["1", "2", "3", "4", "5", "6", "7"],
    )

    match file_choice:
        case "1":
            return LA_01

        case "2":
            return LA_04

        case "3":
            return LA_17

        case "4":
            return LA_20

        case "5":
            return LA_32

        case "6":
            return LA_33

        case "7":
            print("Shutting Down")
            sys.exit(0)


def choose_parameter_set():
    print("\nSelect GA Parameter Set:\n")

    print("1) Parameter Set 1")
    print("   Population Size: 50")
    print("   Generations: 100")
    print("   Crossover Probability: 0.80")
    print("   Mutation Probability: 0.10\n")

    print("2) Parameter Set 2")
    print("   Population Size: 100")
    print("   Generations: 200")
    print("   Crossover Probability: 0.90")
    print("   Mutation Probability: 0.05\n")

    print("3) Parameter Set 3")
    print("   Population Size: 200")
    print("   Generations: 300")
    print("   Crossover Probability: 0.70")
    print("   Mutation Probability: 0.20\n")

    parameter_choice = get_valid_input(
        "Select parameter set (1-3): ",
        ["1", "2", "3"],
    )

    return PARAMETER_SETS[parameter_choice]


def main():
    while True:
        print("\n==============================")
        print("Job Shop Scheduling Problem")
        print("==============================")

        selected_file = choose_file()
        parameters = choose_parameter_set()

        print("\nSelected Configuration:")
        print(f"File: {selected_file}")
        print(f"Population Size: {parameters['population_size']}")
        print(f"Generations: {parameters['generations']}")
        print(
            f"Crossover Probability: "
            f"{parameters['crossover_probability']}"
        )
        print(
            f"Mutation Probability: "
            f"{parameters['mutation_probability']}"
        )

        # Then we run genetic algorithm with parameters from selected config
        #
        # run_ga(
        #     file=selected_file,
        #     population_size=parameters["population_size"],
        #     generations=parameters["generations"],
        #     crossover_probability=parameters["crossover_probability"],
        #     mutation_probability=parameters["mutation_probability"],
        # )


if __name__ == "__main__":
    main()