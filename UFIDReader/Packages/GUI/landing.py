import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("500x600")

landing_frame = customtkinter.CTkFrame(master=root)
landing_frame.pack(pady=2, padx=2, fill="both", expand=True)

label = customtkinter.CTkLabel(master=landing_frame, text="Scan UFID", font=("Roboto", 50))
label.pack(pady=5, padx=10)
label2 = customtkinter.CTkLabel(master=landing_frame, text="or", font=("Roboto", 50))
label2.pack(pady=5, padx=10)
label3 = customtkinter.CTkLabel(master=landing_frame, text="Tap Below", font=("Roboto", 50))
label3.pack(pady=5, padx=10)

img = customtkinter.CTkImage(light_image=Image.open("images/arrow.png"), dark_image=Image.open("images/arrow.png"), size=(200,200))
img_label = customtkinter.CTkLabel(master=landing_frame, text='', image=img)
img_label.pack(pady = 40)

search_button = customtkinter.CTkButton(master=landing_frame, text="Manual Search", width=75, height=50, corner_radius=10,fg_color="blue")
search_button.place(x=350,y=500)

root.mainloop()