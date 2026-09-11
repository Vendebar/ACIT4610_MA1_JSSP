#Obsolete by method in JSSP object
# def decode_JSSP(JSSP: list[list[int]], schedule: list[int], num_jobs: int, num_machines: int):

#     # each index is the job related to the row in the JSSP,
#     #  and the value is the step of the job that is being scheduled
#     machine_times = np.zeros(num_machines, dtype=int)
#     current_job_step = np.zeros(num_jobs, dtype=int)
#     current_machine_step = np.zeros(num_machines, dtype=int)
#     previous_job_end_times = np.zeros(num_jobs, dtype=int)

#     reconstruction = np.full((num_machines, num_jobs, 4), -1, dtype=int)

#     for job in schedule:
#         machine = JSSP[job][current_job_step[job]*2]
#         duration = JSSP[job][current_job_step[job]*2 + 1]
#         current_job_step[job] = current_job_step[job] + 1

#         # If the previous job on another machine ends after the current job is scheduled to start,
#         #  we need to delay the current job's start time
#         #  otherwise, place at the end of the current machine's schedule
#         if(previous_job_end_times[job] > machine_times[machine]):
#             dead_time = previous_job_end_times[job] - machine_times[machine]
#             machine_times[machine] += dead_time                   #machine start time
#             start_time = machine_times[machine]
#             previous_job_end_times[job] = machine_times[machine]  #this job start time
#             machine_times[machine] += duration                    #machine end time
#             previous_job_end_times[job] += duration               #job end time

#         else:
#             start_time = machine_times[machine]
#             machine_times[machine] += duration
#             previous_job_end_times[job] = start_time + duration

#         reconstruction_tuple = (job, machine, start_time, duration)
#         reconstruction[machine][current_machine_step[machine]] = reconstruction_tuple
#         current_machine_step[machine] += 1

#     print(machine_times)
#     print(f"Makespan: {machine_times.max()}")
#     plot_JSSP_Gantt(reconstruction, num_jobs, num_machines)

#     return 0