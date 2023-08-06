import numpy as np
from queue import PriorityQueue
from haversine import haversine

class LocationNode:
    def __init__(self,name,lat,lng):
        self.name = name
        self.lat = lat
        self.lng = lng

class Graph:
    def __init__(self,names):
        self.names = names
        self.adj_list = {}
        self.visited = {}
        self.parent = {}
        self.g_dist = {}
        self.path = []
        
        for name in self.names:
            self.adj_list[name] = []
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0
            
    def reset(self):
        for name in self.names:
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0
        
        self.path = []
        
    @staticmethod
    def find_distance(lat1,lng1,lat2,lng2):
        distance = haversine((lat1,lng1),(lat2,lng2))
        return distance
    
    @staticmethod
    def find_euclidean_dist(lat1,lng1,lat2,lng2):
        distance = ((lat1-lat2)**2 + (lng1-lng2)**2)**0.5
        return distance
    
    def addEdge(self,src,dest):
        distance = round(Graph.find_distance(src.lat,src.lng,dest.lat,dest.lng),2)
        self.adj_list[src.name].append((dest,distance))
        self.adj_list[dest.name].append((src,distance))
        
    def printGraph(self):
        for name in self.names:
            all_adjacents = self.adj_list[name]
            
            for adjacent,distance in all_adjacents:
                print(f"{name} --> {adjacent.name} with distance {distance}")
                
    def printPath(self,dest):
        if self.parent[dest] == -1:
            print(dest, end=" ")
            self.path.append(dest)
            return
        self.printPath(self.parent[dest])
        print(dest, end=" ")
        self.path.append(dest)
        
    def greedy_best_first_search(self,src,dest):
        pq = PriorityQueue()
        pq.put((0,src))
        self.visited[src.name] = 1
        
        while pq.empty() == False:
            element = pq.get()[1]
            print("Currently exploring: ",element.name)
            
            if element.name == dest.name:
                print("Goal has been found.")
                break
            
            for neighbour,distance in self.adj_list[element.name]:
                if self.visited[neighbour.name] != 1:
                    h_dist = Graph.find_distance(neighbour.lat,neighbour.lng,dest.lat,dest.lng)
                    pq.put((h_dist,neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
                    
    def a_star_search(self,src,dest):
        pq = PriorityQueue()
        pq.put((0,src))
        self.visited[src.name] = 1
        
        while pq.empty() == False:
            element = pq.get()[1]
            print("Currently exploring: ",element.name)
            
            if element.name == dest.name:
                print("Goal has been found.")
                break
            
            for neighbour,distance in self.adj_list[element.name]:
                if self.visited[neighbour.name] != 1:
                    h_dist = Graph.find_distance(neighbour.lat,neighbour.lng,dest.lat,dest.lng)
                    self.g_dist[neighbour.name] = self.g_dist[element.name] + distance
                    f_dist = self.g_dist[neighbour.name] + h_dist
                    
                    pq.put((f_dist,neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
                    
    def depth_first_search(self,src,dest):
        stack = [src]
        self.visited[src] = 1
        
        while stack:
            print(stack)
            element = stack.pop()
            print("Currently exploring: ",element)
            
            if element == dest:
                print("Goal has been found.")
                break
                
            for neighbour,distance in self.adj_list[element]:
                if self.visited[neighbour.name] != 1:
                    stack.append(neighbour.name)
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element
        
    def breadth_first_search(self,src,dest):
        queue = [src]
        self.visited[src] = 1
        
        while queue:
            print(queue)
            element = queue.pop(0)
            print("Currently exploring: ",element)
            
            if element == dest:
                print("Goal has been found.")
                break
            
            for neighbour,distance in self.adj_list[element]:
                if self.visited[neighbour.name] != 1:
                    queue.append(neighbour.name)
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element
        
################################

A = LocationNode('A',19.09774223623271, 72.99921512603761)
B = LocationNode('B',19.097369721525737, 72.99788475036623)
C = LocationNode('C',19.09935841070307, 73.00482630729677)
D = LocationNode('D',19.098039600067327, 72.99513816833498)
E = LocationNode('E',19.102829624178575, 72.99773454666139)
F = LocationNode('F',19.103158006559386, 72.9965114593506)
G = LocationNode('G',19.10709178131952, 72.9970693588257)
H = LocationNode('H',19.109625105710315, 72.99805641174318)
I = LocationNode('I',19.11049962328326, 73.00143599510194)

names = ['A','B','C','D','E','F','G','H','I']

g1 = Graph(names)
g1.addEdge(A,B)
g1.addEdge(B,D)
g1.addEdge(D,F)
g1.addEdge(A,E)
g1.addEdge(E,F)
g1.addEdge(F,G)
g1.addEdge(G,H)
g1.addEdge(H,I)
g1.addEdge(C,I)
g1.addEdge(A,C)

g1.printGraph()

g1.depth_first_search(B.name,H.name)
g1.printPath(H.name)
g1.reset()

g1.breadth_first_search(B.name,H.name)
g1.printPath(H.name)
g1.reset()

g1.greedy_best_first_search(B.name,H.name)
g1.printPath(H.name)
g1.reset()

g1.a_star_search(B,H)
g1.printPath(H.name)
g1.reset()