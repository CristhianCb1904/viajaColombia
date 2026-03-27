import customtkinter as ctk
from tkintermapview import TkinterMapView

ctk.set_appearance_mode("dark")

ventana = ctk.CTk()
ventana.title("Viaja por Colombia!")
ventana.geometry("1200x700")

header = ctk.CTkFrame(ventana, fg_color="#A200FF", corner_radius=0)
header.pack(fill="x")

titulo = ctk.CTkLabel(header, text="Viaja por Colombia!", font=("arial", 24, "bold"))

titulo.pack(side="left", padx=20, pady=25)


body = ctk.CTkFrame(ventana, fg_color="#2B2B2B")
body.pack(fill="both", expand=True, padx=20, pady=20)

left_frame = ctk.CTkFrame(body, fg_color="#9000FF")
right_frame = ctk.CTkFrame(body, fg_color="#2B2331")
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

deepButton = ctk.CTkButton(right_frame, text="Busca Profunda", font=("arial", 16, "bold"), fg_color="#A200FF", hover_color="#9000FF")
deepButton.pack(pady=20)
uniformButton = ctk.CTkButton(right_frame, text="Busca Uniforme", font=("arial", 16, "bold"), fg_color="#A200FF", hover_color="#9000FF")
uniformButton.pack(pady=20)

#Mapa interactivo
mapa_frame = ctk.CTkFrame(left_frame, fg_color="#9000FF")
mapa_frame.pack(fill="both", expand=True, padx=20, pady=20)

mapWidget = TkinterMapView(mapa_frame, width=800, height=600, corner_radius=0)
mapWidget.pack(fill="both", expand=True)
mapWidget.set_position(4.5709, -74.2973)  
mapWidget.set_zoom(6)

mapWidget.set_marker(4.5709, -74.0721, text="Bogotá")

ventana.mainloop()