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

        child_A = np.full(self.jobs_num*self.machines_num, -1)
        child_B = np.full(self.jobs_num*self.machines_num, -1)

        child_A[cross_points[0]:cross_points[1]] = schedule_B[cross_points[0]:cross_points[1]]
        child_B[cross_points[0]:cross_points[1]] = schedule_A[cross_points[0]:cross_points[1]]

        print(f"Child A:    {child_A}")
        for i in range(len(schedule_A[cross_points[1]:])):
            child_A[cross_points[1] + i] = schedule_A[i]
        for i in range(len(schedule_A[:cross_points[0]])):
            child_A[i] = schedule_A[i]

        for i in range(len(schedule_B[cross_points[1]:])):
            child_B[cross_points[1] + i] = schedule_B[i]
        for i in range(len(schedule_B[:cross_points[0]])):
            child_B[i] = schedule_B[i]

        print(f"Cross points: {cross_points}")
        print(f"Schedule_A: {schedule_A}")
        print(f"Child A:    {child_A}")
        print(f"Schedule_B: {schedule_B}")
        print(f"Child B:    {child_B}")



