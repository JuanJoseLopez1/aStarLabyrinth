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
    open = PriorityQueue()

    # Se crea una tupla
    open.put((fFunctionDictionary[varStartCoordinate], distanciaManhattan(
        varStartCoordinate, (1, 1)), varStartCoordinate))
    aPath = {}
    while not open.empty():
        currCell = open.get()[2]
        if currCell == (1, 1):
            break
        for d in 'ESNW':
            if objMaze.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                if d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                if d == 'N':
                    childCell = (currCell[0]-1, currCell[1])
                if d == 'S':
                    childCell = (currCell[0]+1, currCell[1])

                temp_g_score = gFunctionDictionary[currCell]+1
                temp_f_score = temp_g_score + \
                    distanciaManhattan(childCell, (1, 1))

                if temp_f_score < fFunctionDictionary[childCell]:
                    gFunctionDictionary[childCell] = temp_g_score
                    fFunctionDictionary[childCell] = temp_f_score
                    open.put((temp_f_score, distanciaManhattan(
                        childCell, (1, 1)), childCell))
                    aPath[childCell] = currCell
    fwdPath = {}
    cell = (1, 1)
    while cell != varStartCoordinate:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return fwdPath


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
