import os, threading
from time import sleep, strftime

class Temperature_Poll_Thread(threading.Thread):
    def __init__(self, time_sleep = 0.1, time_run = 10, file_loc = "../Testdata/core_temp/", name = 'temperature_poll_thread'):
        self.time_sleep = time_sleep
        self.time_run = time_run
        self.file_loc = file_loc

        self.read_temp_cmd = "vcgencmd measure_temp" # cmd to retrieve core_temp of rpi      

        super(Temperature_Poll_Thread, self).__init__(name = name, daemon = True) # daemon, will make it daemon thread which runs in background and terminates when main program exits

        self.file = self.open_file()

        self.sentinel = True

        self.start() # begin the thread, starts running the run function below

    def read_file_identifier(self, file_loc_date):
        curr_count = 0
        for filename in os.listdir(file_loc_date):
            if(filename.startswith("core_temp_") and filename.endswith(".csv")):
                counter = filename[10:-4]
                if(counter.isdigit()):
                    curr_count = max(curr_count, int(counter))

        return curr_count + 1          


    def open_file(self):
        file_loc_date = f"{self.file_loc}{strftime('%m-%d')}"
        print(file_loc_date)
        counter = 0

        if not os.path.exists(file_loc_date):
            try:
                os.makedirs(file_loc_date, exist_ok=True)
            except Exception as e:
                print(f"Error creating directories: {e}")
                exit(1)
        else:
            counter = self.read_file_identifier(file_loc_date)

        new_file_name = f"core_temp_{counter}.csv"

        file_path = os.path.join(file_loc_date, new_file_name)

        return open(file_path, 'a')
        
    def poll_core_temp(self):
        #curr_core_temp_str = os.popen(self.read_temp_cmd, "r",).readline()
        curr_core_temp_str = "temp=44.4"
        curr_core_temp = float(curr_core_temp_str[5:-3]) # temp=44.4'C
        #time = strftime('%H:%M:%S')

        self.file.write(f"{curr_core_temp}\n")


    def run(self):
        while(self.sentinel):
            self.poll_core_temp()
            sleep(self.time_sleep) # determine how many samples are taken in a given second

    def shutdown(self):
        self.file.close()
        self.sentinel = False # exit infinite loop, finish thread      


def main():
    Temp_Poll = Temperature_Poll_Thread(time_run=20) # time_run is the amount of seconds for the temperature to poll. 
    # default frequency is 0.1 for 10 data points a second

    sleep(Temp_Poll.time_run)
    Temp_Poll.shutdown()

main()