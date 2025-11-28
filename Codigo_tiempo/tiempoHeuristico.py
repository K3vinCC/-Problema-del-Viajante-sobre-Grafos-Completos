#==================================================================================================
#                               Metodo heuristica: Nearest Neighbor (NN)
#==================================================================================================
import math
import time

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
inicio_tiempo = time.time()
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

# Calcular longitud total
dist_total = 0
for i in range(len(tour) - 1):
    dist_total += D[tour[i]][tour[i + 1]]

tiempo_total = time.time() - inicio_tiempo

# ================================================================================================
#                             GUARDAR RESULTADOS EN ARCHIVO
# ================================================================================================
import os   # <-- necesario para crear carpetas

# Crear carpeta si no existe
carpeta = "resultados"
os.makedirs(carpeta, exist_ok=True)

salida = ""
salida += f"Prueba realizada con {N} ciudades\n\n"
salida += "============= Viaje NN =============\n\n"

for i in range(len(tour) - 1):
    c1 = tour[i]
    c2 = tour[i + 1]
    salida += f"{nombres[c1]} -> {nombres[c2]} : {D[c1][c2]:.4f} unidades\n"

salida += f"\nLongitud total del tour (NN): {dist_total:.4f} unidades\n\n"
salida += "Ruta completa: " + " -> ".join(nombres[i] for i in tour) + "\n"
salida += f"\nTiempo total de ejecución: {tiempo_total:.6f} segundos\n"

# Nombre dinámico del archivo
nombre_archivo = f"resultado_heuristica_NN_{N}ciudades.txt"

# Ruta completa
ruta_archivo = os.path.join(carpeta, nombre_archivo)

# Guardar
with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(salida)

print(f"Archivo '{ruta_archivo}' creado con éxito.")

