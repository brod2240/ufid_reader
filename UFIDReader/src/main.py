# library imports, and required python modules
import sys, time, os
import signal


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Packages.GUI import * #use __init__.py to classify folders as packages in the eyes of python for import
from Packages.Validation import *

exam_mode = 0 # global var

# for testing latency and storing access times
def process_scan(self):
    start = time.time()
    if len(self.scanner_input.strip()) == 16:
        valid = validate(0, "10000000d340eb60",card_iso=self.scanner_input.strip())
    else:
        valid = validation.validate(0, "10000000d340eb60",card_ufid=self.scanner_input.strip())

    end = time.time()
    time_total =(end - start)
    print(str(time_total))

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Testdata'))

    if not os.path.exists(path):
        os.makedirs(path)

    scantimes_path = os.path.join(path, 'scanTimes.txt') # get absolute path, make sure can find the requirements.txt no matter where file is run from

    if not os.path.exists(scantimes_path):
        with open(scantimes_path, 'a') as f:
            f.write('')
    else:
        with open(scantimes_path, 'a') as f:
            f.write(str(time_total) + '\n')    

    #self.select_frame_by_name("success", student_info=valid)

    if valid["Valid"] == 0:
        self.select_frame_by_name("success", student_info=valid)
    else:
        self.select_frame_by_name("fail", student_info=valid)

    # reset scanner_input for new scan
    self.scanner_input = ""

def gui_main_loop():
    app=App()
    app.select_frame_by_name("scan", student_info=None)
    app.mainloop()

if __name__ == "__main__":
    gui_main_loop()
