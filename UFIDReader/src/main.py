# library imports, and required python modules
import sys, time, os
import signal
import RPi.GPIO as GPIO


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Packages.GUI import * #use __init__.py to classify folders as packages in the eyes of python for import
from Packages.Validation import *

exam_mode = 0 # global var

class Interrupts():
    button_GPIO = 18 # GPIO 18, but using pin 12, see rpi pinout
    hold_time = 2
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_GPIO, GPIO.FALLING, callback=self.toggle_operation_mode, bouncetime=20) # non blocking
        
        
        signal.signal(signal.SIGINT, self.cleanup) # after program exits, cleanup GPIO (ctrl c or otherwise)
        #signal.pause()

    def toggle_operation_mode(self, channel):
        #print("entered")

        start = time.time()
        while(GPIO.input(self.button_GPIO) == 0 and (time.time() - start < self.hold_time)):
            time.sleep(0.01)
            #pass

        if (time.time() - start > self.hold_time): #if button greater 2 second statement active
            print("long press")
            # shutdown
        else:
            print("single press")
            global exam_mode
            exam_mode ^= 1


    def cleanup(self, sig, frame): # set all gpio back to input, and exit safely
        GPIO.cleanup()
        sys.exit(0)
    
    def test_connection(self):
        try:
            while True:
                #time.sleep(0.1)
                pass
        except KeyboardInterrupt:
            self.cleanup()

# run in main for testing, these two lines
# if __name__ == "__main__":
#     interrupts = Interrupts()
#     interrupts.test_connection()

# for testing latency and storing access times
def process_scan(self):
    start = time.time()
    if len(self.scanner_input.strip()) == 16:

        valid = validate(exam_mode, "10000000d340eb60",card_iso=self.scanner_input.strip())
    else:
        valid = validation.validate(exam_mode, "10000000d340eb60",card_ufid=self.scanner_input.strip())
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