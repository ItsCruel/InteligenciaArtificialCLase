import heapq

class NodoArriero:
    def __init__(self, izquierda, derecha, bote, padre=None, accion="", g=0):
        self.izquierda = frozenset(izquierda)
        self.derecha = frozenset(derecha)
        self.bote = bote  # 'I' para izquierda, 'D' para derecha
        self.padre = padre
        self.accion = accion
        self.g = g  # Costo real (numero de cruces)
        
        # Heuristica (h): elementos que faltan por llegar a la derecha
        elementos_totales = {'A', 'L', 'C', 'M'}
        self.h = len(elementos_totales - self.derecha)
        
        self.f = self.g + self.h

    def __lt__(self, otro):
        return self.f < otro.f

def es_orilla_valida(orilla):
    # Si el arriero (A) esta presente, la orilla es segura
    if 'A' in orilla:
        return True
    
    # Si el arriero no esta, revisar combinaciones prohibidas
    if 'L' in orilla and 'C' in orilla: # Coyote y Cabra solos
        return False
    if 'C' in orilla and 'M' in orilla: # Cabra y Maiz solos
        return False
        
    return True

def expandir_nodos(nodo):
    sucesores = []
    
    # Verificamos de que lado esta el bote para saber el origen y destino
    if nodo.bote == 'I':
        origen = set(nodo.izquierda)
        destino = set(nodo.derecha)
        nuevo_bote = 'D'
    else:
        origen = set(nodo.derecha)
        destino = set(nodo.izquierda)
        nuevo_bote = 'I'

    # El arriero siempre debe estar en la orilla donde cruza
    if 'A' not in origen:
        return sucesores

    # El arriero puede viajar solo o con un solo objeto/animal
    compañeros = [None] + [elem for elem in origen if elem != 'A']

    for comp in compañeros:
        nueva_origen = set(origen)
        nuevo_destino = set(destino)

        # Movemos al arriero
        nueva_origen.remove('A')
        nuevo_destino.add('A')

        # Si lleva un compañero, tambien lo movemos
        accion = "El arriero cruza solo"
        if comp is not None:
            nueva_origen.remove(comp)
            nuevo_destino.add(comp)
            accion = f"El arriero cruza con {comp}"

        # Reconstruimos como quedan las orillas despues del movimiento
        if nodo.bote == 'I':
            izq_resultante = nueva_origen
            der_resultante = nuevo_destino
        else:
            izq_resultante = nuevo_destino
            der_resultante = nueva_origen

        # Validamos que ninguna orilla quede en un estado prohibido
        if es_orilla_valida(izq_resultante) and es_orilla_valida(der_resultante):
            hijo = NodoArriero(
                izquierda=izq_resultante,
                derecha=der_resultante,
                bote=nuevo_bote,
                padre=nodo,
                accion=accion,
                g=nodo.g + 1
            )
            sucesores.append(hijo)

    return sucesores

def a_estrella_arriero():
    # Estado inicial: todos en la izquierda y el bote en la izquierda
    inicio = NodoArriero(izquierda={'A', 'L', 'C', 'M'}, derecha=set(), bote='I', g=0)
    
    frontera = []
    heapq.heappush(frontera, (inicio.f, inicio))
    explorados = set()

    while frontera:
        _, actual = heapq.heappop(frontera)

        # Si todos estan en la derecha, terminamos
        if len(actual.derecha) == 4:
            return reconstruir_camino(actual)

        estado_tupla = (frozenset(actual.izquierda), frozenset(actual.derecha), actual.bote)
        if estado_tupla in explorados:
            continue
        explorados.add(estado_tupla)

        for hijo in expandir_nodos(actual):
            h_tupla = (frozenset(hijo.izquierda), frozenset(hijo.derecha), hijo.bote)
            if h_tupla not in explorados:
                heapq.heappush(frontera, (hijo.f, hijo))

    return None

def reconstruir_camino(nodo):
    camino = []
    actual = nodo
    while actual.padre is not None:
        camino.append((actual.accion, f"Izquierda: {set(actual.izquierda)} | Derecha: {set(actual.derecha)} (Bote: {actual.bote})", actual.g, actual.h, actual.f))
        actual = actual.padre
    camino.reverse()
    return camino

if __name__ == "__main__":
    print("Resolviendo el problema del arriero con A*...\n")
    solucion = a_estrella_arriero()
    
    if solucion:
        print(f"¡Exito! Solucion encontrada en {len(solucion)} pasos:\n")
        for i, (accion, estado_desc, g, h, f) in enumerate(solucion, 1):
            print(f"Paso {i}: {accion}")
            print(f"   Estado -> {estado_desc}")
            print(f"   Costos -> g={g}, h={h}, f={f}\n")
    else:
        print("No se encontro ninguna solucion.")