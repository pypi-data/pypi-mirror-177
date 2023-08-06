def search_gbfs_astar():
    print('''
    ######################### GBFS-ASTAR Graph

import numpy as np
from haversine import haversine
from queue import PriorityQueue


x=[1,3,2,5,4,6]
y=[1,2,4,3,6,6]


class Point:
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y


class Graph:
    def __init__(self,nodes,name):
        self.name=name
        self.nodes=nodes
        self.adj_list={}
        self.visited={}
        self.parent={}
        self.g_dist={}
        self.path=[]
        for name in self.name:
            self.adj_list[name]=[]
            self.g_dist[name]=0
            self.visited[name]=0
            self.parent[name]=-1
        self.distance_tracker=0.0
    
    @staticmethod
    def find_distance(x1,x2,y1,y2):
        distance=(((x2-x1)**2)+((y2-y1)**2))**0.5
        return distance
        
    def addEdge2(self,source,destination):
        distance=round(Graph.find_distance(source.x,destination.x,source.y,destination.y))
        self.adj_list[source.name].append((destination,distance))
        self.adj_list[destination.name].append((source,distance))
    
    def reset(self):
        self.path=[]
        for name in self.name:
            self.visited[name] = 0
            self.parent[name] = -1
            self.g_dist[name] = 0
                
    def printGraph2(self):
        for name in self.name:
            all_adjacents=self.adj_list[name]
            for adjacents,distance in all_adjacents:
                print(f'{name}---{adjacents.name} with distance {distance}')
                
    def gbfs(self,src,dest):
        pq=PriorityQueue()
        pq.put((0,src))
        self.visited[src.name]=1
        self.path.append(src.name)
        while pq.empty()==False:
            element=pq.get()[1]
            print(f"Currently exploring:{element.name}")
            if element.name==dest.name:
                self.path.append(element.name)
                print("Goal has been found")
                break
            for neighbour,distance in self.adj_list[element.name]:
                if self.visited[neighbour.name] !=1:
                    h_dist=Graph.find_distance(neighbour.x,dest.x,neighbour.y,dest.y)
                    pq.put((h_dist,neighbour))
                    self.visited[neighbour.name]=1
                    self.parent[neighbour.name]=element.name
                    self.path.append(neighbour.name)

    def a_star(self,src,dest):
        pq=PriorityQueue()
        pq.put((0,src))
        self.visited[src.name]=1
        self.path.append(src.name)
        while pq.empty()==False:
            element=pq.get()[1]
            print(f"Currently exploring:{element.name}")
            if element.name==dest.name:
                self.path.append(element.name)
                print("Goal has been found")
                break
            for neighbour,distance in self.adj_list[element.name]:
                if self.visited[neighbour.name] !=1:
                    h_dist=Graph.find_distance(neighbour.x,dest.x,neighbour.y,dest.y)
                    self.g_dist[neighbour.name]=self.g_dist[element.name]+distance
                    f_dist=self.g_dist[neighbour.name]+h_dist
                    pq.put((f_dist,neighbour))
                    self.visited[neighbour.name]=1
                    self.parent[neighbour.name]=element.name
                    self.path.append(neighbour.name)
                    
    def printPath(self,j):
        if self.parent[j]==-1:
            print(j,end=" ")
            self.path.append(j)
            return j
        self.printPath(self.parent[j])
        print(j,end=" ")
        self.path.append(j)
            
A=Point('A',1,1)
B=Point('B',3,2)
C=Point('C',2,4)
D=Point('D',5,3)
E=Point('E',4,6)
F=Point('F',6,6)

names=['A','B','C','D','E','F']
nodes=len(names)

g1=Graph(nodes,names)
g1.addEdge2(A,B)
g1.addEdge2(A,C)
g1.addEdge2(C,D)
g1.addEdge2(B,D)
g1.addEdge2(B,E)
g1.addEdge2(E,F)
g1.addEdge2(D,F)
g1.printGraph2()

g1.reset()
g1.gbfs(A,F)

g1.printPath(F.name)

g1.reset()
g1.a_star(A,F)

g1.a_star(A,F)

g1.printPath(F.name)

######################### GBFS-ASTAR Coordinates

import numpy as np
from haversine import haversine
from queue import PriorityQueue

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
        self.g_dist = {}
        self.names = names
        self.path=[]
        
        # The for loop here is to initalize the adjacent list of each node as an empty list to which we will add
        # elements whenever we add edges. We also initalize the visited dict with 0 (indicating unexplored) for each node
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
        
    def addEdge(self, source, destination):
        distance = round(Graph.find_distance(source.lat, source.lng, destination.lat, destination.lng),2)
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
                    h_dist = Graph.find_distance(neighbour.lat,neighbour.lng,dest.lat,dest.lng)
                    pq.put((h_dist, neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
    
    #best_first_search
    #1 Create an object pq of the PriorityQueue class. (line 3)
    #2 Put the initial distance(set as 0) and source element in a tuple and insert in the priority queue as its first element. (line 4)
    #3 Set the source element as visited since it's now being visited/explored. (line 5)
    #4 Run the program till line 20 until the priority queue is empty. (line 7)
    #5 Retrieve the element (only the element, not the distance associated with it at 0 index of the tuple) with the highest priority from pq using the get() method of Priority Queue class. (line 8)
    #6 Print this element's name as the element being currently explored. (line 9)
    #7 Check if the element obtained in line 8 is the destination, if yes print "Goal has been found." and then break out of the loop otherwise go on with the program. (lines 11-13)
    #8 Iterate through all the adjacent neighbours of our obtained element and run the program till line 20 with each iteration. (line 15)
    #9 Check if the neighbouring element has been visited before or not, if yes then go to the next iteration, otherwise go on with the program. (line 16)
    #10 Calculate the distance between the neighbouring element and the destination using the find_distance method of the Graph class and store it as the heuristic distance (h_dist). (line 17)
    #11 Put the heuristic distance and neighbour element object in a tuple and insert it in the priority queue pq. (line 18)
    #12 Set the neighbour element just explored as visited since it has now been visited/explored. (line 19)
    #13 Set the name of the parent of the neighbour element just explored as the element obtained in line 8. This will allow us to backtrack to find the path to be taken from source to destination. (line 20)

    
                    
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
                    h_dist = Graph.find_distance(neighbour.lat,neighbour.lng,dest.lat,dest.lng)
                    f_dist = self.g_dist[neighbour.name] + h_dist
                    
                    pq.put((f_dist, neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name
    # a_star search                   
    #1 Create an object pq of the PriorityQueue class. (line 3)
    #2 Put the initial distance(set as 0) and source element in a tuple and insert in the priority queue as its first element. (line 4)
    #3 Set the source element as visited since it's now being visited/explored. (line 5)
    #4 Run the program till line 24 until the priority queue is empty. (line 7)
    #5 Retrieve the element (only the element, not the distance associated with it at 0 index of the tuple) with the highest priority from pq using the get() method of Priority Queue class. (line 8)
    #6 Print this element's name as the element being currently explored. (line 9)
    #7 Check if the element obtained in line 8 is the destination, if yes print "Goal has been found." and then break out of the loop otherwise go on with the program. (lines 11-13)
    #8 Iterate through all the adjacent neighbours of our obtained element and run the program till line 24 with each iteration. (line 15)
    #9 Check if the neighbouring element has been visited before or not, if yes then go to the next iteration, otherwise go on with the program. (line 16)
    #10 Store the g_dist for the neighbour element as the sum of g_dist for the obtained element in line 8 and the distance between that element and the neighbour element. (line 18)
    #11 Calculate the distance between the neighbouring element and the destination using the find_distance method of the Graph class and store it as the heuristic distance (h_dist). (line 19)
    #12 Store f_dist as the sum of h_dist (calculated in line 19) and g_dist for the neighbour element (calculated in line 18). (line 20)
    #13 Put the f_dist and neighbour element object in a tuple and insert it in the priority queue pq. (line 22)
    #14 Set the neighbour element just explored as visited since it has now been visited/explored. (line 23)
    #15 Set the name of the parent of the neighbour element just explored as the element obtained in line 8. This will allow us to backtrack to find the path to be taken from source to destination. (line 24)   

        
    def printPath(self, j):
        if self.parent[j] == -1 : 
            print(j,end=" ")
            self.path.append(j) 
            return
        self.printPath(self.parent[j]) 
        print(j,end=" ")
        self.path.append(j)

coods = {'A':[19.110014737929422, 72.83722667058736],
'B':[19.108421177504923, 72.83701536065512],
'C':[19.10808338641388, 72.84044818949215],
'D':[19.104255923506848, 72.83948295513042],
'E':[19.100541511748673, 72.83952159010958],
'F':[19.10042777921402, 72.84073421821141], # goal
'G':[19.10259694454942, 72.83692278689],
'H':[19.101521348929513, 72.83948666203591]}

A = LocationNode('A',19.110014737929422, 72.83722667058736)
B = LocationNode('B',19.108421177504923, 72.83701536065512)
C = LocationNode('C',19.10808338641388, 72.84044818949215)
D = LocationNode('D',19.104255923506848, 72.83948295513042)
E = LocationNode('E',19.100541511748673, 72.83952159010958)
F = LocationNode('F',19.10042777921402, 72.84073421821141)
G = LocationNode('G',19.10259694454942, 72.83692278689)
H = LocationNode('H',19.101521348929513, 72.83948666203591)

names = ['A','B','C','D','E','F','G','H']
nodes = len(names)

g2 = Graph(nodes,names)
g2.addEdge(A,B)
g2.addEdge(B,C)
g2.addEdge(C,D)
g2.addEdge(D,H)
g2.addEdge(H,E)
g2.addEdge(E,F)
g2.addEdge(B,G)
g2.addEdge(G,H)

g2.printGraph()

g2.best_first_search(A,F)

g2.printPath(F.name)

g2.parent

path = g2.path
path

g2.reset()

g2.a_star_search(A,F)

g2.printPath(F.name)

g2.parent

path = g2.path
path

distance = 0
for i in range(len(path)-1):
    distance += haversine(coods[path[i]],coods[path[i+1]])
print(round(distance,2),"Kms /", round(distance,2)*1000, "m")
''')

search_gbfs_astar()