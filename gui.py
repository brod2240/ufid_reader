import customtkinter
import os
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("image_example.py")
        self.geometry("1000x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="UFID ATTENDANCE CHECK",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Scan ID",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Manual Search",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="")
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        label = customtkinter.CTkLabel(self.home_frame, text="Scan UFID", font=("Roboto", 50))
        label.grid(pady=5, padx=10)
        label2 = customtkinter.CTkLabel(self.home_frame, text="or", font=("Roboto", 50))
        label2.grid(pady=5, padx=10)
        label3 = customtkinter.CTkLabel(self.home_frame, text="Tap Below", font=("Roboto", 50))
        label3.grid(pady=5, padx=10)

        img = customtkinter.CTkImage(light_image=Image.open("images/arrow.png"), dark_image=Image.open("images/arrow.png"), size=(200,200))
        img_label = customtkinter.CTkLabel(self.home_frame, text='', image=img)
        img_label.grid(pady = 40)

        text_box = customtkinter.CTkTextbox(self.home_frame)
        text_box.focus_force()
        text_box.grid()

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        manual_label = customtkinter.CTkLabel(self.second_frame, text="Type UFID", font=("Roboto", 50))
        manual_label.grid(pady=5, padx=10)
        manual_label.place(anchor="c",relx=0.5, rely=0.15)
        manual_label2 = customtkinter.CTkLabel(self.second_frame, text="Below", font=("Roboto", 50))
        manual_label2.grid(pady=5, padx=10)
        manual_label2.place(anchor="c",relx=0.5, rely=0.30)
        input_box = customtkinter.CTkEntry(self.second_frame, placeholder_text="Type in UFID", height=50, width=200, justify='center', corner_radius=15, state="normal")
        input_box.grid(pady=20)
        input_box.place(anchor="c",relx=0.5, rely=0.5)
        search_button = customtkinter.CTkButton(self.second_frame, text="Search", width=150, height=40, corner_radius=10, font=("Roboto", 15))
        search_button.grid(padx=5, pady=10)
        search_button.place(anchor="c", relx=0.5, rely=0.65)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()


