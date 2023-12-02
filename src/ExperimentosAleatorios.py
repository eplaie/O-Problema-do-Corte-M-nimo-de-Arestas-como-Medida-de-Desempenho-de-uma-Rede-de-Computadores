import networkx as nx
import time
import numpy as np
from collections import defaultdict 
import random

class Graph: 
    def __init__(self, graph): 
        self.graph = graph
        self.org_graph = [i[:] for i in graph]
        self.ROW = len(graph) 
        self.COL = len(graph[0]) 

    def BFS(self, s, t, parent): 
        visited = [False] * (self.ROW)
        queue = []
        queue.append(s)
        visited[s] = True

        while queue: 
            u = queue.pop(0) 

            for ind, val in enumerate(self.graph[u]): 
                if visited[ind] == False and val > 0: 
                    queue.append(ind) 
                    visited[ind] = True
                    parent[ind] = u 

        return True if visited[t] else False

    def minCut(self, s, t): 
        parent = [-1] * (self.ROW) 
        max_flow = 0 
        while self.BFS(s, t, parent): 
            path_flow = float("Inf") 
            v = t 

            while v != s: 
                path_flow = min(path_flow, self.graph[parent[v]][v]) 
                v = parent[v] 

            max_flow += path_flow 

            v = t 
            while v != s: 
                u = parent[v] 
                self.graph[u][v] -= path_flow 
                self.graph[v][u] += path_flow 
                v = parent[v] 


        return max_flow

# Usa os vertices de maior grau para calcular o s,t-corte
def cutHighestDegree(graph):
    start_time = time.time()

    distances = np.full((len(graph), len(graph)), fill_value=0)
    
    for edge in graph.edges(data=True):
        source, target, weight = edge
        distances[source][target] = 1
        distances[target][source] = 1


    s = 0
    for i in range(len(graph)):
        if(sum(distances[i]) > sum(distances[s])):
            s = i

    t = 1 if s == 0 else 0
    for i in range(len(graph)):
        if(i != s and sum(distances[i]) > sum(distances[t])):
            t = i

    g = []

    for i in range(len(graph)):
        aux = []
        for j in range(len(graph)):
            aux.append(0)
        g.append(aux)
            
    
    for edge in graph.edges(data=True):
        source, target, weight = edge
        g[source][target] = 1
        g[target][source] = 1


    g_ = Graph(g)
    cut_value = g_.minCut(s, t)

    time_cut = time.time() - start_time

    return cut_value, time_cut

# Usa os vertices de menor grau para calcular o s,t-corte
def cutLowestDegree(graph):
    start_time = time.time()

    distances = np.full((len(graph), len(graph)), fill_value=0)
    
    for edge in graph.edges(data=True):
        source, target, weight = edge
        distances[source][target] = 1
        distances[target][source] = 1


    s = 0
    for i in range(len(graph)):
        if(sum(distances[i]) < sum(distances[s])):
            s = i

    t = 1 if s == 0 else 0
    for i in range(len(graph)):
        if(i != s and sum(distances[i]) < sum(distances[t])):
            t = i

    g = []

    for i in range(len(graph)):
        aux = []
        for j in range(len(graph)):
            aux.append(0)
        g.append(aux)
            
    
    for edge in graph.edges(data=True):
        source, target, weight = edge
        g[source][target] = 1
        g[target][source] = 1


    g_ = Graph(g)
    cut_value = g_.minCut(s, t)

    time_cut = time.time() - start_time

    return cut_value, time_cut

def exact_cut(graph):
    # Calculando o corte mínimo usando networkx
    start_time = time.time()
    cut_value, partition = nx.stoer_wagner(graph)
    elapsed_time = time.time() - start_time

    return cut_value, partition, elapsed_time

numero_vertices = [10, 20, 50, 100, 200, 500, 1000]
densidade = [0.3, 0.5, 0.7, 0.9]

for n in numero_vertices:
    for d in densidade:
        print("#################################################################")
        print("Numero de vertices: {}, Densidade: {}".format(n, d))

        G = nx.connected_watts_strogatz_graph(n, int(0.4 * n), d)

        # Algoritmos heurísticos
        heuristic_cut_value, heuristic_cut_time = cutHighestDegree(G)
        print("Vertices maior grau")
        print(f"Tamanho do Corte Mínimo: {heuristic_cut_value}")
        print(f"Tempo de execução do corte mínimo: {heuristic_cut_time:.6f} segundos")
        print("-------------------------------------------------------------------")
        heuristic_cut_value, heuristic_cut_time = cutLowestDegree(G)
        print("Vertices menor grau")
        print(f"Tamanho do Corte Mínimo: {heuristic_cut_value}")
        print(f"Tempo de execução do corte mínimo: {heuristic_cut_time:.6f} segundos")
        print("-------------------------------------------------------------------")

        # Algoritmo exato

        exact_cut_value, _, exact_cut_time = exact_cut(G)
        print("Algoritmo Exato - Stoer Wagner")
        print(f"Tamanho do Corte Mínimo: {exact_cut_value}")
        print(f"Tempo de execução do corte mínimo: {exact_cut_time:.6f} segundos")
        print("-------------------------------------------------------------------")