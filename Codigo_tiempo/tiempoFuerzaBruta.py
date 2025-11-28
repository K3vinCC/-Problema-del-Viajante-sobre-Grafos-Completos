#==================================================================================================
#                             Metodo (fuerza bruta)
#==================================================================================================
import math
import time   # medir el tiempo
import os  # para guardar archivo con los datos

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

nombres = list(ciudades.keys()) #listar nombre de las ciudades 
coordenadas = list(ciudades.values()) #enlistar las cordenadas de las ciudades 
#Ver cantidad de ciudades
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
inicio_tiempo = time.time()   # <-- iniciar cronómetro
origen = 0  # ciudad de inicio
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

salida = ""
# ================================
# Resultado final
# ================================
salida += "\n====================================\n"
salida += "=========== MEJOR RUTA =============\n"
salida += "====================================\n\n"

for i in range(len(mejorRuta) - 1):
    c1 = mejorRuta[i]
    c2 = mejorRuta[i + 1]
    nombre1 = nombres[c1]
    nombre2 = nombres[c2]
    dist = D[c1][c2]
    salida += f"{nombre1} -> {nombre2} : {dist:.4f} unidades\n"

salida += f"\nDistancia total óptima: {mejorDistancia:.4f} unidades\n"

ruta_nombres = " -> ".join(nombres[i] for i in mejorRuta)
salida += "\nRuta completa: " + ruta_nombres + "\n"

# ================================
# Tiempo total
# ================================
tiempo_total = time.time() - inicio_tiempo
salida += f"\nTiempo total de ejecución: {tiempo_total:.4f} segundos\n"

# ================================
# Guardar en archivo (con carpeta)
# ================================

# Crear la carpeta si no existe
carpeta = "resultados"
os.makedirs(carpeta, exist_ok=True)

# Nombre dinámico del archivo
nombre_archivo = f"resultado_fuerza_bruta_{N}ciudades.txt"

# Ruta completa final
ruta_archivo = os.path.join(carpeta, nombre_archivo)

# Guardar los resultados
with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(salida)

print(f"Archivo '{ruta_archivo}' creado con éxito.")
