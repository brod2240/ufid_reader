# import gui functions
#import customtkinter
import sys
import time
import os, subprocess
#sys.path.append("../GUI")
#from gui import *
sys.path.append('../Validation')
import validation
from gui import *

f=open("../Testdata/time/scanTimes.txt","w")
def changeFrame(self,state):
    if state == 0 :
        self.select_frame_by_name("scan")
    elif state == 1:
        self.select_frame_by_name("course")
    elif state == -1 :
        self.select_frame_by_name("manual")
    
    

def frameLoop(self,queue,state):
    #test = input()
   # print(state)
    #changeFrame(self,0)
   # test = input()
    #changeFrame(self,0)
    #state = state + 1

   if queue.qsize() > 0 :
       nextState = queue.get()
       changeFrame(self,0)
       # print(nextState)
   else :
      nextState = state
      changeFrame(self,1)
    
    #while(1) :
       # maer = 9
   self.after(1000,lambda: frameLoop(self,queue,state))


def capture_scan(self, event):
    self.scan_in += event.char

    if event.keysym == "Return":
        self.process_scan()

def process_scan(self):
    start = time.time()
    if len(self.scanner_input.strip()) == 16:

        valid = validation.validate("10000000d340eb60",card_iso=self.scanner_input.strip())
    else:
        valid = validation.validate("10000000d340eb60",card_ufid=self.scanner_input.strip())
    end = time.time()
    time_total =(end - start)
    print(str(time_total))
    f.write(str(time_total)+'\n')
    f.flush()
    if valid["Valid"] == 0:

       # self.select_frame_by_name("success")
        #self.after(3000,self.select_frame_by_name("scan"))
        self.select_frame_by_name("success")
        #sleep(3)
       # self.select_frame_by_name("scan")
    else:
        self.select_frame_by_name("fail")
       # self.after(3000,self.select_frame_by_name("scan"))
    self.scanner_input = ""

def gui_main_loop():
    app=App()

   # print(dir(validation))
    #app.select_frame_by_name("scan")
   # app.after(0,frameLoop(app,shared_queue,1))
    app.select_frame_by_name("scan")
    app.mainloop()
    print("gothere")
   # valid = validation.validate("10000000d340eb60",card_iso="2000000000000000")
   # print(valid["Valid"])
   # time.sleep(5)
   # while(1):

        # call corresponding functions to display certain states
        #gui.main()
        #os.system('DISPAY=:0 python ../GUI/gui.py')
       # subprocess.run(['python','../GUI/gui.py'])
        
       # app.select_frame_by_name("scan")
        #state = 6

        #if state == 0: # loading screen
           # print() # temp
        #elif state == 1: # display student
           # print()
        #elif(state == 2): # scan ID prompt, etc
           # print()

        # if shutdown: 
        #     break

if __name__ == "__main__":
    gui_main_loop()
    #f.flush()
   # f.close()
