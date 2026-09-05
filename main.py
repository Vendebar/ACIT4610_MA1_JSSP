from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def read_JSSP(file_path: str) -> tuple[int, int, list[list[int]]]:

	values = Path(file_path).read_text(encoding="utf-8").split()
	if len(values) < 2:
		raise ValueError("The file must define the number of jobs and machines.")

	try:
		jobs, machines = map(int, values[:2])
		schedule = list(map(int, values[2:]))
	except ValueError as error:
		raise ValueError("The file must contain only integers.") from error

	if jobs < 0 or machines < 0:
		raise ValueError("jobs and machines must be non-negative.")

	columns = 2 * machines
	expected_schedule_values = jobs * columns
	if len(schedule) != expected_schedule_values:
		raise ValueError(
			"Expected " + str(expected_schedule_values) + " schedule values, "
			"but found " + str(len(schedule)) + "."
		)

	JSSP = [
		schedule[index * columns : (index + 1) * columns  ]
		for index in range(jobs)
	]
	return jobs, machines, JSSP

def plot_JSSP(JSSP: list[list[int]], schedule: list[int], num_jobs: int, num_machines: int):

	# each index is the job related to the row in the JSSP,
	#  and the value is the step of the job that is being scheduled
	machine_times = np.zeros(num_machines, dtype=int)
	current_job_step = list(np.zeros(num_jobs, dtype=int))
	previous_job_end_times = np.zeros(num_jobs, dtype=int)
	for job in schedule:
		machine = JSSP[job][current_job_step[job]*2]
		duration = JSSP[job][current_job_step[job]*2 + 1]
		current_job_step[job] = current_job_step[job] + 1

		# If the previous job on another machine ends after the current job is scheduled to start,
		#  we need to delay the current job's start time
		if(previous_job_end_times[job] > machine_times[machine]):
			dead_time = previous_job_end_times[job] - machine_times[machine]
			machine_times[machine] += dead_time                   #machine start time
			previous_job_end_times[job] = machine_times[machine] #job start time
			machine_times[machine] += duration                    #machine end time
			previous_job_end_times[job] += duration               #job end time
		else:
			machine_times[machine] += duration
			previous_job_end_times[job] += duration

		#print("Job: " + str(job) + ", Machine: " + str(machine) + ", Duration: " + str(duration))
		print(f"Machine times: {machine_times}")
		print(f"Previous job end times: {previous_job_end_times}")

	print(machine_times)

	return 0

if __name__ == "__main__":

	file = "testCases/la01.txt"
	jobs, machines, given_JSSP = read_JSSP(file)
	
	print("Jobs: " + str(jobs) + ", Machines: " + str(machines))
	for job in given_JSSP:
		for machine, duration in zip(job[::2], job[1::2]):
			print(" Machine: " + str(machine) + ", Duration: " + str(duration), end="")
		print()

	rng = np.random.default_rng()
	arr = np.repeat(np.arange(0, jobs), machines)
	rng.shuffle(arr)
	print(arr)
	print(len(arr))
	plot_JSSP(given_JSSP, arr, jobs, machines)
	print("bye!")

# txt structure
# jobs machines
# each row is a job
# every pair of numbers in a row is the machine number (which one) and the duration required on that machine.
# order of pairs implies the machine order that the job must run trough
# e.x.:
# 10 5
# 1 21 0 53 4 95 3 55 2 34
# ... (9 more rows)
# 
# (1 21)(0 53)(4 95)(3 55)(2 34) means:
# run this job on machine 1 for 21 min
# then on machine 0 for 53 min
# ... and finally, on machine 2 for 34 min
# each chromosome could be a 4-tuple of 4 ints,:
# (job num, machine num, duration, start time)
# to represent the problem space, could be:
# 2d array of these 3-tuples that omits the machine num of the
# 4-tuple above, row in 2d array could imply machine?
#    NOTE This might make it harder to verify job order is correct
# we could make it a 5-tuple including which step of the job it is
#  to preserve job order in the tuple so we don't have to do much
#  extra array navigation, just 1d array search+retrevial
# we could also have a 2d array like the original data but there would be logic
#  around the columns since that is each stage of the job?
#  so in the setup, run everything in column one first before moving on to column 2
#  this may perclude us from the optimals, but guarantees no conflicts
#  [job#][job order#] so position [2][3] is job 2, and the 4th step in the job process?
#  and the 3-tuple in there represents the machine num, duration, and time start?
# in any case, we read in the original data as a 2d int array 
#  for the use of initialization and verification
#  we have to verify all jobs are run, and in order, and not overlapping
#THE BELOW FEELS THE BEST SO FAR!!!
#if we use a 2d array of [job#][machine#] of ints where the int represnts the next machine to run,
#  from 0-(job# x machine# -1), then we can also gaurantee correct order by comparing
#  to the original data and changing the ordering (sorting) within rows (jobs) to ensure valid solutions

#For GA, all we're really changing is start time. the time implies
#  order. If we use above, it's just order and we calculate start time. much better
# resource on using libraries to draw gantt charts
# https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib

