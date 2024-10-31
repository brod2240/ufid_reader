import customtkinter, os
from PIL import Image

from src.main import process_scan

image_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images'))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}")
        self.scanner_input = ""

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="UFID ATTENDANCE CHECK", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.course_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Enter Course ID",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.course_button_event)
        self.course_button.grid(row=1, column=0, sticky="ew")
        self.scan_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Scan ID",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.scan_button_event)
        self.scan_button.grid(row=2, column=0, sticky="ew")

        self.manual_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Manual Search",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.manual_button_event)
        self.manual_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        self.exit_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=lambda:self.destroy())
        self.exit_button.grid(row=7, column=0, sticky="ew")

        #create course id input page
        self.landing_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        landing_label = customtkinter.CTkLabel(self.landing_frame, text="ID Scanned Successfully!", font=("Roboto", 50))
        landing_label.grid(pady=5, padx=10)
        landing_label.place(anchor="c",relx=0.5, rely=0.15)
        landing_label2 = customtkinter.CTkLabel(self.landing_frame, text="ID", font=("Roboto", 50))
        landing_label2.grid(pady=5, padx=10)
        landing_label2.place(anchor="c",relx=0.5, rely=0.30)
        course_box = customtkinter.CTkEntry(self.landing_frame, placeholder_text="Type Course ID", height=50, width=200, justify='center', corner_radius=15, state="normal")
        course_box.grid(pady=20)
        course_box.place(anchor="c",relx=0.5, rely=0.5)
        search_button = customtkinter.CTkButton(self.landing_frame, text="Enter", width=150, height=40, corner_radius=10, font=("Roboto", 15), command=lambda:self.select_frame_by_name("scan"))
        search_button.grid(padx=5, pady=10)
        search_button.place(anchor="c", relx=0.5, rely=0.65)

        # create scan frame
        self.scan_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.scan_frame.grid_columnconfigure(0, weight=1)

        self.scan_frame_large_image_label = customtkinter.CTkLabel(self.scan_frame, text="")
        self.scan_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        label = customtkinter.CTkLabel(self.scan_frame, text="Scan UFID", font=("Roboto", 50))
        label.grid(pady=5, padx=10)
        label2 = customtkinter.CTkLabel(self.scan_frame, text="or", font=("Roboto", 50))
        label2.grid(pady=5, padx=10)
        label3 = customtkinter.CTkLabel(self.scan_frame, text="Tap Below", font=("Roboto", 50))
        label3.grid(pady=5, padx=10)



        img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_dir_path, "arrow.png")), dark_image=Image.open(os.path.join(image_dir_path, "arrow.png")), size=(200,200))
        img_label = customtkinter.CTkLabel(self.scan_frame, text='', image=img)
        img_label.grid(pady = 40)

        # create manual search frame
        self.manual_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        manual_label = customtkinter.CTkLabel(self.manual_frame, text="Type UFID", font=("Roboto", 50))
        manual_label.grid(pady=5, padx=10)
        manual_label.place(anchor="c",relx=0.5, rely=0.15)
        manual_label2 = customtkinter.CTkLabel(self.manual_frame, text="Below", font=("Roboto", 50))
        manual_label2.grid(pady=5, padx=10)
        manual_label2.place(anchor="c",relx=0.5, rely=0.30)
        self.input_box = customtkinter.CTkEntry(self.manual_frame, placeholder_text="Type in UFID", height=50, width=200, justify='center', corner_radius=15, state="normal")
        self.input_box.grid(pady=20)
        self.input_box.place(anchor="c",relx=0.5, rely=0.5)
        search_button = customtkinter.CTkButton(self.manual_frame, text="Search", width=150, height=40, corner_radius=10, font=("Roboto", 15), command=lambda:self.select_frame_by_name("fail"))
        search_button.grid(padx=5, pady=10)
        search_button.place(anchor="c", relx=0.5, rely=0.65)

        #create success page
        self.success_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.success_frame.grid_rowconfigure(0, weight=1)
        self.success_frame.grid_columnconfigure(1, weight=1)
        #self.success_frame.pack(expand=True, fill='both')
        self.success_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_dir_path, "checkmark.png")), dark_image=Image.open(os.path.join(image_dir_path, "checkmark.png")), size=(500,500))
        self.success_image_label = customtkinter.CTkLabel(self.success_frame, text='', image=self.success_image)
        self.success_image_label.grid(padx=10)
        self.success_image_label.place(anchor="c",relx=0.5, rely=0.25)

        #create fail page
        self.fail_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fail_frame.grid_rowconfigure(0, weight=1)
        self.fail_frame.grid_columnconfigure(1, weight=1)
        self.fail_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_dir_path, "incorrect.png")), dark_image=Image.open(os.path.join(image_dir_path, "incorrect.png")), size=(500,500))
        self.fail_image_label = customtkinter.CTkLabel(self.fail_frame, text='', image=self.fail_image)
        self.fail_image_label.grid(padx=10)
        self.fail_image_label.place(anchor="c",relx=0.5, rely=0.25)

        # select default frame
       # self.select_frame_by_name("course")
        self.bind_all("<Key>", self.capture_scan)




    def select_frame_by_name(self, name):
        # set button color for selected button
        self.course_button.configure(fg_color=("gray75", "gray25") if name == "course" else "transparent")
        self.scan_button.configure(fg_color=("gray75", "gray25") if name == "scan" else "transparent")
        self.manual_button.configure(fg_color=("gray75", "gray25") if name == "manual" else "transparent")
        # show selected frame
        if name == "scan":
            self.scan_frame.grid(row=0, column=1, sticky="nsew")
            self.navigation_frame.grid(row=0, column=0, sticky="nsew")
            self.navigation_frame.grid_rowconfigure(4, weight=1)
        else:
            self.scan_frame.grid_forget()
        if name == "manual":
            self.manual_frame.grid(row=0, column=1, sticky="nsew")
            self.navigation_frame.grid(row=0, column=0, sticky="nsew")
            self.navigation_frame.grid_rowconfigure(4, weight=1)
        else:
            self.manual_frame.grid_forget()
        if name == "course":
            self.landing_frame.grid(row=0, column=1, sticky="nsew")
            self.navigation_frame.grid_forget()
        else:
            self.landing_frame.grid_forget()
        if name == "success":
            self.success_frame.grid(row=0,column=1, sticky="nsew")
            self.success_frame.update_idletasks()
           # time.sleep(2)
            #self.select_frame_by_name("scan")
            #self.success_frame.tkraise()
            #print("Here")
            #self.navigation_frame.grid_forget()
            self.after(3000, lambda: self.select_frame_by_name("scan"))

        else:
            self.success_frame.grid_forget()
        if name == "fail":
            self.fail_frame.grid(row=0,column=1, sticky="nsew")
           # self.navigation_frame.grid_forget()
            self.fail_frame.update_idletasks()
            
            self.after(3000, lambda: self.select_frame_by_name("scan"))
        else:
            self.fail_frame.grid_forget()

    def scan_button_event(self):
        self.select_frame_by_name("scan")

    def manual_button_event(self):
        self.select_frame_by_name("manual")

    def course_button_event(self):
        self.select_frame_by_name("course")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def capture_scan(self,event):
        # self.scanner_input+=event.char
        # if event.keysym == "Return":
        #     process_scan(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()