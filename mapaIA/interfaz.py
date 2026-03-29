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
    "Bogotá": (4.7110, -74.0721),
    "Tunja": (5.5353, -73.3678),
    "Bucaramanga": (7.1193, -73.1227),
    "Medellín": (6.2442, -75.5812),
    "Manizales": (5.0703, -75.5138),
    "Pereira": (4.8133, -75.6961)
}

grafo = {
    "Bogotá": {"Tunja": 2, "Manizales": 5},
    "Tunja": {"Bogotá": 2, "Bucaramanga": 3},
    "Bucaramanga": {"Tunja": 3},
    "Manizales": {"Bogotá": 5, "Pereira": 1},
    "Pereira": {"Manizales": 1, "Medellín": 4},
    "Medellín": {"Pereira": 4}
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
    if ruta:
        r = dibujar_ruta(ruta)
        animar_ruta(r)


def ejecutar_ucs():
    ruta, _ = UCS(origen.get(), destino.get())
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