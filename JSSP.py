import numpy as np
import numpy.typing as npt
import copy

from parameter import GAParameters
from test_case import JSSPProblem

class JSSP:
    def __init__(
            self, population_num: int, 
            generation_num:int, 
            crossover_rate: float, 
            mutation_rate: float,
            JSSP_phenotype: npt.ArrayLike, 
            jobs_num: int, 
            machines_num: int,
            seed: int | None = None
        ):

        self.population_num = population_num
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generation_num = generation_num
        self.JSSP_phenotype = np.asarray(JSSP_phenotype)
        self.jobs_num = jobs_num
        self.machines_num = machines_num
        self.rng = np.random.default_rng(seed)
        self.population = np.zeros((self.population_num, self.jobs_num*self.machines_num), dtype=int)
        self.population_fitness = np.zeros(self.population.shape[0], dtype=int)
        self.initialize_population()

    def get_population_num(self) -> int:
        return self.population_num

    def get_generation_num(self) -> int:
        return self.generation_num

    def get_crossover_rate(self) -> float:
        return self.crossover_rate

    def get_mutation_rate(self) -> float:
        return self.mutation_rate

    def initialize_population(self):
        idx = 0
        for genotype in self.population:
            arr = np.repeat(np.arange(0, self.jobs_num), self.machines_num)
            self.rng.shuffle(arr)
            self.population[idx] = arr
            idx += 1

    def decode_JSSP(
            self, 
            schedule: npt.NDArray[np.int_], 
            is_displayed: bool=False
            ):

        # each index is the job related to the row in the JSSP,
        #  and the value is the step of the job that is being scheduled
        machine_times = np.zeros(self.machines_num, dtype=int)
        current_job_step = np.zeros(self.jobs_num, dtype=int)
        current_machine_step = np.zeros(self.machines_num, dtype=int)
        previous_job_end_times = np.zeros(self.jobs_num, dtype=int)
        reconstruction = None

        # reconstruction is only useful for displaying a Gantt chart.
        #   It is extra unnecessary computation when running the GA regularly
        if is_displayed:
            reconstruction = np.full(
                (self.machines_num, self.jobs_num, 4),
                -1,
                dtype=int
            )

        for job in schedule:
            machine = self.JSSP_phenotype[job][current_job_step[job]*2]
            duration = self.JSSP_phenotype[job][current_job_step[job]*2 + 1]
            current_job_step[job] = current_job_step[job] + 1

            # If the previous job on another machine ends after the current job is scheduled to start,
            #  we need to delay the current job's start time
            #  otherwise, place at the end of the current machine's schedule
            if(previous_job_end_times[job] > machine_times[machine]):
                dead_time = previous_job_end_times[job] - machine_times[machine]
                machine_times[machine] += dead_time                   #machine start time

                # Added because start_time is needed for reconstruction
                start_time = machine_times[machine]

                previous_job_end_times[job] = machine_times[machine]  #this job start time
                machine_times[machine] += duration                    #machine end time
                previous_job_end_times[job] += duration               #job end time

            else:
                start_time = machine_times[machine]
                machine_times[machine] += duration
                previous_job_end_times[job] = start_time + duration

            if is_displayed:
                assert reconstruction is not None
                reconstruction_tuple = (job, machine, start_time, duration)
                reconstruction[machine][current_machine_step[machine]] = reconstruction_tuple
                current_machine_step[machine] += 1

        if is_displayed:
            return machine_times.max(), reconstruction

        return machine_times.max(), None

    def calculate_population_fitness(self) -> tuple[int, npt.NDArray[np.int_], int, npt.NDArray[np.int_]]:
        worst_makespan = -1
        worst_individual: npt.NDArray[np.int_] = np.empty(0, dtype=int)
        best_makespan = -1
        best_individual: npt.NDArray[np.int_] = np.empty(0, dtype=int)
        for index in np.ndindex(self.population.shape[0]):
            individual = self.population[index]
            makespan, reconstruction = self.decode_JSSP(individual)
            self.population_fitness[index[0]] = makespan
            if best_makespan == -1 or best_makespan > makespan:
                best_makespan = makespan
                best_individual = individual
            if worst_makespan < makespan:
                worst_makespan = makespan
                worst_individual = individual

        return best_makespan, best_individual, worst_makespan, worst_individual


   

    def jox_crossover(self, schedule_A: np.ndarray, schedule_B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        job_preserve = self.rng.integers(0,self.jobs_num)
        child_A = copy.deepcopy(schedule_A)
        child_B = copy.deepcopy(schedule_B)

        child_idx = 0
        for idx, value in np.ndenumerate(schedule_A):
            if value == job_preserve:
                continue
            while child_B[child_idx] == job_preserve:
                child_idx += 1
                if child_idx >= child_B.size: break
            child_B[child_idx] = value
            child_idx += 1

        child_idx = 0
        for idx, value in np.ndenumerate(schedule_B):
            if value == job_preserve:
                continue
            while child_A[child_idx] == job_preserve:
                child_idx += 1
                if child_idx >= child_A.size: break
            child_A[child_idx] = value
            child_idx += 1
        return child_A.copy(), child_B.copy()

    def mutation_swap(self, schedule: np.ndarray) -> np.ndarray:
        mutation_points = np.sort(self.rng.choice(schedule.size, size=2, replace=False))
        #Let's gaurantee that the swap actually changes something
        while schedule[mutation_points[0]] == schedule[mutation_points[1]]:
            mutation_points = np.sort(self.rng.choice(schedule.size, size=2, replace=False))
        schedule[[mutation_points[0], mutation_points[1]]] = schedule[[mutation_points[1], mutation_points[0]]]

        return schedule

def create_JSSP(
    problem: JSSPProblem,
    parameters: GAParameters,
    seed: int | None = None,
) -> JSSP:

    return JSSP(

        population_num=
            parameters[
                "population_size"
            ],

        generation_num=
            parameters[
                "generations"
            ],

        crossover_rate=
            parameters[
                "crossover_probability"
            ],

        mutation_rate=
            parameters[
                "mutation_probability"
            ],

        JSSP_phenotype=
            problem["schedule"],

        jobs_num=
            problem["jobs"],

        machines_num=
            problem["machines"],

        seed=seed
    )




