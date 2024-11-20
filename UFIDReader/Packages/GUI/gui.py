import customtkinter, os
from PIL import Image, ImageTk
import time, threading

from src.main import process_scan

image_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images'))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # for hard coded resolution testing
        #screen_width = 1080
        #screen_height = 720

        # Dynamic font sizes based on screen size
        font_size_information = max(16, int(screen_height * 0.04))  # Minimum size for font is 16, make sure at least that value
        font_size_prompt = max(16, int(screen_height * 0.1))
        font_size_result = max(16, int(screen_height * 0.04))
        font_size_loading = max(16, int(screen_height * 0.06))

        # Dynamic image sizes based on screen size
        prompt_image_size = int(screen_height * 0.3)
        result_image_size = int(screen_height* 0.5)
        spinner_gif_size = int(screen_height* 0.3)
        gator_logo_size = int(screen_height*0.25)

        self.geometry(f"{screen_width}x{screen_height}")
        self.scanner_input = ""
        self.prev_scan = ""

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create information frame, which contains project name and current date/time. Will be displayed at all times on left side of screen.
        self.information_frame_init(font_size_information, screen_height, gator_logo_size)

        # create scan frame with prompt text and arrow image
        self.scan_frame_init(font_size_prompt, screen_height, prompt_image_size)

        # create loading frame for spinner gif
        #self.loading_frame_init(spinner_gif_size, font_size_loading)

        # #create success frame with image and text label
        self.success_frame_init(result_image_size, font_size_result)

        # #create fail frame with image and text label
        self.fail_frame_init(result_image_size, font_size_result)

        # make "interrupt" for any incoming key strokes in tkinter instance, which will be the iso or ufid
        self.bind_all("<Key>", self.capture_scan)

    def information_frame_init(self, font_size_information, screen_height, gator_logo_size):
        self.information_frame = customtkinter.CTkFrame(
            self, 
            corner_radius=0
        )
        self.information_frame.grid(row=0, column=0, sticky="nsew")

        # project name
        self.information_frame.grid_rowconfigure(0, weight=1)    
        self.information_frame_title_top = customtkinter.CTkLabel(
            self.information_frame, 
            text = " UFID Check-In \n System ", 
            compound = "left", 
            font = customtkinter.CTkFont(size=font_size_information, weight="bold")
        )
        self.information_frame_title_top.grid(row=0, column=0, padx=0, pady=int(screen_height * 0.05), sticky="new")

        self.information_frame_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_dir_path, "gators_logo.png")),
            size=(gator_logo_size,gator_logo_size*(2/3))
        )

        self.information_frame_image_label = customtkinter.CTkLabel(
            self.information_frame, 
            text = "",
            compound = "left", 
            image = self.information_frame_image,
            font = customtkinter.CTkFont(size=font_size_information, weight="bold")
        )
        self.information_frame_image_label.place(anchor="c", relx=0.5, rely=0.3)

        self.invisible_text_box = customtkinter.CTkEntry(
            self.information_frame,
            font=customtkinter.CTkFont(size=font_size_information, weight="bold"),
            fg_color="transparent",
            border_width=0,
            text_color="black",
            justify="center",
        )
        self.invisible_text_box.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, int(screen_height * 0.05)))

        # mostly for testing, with an empty text field users cant see it, and they cant use it anyway with no mouse plugged in during expected use
        # is positioned directly over the date and time, touching the left side of the screen
        self.exit_button = customtkinter.CTkButton(
            self.information_frame, 
            corner_radius=0, 
            height=40, 
            border_spacing=10, 
            text="",
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w", 
            command=lambda:self.destroy()
        )
        self.exit_button.grid(row=2, column=0, sticky="ew")

        # current date and time
        self.information_frame_time = customtkinter.CTkLabel(
            self.information_frame, 
            text = "", 
            compound = "left", 
            font = customtkinter.CTkFont(size=max(16,font_size_information-10), weight="bold")
        )
        self.information_frame_time.grid(row=3, column=0, padx=0, pady=(0, int(screen_height * 0.05)), sticky="sew")
        self.update_time() # start method to change current date and time every second, used to make sure display doesnt go to sleep

    def scan_frame_init(self, font_size_prompt, screen_height, prompt_image_size):
        self.scan_frame = customtkinter.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color="white",
            bg_color="white"
        )
        self.scan_frame.grid_columnconfigure(0, weight=1)

        self.prompt_label = customtkinter.CTkLabel(
            self.scan_frame, 
            text=" Swipe UFID or \n tap below", 
            #font=("Roboto", font_size_prompt),
            font=customtkinter.CTkFont("Roboto",size=font_size_prompt),#, weight="bold"),
            anchor="center",
            text_color="black"#'#0f4ef5'
        )
        self.prompt_label.grid(padx=0, pady=(int(screen_height * 0.1), int(screen_height * 0.01)))

        img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_dir_path, "arrow.png")), 
            size=(prompt_image_size,prompt_image_size)
        )
        self.img_label = customtkinter.CTkLabel(
            self.scan_frame, 
            text='', 
            image=img
        )
        self.img_label.grid(padx=0, pady = int(screen_height * 0.01))

    def loading_frame_init(self, spinner_gif_size, font_size_loading):
        self.loading_frame = customtkinter.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color="white"
        )        
        self.loading_frame.grid_rowconfigure(0, weight=1)
        self.loading_frame.grid_columnconfigure(1, weight=1)

        self.spinner_gif = Image.open(os.path.join(image_dir_path, "loading.gif"))
        self.frames = []

        with Image.open(os.path.join(image_dir_path, "loading.gif")) as image:
            try:
                while True:
                    frame = customtkinter.CTkImage(
                        light_image=image.copy(),
                        size=(spinner_gif_size,spinner_gif_size)
                    )
                    image.seek(image.tell() + 1)
                    self.frames.append(frame)
            except EOFError: # reached end of gif frames, continue
                pass

        self.is_loading = 0

        self.loading_label = customtkinter.CTkLabel(
            self.loading_frame, 
            text='', 
            image=None
        )
        self.loading_label.place(anchor="c", relx=0.5, rely=0.60)

        self.loading_text = customtkinter.CTkLabel(
            self.loading_frame, 
            text="Validating...", 
            font=("Roboto", font_size_loading),
            image=None
        )
        self.loading_text.place(anchor="c", relx=0.5, rely=0.45)

        self.update_animation()
        

    def success_frame_init(self, result_image_size, font_size_result):
        self.success_frame = customtkinter.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color="white",
            bg_color="white"
        )
        self.success_frame.grid_rowconfigure(0, weight=1)
        self.success_frame.grid_columnconfigure(1, weight=1)

        self.success_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_dir_path, "success_gator_tp.png")),
            size=(result_image_size,result_image_size)
        )
        
        # self.success_image = customtkinter.CTkImage(
        #     light_image=Image.open(os.path.join(image_dir_path, "checkmark.png")),
        #     size=(result_image_size,result_image_size)
        # )        
        
        self.success_image_label = customtkinter.CTkLabel(
            self.success_frame, 
            text="", 
            image=self.success_image
        )
        self.success_image_label.place(anchor="c",relx=0.5, rely=0.40)

        self.success_text_label = customtkinter.CTkLabel(
            self.success_frame, 
            text="",
            font=("Roboto", font_size_result)
        )
        self.success_text_label.place(anchor="c", relx=0.5, rely=0.75)
    
    def fail_frame_init(self, result_image_size, font_size_result):
        self.fail_frame = customtkinter.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color="white",
            bg_color="white"
        )
        self.fail_frame.grid_rowconfigure(0, weight=1)
        self.fail_frame.grid_columnconfigure(1, weight=1)

        self.fail_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_dir_path, "incorrect.png")), 
            size=(result_image_size,result_image_size)
        )

        self.fail_image_label = customtkinter.CTkLabel(
            self.fail_frame, 
            text='', 
            image=self.fail_image
        )
        self.fail_image_label.place(anchor="c",relx=0.5, rely=0.40)

        self.fail_text_label = customtkinter.CTkLabel(
            self.fail_frame, 
            text="",
            font=("Roboto", font_size_result)
        )
        self.fail_text_label.place(anchor="c", relx=0.5, rely=0.75)

    def update_time(self):
        current_date = time.strftime("%d %b %Y")
        current_time = time.strftime("%I:%M:%S").lstrip('0')

        self.information_frame_time.configure(text=f" {current_date} \n {current_time} ")
        self.after(1000, self.update_time)

    def update_animation(self, frame_index = 0):
        if(self.is_loading == 1):
            print(self.is_loading)
            self.loading_label.configure(image=self.frames[frame_index])
            temp = (frame_index + 1) % len(self.frames)
            self.after(10, lambda: self.update_animation(temp))
        else:
            self.after(10, lambda: self.update_animation(frame_index))

    def select_frame_by_name(self, name, student_info):
        self.scan_frame.grid_remove()
        self.success_frame.grid_remove()
        self.fail_frame.grid_remove()
        #self.loading_frame.grid_forget()
    
        match name:
            case "scan":
                self.scan_frame.grid(row=0, column=1, sticky="nsew")
            case "load":
                pass
                #self.loading_frame.grid(row=0, column=1, sticky="nsew")
                #self.is_loading = 1
            case "success":
                output = "" + student_info["First Name"] + " " + student_info["Last Name"] + " has been validated successfully."

                self.success_text_label.configure(text=output)
                self.success_text_label.place(anchor="c", relx=0.5, rely=0.75)

                self.success_frame.grid(row=0,column=1, sticky="nsew")
                self.success_frame.update_idletasks()

                self.after(3500, lambda: self.select_frame_by_name("scan", student_info=None))
            case "fail":
                output = ""
                match student_info["Valid"]:
                    case -1:
                        output = "Serial Number not found."
                    case -2:
                        output = "UFID not found. Please use the form provided by your\nprofessor to add yourself to the system."
                    case -3:
                        output = "Incorrect time. Please scan during your class period."
                    case -4:
                        output = "Please scan during a school day."
                    case _:
                        output = ""

                self.fail_text_label.configure(text=output)
                self.fail_text_label.place(anchor="c", relx=0.5, rely=0.75)

                self.fail_image_label.place(anchor="c",relx=0.5, rely=0.40)

                self.after(100, lambda : self.fail_frame.grid(row=0,column=1, sticky="nsew"))
                
                self.fail_frame.update_idletasks()
                
                self.after(5000, lambda: self.select_frame_by_name("scan", student_info=None))
            case _:
                self.scan_frame.grid_forget()
                self.success_frame.grid_forget()
                self.fail_frame.grid_forget()
        
    def capture_scan(self,event):
        self.scanner_input+=event.char
        if event.keysym == "Return":
                #self.select_frame_by_name("load", student_info=None)
                process_scan(self)
                self.invisible_text_box.delete(0, 'end') #testing purposes, clear text box

if __name__ == "__main__":
    app = App()
    app.mainloop()