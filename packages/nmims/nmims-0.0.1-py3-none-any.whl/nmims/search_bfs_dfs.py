def search_bfs_dfs():
    print('''
    
############# BFS-DFS Graph

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
        
        # The for loop here is to initalize the adjacent list of each node as an empty list to which we will add
        # elements whenever we add edges. We also initalize the visited dict with 0 (indicating unexplored) for each node
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

    #bfs
    #1 Put the source element in the queue. (line 3)
    #2 Set the source element as visited. (line 4)
    #3 Run the program till line 9 until the queue is empty. (line 6)
    #4 Print the current elements inside the queue. (line 7)
    #5 Pop out the first element in the queue and print it to show that we are exploring it. (line 8 and 9)
    #6 Check if the element popped at line 8 is the destination, if yes print "Goal has been found." and then break out of the loop otherwise go on with the program. (lines 11-13)
    #7 Check for the adjacent elements of the element popped in line 8 and check if each adjacent element has been visited or not. If not, then push them in the queue and set the neighbour element as visited. (lines 15-18)                    
    
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

    #dfs
    #1 Put the source element in the stack. (line 3)
    #2 Set the source element as visited. (line 4)
    #3 Run the program till line 9 until the stack is empty. (line 6)
    #4 Print the current elements inside the stack. (line 7)
    #5 Pop out the top most element (last element) in the stack and print it to show that we are exploring it. (line 8 and 9)
    #6 Check if the element popped at line 8 is the destination, if yes print "Goal has been found." and then break out of the loop otherwise go on with the program. (lines 11-13)
    #7Check for the adjacent elements of the element popped in line 8 and check if each adjacent element has been visited or not. If not, then push them onto the stack and set the neighbour element as visited. (lines 15-18)
                    
    def printPath(self, j):
        if self.parent[j] == -1 : 
            print(j,end=" ")
            self.path.append(j) 
            return
        self.printPath(self.parent[j]) 
        print(j,end=" ")
        self.path.append(j)


A = Point('A',1,2)
B = Point('B',2,6)
C = Point('C',3,3)
D = Point('D',5,6)


names = ['A','B','C','D']
nodes = len(names)

g1 = Graph(nodes,names)
g1.addEdge(A,B)
g1.addEdge(A,C)
g1.addEdge(B,C)
g1.addEdge(B,D)
g1.addEdge(C,D)


g1.printGraph()

g1.dfs(A.name,D.name)

g1.printPath('D')

g1.reset()

g1.bfs(A.name,D.name)

g1.printPath('D')

#################### BFS-DFS Coordinates

import numpy as np
from haversine import haversine
from queue import PriorityQueue

coods = {'A':[19.107344940635752, 72.83750439746517],
'B':[19.10731366839371, 72.8378642431011],
'C':[19.108279964192004, 72.8379852901361],
'D':[19.108113250686728, 72.83998067137303],
'E':[19.108228490593877, 72.83998448261089],
'F':[19.107373705083035, 72.83696773529932],
'G':[19.108431263605976, 72.83703359263299]}


class LocationNode:
    
    def __init__(self,name,lat,lng):
        self.name = name
        self.lat = lat
        self.lng = lng


class Graph:

    def __init__(self, nodes, names):
        self.nodes = nodes
        self.adj_list = {}
        self.visited = {}
        self.parent = {}
        self.names = names
        self.path=[]
        
        # The for loop here is to initalize the adjacent list of each node as an empty list to which we will add
        # elements whenever we add edges. We also initalize the visited dict with 0 (indicating unexplored) for each node
        for name in self.names:
            self.adj_list[name] = []
            self.visited[name] = 0
            self.parent[name] = -1
            
        self.distance_tracker = 0.0
        
    @staticmethod
    def find_distance(lat1,lng1,lat2,lng2):
        distance = haversine((lat1,lng1),(lat2,lng2))
        return distance
    
    def reset(self):
        for name in self.names:
            self.visited[name] = 0
            self.parent[name] = -1
        
    def addEdge(self, source, destination):
        distance = round(Graph.find_distance(source.lat, source.lng, destination.lat, destination.lng),2)
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



A = LocationNode('A',19.107344940635752, 72.83750439746517)
B = LocationNode('B',19.10731366839371, 72.8378642431011)
C = LocationNode('C',19.108279964192004, 72.8379852901361)
D = LocationNode('D',19.108113250686728, 72.83998067137303)
E = LocationNode('E',19.108228490593877, 72.83998448261089)
F = LocationNode('F',19.107373705083035, 72.83696773529932)
G = LocationNode('G',19.108431263605976, 72.83703359263299)

names = ['A','B','C','D','E','F','G']
nodes = len(names)

g2 = Graph(nodes,names)
g2.addEdge(A,B)
g2.addEdge(A,F)
g2.addEdge(F,G)
g2.addEdge(G,C)
g2.addEdge(B,C)
g2.addEdge(C,D)
g2.addEdge(D,E)

g2.printGraph()

g2.reset()
g2.bfs(A.name,E.name)

g2.reset()
g2.bfs(A.name,E.name)

g2.printPath(E.name)

path = g2.path
path

g2.reset()
g2.dfs(A.name,E.name)

g2.printPath(E.name)

path = g2.path
path


distance = 0
for i in range(len(path)-1):
    distance += haversine(coods[path[i]],coods[path[i+1]])
print(round(distance,2),"Kms /", round(distance,2)*1000, "m")
''')

search_bfs_dfs()