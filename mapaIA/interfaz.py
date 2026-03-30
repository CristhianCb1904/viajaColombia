# busqueda de mapa de colombia - inteligencia Artificial
# 30/03/2026
# integrantes: Julian Alejandro Garcia Rubio, Cristhian Camilo Bermudez Silva, Miguel Angel Gonzales Contreras
# Profesor: Helioth Sanchez

# Indicaciones para iniciar el programa:
# -tener instalado Python
# -instalar las siguientes linesa de codigo para las librerias:

# * python -m pip install numpy
# * python -m pip install tkintermapview
# * python -m pip install customtkinter tkintermapview requests polyline

import customtkinter as ctk
from tkinter import StringVar
import tkintermapview
import requests
import polyline
import threading
import time
import heapq

# configuracion de la api a utilizar
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdlZWFiODljNjI4ZTRjYzE4YTdmZGUxMzcyMjQ4ZmJhIiwiaCI6Im11cm11cjY0In0="

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# coordenadas y grafos
coordenadas = {
    "Leticia": (-4.2153, -69.9408),
    "Arauca": (7.0869, -70.7619),
    "Barranquilla": (10.9685, -74.7813),
    "Cartagena": (10.3910, -75.4794),
    "Florencia": (1.6133, -75.5636),
    "Yopal": (5.3372, -72.3848),
    "Popayán": (2.4545, -76.6068),
    "Valledupar": (10.4631, -73.2532),
    "Quibdó": (5.6945, -76.6611),
    "Montería": (8.7470, -75.8448),
    "Bogotá": (4.7110, -74.0721),
    "Inírida": (3.8672, -67.9231),
    "San José del Guaviare": (2.5689, -72.6394),
    "Neiva": (2.9273, -75.2819),
    "Riohacha": (11.5449, -72.9070),
    "Santa Marta": (11.2408, -74.1990),
    "Villavicencio": (4.1420, -73.6268),
    "Pasto": (1.2136, -77.2819),
    "Cúcuta": (7.8891, -72.4968),
    "Mocoa": (1.1528, -76.6636),
    "Armenia": (4.5339, -75.6811),
    "San Andrés": (12.5833, -81.7000),
    "Sincelejo": (9.3047, -75.3978),
    "Ibagué": (4.4389, -75.2322),
    "Cali": (3.4516, -76.5320),
    "Mitú": (1.1983, -70.1733),
    "Puerto Carreño": (6.1850, -67.4933),
    "Tunja": (5.5353, -73.3678),
    "Bucaramanga": (7.1193, -73.1227),
    "Medellín": (6.2442, -75.5812),
    "Manizales": (5.0703, -75.5138),
    "Pereira": (4.8133, -75.6961)
}

grafo = {
    
    "Bogotá": {
        "Tunja": 2,
        "Villavicencio": 3,
        "Ibagué": 4,
        "Neiva": 5,
        "Manizales": 6
    },

    "Tunja": {
        "Bogotá": 2,
        "Bucaramanga": 4,
        "Yopal": 5
    },

    "Bucaramanga": {
        "Tunja": 4,
        "Cúcuta": 3,
        "Arauca": 6,
        "Medellín": 7
    },

    "Cúcuta": {
        "Bucaramanga": 3,
        "Arauca": 7
    },

    "Arauca": {
        "Cúcuta": 7,
        "Bucaramanga": 6,
        "Yopal": 5
    },

    "Yopal": {
        "Tunja": 5,
        "Arauca": 5,
        "Villavicencio": 4
    },

    "Villavicencio": {
        "Bogotá": 3,
        "Yopal": 4,
        "San José del Guaviare": 6
    },

    "San José del Guaviare": {
        "Villavicencio": 6,
        "Florencia": 5,
        "Inírida": 8,
        "Mitú": 9
    },

    "Inírida": {
        "San José del Guaviare": 8,
        "Puerto Carreño": 7,
        "Mitú": 8
    },

    "Puerto Carreño": {
        "Inírida": 7,
        "Yopal": 9
    },

    "Mitú": {
        "Inírida": 8,
        "San José del Guaviare": 9,
        "Leticia": 10
    },

    "Leticia": {
        "Mitú": 10
    },

    "Florencia": {
        "San José del Guaviare": 5,
        "Neiva": 4,
        "Mocoa": 5
    },

    "Neiva": {
        "Bogotá": 5,
        "Florencia": 4,
        "Ibagué": 3,
        "Popayán": 6
    },

    "Ibagué": {
        "Bogotá": 4,
        "Neiva": 3,
        "Armenia": 3,
        "Manizales": 4,
        "Cali": 5
    },

    "Manizales": {
        "Bogotá": 6,
        "Ibagué": 4,
        "Pereira": 2,
        "Medellín": 4
    },

    "Pereira": {
        "Manizales": 2,
        "Armenia": 2,
        "Medellín": 5
    },

    "Armenia": {
        "Pereira": 2,
        "Ibagué": 3,
        "Cali": 3
    },

    "Medellín": {
        "Manizales": 4,
        "Pereira": 5,
        "Bucaramanga": 7,
        "Montería": 5,
        "Quibdó": 6
    },

    "Quibdó": {
        "Medellín": 6,
        "Cali": 6
    },

    "Cali": {
        "Armenia": 3,
        "Ibagué": 5,
        "Popayán": 3,
        "Quibdó": 6
    },

    "Popayán": {
        "Cali": 3,
        "Pasto": 4,
        "Neiva": 6,
        "Mocoa": 5
    },

    "Pasto": {
        "Popayán": 4,
        "Mocoa": 4
    },

    "Mocoa": {
        "Pasto": 4,
        "Popayán": 5,
        "Florencia": 5
    },

    "Montería": {
        "Medellín": 5,
        "Sincelejo": 3,
        "Cartagena": 5
    },

    "Sincelejo": {
        "Montería": 3,
        "Cartagena": 3,
        "Barranquilla": 5
    },

    "Cartagena": {
        "Sincelejo": 3,
        "Barranquilla": 2,
        "Montería": 5
    },

    "Barranquilla": {
        "Cartagena": 2,
        "Santa Marta": 2,
        "Sincelejo": 5
    },

    "Santa Marta": {
        "Barranquilla": 2,
        "Riohacha": 3,
        "Valledupar": 4
    },

    "Riohacha": {
        "Santa Marta": 3,
        "Valledupar": 4
    },

    "Valledupar": {
        "Santa Marta": 4,
        "Riohacha": 4,
        "Bucaramanga": 6
    },

    "San Andrés": {
    }

}

# busqueda por profundidad
def DFS(inicio, destino, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(inicio)
    camino.append(inicio)

    if inicio == destino:
        return camino

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            resultado = DFS(vecino, destino, visitados, camino.copy())
            if resultado:
                return resultado

    return None

# busqueda costo uniforme
def UCS(inicio, destino):
    cola = [(0, inicio, [])]

    while cola:
        costo, nodo, camino = heapq.heappop(cola)
        camino = camino + [nodo]

        if nodo == destino:
            return camino, costo

        for vecino, peso in grafo[nodo].items():
            heapq.heappush(cola, (costo + peso, vecino, camino))

    return None, None


# ruta
def obtener_ruta(puntos):
    coords = [[lon, lat] for lat, lon in puntos]

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {"coordinates": coords}

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    ruta = data["routes"][0]

    geometry = ruta["geometry"]
    decoded = polyline.decode(geometry)

    distancia = ruta["summary"]["distance"] / 1000
    duracion = ruta["summary"]["duration"] / 60

    return decoded, distancia, duracion

# mapa
def dibujar_ruta(ruta):
    mapWidget.delete_all_path()
    mapWidget.delete_all_marker()

    puntos = [coordenadas[c] for c in ruta]

    ruta_real, distancia, tiempo = obtener_ruta(puntos)

    mapWidget.set_path(ruta_real)

    for i, ciudad in enumerate(ruta):
        lat, lon = coordenadas[ciudad]

        if i == 0:
            mapWidget.set_marker(lat, lon, text=f"🚀 Inicio: {ciudad}")
        elif i == len(ruta) - 1:
            mapWidget.set_marker(lat, lon, text=f"🏁 Destino: {ciudad}")
        else:
            mapWidget.set_marker(lat, lon, text=f"📍 {ciudad}")

    lats = [p[0] for p in ruta_real]
    lons = [p[1] for p in ruta_real]

    top_left = (max(lats), min(lons))
    bottom_right = (min(lats), max(lons))

    mapWidget.fit_bounding_box(top_left, bottom_right)

    ruta_texto = "\n".join([f"  • {c}" for c in ruta])

    label_resultado.configure(
        text=f"📍 Ruta:\n{ruta_texto}\n\n📏 {distancia:.2f} km\n⏱ {tiempo:.1f} min"
    )

    return ruta_real


def animar_ruta(ruta_real):
    def mover():
        marker = None
        for lat, lon in ruta_real:
            if marker:
                marker.set_position(lat, lon)
            else:
                marker = mapWidget.set_marker(lat, lon, text="🚗")
            time.sleep(0.02)

    threading.Thread(target=mover).start()


def ejecutar_dfs():
    ruta = DFS(origen.get(), destino.get())
    if origen.get() == destino.get():
        label_resultado.configure(text="📍 Ruta:\n  • " + origen.get() + "\n\n📏 0 km\n⏱ 0 min")
        return
    elif origen.get() == "San Andrés" or destino.get() == "San Andrés":
        label_resultado.configure(text="❌ No hay ruta disponible para San Andrés")
        return
    elif origen.get()=="" or destino.get()=="":
        label_resultado.configure(text="❌ Por favor, seleccione ambos campos")
        return
    elif origen.get() == "Leticia" or destino.get() == "Leticia":
        label_resultado.configure(text="❌ No hay ruta disponible para Leticia")
        return
    
    if ruta:
        r = dibujar_ruta(ruta)
        animar_ruta(r)


def ejecutar_ucs():
    ruta, _ = UCS(origen.get(), destino.get())
    if origen.get() == destino.get():
        label_resultado.configure(text="📍 Ruta:\n  • " + origen.get() + "\n\n📏 0 km\n⏱ 0 min")
        return
    elif origen.get() == "San Andrés" or destino.get() == "San Andrés":
        label_resultado.configure(text="❌ No hay ruta terrestre disponible para San Andrés")
        return
    elif origen.get()=="" or destino.get()=="":
        label_resultado.configure(text="❌ Por favor, seleccione ambos campos")
        return
    elif origen.get() == "Leticia" or destino.get() == "Leticia":
        label_resultado.configure(text="❌ No hay ruta terrestredisponible para Leticia")
        return
    
    if ruta:
        r = dibujar_ruta(ruta)
        animar_ruta(r)


ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Viaja por Colombia")
app.geometry("1000x600")


COLOR_BG = "#10002B"
COLOR_PANEL = "#240046"
COLOR_PRIMARY = "#7B2CBF"
COLOR_HOVER = "#5A189A"
COLOR_INPUT = "#3C096C"
COLOR_TEXT = "#E0AAFF"

app.configure(fg_color=COLOR_BG)


frame_left = ctk.CTkFrame(app, fg_color=COLOR_BG)
frame_left.pack(side="left", fill="both", expand=True)

frame_right = ctk.CTkFrame(app, width=250, fg_color=COLOR_PANEL)
frame_right.pack(side="right", fill="y")


mapWidget = tkintermapview.TkinterMapView(frame_left, width=700, height=600)
mapWidget.pack(fill="both", expand=True)
mapWidget.set_position(4.5, -74)
mapWidget.set_zoom(5)


origen = StringVar()
destino = StringVar()


ctk.CTkLabel(
    frame_right,
    text="Inicio",
    text_color=COLOR_TEXT
).pack(pady=5)

ctk.CTkComboBox(
    frame_right,
    values=list(coordenadas.keys()),
    variable=origen,
    fg_color=COLOR_INPUT,
    button_color=COLOR_PRIMARY,
    button_hover_color=COLOR_HOVER
).pack(pady=5)

ctk.CTkLabel(
    frame_right,
    text="Destino",
    text_color=COLOR_TEXT
).pack(pady=5)

ctk.CTkComboBox(
    frame_right,
    values=list(coordenadas.keys()),
    variable=destino,
    fg_color=COLOR_INPUT,
    button_color=COLOR_PRIMARY,
    button_hover_color=COLOR_HOVER
).pack(pady=5)


ctk.CTkButton(
    frame_right,
    text="DFS",
    command=ejecutar_dfs,
    fg_color=COLOR_PRIMARY,
    hover_color=COLOR_HOVER
).pack(pady=5)

ctk.CTkButton(
    frame_right,
    text="UCS",
    command=ejecutar_ucs,
    fg_color=COLOR_PRIMARY,
    hover_color=COLOR_HOVER
).pack(pady=5)


label_resultado = ctk.CTkLabel(
    frame_right,
    text="",
    justify="left",
    text_color=COLOR_TEXT
)
label_resultado.pack(pady=10)

app.mainloop()