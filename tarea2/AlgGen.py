#TSP with genetic algorithm
import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations

#Declaracion de las constantes a utilizar
n_ciudades = 90
rango_plano = 80000
population_size = 18

def encontrar_n_mejores(res, n):
  return res.argsort()[-n:][::-1]
  
def calc_distancia(permutation, ciudades, k):
  suma = 0
  for i in range(1, len(permutation)):
    suma += np.linalg.norm(ciudades[permutation[k][i]] - ciudades[permutation[k][i - 1]])
  suma += np.linalg.norm(ciudades[permutation[k][0]] - ciudades[permutation[k][-1]])
  return suma

def calc_dist(permutation, ciudades):
  suma = 0
  for i in range(1, len(permutation)):
    suma += np.linalg.norm(ciudades[permutation[i]] - ciudades[permutation[i - 1]])
  suma += np.linalg.norm(ciudades[permutation[0]] - ciudades[permutation[-1]])
  return suma

#Funcion que nos permite hacer un swap de manera random de 2 ciudades en un camino hamiltoneano
def swap_2values(permutation):
  largo = len(permutation)
  copia = np.zeros(largo)
  for i in range(len(permutation)):
    copia[i] = permutation[i]
  a = np.random.randint(largo)
  b = np.random.randint(largo)
  aux = copia[a]
  copia[a] = copia[b]
  copia[b] = aux
  return copia

def cross_over(padre1, padre2):
  largo = len(padre1)
  usados = np.zeros(largo)
  hijo = np.zeros(largo)
  for i in range(len(padre1)):
    #Decidimos si el iesimo gen hereda del padre1 o 2, cuidado que debemos mantener el camino hamiltoniano
    #en caso de que ninguno de los padres pueda otorgar un gen que no rompa la condicion de camino
    #haremos una mutacion poniendo un elemento al azar entre los que faltan por designar para seguir manteniendo un camino
    coin = np.random.randint(2)
    if coin == 0:
      if not usados[padre1[i]]:
        usados[padre1[i]] = 1
        hijo[i] = padre1[i]
      elif not usados[padre2[i]]:
        usados[padre2[i]] = 1
        hijo[i] = padre2[i]
      else:
        #seleccionamos uno al azar entre las ciudades que no se han visitado
        indice = np.random.randint(largo)
        while usados[indice] == 0:
          indice = np.random.randint(largo)
        hijo[i] = indice
        usados[indice] = 1
    elif coin == 1:
      if not usados[padre2[i]]:
        usados[padre2[i]] = 1
        hijo[i] = padre2[i]
      elif not usados[padre1[i]]:
        usados[padre1[i]] = 1
        hijo[i] = padre1[i]
      else:
        #seleccionamos uno al azar entre las ciudades que no se han visitado
        indice = np.random.randint(largo)
        while usados[indice] == 0:
          indice = np.random.randint(largo)
        hijo[i] = indice
        usados[indice] = 1
  return hijo

def resp_exacta(n_ciudades = n_ciudades):
#No dejaremos que esto se calcule si hay más de 9 ciudades, ya que se demorará mucho
  if n_ciudades > 9:
      return
  perms = permutations(np.random.permutation(n_ciudades), n_ciudades)
  menor = 1e9
  for p in perms:
    p = np.array(p)
    distancia = calc_dist(p, ciudades)
    if distancia < menor:
      menor = distancia
  return menor


def dist_AlgGen(n_ciudades=n_ciudades, population_size = population_size, rango_plano = rango_plano, it = 800, freq = 20):
    permutation = [0]*population_size
#se definen las posiciones de las ciudades de antemano
    ciudades = np.random.randint(rango_plano, size=(n_ciudades,2)) - (rango_plano/2, rango_plano/2)
    for i in range(population_size):
        permutation[i] = np.random.permutation(n_ciudades)

#Ahora calcularemos el valor utilizando algoritmos genéticos
    permutation = np.array(permutation)
    ciudades.astype(int)
    res = []
    while it > 0:
        candidatos = [0]*population_size
        distancias = np.zeros(population_size)
        for i in range(len(permutation)):
            distancias[i] = calc_distancia(permutation, ciudades, i)
            distancias[i].astype(int)
        indices = encontrar_n_mejores(-distancias, 3)
#Elegimos los 3 mejores elementos para que sigan con vida
        indices.astype(int)
        for i in range(len(indices)):
            candidatos[i] = permutation[indices[i]]
            candidatos[i].astype(int)
#Los siguientes 3 elementos son creados haciendo cross over entre los 3 primeros
        for i in range(3):
            candidatos[len(indices) + i] = cross_over(candidatos[i%3], candidatos[(i+1)%3])
            candidatos[len(indices) + i].astype(int)
#Todos los demás son creados mutando los 6 elementos ya existentes
        for i in range(population_size - 2*len(indices)):
            candidatos[2*len(indices) + i] = swap_2values(candidatos[i%(2*len(indices))])
            candidatos[2*len(indices) + i].astype(int)
        for i in range(len(candidatos)):
            permutation[i] = candidatos[i]
            permutation[i].astype(int)
            permutation.astype(int)
        if it % freq == 0:
            res.append(calc_distancia(candidatos, ciudades, 0))
        it -=1
    return res

def plot_res(res, n_c = n_ciudades, p_s = population_size):
  plt.plot(res, label='Algoritmo genético')
  if(n_c <= 9):
    exact = np.zeros(len(res))
    exact[0:len(res)] = resp_exacta()
    plt.plot(exact, label='Solución exacta')

  plt.title("Sol exacta vs Algoritmo genético para 90 ciudades y 18 candidatos")
  plt.ylabel("Distancia total recorrida")
  plt.xlabel("Generaciones, 5 unidades de medida equivalen a 100 generaciones")

  # Add a legend
  plt.legend()

  # Show the plot
  plt.show()

def main():
    res = dist_AlgGen()
    plot_res(res)
    
main()
