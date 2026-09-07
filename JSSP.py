import numpy as np

class JSSP:
    def __init__(self, population_num: int, generation_num:int, crossover_rate: float, mutation_rate: float,
                 JSSP_phenotype: list[list[int]], jobs_num: int, machines_num: int):
        self.population_num = population_num
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generation_num = generation_num
        self.JSSP_phenotype = JSSP_phenotype
        self.jobs_num = jobs_num
        self.machines_num = machines_num
        self.population = np.zeros((self.population_num, self.jobs_num*self.machines_num), dtype=int)
        self.initialize_population()
        self.rng = np.random.default_rng()

    def get_population_num(self) -> int:
        return self.population_num

    def initialize_population(self):
        idx = 0
        for genotype in self.population:
            rng = np.random.default_rng()
            arr = np.repeat(np.arange(0, self.jobs_num), self.machines_num)
            rng.shuffle(arr)
            self.population[idx] = arr
            idx += 1

    def order_crossover(self, schedule_A: np.ndarray, schedule_B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        cross_points = np.sort(self.rng.choice(self.jobs_num*self.machines_num, size=2, replace=False))

        child_A = np.full(self.jobs_num*self.machines_num, self.jobs_num+1)
        child_B = np.full(self.jobs_num*self.machines_num, self.jobs_num+1)

        child_A[cross_points[0]:cross_points[1]] = schedule_B[cross_points[0]:cross_points[1]]
        child_B[cross_points[0]:cross_points[1]] = schedule_A[cross_points[0]:cross_points[1]]

        outer_arr_A = schedule_A[(np.arange(len(schedule_A)) < cross_points[0]) | (np.arange(len(schedule_A)) >= cross_points[1])]
        outer_arr_B = schedule_B[(np.arange(len(schedule_B)) < cross_points[0]) | (np.arange(len(schedule_B)) >= cross_points[1])]
        crosspoint_span = cross_points[1]-cross_points[0]

        #TODO need to account for extra/too few of each job operations during crossover
        for i in range(len(outer_arr_A)):
            child_idx = i + cross_points[1]
            if child_idx >= child_A.size:
                child_idx = child_idx - child_A.size
            child_A[child_idx] = outer_arr_A[i]
            
        for i in range(len(outer_arr_B)):
            child_idx = i + cross_points[1]
            if child_idx >= child_B.size:
                child_idx = child_idx - child_B.size
            child_B[child_idx] = outer_arr_B[i]

        print(f"Cross points: {cross_points}")
        counts = np.bincount(child_A, minlength=self.jobs_num+1)
        print(f"Child A:        {child_A}")
        print(f"Counts child_A: {counts}")
        print(f"Schedule_A: {schedule_A}")
        print(f"Child A:    {child_A}")
        print(f"Schedule_B: {schedule_B}")
        print(f"Child B:    {child_B}")



