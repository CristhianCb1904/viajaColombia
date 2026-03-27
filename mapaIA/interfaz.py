import numpy as np
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
deepButton.pack(padx=20, pady=20)
uniformButton = ctk.CTkButton(right_frame, text="Busca Uniforme", font=("arial", 16, "bold"), fg_color="#A200FF", hover_color="#9000FF")
uniformButton.pack(padx=20, pady=20)

#Mapa interactivo
mapa_frame = ctk.CTkFrame(left_frame, fg_color="#9000FF")
mapa_frame.pack(fill="both", expand=True, padx=20, pady=20)

mapWidget = TkinterMapView(mapa_frame, width=800, height=600, corner_radius=0)
mapWidget.pack(fill="both", expand=True)
mapWidget.set_position(4.5709, -74.2973)  
mapWidget.set_zoom(6)

mapWidget.set_marker(4.5709, -74.0721, text="Bogotá")

ventana.mainloop()


#Capitales

capitales = np.array([
                    "Leticia", "Medellín", "Arauca", "Barranquilla", "Cartagena", "Tunja", "Manizales", "Florencia",
                    "yopal", "Popayán", "Valledupar", "Quibdó", "Montería", "Bogotá", "Inírida", "San José del Guaviare",
                    "Neiva", "Riohacha", "Santa Marta", "Villavicencio", "San Juan de Pasto", "San José de Cúcuta", 
                    "Mocoa", "Armenia", "Pereira", "San Andrés", "Bucaramanga", "Sincelejo", "Ibagué", "Cali", "Mitú", "Puerto Carreño" ] )

# Coordenadas de las capitales
#coordenadas = np.array([[ -4.215, -69.940], [6.244, -75.573], [7.086, -70.759], [10.968, -74.781], [10.391, -75.479], [5.537, -73.367], [5.068, -75.517],
#                        [1.613, -75.567], [2.454, -76.606], [2.444, -76.614], [10.463, -73.253], [5.694, -76.651], [8.753, -75.879], [4.5709, -74.2973], [2.585, -72.639],
#                        [2.927, -75.280], [11.544, -72.907], [11.240, -74.199], [4.142, -73.629], [7.893, -72.507], [1.258, -77.281], [4.533, -75.681], [4.814, -75.696], [12.584, -81.700],
#                        [7.119, -73.122], [4.438, -75.232], [3.451, -76.531], [1.252, -70.221], [6.186, -67.493] ])