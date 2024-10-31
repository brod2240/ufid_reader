# library imports, and required python modules
import sys, time, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Packages.GUI import * #use __init__.py to classify folders as packages in the eyes of python for import
from Packages.Validation import *

# for testing latency and storing access times
def process_scan(self):
    start = time.time()
    if len(self.scanner_input.strip()) == 16:

        valid = validate("10000000d340eb60",card_iso=self.scanner_input.strip())
    else:
        valid = validation.validate("10000000d340eb60",card_ufid=self.scanner_input.strip())
    end = time.time()
    time_total =(end - start)
    print(str(time_total))

    scantimes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Testdata/scanTimes.txt')) # get absolute path, make sure can find the requirements.txt no matter where file is run from

    if not os.path.exists(scantimes_path):
        with open(scantimes_path, 'a') as f:
            f.write('')
    else:
        with open(scantimes_path, 'a') as f:
            f.write(str(time_total) + '\n')    

    f.write(str(time_total)+'\n')
    f.flush()
    if valid["Valid"] == 0:
        self.select_frame_by_name("success")
    else:
        self.select_frame_by_name("fail")
    self.scanner_input = ""

def gui_main_loop():
    app=App()
    app.select_frame_by_name("scan")
    app.mainloop()

if __name__ == "__main__":
    gui_main_loop()