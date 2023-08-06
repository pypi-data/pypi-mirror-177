def search():
    print('''
    for symbol in symbols:
    if model_check(knowledge_base4,symbol):
        print(symbol)
    
sns.set_style('darkgrid')
plt.rcParams['font.size']=18
plt.rcParams['figure.figsize']=(20,8)

x=[1,3,5,1,6,11]
y=[2,6,4,10,10,7]
plt.scatter(x,y,s=100)

plt.annotate('A',(x[0],y[0]))
plt.annotate('B',(x[1],y[1]))
plt.annotate('C',(x[2],y[2]))
plt.annotate('D',(x[3],y[3]))
plt.annotate('E',(x[4],y[4]))
plt.annotate('F',(x[5],y[5]))

plt.plot([1,3],[2,6])
plt.plot([1,5],[2,4])
plt.plot([3,1],[6,10])
plt.plot([5,6],[4,10])
plt.plot([6,11],[10,7])
plt.plot([1,11],[10,7])
plt.plot([3,6],[6,10])

class Point:
    def __init__(self,names,x,y):
        self.names=names
        self.x=x
        self.y=y
class Graph:
    def __init__(self,nodes,names):
        self.nodes=nodes
        self.names=names
        self.adj_list={}
        self.visited={}
        self.parent={}
        self.path=[]
        
        for name in self.names:
            self.adj_list[name]=[]
            self.visited[name]=0
            self.parent[name]=-1
            
        self.distance_tracker=0.0
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
        self.adj_list[source.names].append((destination.names,distance))
        self.adj_list[destination.names].append((source.names,distance))
        
    
    def printGraph(self):
        for name in self.names:
            all_adjacents=self.adj_list[name]
            for adjacents,distance in all_adjacents:
                print(f'{name}----->{adjacents} with distance {distance}')
    
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
    
    def dfs(self,src,dest):
        stack=[src]
        self.visited[src]=1
        
        while stack:
            print(stack)
            element=stack.pop()
            print(f'Currently exploring {element}')
            if element==dest:
                print('Goal has been found')
                break
            for neighbour,distance in self.adj_list[element]:
                    if self.visited[neighbour]!=1:
                        stack.append(neighbour)
                        self.visited[neighbour]=1
                        self.parent[neighbour]=element
    
    def printPath(self,j):
        if self.parent[j]==-1:
            print('j',end=" ")
            self.path.append(j)
            return
        
        
        self.printPath(self.parent[j])
        print('j',end=" ")
        self.path.append(j)
                
            
A=Point('A',1,2)
B=Point('B',3,6)
C=Point('C',5,4)
D=Point('D',1,10)
E=Point('E',6,10)
F=Point('F',11,7)

names=['A','B','C','D','E','F']
nodes=len(names)

g1=Graph(nodes,names)
g1.addEdge(A,B)
g1.addEdge(A,C)
g1.addEdge(B,D)
g1.addEdge(C,E)
g1.addEdge(D,F)
g1.addEdge(B,E)
g1.addEdge(E,F)

g1.printGraph()

g1.reset()

g1.dfs('A','F')

g1.bfs('A','F')

import matplotlib.pyplot as plt
import seaborn as sns
from queue import PriorityQueue

sns.set_style("darkgrid")
plt.rcParams['font.size']=8
plt.rcParams['figure.figsize']=(20,8)

x=[1,3,2,5,4,6]
y=[1,2,4,3,6,6]
plt.scatter(x,y,s=100)
plt.annotate('A',(x[0],y[0]))
plt.annotate('B',(x[1],y[1]))
plt.annotate('C',(x[2],y[2]))
plt.annotate('D',(x[3],y[3]))
plt.annotate('E',(x[4],y[4]))
plt.annotate('F',(x[5],y[5]))

plt.plot([1,3],[1,2])
plt.plot([1,2],[1,4])
plt.plot([3,5],[2,3])
plt.plot([2,4],[4,6])
plt.plot([2,5],[4,3])
plt.plot([4,6],[6,6])
plt.plot([3,4],[2,6])
plt.plot([5,6],[3,6])

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

g1.gbfs(A,F)

g1.printPath(F.name)

g1.reset()

g1.a_star(A,F)

g1.printPath(F.name)

g1.printGraph2()

''')

search()