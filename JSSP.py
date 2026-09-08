import numpy as np
import copy

class JSSP:
    def __init__(self, population_num: int, generation_num:int, crossover_rate: float, mutation_rate: float,
                 JSSP_phenotype: np.NDArray[np.int_], jobs_num: int, machines_num: int):
        self.population_num = population_num
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generation_num = generation_num
        self.JSSP_phenotype = np.asarray(JSSP_phenotype)
        self.jobs_num = jobs_num
        self.machines_num = machines_num
        self.population = np.zeros((self.population_num, self.jobs_num*self.machines_num), dtype=int)
        self.population_fitness = np.zeros(self.population.shape[0], dtype=int)
        self.initialize_population()
        self.rng = np.random.default_rng()

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
            rng = np.random.default_rng()
            arr = np.repeat(np.arange(0, self.jobs_num), self.machines_num)
            rng.shuffle(arr)
            self.population[idx] = arr
            idx += 1

    def decode_JSSP(self, schedule: np.NDArray[np.int_], is_displayed: bool=False) -> tuple[int, np.NDArray[np.int_]]:

        # each index is the job related to the row in the JSSP,
        #  and the value is the step of the job that is being scheduled
        machine_times = np.zeros(self.machines_num, dtype=int)
        current_job_step = np.zeros(self.jobs_num, dtype=int)
        current_machine_step = np.zeros(self.machines_num, dtype=int)
        previous_job_end_times = np.zeros(self.jobs_num, dtype=int)

        if is_displayed: reconstruction = np.full((self.machines_num, self.jobs_num, 4), -1, dtype=int)

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
                start_time = machine_times[machine]
                previous_job_end_times[job] = machine_times[machine]  #this job start time
                machine_times[machine] += duration                    #machine end time
                previous_job_end_times[job] += duration               #job end time

            else:
                start_time = machine_times[machine]
                machine_times[machine] += duration
                previous_job_end_times[job] = start_time + duration

            if is_displayed: reconstruction_tuple = (job, machine, start_time, duration)
            if is_displayed: reconstruction[machine][current_machine_step[machine]] = reconstruction_tuple
            current_machine_step[machine] += 1

        #print(machine_times)
        #print(f"Makespan: {machine_times.max()}")

        if is_displayed: return machine_times.max(), reconstruction
        return machine_times.max(), None

    def calculate_population_fitness(self) -> tuple[int, np.NDArray[np.int_], int, np.NDArray[np.int_]]:
        worst_makespan = -1
        worst_reconstruction = ""
        best_makespan = -1
        best_reconstruction = ""
        for index in np.ndindex(self.population.shape[0]):
            individual = self.population[index]
            print(individual)
            makespan, reconstruction = self.decode_JSSP(individual)
            self.population_fitness[index[0]] = makespan
            if best_makespan == -1 or best_makespan > makespan:
                best_makespan = makespan
                best_reconstruction = reconstruction
            if worst_makespan < makespan:
                worst_makespan = makespan
                worst_reconstruction = reconstruction

        return best_makespan, best_reconstruction, worst_makespan, worst_reconstruction


    def order_crossover(self, schedule_A: np.ndarray, schedule_B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        cross_points = np.sort(self.rng.choice(schedule_A.size, size=2, replace=False))

        child_A = np.full(schedule_A.size, self.jobs_num)
        child_B = np.full(schedule_B.size, self.jobs_num)

        child_A[cross_points[0]:cross_points[1]] = schedule_B[cross_points[0]:cross_points[1]]
        child_B[cross_points[0]:cross_points[1]] = schedule_A[cross_points[0]:cross_points[1]]

        rolled_arr_A = np.roll(schedule_A, -cross_points[1])
        rolled_arr_B = np.roll(schedule_B, -cross_points[1])
        crosspoint_span = cross_points[1]-cross_points[0]

        #TODO need to account for extra/too few of each job operations during crossover
        counts_A = np.bincount(child_A, minlength=self.jobs_num)
        print(f"Child A: {child_A}")
        print(f"Counts child_A: {counts_A}")
        print(f"child_A roll: {rolled_arr_A}")
        print("----------------------------------------------------------------")
        for i in range(len(rolled_arr_A)-crosspoint_span):
            child_idx = i + cross_points[1]
            if child_idx >= child_A.size:
                child_idx = child_idx - child_A.size
            child_A[child_idx] = rolled_arr_A[i]
            
        for i in range(len(rolled_arr_B)):
            child_idx = i + cross_points[1]
            if child_idx >= child_B.size:
                child_idx = child_idx - child_B.size
            child_B[child_idx] = rolled_arr_B[i]

        counts = np.bincount(child_B, minlength=self.jobs_num)
        #print(f"Counts child_B: {counts}")
        for i in range(len(rolled_arr_B)):
            child_idx = i + cross_points[1]
            if child_idx >= child_B.size:
                child_idx = child_idx - child_B.size
            child_B[child_idx] = rolled_arr_B[i]

        print(f"Cross points: {cross_points}")
        counts = np.bincount(child_A, minlength=self.jobs_num)
        print(f"Child A:        {child_A}")
        print(f"Counts child_A: {counts}")
        print(f"Schedule_A: {schedule_A}")
        print(f"Child A:    {child_A}")
        print(f"Schedule_B: {schedule_B}")
        #print(f"Child B:    {child_B}")

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

        #print(f"Job:        {job_preserve}")
        #print(f"Schedule_A: {schedule_A}")
        #print(f"Child A:    {child_A}")
        #print(f"Schedule_B: {schedule_B}")
        #print(f"Child B:    {child_B}")
        #counts = np.bincount(child_A, minlength=self.jobs_num)
        #print(f"Counts child_A: {counts}")
        #counts = np.bincount(child_B, minlength=self.jobs_num)
        #print(f"Counts child_B: {counts}")

        return child_A, child_B

    def mutation_swap(self, schedule: np.ndarray) -> np.ndarray:
        mutation_points = np.sort(self.rng.choice(schedule.size, size=2, replace=False))
        #Let's gaurantee that the swap actually changes something
        while schedule[mutation_points[0]] == schedule[mutation_points[1]]:
            mutation_points = np.sort(self.rng.choice(schedule.size, size=2, replace=False))
        schedule[[mutation_points[0], mutation_points[1]]] = schedule[[mutation_points[1], mutation_points[0]]]

        return schedule





