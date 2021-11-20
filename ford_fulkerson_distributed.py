import mpi4py

#Ova klasa Graph predstavlja usmjereni graf na temelju matrice susjedstva.
class Graph:

    def __init__(self, graph):
        self.graph = graph  #residual graph
        self.ROW = len(graph)



#Ova metoda nam vraća true ako postoji put od source do sink (t) u grafu. source i sink predstavljaju
#Čvorove između kojih tražimo max flow.

    def BFS(self, s, t, parent):

       #Za početak se svi vrhovi označe kao ne posjećeni
        visited = [False] * (self.ROW)

        #Kreira se que (red čekanja) u koji dolaze čvorovi
        queue = []

        #U red čekanja se doda čvor i označi se kao posjećen
        queue.append(s)
        visited[s] = True

        #BFS je breadth first search, to je neki standardni algoritam
        while queue:

            #Iz reda čekanja se izbaci čvor s kojim ćemo sad radit
            u = queue.pop(0)

            # Dohvatimo sve susjedne vrhove trenutnog čvora
            # Ako susjedni čvor nije postavljen kao "visited" (posjećen)
            # Onda ga mi postavimo na posjećen i stavimo ga u red čekanja
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    # U trenutku kada pronađemo vezu sa sinkom (krajnjom točkom)
                    # nema potrebe da više tražimo i možemo vratit istinu
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True

            #Ako ne pronađemo vezu od poslanog puta, onda zaključimo da ne postoji i vratimo false
        return False

    #Ova metoda će vratiti max flow između 2 točke (source i sink)
    def FordFulkerson(self, source, sink):

        #Ova lista će biti popunjena s rezultatima BFS -a i pohranjuje putanju
        parent = [-1] * (self.ROW)

        max_flow = 0  #Na početku nema protoka

        # Dok god postoji put od izvora do ishodišta, obavlja se postupak (while)
        while self.BFS(source, sink, parent):

        #Tražimo maksimalni protok u grafu preko puteva koji su povezani
            #Inicijalno postavimo flow na "Inf", odnosno beskonačno, razlog tomu je što tražimo najmanji broj od svih,
            #a što god nađemo biti će manje od beskonačnosti
            path_flow = float("Inf")
            s = sink
            while (s != source):
                #Dok god ne dođemo do kraja, prolazeći kroz čvorove tražimo minimalnu vrijednost između dvije točke
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Tu vrijednost dodamo na globalni protok
            max_flow += path_flow

            #Uredimo vrijednosti u grafu, odnosno maknemo već izračunati kapacitet iz grafa,
            #i postavimo se na sljedeći čvor
            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        #Vratimo maksimalni protok ko rezultat
        return max_flow


from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

root = 0

max_processors = comm.size

graph = [[0, 16, 13, 0, 0, 0],
         [0, 0, 10, 12, 0, 0],
         [0, 4, 0, 0, 14, 0],
         [0, 0, 9, 0, 0, 20],
         [0, 0, 0, 7, 0, 4],
         [0, 0, 0, 0, 0, 0]]

bin_size = len(graph)/max_processors
g = Graph(graph)
g.FordFulkerson(0, 5)