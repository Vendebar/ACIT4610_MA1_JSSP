import json

from pathlib import Path

import numpy as np

from parameter import GAParameters, PARAMETER_SETS


RESULT_DIRECTORY = Path(__file__).parent / "results"


def get_parameter_set_number(
    parameters: GAParameters
) -> str:

    for number, parameter_set in PARAMETER_SETS.items():

        if parameter_set == parameters:

            return number

    return "custom"


def get_next_run_number(
    result_directory: Path
) -> int:

    run_files = list(
        result_directory.glob("run_*.json")
    )

    return len(run_files) + 1


def update_summary(
    result_directory: Path,
    instance: str,
    parameter_set: str,
    parameters: GAParameters
) -> tuple[Path, dict]:

    run_files = sorted(
        result_directory.glob("run_*.json")
    )

    runs = []

    for run_file in run_files:

        with run_file.open(
            "r",
            encoding="utf-8"
        ) as file:

            runs.append(
                json.load(file)
            )

    makespans = np.array(
        [
            run["best_makespan"]
            for run in runs
        ],
        dtype=float
    )

    execution_times = np.array(
        [
            run["execution_time"]
            for run in runs
        ],
        dtype=float
    )

    convergence_generations = np.array(
        [
            run["convergence_generation"]
            for run in runs
        ],
        dtype=float
    )

    best_run_index = int(
        np.argmin(makespans)
    )

    generation_average_makespans = np.array(
        [
            generation["average"]
            for run in runs
            for generation in run.get(
                "generations",
                []
            )
            if "average" in generation
        ],
        dtype=float
    )

    summary = {

        "instance": instance,

        "parameter_set": parameter_set,

        "parameters": parameters,

        "runs": len(runs),

        "best_makespan_across_run_bests": int(
            np.min(makespans)
        ),

        "worst_makespan_across_run_bests": int(
            np.max(makespans)
        ),

        "worst_makespan_across_run_worsts": int(
            np.max(
                [
                    run["worst_makespan"]
                    for run in runs
                ]
            )
        ),

        "average_makespan_across_run_bests": float(
            np.mean(makespans)
        ),

        "average_makespan_across_all_gens": (
            float(
                np.mean(
                    generation_average_makespans
                )
            )
            if generation_average_makespans.size > 0
            else None
        ),

        "standard_deviation_across_run_bests": float(
            np.std(makespans)
        ),

        "average_execution_time": float(
            np.mean(execution_times)
        ),

        "min_execution_time": float(
            np.min(execution_times)
        ),

        "max_execution_time": float(
            np.max(execution_times)
        ),

        "average_convergence_generation": float(
            np.mean(convergence_generations)
        ),

        "best_run": runs[
            best_run_index
        ]["run"]
    }

    summary_path = (
        result_directory
        / "summary.json"
    )

    with summary_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    return summary_path, summary


def save_run(
    filepath: str,
    parameters: GAParameters,
    seed: int,
    best_makespan: int,
    worst_makespan: int,
    convergence_generation: int,
    execution_time: float,
    final_average_fitness: float,
    final_standard_deviation: float,
    best_individual,
    generation_results: list[dict]
) -> tuple[
    Path,
    Path,
    Path,
    bool
]:

    instance = Path(filepath).stem

    parameter_set = (
        get_parameter_set_number(
            parameters
        )
    )

    result_directory = (
        RESULT_DIRECTORY
        / instance
        / f"parameter_{parameter_set}"
    )

    result_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    run_number = get_next_run_number(
        result_directory
    )

    result = {

        "instance": instance,

        "parameter_set": parameter_set,

        "parameters": parameters,

        "run": run_number,

        "seed": seed,

        "best_makespan": int(
            best_makespan
        ),

        "worst_makespan": int(
            worst_makespan
        ),

        "convergence_generation":
            int(convergence_generation),

        "execution_time": float(
            execution_time
        ),

        "final_population_average":
            float(final_average_fitness),

        "final_population_standard_deviation":
            float(final_standard_deviation),

        "best_individual":
            best_individual.tolist(),

        "generations":
            generation_results
    }

    run_path = (
        result_directory
        / f"run_{run_number:03}.json"
    )

    with run_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )

    summary_path, summary = update_summary(
        result_directory,
        instance,
        parameter_set,
        parameters
    )

    best_gantt_path = (
        result_directory
        / "best_gantt.png"
    )

    is_best_run = (
        summary["best_run"]
        == run_number
    )

    return (
        run_path,
        summary_path,
        best_gantt_path,
        is_best_run
    )