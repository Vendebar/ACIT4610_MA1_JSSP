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

#For GA, all we're rally changing is start time. the time implies
#  order
# resource on using libraries to draw gantt charts
# https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib
