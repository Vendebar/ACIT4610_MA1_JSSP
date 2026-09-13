# #Obsolete by method in JSSP object
# # def decode_JSSP(JSSP: list[list[int]], schedule: list[int], num_jobs: int, num_machines: int):

# #     # each index is the job related to the row in the JSSP,
# #     #  and the value is the step of the job that is being scheduled
# #     machine_times = np.zeros(num_machines, dtype=int)
# #     current_job_step = np.zeros(num_jobs, dtype=int)
# #     current_machine_step = np.zeros(num_machines, dtype=int)
# #     previous_job_end_times = np.zeros(num_jobs, dtype=int)

# #     reconstruction = np.full((num_machines, num_jobs, 4), -1, dtype=int)

# #     for job in schedule:
# #         machine = JSSP[job][current_job_step[job]*2]
# #         duration = JSSP[job][current_job_step[job]*2 + 1]
# #         current_job_step[job] = current_job_step[job] + 1

# #         # If the previous job on another machine ends after the current job is scheduled to start,
# #         #  we need to delay the current job's start time
# #         #  otherwise, place at the end of the current machine's schedule
# #         if(previous_job_end_times[job] > machine_times[machine]):
# #             dead_time = previous_job_end_times[job] - machine_times[machine]
# #             machine_times[machine] += dead_time                   #machine start time
# #             start_time = machine_times[machine]
# #             previous_job_end_times[job] = machine_times[machine]  #this job start time
# #             machine_times[machine] += duration                    #machine end time
# #             previous_job_end_times[job] += duration               #job end time

# #         else:
# #             start_time = machine_times[machine]
# #             machine_times[machine] += duration
# #             previous_job_end_times[job] = start_time + duration

# #         reconstruction_tuple = (job, machine, start_time, duration)
# #         reconstruction[machine][current_machine_step[machine]] = reconstruction_tuple
# #         current_machine_step[machine] += 1

# #     print(machine_times)
# #     print(f"Makespan: {machine_times.max()}")
# #     plot_JSSP_Gantt(reconstruction, num_jobs, num_machines)

# #     return 0

#  def order_crossover(self, schedule_A: np.ndarray, schedule_B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
#         cross_points = np.sort(self.rng.choice(schedule_A.size, size=2, replace=False))

#         child_A = np.full(schedule_A.size, self.jobs_num)
#         child_B = np.full(schedule_B.size, self.jobs_num)

#         child_A[cross_points[0]:cross_points[1]] = schedule_B[cross_points[0]:cross_points[1]]
#         child_B[cross_points[0]:cross_points[1]] = schedule_A[cross_points[0]:cross_points[1]]

#         rolled_arr_A = np.roll(schedule_A, -cross_points[1])
#         rolled_arr_B = np.roll(schedule_B, -cross_points[1])
#         crosspoint_span = cross_points[1]-cross_points[0]

#         #TODO need to account for extra/too few of each job operations during crossover
#         counts_A = np.bincount(child_A, minlength=self.jobs_num)
#         for i in range(len(rolled_arr_A)-crosspoint_span):
#             child_idx = i + cross_points[1]
#             if child_idx >= child_A.size:
#                 child_idx = child_idx - child_A.size
#             child_A[child_idx] = rolled_arr_A[i]
            
#         for i in range(len(rolled_arr_B)):
#             child_idx = i + cross_points[1]
#             if child_idx >= child_B.size:
#                 child_idx = child_idx - child_B.size
#             child_B[child_idx] = rolled_arr_B[i]

#         counts = np.bincount(child_B, minlength=self.jobs_num)
#         for i in range(len(rolled_arr_B)):
#             child_idx = i + cross_points[1]
#             if child_idx >= child_B.size:
#                 child_idx = child_idx - child_B.size
#             child_B[child_idx] = rolled_arr_B[i]

#         print(f"Cross points: {cross_points}")
#         counts = np.bincount(child_A, minlength=self.jobs_num)
#         print(f"Child A:        {child_A}")
#         print(f"Counts child_A: {counts}")
#         print(f"Schedule_A: {schedule_A}")
#         print(f"Child A:    {child_A}")
#         print(f"Schedule_B: {schedule_B}")
#         #print(f"Child B:    {child_B}")