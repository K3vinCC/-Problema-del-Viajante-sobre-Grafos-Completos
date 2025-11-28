#==================================================================================================
#                               Metodo heuristica: Nearest Neighbor (NN)
#==================================================================================================
import math
import matplotlib.pyplot as plt

# Calcular Distancias Euclidianas
def distancia_euclidiana(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# Ciudades y sus coordenadas
ciudades = {
    "Moscú": (55.751244, 37.618423),                 #1
    "Tver": (56.8584, 35.9006),                      #2
    "Vladimir": (56.143063, 40.410934),              #3 
    "San Petersburgo": (59.93750, 30.30861),         #4 
    "Pskov": (57.8170, 28.3330),                     #5 
    "Veliky Novgorod": (58.5213, 31.2710),           #6 
    "Nizhni Nóvgorod": (56.296505, 43.936058),       #7 
    "Kazan": (55.79639, 49.10889),                   #8 
    "Samara": (53.20278, 50.14083),                  #9 
    "Saratov": (51.592365, 45.960804),               #10 
}

# Listas auxiliares
nombres = list(ciudades.keys())
coordenadas = list(ciudades.values())
N = len(nombres)
# Crear matriz vacia para almacenar la matris Dij
D = []
for i in range(N): #toma en cuenta la cantidad de ciudades y crea una matriz de NxN
    fila = []
    for j in range(N):
        fila.append(0)
    D.append(fila) #a la matriz cada nij se le asigna valor 0


for i in range(N):
    for j in range(N):
        if i != j:
            lat1, lon1 = coordenadas[i]
            lat2, lon2 = coordenadas[j]
            D[i][j] = distancia_euclidiana(lat1, lon1, lat2, lon2)

#=======================================================
#    Implementación NN
#======================================================
origen = 0  # Ciudad inicial: Santiago
ciudad_actual = origen
ciudades_visitadas = set([origen])
tour = [origen]

for _ in range(N - 1):
    primera = True
    dist_min = None
    ciudad_cercana = None

    for j in range(N):
        if j not in ciudades_visitadas:
            d = D[ciudad_actual][j]

            if primera:
                dist_min = d
                ciudad_cercana = j
                primera = False

            elif d < dist_min:
                dist_min = d
                ciudad_cercana = j

    tour.append(ciudad_cercana)
    ciudades_visitadas.add(ciudad_cercana)
    ciudad_actual = ciudad_cercana

# Cerrar ciclo regresando al origen
tour.append(origen)

# ================================
# Dibujar la ruta
# ================================
fig, ax = plt.subplots(figsize=(12,8))

# Dibujar ciudades
for i, (lat, lon) in enumerate(coordenadas):
    ax.scatter(lon, lat, color='red', s=50)
    ax.text(lon, lat, nombres[i], fontsize=10,
            ha='right', va='bottom')

# Dibujar ruta en azul con flechas
for i in range(len(tour)-1):
    x_start, y_start = coordenadas[tour[i]][1], coordenadas[tour[i]][0]
    x_end, y_end = coordenadas[tour[i+1]][1], coordenadas[tour[i+1]][0]
    ax.plot([x_start, x_end], [y_start, y_end], color='blue', linewidth=2)
    ax.annotate("",
                xy=(x_end, y_end),
                xytext=(x_start, y_start),
                arrowprops=dict(arrowstyle="->", color='blue', lw=1.5))

ax.set_title("Ruta Nearest Neighbor (Método Heurístico)")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.grid(True)
plt.show()
