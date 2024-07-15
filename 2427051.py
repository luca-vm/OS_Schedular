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
