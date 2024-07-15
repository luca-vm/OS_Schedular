import sys
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Define the process data clas
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency

def main():
    # Check if the correct number of arguments is provided
    import sys
    if len(sys.argv) != 2:
        return 1

    # Extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # Define the number of processes
    num_processes = 0

    # Initialize an empty list for process data
    data_set = []

    # Open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # Read the number of processes from the file
            num_processes = int(file.readline().strip())

            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency))
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1


    """
    TODO Your Algorithm - assign your output to the output variable
    """

      # Implement your scheduling algorithm here
    def fcfs_scheduler(processes):
        schedule_order = []
        current_time = 0

        while len(processes) > 0:
            process = processes.pop(0)

            dur = process.duration

            # Add the current time step for the duration of the process
            i = 0
            while i < dur:
                i+=1
                current_time += 1
                # Check for IO and add it if needed
                if process.io_frequency > 0 and (i) % (process.io_frequency + 1) == 0:
                    schedule_order.append('!' + process.name)
                    dur += 1
                else:
                    schedule_order.append(process.name)

        
        return ' '.join(schedule_order)  # Join the scheduling order with spaces

        # output = fcfs_scheduler(data_set)

  
    # def mlfq_scheduler(processes):
        schedule_order = []
        current_time = 0

        # Define multiple priority queues (queues is a list of lists)
        queues = [[] for _ in range(3)]

        while len(processes) > 0:
            # Check for new arrivals and place them in the highest priority queue (queue[0])
            for process in processes:
                if process.arrival_time <= current_time:
                    queues[0].append(process)
                    processes.remove(process)

            for queue in queues:
                if queue:
                    # Get the next process from the highest non-empty queue
                    process = queue.pop(0)

                    i = 0
                    while process.duration > 0:
                        current_time += 1

                        # Check for IO and add it if needed
                        if process.io_frequency > 0 and current_time % (process.io_frequency + 1) == 0:
                            schedule_order.append('!' + process.name)
                        else:
                            schedule_order.append(process.name)
                            process.duration -= 1

                        i += 1

                    if process.duration > 0:
                        # Move the process to a lower priority queue (if available)
                        next_queue = min(queues.index(queue) + 1, len(queues) - 1)
                        queues[next_queue].append(process)

                    # No need to process further in lower priority queues in this time slice
                    break

        return ' '.join(schedule_order)  # Join the scheduling order with spaces
    # the scheduling order with spaces

    def mlfq_scheduler(processes):
        schedule_order = []
        current_time = 0

        # Define the time slices for each queue
        time_slices = [5, 10, 20]

        # Create multiple queues
        queues = [[] for _ in range(len(time_slices))]

        while len(processes) > 0 or any(queues):
            # Move arrived processes to the appropriate queue
            for process in processes:
                if process.arrival_time <= current_time:
                    queues[0].append(process)

            # Iterate through the queues
            for i, queue in enumerate(queues):
                if not queue:
                    continue

                process = queue.pop(0)
                remaining_time = min(time_slices[i], process.duration)

                for _ in range(remaining_time):
                    current_time += 1

                    # Check for IO and add it if needed
                    if process.io_frequency > 0 and current_time % process.io_frequency == 0:
                        schedule_order.append('!' + process.name)
                    else:
                        schedule_order.append(process.name)

                if process.duration > remaining_time:
                    # Move the process to a higher priority queue
                    queues[min(i + 1, len(queues) - 1)].append(process)

            # Remove completed processes
            for i, queue in enumerate(queues):
                queues[i] = [process for process in queue if process.duration > 0]

        return ' '.join(schedule_order)  # Join the scheduling order with spaces

   
    #     schedule_order = []
    #     current_time = 0

    #     while len(processes) > 0:
    #         # Find the process with the shortest remaining execution time
    #         arrived_processes = [p for p in processes if p.arrival_time <= current_time]
    #         shortest_process = min(arrived_processes, key=lambda x: x.duration)

    #         process = shortest_process
    #         dur = process.duration
    #         i = 0
    #         while (process.name == shortest_process.name) and ( i < dur):
    #             i+=1
    #             current_time += 1
    #             if process.io_frequency > 0 and (i) % (process.io_frequency + 1) == 0:
    #                 schedule_order.append('!' + process.name)
    #                 dur += 1
    #                 # process.duration += 1
    #             else:
    #                 schedule_order.append(process.name)
    #                 process.duration -= 1
                
                
    #             arrived_processes = [p for p in processes if p.arrival_time <= current_time]
    #             shortest_process = min(arrived_processes, key=lambda x: x.duration)


    #             if (i >= dur):
    #                 processes.remove(process)
    #                 break


                    
    #     return ' '.join(schedule_order)  # Join the scheduling order with spaces
    def stcf_scheduler(processes):
        schedule_order = []
        current_time = 0

        while len(processes) > 0:
            # Find the process with the shortest remaining execution time
            arrived_processes = [p for p in processes if p.arrival_time <= current_time]
            
            if not arrived_processes:
                current_time += 1
                continue

            shortest_process = min(arrived_processes, key=lambda x: x.duration)

            process = shortest_process
            dur = process.duration

            i = 0
            while process.duration > 0:
                i += 1
                current_time += 1

                # Check for IO and add it if needed
                if process.io_frequency > 0 and i % (process.io_frequency + 1) == 0:
                    schedule_order.append('!' + process.name)
                    process.duration += 1  # Add an extra time step for IO
                else:
                    schedule_order.append(process.name)

                process.duration -= 1

            # Remove the completed process from the list
            processes.remove(process)

        return ' '.join(schedule_order)  # Join the scheduling order with spaces
   


    output = stcf_scheduler(data_set)
        

    # output = "AB AC AB !AD BA CB !BL BX AB" #Example output


    """
    End of your algorithm
    """

    

    # Open a file for writing
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
