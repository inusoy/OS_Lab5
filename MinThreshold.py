import Processor as pr
import numpy as np
import copy


def minThreshold(process_list_to_copy, p, r, time_max, N):
    # N - number of processors (50-100)
    # p - threshold of processor utilization (process will be send there if utilization in smaller than p)
    # z - maximum amount of queries for processor utilization
    # time_max - maximum number of ticks
    sum_of_means = 0
    sum_of_requests = 0
    sum_of_process_migrations = 0
    processor_list = []
    process_list = copy.deepcopy(process_list_to_copy)
    for i in range(N):
        processor_list.append(pr.CProcessor())  # create a list of N processors

    for i in range(time_max):  # simulate the passing of time
        for process in process_list:
            process.starting_time -= 1  # decrease starting time of all processes in queue
            if process.starting_time == 0:  # if a process starting time reaches 0, it's added to a random processor
                p_temp = p  # keep track of how many times you've asked for other processes utilization
                times_repeated = 0
                if processor_list[process.starting_proc].utilization > p:
                    while p_temp:
                        times_repeated += 1
                        random_processor = np.random.randint(0, N)  # randomly choose a processor
                        sum_of_requests += 1
                        if processor_list[random_processor].calc_util() < p_temp:  # ask for its utilization, and if it's lower than p
                            processor_list[random_processor].processes_running.append(process)  # give it that process
                            sum_of_process_migrations += 1
                            break
                        else:
                            if times_repeated == N:
                                p_temp += 1  # if you've asked N times, increase the acceptable load
                                times_repeated = 0
                else:
                    processor_list[process.starting_proc].processes_running.append(process)

        for processor in processor_list:  # update running time of all processes on all processors
            if processor.utilization < r:
                random_processor = np.random.randint(0, N)
                if processor.utilization < processor_list[random_processor].calc_util():
                    processor.processes_running.append(processor_list[random_processor].processes_running[0])
                    del processor_list[random_processor].processes_running[0]
            for process_running in processor.processes_running:
                process_running.time_required -= 1
                if process_running.time_required == 0:
                    processor.processes_running.remove(process_running)
            processor.update_mean_util()  # update mean processor load of each processor

    # print("Minimum Threshold processor request, average utilization of each processor:")
    for temp in range(len(processor_list)):
        # print("Processor {0}: {1:3.2f}%".format(temp, processor_list[temp].get_mean_util()))
        sum_of_means += processor_list[temp].get_mean_util()
    # print("Mean utilization of all processors: {0:3.2f}%".format(sum_of_means / N))
    # print("Number of requests sent: {0}".format(sum_of_requests))
    # print("Number of processes migrated: {0}".format(sum_of_process_migrations))
    return sum_of_means/N, sum_of_requests, sum_of_process_migrations
