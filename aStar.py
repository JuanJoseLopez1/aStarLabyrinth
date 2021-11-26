from pyamaze import maze, agent, textLabel
from queue import PriorityQueue


def distanciaManhattan(parCoordinate1, parCoordinate2):
    varX1, varY1 = parCoordinate1
    varX2, varY2 = parCoordinate2
    return abs(varX1-varX2) + abs(varY1-varY2)


def aStar(objMaze):

    # Coordenada de inicio, ultima fila y columna del laberinto
    varStartCoordinate = (objMaze.rows, objMaze.cols)

    """
    f(n) = g(n) + h(n)
    f(n) es el costo de un nodo a otro, es este caso de una coordenada a otra (objetivo).
    g(n) es el costo para alcanzar un nodo de inicio hasta un nodo N.
    h(n) es la funcion heuristica (distancia de manhattan), es el costo estimado para alcanzar el objetivo.
    """

    # Diccionarios
    # varDictionaryCoordinate es la llave, float('inf') es el valor
    # float('inf') es un numero infinito
    # objMaze.grid trae las posiciones (1,1),(2,2)...(n,n)

    # Funcion g(n)
    gFunctionDictionary = {varDictionaryCoordinate: float(
        'inf') for varDictionaryCoordinate in objMaze.grid}

    # gFunctionDictionary = 0 en la posicion maxima del laberinto, ej: (10,10) para un laberinto 10x10
    gFunctionDictionary[varStartCoordinate] = 0

    # Funcion f(n)
    fFunctionDictionary = {varDictionaryCoordinate: float(
        'inf') for varDictionaryCoordinate in objMaze.grid}

    """
    Segun la funcion f(n), tenemos que:
    g(n) = 0
    h(n) = Distancia manhattan entre el inicio (10,10) en un laberinto 10x10 y el objetivo ubicado en (1,1).
    Por lo tanto tenemos que f(n) = 0 + h((10,10)(1,1))       
    """
    fFunctionDictionary[varStartCoordinate] = distanciaManhattan(
        varStartCoordinate, (1, 1))

    # Cola de prioridad, el menor elemento esta de primero en la lista.
    objPriorityQueue = PriorityQueue()

    # Se crea una tupla
    objPriorityQueue.put((fFunctionDictionary[varStartCoordinate], distanciaManhattan(
        varStartCoordinate, (1, 1)), varStartCoordinate))

    varPathGoaltoStart = {}

    # Recorrer la cola de prioridad
    while not objPriorityQueue.empty():

        # obtiene la coordenada de inicio
        varCurrentCoordenate = objPriorityQueue.get()[2]
        if varCurrentCoordenate == (1, 1):
            break
        # bucle que recorre una cadena de caracteres
        for d in 'ESNW':
            # Verifica que el camino este disponible, varCurrentCoordenate es la llave y d el valor, .maze_map es un directorio y solo sera igual a True cuando el valor sea 1.
            if objMaze.maze_map[varCurrentCoordenate][d] == True:
                # Direcciones posibles de movimiento en el laberinto, E(East), W(West),N(North), S(South).
                # varCurrentCoordenate[0] = X del tamanio del laberinto
                # varCurrentCoordenate[1] = Y del tamanio del laberinto
                if d == 'E':
                    varChildCoordenate = (
                        varCurrentCoordenate[0], varCurrentCoordenate[1]+1)
                if d == 'W':
                    varChildCoordenate = (
                        varCurrentCoordenate[0], varCurrentCoordenate[1]-1)
                if d == 'N':
                    varChildCoordenate = (
                        varCurrentCoordenate[0]-1, varCurrentCoordenate[1])
                if d == 'S':
                    varChildCoordenate = (
                        varCurrentCoordenate[0]+1, varCurrentCoordenate[1])

                varGFunctionValue = gFunctionDictionary[varCurrentCoordenate]+1
                #funcion f(n) = g(n) + h(n)
                varFFunctionValue = varGFunctionValue + \
                    distanciaManhattan(varChildCoordenate, (1, 1))

                #Funcionamiento del algoritmo dependiendo de la f(n).
                if varFFunctionValue < fFunctionDictionary[varChildCoordenate]:
                    gFunctionDictionary[varChildCoordenate] = varGFunctionValue
                    fFunctionDictionary[varChildCoordenate] = varFFunctionValue
                    objPriorityQueue.put((varFFunctionValue, distanciaManhattan(
                        varChildCoordenate, (1, 1)), varChildCoordenate))
                    varPathGoaltoStart[varChildCoordenate] = varCurrentCoordenate
    #Direcciones de la trayectoria desde el inicio hasta el objetivo.   
    varPathStartToGoal = {}
    varCoordenate = (1, 1)
    while varCoordenate != varStartCoordinate:
        varPathStartToGoal[varPathGoaltoStart[varCoordenate]] = varCoordenate
        varCoordenate = varPathGoaltoStart[varCoordenate]
    #Trayectoria que se enviara al graficador del laberinto
    return varPathStartToGoal


if __name__ == '__main__':
    m = maze(5, 5)
    m.CreateMaze()

    print(m.maze_map)
    print(m.grid)
    path = aStar(m)

    a = agent(m, footprints=True)
    b = agent(m, footprints=True)
    m.tracePath({a: path})
    m.tracePath({b: m.path})
    l = textLabel(m, 'A Star Path Length', len(path)+1)

    m.run()
