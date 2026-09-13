import secrets

import time

from parameter import GAParameters

from test_case import read_JSSP

from JSSP import create_JSSP

from ga import GA_run

from gantt_builder import plot_JSSP_Gantt

from results import save_run


def controller(
    filepath: str,
    parameters: GAParameters,
    runs: int = 1
):

    problem = read_JSSP(
        filepath
    )
    for run in range(1, runs+1):

        print(
            f"\nRun {run}/{runs}"
        )

        seed = secrets.randbits(
            32
        )

        # Don't start time until after file operations, just in case

        start_time = (
            time.perf_counter()
        )

        JSSP_obj = create_JSSP(
            problem,
            parameters,
            seed
        )

        (
            individual_best_makespan,
            individual_best,
            generation_converge,
            current_average_fitness,
            current_standard_deviation,
            individual_worst_makespan,
            generation_results
        ) = GA_run(
            JSSP_obj
        )

        end_time = (
            time.perf_counter()
        )

        execution_time = (
            end_time
            - start_time
        )

        (
            run_path,
            summary_path,
            best_gantt_path,
            is_best_run
        ) = save_run(

            filepath=
                filepath,

            parameters=
                parameters,

            seed=
                seed,

            best_makespan=
                individual_best_makespan,

            worst_makespan=
                individual_worst_makespan,

            convergence_generation=
                generation_converge,

            execution_time=
                execution_time,

            final_average_fitness=
                current_average_fitness,

            final_standard_deviation=
                current_standard_deviation,

            best_individual=
                individual_best,

            generation_results=
                generation_results
        )

        print(
            f"Idv Best Makespan: "
            f"{individual_best_makespan}"
        )

        print(
            f"Idv Worst Makespan: "
            f"{individual_worst_makespan}"
        )

        print(
            f"Last Generation Improvement: "
            f"{generation_converge}"
        )

        print(
            f"Execution Time: "
            f"{execution_time:.6f}"
        )

        print(
            f"Seed: {seed}"
        )

        print(
            f"Run saved to: "
            f"{run_path}"
        )

        print(
            f"Summary saved to: "
            f"{summary_path}"
        )

        time_result, reconstruction = (
            JSSP_obj.decode_JSSP(
                individual_best,
                True
            )
        )

        if is_best_run:

            plot_JSSP_Gantt(
                reconstruction,  # type: ignore
                problem["jobs"],
                problem["machines"],
                str(best_gantt_path)
            )

            print(
                f"New best run. "
                f"Gantt saved to: "
                f"{best_gantt_path}"
            )

        else:

            plot_JSSP_Gantt(
                reconstruction,  # type: ignore
                problem["jobs"],
                problem["machines"]
            )