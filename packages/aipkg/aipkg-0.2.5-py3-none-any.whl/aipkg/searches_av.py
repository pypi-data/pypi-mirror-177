############################ A STar and GBFS with HAVERSINE########################################


import numpy as np
import folium
from haversine import haversine
from queue import PriorityQueue

class Point:
    
    def __init__(self,name,latitude,longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        
class Graph:

    def __init__(self, nodes, names):
        self.nodes = nodes
        self.adj_list = {}
        self.visited = {}
        self.parent = {}
        self.g_dist = {}
        self.names = names
        self.path=[]
        
        for name in self.names:
            self.adj_list[name] = []
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0           
            
        self.distance_tracker = 0.0
        
    @staticmethod
    def find_distance(lat1,lng1,lat2,lng2):
        distance = haversine((lat1,lng1),(lat2,lng2))
        return distance
    
    def reset(self):
        for name in self.names:
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0
        self.path=[]
        
    def addEdge(self, source, destination):
        distance = round(Graph.find_distance(source.latitude, source.longitude, destination.latitude, destination.longitude),2)
        self.adj_list[source.name].append((destination,distance))
        self.adj_list[destination.name].append((source,distance))
        
    def printGraph(self):
        for name in self.names:
            all_adjacents = self.adj_list[name]
            for adjacent,distance in all_adjacents:
                print(f"{name} -> {adjacent.name} with distance {distance}")
    
    def best_first_search(self, src, dest):
        
        pq = PriorityQueue()
        pq.put((0,src))
        self.visited[src.name] = 1
        
        while pq.empty() == False:
            element = pq.get()[1]
            print("Currently Exploring:", element.name)
            
            if element.name == dest.name:
                print("Goal has been found")
                break
            
            for neighbour, distance in self.adj_list[element.name]:
                if self.visited[neighbour.name] != 1:
                    h_dist = Graph.find_distance(neighbour.latitude,neighbour.longitude,dest.latitude,dest.longitude)
                    pq.put((h_dist, neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
                    
                    
                    
#     Create an object pq of the PriorityQueue class. (line 3)
# Put the initial distance(set as 0) and source element in a tuple and insert in the priority queue as its first element. (line 4)
# Set the source element as visited since it's now being visited/explored. (line 5)
# Run the program till line 24 until the priority queue is empty. (line 7)
# Retrieve the element (only the element, not the distance associated with it at 0 index of the tuple) with the highest priority from pq using the get() method of Priority Queue class. (line 8)
# Print this element's name as the element being currently explored. (line 9)
# Check if the element obtained in line 8 is the destination, if yes print "Goal has been found." and then break out of the loop otherwise go on with the program. (lines 11-13)
# Iterate through all the adjacent neighbours of our obtained element and run the program till line 24 with each iteration. (line 15)
# Check if the neighbouring element has been visited before or not, if yes then go to the next iteration, otherwise go on with the program. (line 16)
# Store the g_dist for the neighbour element as the sum of g_dist for the obtained element in line 8 and the distance between that element and the neighbour element. (line 18)
# Calculate the distance between the neighbouring element and the destination using the find_distance method of the Graph class and store it as the heuristic distance (h_dist). (line 19)
# Store f_dist as the sum of h_dist (calculated in line 19) and g_dist for the neighbour element (calculated in line 18). (line 20)
# Put the f_dist and neighbour element object in a tuple and insert it in the priority queue pq. (line 22)
# Set the neighbour element just explored as visited since it has now been visited/explored. (line 23)
# Set the name of the parent of the neighbour element just explored as the element obtained in line 8. This will allow us to backtrack to find the path to be taken from source to destination. (line 24)
    
    
    
    def a_star_search(self, src, dest):
        
        pq = PriorityQueue()
        pq.put((0,src))
        self.visited[src.name] = 1
        
        while pq.empty() == False:
            element = pq.get()[1]
            print("Currently Exploring:", element.name)
            
            if element.name == dest.name:
                print("Goal has been found")
                break
            
            for neighbour, distance in self.adj_list[element.name]:
                if self.visited[neighbour.name] != 1:
                    
                    self.g_dist[neighbour.name] = self.g_dist[element.name] + distance
                    h_dist = Graph.find_distance(neighbour.latitude,neighbour.longitude,dest.latitude,dest.longitude)
                    f_dist = self.g_dist[neighbour.name] + h_dist
                    
                    pq.put((f_dist, neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
                    

#            Create a priority queue "pq" (line 3). The priority queue defines the priority that the algorithm must take into consideration while executing (priority is shortest distance in this case).
# Put the initial distance covered and the source element into the priorityqueue (line 4). initial distance will be zero as the algorithm hasnt moved from the source.
# keep track of what element has been visited by creating another frontier to store them in (line 5).
# run a loop while the priorityqueue is still not empty (line 7)
# in the loop, retrieve the immediate next element in the priorityqueue which is at the shortest distance from the current element. Then, Print the name of the element currently being explored (line 8-9)
# if the element currently being explored is the destination, then print that the goal has been found and break out of the loop (line 11 - 13). if it is not the destination, continue on to the next steps of the loop.
# check the elements adjacent to the element previously popped. (line 15)
# if the neighboring element has not been previously popped, create the your function f_dist. f_dist is the sum of h_dist and and g_dist where: h_dist is the distance between current element and destination; g_dist is the distance between current element and source (line 16 - 20)
# put that element and its total distance (f_dist) value into the priorityqueue. (line 22)
# Once the neighboring element has been popped, store it in the frontier. (line 23-24)         
                    
                    
    def printPath(self, j):
        if self.parent[j] == -1 : 
            print(j,end=" ")
            self.path.append(j) 
            return
        self.printPath(self.parent[j]) 
        print(j,end=" ")
        self.path.append(j)
        
coods = {'A':[19.09774223623271, 72.99921512603761],
'B':[19.097369721525737, 72.99788475036623],
'C':[19.09935841070307, 73.00482630729677],
'D':[19.098039600067327, 72.99513816833498],
'E':[19.102829624178575, 72.99773454666139],
'F':[19.103158006559386, 72.9965114593506],
'G':[19.10709178131952, 72.9970693588257],
'H':[19.109625105710315, 72.99805641174318],
'I':[19.11049962328326, 73.00143599510194]}

A = Point('A',19.09774223623271, 72.99921512603761)
B = Point('B',19.097369721525737, 72.99788475036623)
C = Point('C',19.09935841070307, 73.00482630729677)
D = Point('D',19.098039600067327, 72.99513816833498)
E = Point('E',19.102829624178575, 72.99773454666139)
F = Point('F',19.103158006559386, 72.9965114593506)
G = Point('G',19.10709178131952, 72.9970693588257)
H = Point('H',19.109625105710315, 72.99805641174318)
I = Point('I',19.11049962328326, 73.00143599510194)

names = ['A','B','C','D','E','F','G','H','I']
nodes = len(names)

g1 = Graph(nodes,names)
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

print(g1.best_first_search(B,H))
print(g1.printPath(H.name))
g1.reset()
print(g1.a_star_search(B,H))
print(g1.printPath(H.name))


############# BFS AND DFS WITH HAVERSINE ##########################################

# DFS AND BFS  with MAP COORDINATES

import numpy as np
import folium
from haversine import haversine
from queue import PriorityQueue

class Point:
    
    def __init__(self,name,latitude,longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        
class Graph:

    def __init__(self, nodes, names):
        self.nodes = nodes
        self.adj_list = {}
        self.visited = {}
        self.parent = {}
        self.g_dist = {}
        self.names = names
        self.path=[]
        
        for name in self.names:
            self.adj_list[name] = []
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0           
            
        self.distance_tracker = 0.0
        
    @staticmethod
    def find_distance(lat1,lng1,lat2,lng2):
        distance = haversine((lat1,lng1),(lat2,lng2))
        return distance
    
    def reset(self):
        for name in self.names:
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0
        self.path=[]
        
    def addEdge(self, source, destination):
        distance = round(Graph.find_distance(source.latitude, source.longitude, destination.latitude, destination.longitude),2)
        self.adj_list[source.name].append((destination.name,distance))
        self.adj_list[destination.name].append((source.name,distance))
        
    def printGraph(self):
        for name in self.names:
            all_adjacents = self.adj_list[name]
            for adjacent,distance in all_adjacents:
                print(f"{name} -> {adjacent} with distance {distance}")
    
    
                    
    def bfs(self, src, dest):
        
        queue = [src]
        self.visited[src] = 1
        
        while queue:
            print(queue)
            element = queue.pop(0)
            print("Currently Exploring:", element)
            
            if element == dest:
                print("Goal has been found")
                break
                
            for neighbour, distance in self.adj_list[element]:
                if self.visited[neighbour] != 1:
                    queue.append(neighbour)
                    self.visited[neighbour] = 1
                    self.parent[neighbour] = element
                    
#         Put the source element into a Stack (line 3)
# keep track of what element has been visited by creating another frontier to store them in (line 4).
# Run a while loop till the stack is empty (line 6)
# In the loop, first print all the elements in the stack (line 7)
# Pop the element at the last index within the stack, i.e, the last element of the stack. print a statement to show we are exploring that element (line 8-9)
# check if the element currently being explored is the destination. If the destination has been reached, print a statement saying that the goal has been found, and break out of the loop. If the destination has not been found, continue towards the next step of the loop. (line 11-13)
# check the elements adjacent to the element previously popped. if the elemnts have not been already popped, append them onto the stack. if they have been explored, store them in the frontier. (line 15 - 18)
                    
    
    def dfs(self, src, dest):
        
        stack = [src]
        self.visited[src] = 1
        
        while stack:
            print(stack)
            element = stack.pop()
            print("Currently Exploring:", element)
            
            if element == dest:
                print("Goal has been found")
                break
                
            for neighbour, distance in self.adj_list[element]:
                if self.visited[neighbour] != 1:
                    stack.append(neighbour)
                    self.visited[neighbour] = 1
                    self.parent[neighbour] = element
                    
#            Put the source element into a Queue (line 3)
# keep track of what element has been visited by creating another frontier to store them in (line 4).
# Run a while loop till the queue is empty (line 6)
# In the loop, first print all the elements in the queue (line 7)
# Pop the element at the zeroth index within the queue, i.e, the first element of the queue. print a statement to show we are exploring that element (line 8-9)
# check if the element currently being explored is the destination. If the destination has been reached, print a statement saying that the goal has been found, and break out of the loop. If the destination has not been found, continue towards the next step of the loop. (line 11-13)
# check the elements adjacent to the element previously popped. if the elemnts have not been already popped, append them onto the queue. if they have been explored, store them in the frontier. (line 15 - 18)         

                    
    def printPath(self, j):
        if self.parent[j] == -1 : 
            print(j,end=" ")
            self.path.append(j) 
            return
        self.printPath(self.parent[j]) 
        print(j,end=" ")
        self.path.append(j)
        
coods = {'A':[19.09774223623271, 72.99921512603761],
'B':[19.097369721525737, 72.99788475036623],
'C':[19.09935841070307, 73.00482630729677],
'D':[19.098039600067327, 72.99513816833498],
'E':[19.102829624178575, 72.99773454666139],
'F':[19.103158006559386, 72.9965114593506],
'G':[19.10709178131952, 72.9970693588257],
'H':[19.109625105710315, 72.99805641174318],
'I':[19.11049962328326, 73.00143599510194]}

A = Point('A',19.09774223623271, 72.99921512603761)
B = Point('B',19.097369721525737, 72.99788475036623)
C = Point('C',19.09935841070307, 73.00482630729677)
D = Point('D',19.098039600067327, 72.99513816833498)
E = Point('E',19.102829624178575, 72.99773454666139)
F = Point('F',19.103158006559386, 72.9965114593506)
G = Point('G',19.10709178131952, 72.9970693588257)
H = Point('H',19.109625105710315, 72.99805641174318)
I = Point('I',19.11049962328326, 73.00143599510194)

names = ['A','B','C','D','E','F','G','H','I']
nodes = len(names)

g1 = Graph(nodes,names)
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

print(g1.bfs(B.name,H.name))
print(g1.printPath(H.name))
g1.reset()
print(g1.dfs(B.name,H.name))
print(g1.printPath(H.name))


###################################BFS AND DFS WITH EUCLIDEAN ##########

#DFS AND BFS with euclidean distance

class Point:
   
    def __init__(self,name,x,y):
        self.name = name
        self.x = x 
        self.y = y
        
class Graph:
    
    def __init__(self, nodes, names):
        self.nodes = nodes
        self.adj_list = {}
        self.visited = {}
        self.parent = {}
        self.names = names
        self.path=[]
        
        for name in self.names:
            self.adj_list[name] = []
            self.visited[name] = 0
            self.parent[name] = -1
            
        self.distance_tracker = 0.0
        
    @staticmethod
    def find_distance(x1,x2,y1,y2):
        distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
        return distance
    
    def reset(self):
        for name in self.names:
            self.visited[name] = 0
            self.parent[name] = -1
        
        
    def addEdge(self, source, destination):
        distance = round(Graph.find_distance(source.x, destination.x, source.y, destination.y))
        self.adj_list[source.name].append((destination.name,distance))
        self.adj_list[destination.name].append((source.name,distance))
        
    def printGraph(self):
        for name in self.names:
            all_adjacents = self.adj_list[name]
            for adjacent,distance in all_adjacents:
                print(f"{name} -> {adjacent} with distance {distance}")
                                
    def bfs(self, src, dest):
        
        queue = [src]
        self.visited[src] = 1
        
        while queue:
            print(queue)
            element = queue.pop(0)
            print("Currently Exploring:", element)
            
            if element == dest:
                print("Goal has been found")
                break
                
            for neighbour, distance in self.adj_list[element]:
                if self.visited[neighbour] != 1:
                    queue.append(neighbour)
                    self.visited[neighbour] = 1
                    self.parent[neighbour] = element
                    
    def dfs(self, src, dest):
        
        stack = [src]
        self.visited[src] = 1
        
        while stack:
            print(stack)
            element = stack.pop()
            print("Currently Exploring:", element)
            
            if element == dest:
                print("Goal has been found")
                break
                
            for neighbour, distance in self.adj_list[element]:
                if self.visited[neighbour] != 1:
                    stack.append(neighbour)
                    self.visited[neighbour] = 1
                    self.parent[neighbour] = element
                    
                    
    def printPath(self, j):
        if self.parent[j] == -1 : 
            print(j,end=" ")
            self.path.append(j) 
            return
        self.printPath(self.parent[j]) 
        print(j,end=" ")
        self.path.append(j)
        
A = Point('A',1,1)
B = Point('B',3,2)
C = Point('C',2,4)
D = Point('D',5,3)
E = Point('E',4,6)
F = Point('F',6,6)

names = ['A','B','C','D','E','F']
nodes = len(names)

g1 = Graph(nodes,names)
g1.addEdge(A,B)
g1.addEdge(A,C)
g1.addEdge(B,D)
g1.addEdge(B,E)
g1.addEdge(C,D)
g1.addEdge(C,E)
g1.addEdge(D,F)
g1.addEdge(E,F)

g1.printGraph()

print(g1.bfs(A.name,E.name))
print(g1.printPath(E.name))
g1.reset()
print(g1.dfs(A.name,E.name))
print(g1.printPath(E.name))


########################################## A STAR AND GBFS WITH EUCLIDEAN ##################3

import numpy as np
from queue import PriorityQueue
from haversine import haversine


# In[2]:


class Point:
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y


# In[17]:


class Graph:
    def __init__(self,nodes,names):
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
        
#     @staticmethod
#     def find_distance(lat1,lng1,lat2,lng2):
#         distance = haversine((lat1,lng1),(lat2,lng2))
#         return distance
    
    @staticmethod
    def find_distance(x1,y1,x2,y2):
        distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
        return distance
    
    def addEdge(self,src,dest):
        distance = round(Graph.find_distance(src.x,src.y,dest.x,dest.y),2)
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
                    h_dist = Graph.find_distance(neighbour.x,neighbour.y,dest.x,dest.y)
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
                    h_dist = Graph.find_distance(neighbour.x,neighbour.y,dest.x,dest.y)
                    self.g_dist[neighbour.name] = self.g_dist[element.name] + distance
                    f_dist = self.g_dist[neighbour.name] + h_dist
                    
                    pq.put((f_dist,neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
                    
  


# In[27]:


A = Point('A',1,1)
B = Point('B',3,2)
C = Point('C',2,4)
D = Point('D',5,3)
E = Point('E',4,6)
F = Point('F',6,6)

names = ['A','B','C','D','E','F']
nodes = len(names)

g2 = Graph(nodes,names)
g2.addEdge(A,B)
g2.addEdge(A,C)
g2.addEdge(B,D)
g2.addEdge(B,E)
g2.addEdge(C,D)
g2.addEdge(C,E)
g2.addEdge(D,F)
g2.addEdge(E,F)

g2.printGraph()

# print(g1.best_first_search(A,E))
# print(g1.printPath(E.name))
g2.reset()
print(g2.a_star_search(A,E))
print(g2.printPath(E.name))