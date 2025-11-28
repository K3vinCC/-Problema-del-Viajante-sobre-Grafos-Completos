#==================================================================================================
#                             Metodo (fuerza bruta)
#==================================================================================================
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#Calcular Distancias Euclidianas
def distancia_euclidiana(lat1,lon1,lat2,lon2):
    distancia = math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2) #raiz((lat1-lat2)**2 + (lon1-lon2)**2)
    return distancia

#cidudades y sus coordenadas
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

nombres = list(ciudades.keys()) #listar nombre de las ciudades (bajo el valor de keys en el diccionario)
coordenadas = list(ciudades.values()) #enlistar las cordenadas de las ciudades (bajo el valor de values en el diccionario)
#Ver cantidad de ciudades
N = len(nombres)
# Crear matriz NxN
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

#==================================================================================================
# Calcular permultaciones
#==================================================================================================
def permutar(lista):\
    #manejo de errores en caso de que la lista este vacia o solo tenga un valor
    if len(lista) == 0: 
        return []
    if len(lista) == 1:
        return [lista]
    
    resultado = []
    for i in range(len(lista)):
        elem = lista[i]
        resto = lista[:i] + lista[i+1:]
        for p in permutar(resto):
            resultado.append([elem] + p)
    return resultado

#====================================
# Calcular distancia total
#====================================
def calcular_distancia_total (ruta , D):
    total = 0
    for i in range(len(ruta)-1):
        total += D[ruta[i]][ruta[i+1]]
    return total    

#===========================================
# inicio de codigo
#===========================================
origen = 0  # ciudad de inicio (en este caso santiago)
otras = [i for i in range(N) if i != origen]

permutaciones = permutar(otras)

mejorRuta = None
mejorDistancia = 0
primera_distancia = True

print(f"=== rutas ===\n")

contador = 1

for p in permutaciones:
    ruta = [origen] + p + [origen]
    distancia = calcular_distancia_total(ruta, D)

    # Mostrar cada ruta con índices y distancia
    print(f"Ruta {contador}: {ruta}  ->  Distancia: {distancia:.4f}")
    contador += 1

    # Actualizar mejor ruta
    if primera_distancia:
        mejorRuta = ruta
        mejorDistancia = distancia
        primera_distancia = False
    elif distancia < mejorDistancia:
        mejorRuta = ruta
        mejorDistancia = distancia

# ===========================================
# Mostrar resultado final
# ===========================================

print("\n====================================")
print("             MEJOR RUTA  ")
print("====================================\n")

# Mostrar la ruta con nombres y distancias entre tramos
for i in range(len(mejorRuta) - 1):
    c1 = mejorRuta[i]
    c2 = mejorRuta[i + 1]
    nombre1 = nombres[c1]
    nombre2 = nombres[c2]
    dist = D[c1][c2]
    print(f"{nombre1} -> {nombre2} : {dist:.4f} unidades")

print(f"\nDistancia total óptima: {mejorDistancia:.4f} unidades\n")

# Ruta con nombres en formato fácil de leer
ruta_nombres = " -> ".join(nombres[i] for i in mejorRuta)
print("Ruta completa:", ruta_nombres)



# ================================
# Configurar figura
# ================================
fig, ax = plt.subplots(figsize=(12,8))
plt.subplots_adjust(bottom=0.2)

# Dibujar ciudades
# Dibujar ciudades
for i, (lat, lon) in enumerate(coordenadas):
    ax.scatter(lon, lat, color='red', s=50)
    ax.text(lon, lat, nombres[i], fontsize=10,
            ha='right', va='bottom')  # ajusta la posición relativa al punto


# ================================
# Dibujar todas las rutas en gris plomo
# ================================
for p in permutaciones:
    ruta = [origen] + p + [origen]
    xs = [coordenadas[i][1] for i in ruta]
    ys = [coordenadas[i][0] for i in ruta]
    ax.plot(xs, ys, color='lightgray', linewidth=0.5)

# Variables para interactuar
ruta_idx = [0]
linea_actual = None
flechas = []

# ================================
# Función para dibujar ruta seleccionada
# ================================
def dibujar_ruta(ruta, color='red'):
    global linea_actual, flechas
    # Borrar línea y flechas anteriores
    if linea_actual:
        linea_actual.remove()
    for f in flechas:
        f.remove()
    flechas = []
    
    xs = [coordenadas[i][1] for i in ruta]
    ys = [coordenadas[i][0] for i in ruta]
    linea_actual, = ax.plot(xs, ys, color=color, linewidth=2, marker='o')
    
    # Flechas
    for i in range(len(ruta)-1):
        f = ax.annotate("",
                    xy=(coordenadas[ruta[i+1]][1], coordenadas[ruta[i+1]][0]),
                    xytext=(coordenadas[ruta[i]][1], coordenadas[ruta[i]][0]),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
        flechas.append(f)
    plt.draw()

# ================================
# Botones
# ================================
def mostrar_siguiente(event):
    ruta_idx[0] = (ruta_idx[0]+1) % len(permutaciones)
    ruta = [origen] + permutaciones[ruta_idx[0]] + [origen]
    dibujar_ruta(ruta, color='red')

def mostrar_optima(event):
    dibujar_ruta(mejorRuta, color='blue')

ax_next = plt.axes([0.7, 0.05, 0.1, 0.075])
ax_best = plt.axes([0.81, 0.05, 0.1, 0.075])
btn_next = Button(ax_next, 'Siguiente')
btn_next.on_clicked(mostrar_siguiente)
btn_best = Button(ax_best, 'Óptima')
btn_best.on_clicked(mostrar_optima)

# ================================
# Mostrar primera ruta
# ================================
dibujar_ruta([origen]+permutaciones[0]+[origen], color='red')
ax.set_title("Ruta optima por busqueda exhaustiva")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.grid(True)
plt.show()
