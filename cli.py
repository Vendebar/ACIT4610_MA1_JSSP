import sys

import controller

from parameter import GAParameters, PARAMETER_SETS
from test_case import get_test_cases, get_test_case_dimensions


def get_valid_input(prompt: str, valid_choices: list[str]) -> str:
    while True:
        choice = input(prompt).strip()

        if choice in valid_choices:
            return choice

        print(
            f"Invalid choice. Please enter one of these options: "
            f"{', '.join(valid_choices)}"
        )

def select_runs()-> int:
    while True:
        try:
            runs = int(
                input(
                    "\nHow many individual runs do you want? "
                    "(1-100, runs are sequential): "
                )
            )

            if 1 <= runs <= 100:
                return runs

            print("Please give a number between 1 and 100.")

        except ValueError:
            print("Please give a number.")



def print_test_cases() -> None:
    test_cases = get_test_cases()

    for index, test_case in enumerate(test_cases, start=1):
        jobs, machines = get_test_case_dimensions(test_case)

        print(
            f"{index}) {test_case.stem} "
            f"- {jobs} jobs, {machines} machines"
        )


def choose_file() -> str:
    print("\nSelect Job Shop Scheduling Problem:\n")

    test_cases = get_test_cases()

    print_test_cases()

    exit_choice = str(len(test_cases) + 1)

    print(f"{exit_choice}) Exit")

    valid_choices = [
        str(i)
        for i in range(1, len(test_cases) + 1)
    ] + [exit_choice]

    file_choice = get_valid_input(
        f"\nSelect a file (1-{exit_choice}): ",
        valid_choices,
    )

    if file_choice == exit_choice:
        print("Shutting Down")
        sys.exit(0)

    selected_index = int(file_choice) - 1

    return str(test_cases[selected_index])


def print_parameter_sets() -> None:
    for number, parameters in PARAMETER_SETS.items():

        print(f"{number}) Parameter Set {number}")

        for parameter_name, value in parameters.items():

            display_name = parameter_name.replace("_", " ").title()

            if isinstance(value, float):
                print(f"   {display_name}: {value:.2f}")
            else:
                print(f"   {display_name}: {value}")

        print()


def choose_parameter_set() -> GAParameters:
    print("\nSelect Parameter Set:\n")

    print_parameter_sets()

    parameter_choice = get_valid_input(
        f"Select parameter set ({'-'.join(PARAMETER_SETS.keys())}): ",
        list(PARAMETER_SETS.keys()),
    )

    return PARAMETER_SETS[parameter_choice]


def run_cli() -> None:
    while True:

        print("\n==============================")
        print("Job Shop Scheduling Problem")
        print("==============================")

        selected_file = choose_file()
        parameters = choose_parameter_set()

        controller.controller(
            filepath=selected_file,
            parameters=parameters,
        )