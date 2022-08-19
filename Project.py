''' 
Max Flow Algorithms

Made by: Rehab, Ekram, Reem, Fadyah
Date: May 2022

'''

import copy # to make residual graph 
import time # to make sleep in the animation
from tkinter import * # for GUI


# ----------------------- Ford-Fulkerson Algorithm ----------------------------

# return the path from source to sink if exist using DSF
def DFS(graph, residualGraph, source, sink): # O(V^2)
    
    stack = [source] # O(1)
    paths = {source:[]} # O(1)    
    
    while stack: # O(V)
        
        u = stack.pop() # O(1)  
  
        for v in range(len(graph)): # O(V)
            if graph[u][v] - residualGraph[u][v] > 0  and v not in paths: # O(1)
                
                paths[v] = paths[u] + [(u,v)]
               
                if v == sink: # O(1)                                        
                    return paths[v]                
                
                stack.append(v) # O(1)             
                        
    return None


def Ford_Fulkerson(graph, source, sink): # O(V^2 * len(path))
    
    # construct the residual graph than contains the residual capaciy
    residualGraph = [[0] * len(graph) for i in range(len(graph))] # O(V)   
    
    path = DFS(graph, residualGraph, source, sink) # O(V^2)
    
    while path != None: # O(P + V^2)
        colorPath(path) # O(P)
        flow = min(graph[u][v] - residualGraph[u][v] for u,v in path) # O(P)
        
        for u, v in path: # O(P)
            residualGraph[u][v] += flow 
            residualGraph[v][u] -= flow            
            lines[u][v].updateCapacity(graph[u][v] - flow)
            
        clearPath(path) # O(P)
        
        path = DFS(graph, residualGraph, source, sink) # O(V^2)
        
    return sum(residualGraph[source][i] for i in range(len(graph)))

# ------------------------ Edmonds-Karp Algorithm -----------------------------

# Return True if there is node that has not iterated.
def bfs(graph, s, t, parent): # O(V^2)
    
    # Mark all the vertices as not visited
    visited = [False] * len(graph) # O(1)
    
    queue = []  # Create a queue for BFS   # O(1)
    
    # Mark the source node as visited and enqueue it
    queue.append(s) # O(1)
    visited[s] = True # O(1)
 
    # Standard BFS Loop
    while queue: # queue not empty  # O(V^2)
        u = queue.pop(0) # Dequeue a vertex from queue and print it # O(1)
       
        for ind in range(len(graph[u])): # O(V)         
            
            if not visited[ind] and graph[u][ind] > 0: # O(1)
                queue.append(ind) # O(1)
                visited[ind] = True # O(1)
                parent[ind] = u # O(1)
  
    return visited[t]  # O(1) 


# Returns the maximum flow from s to t in the given graph 
def Edmonds_Karp(graph, source, sink):
    
    # This array is filled by BFS and to store path    
    parent = [-1] * (len(graph))  # make parent of all vertix -1  # O(1)   
    residualGraph = copy.deepcopy(graph) # O(V^2)
    max_flow = 0 # There is no flow initially   # O(1)  
    
    # Augment the flow while there is path from source to sink
    while bfs(residualGraph, source, sink, parent): # O(V^2)        
       
        path_flow = float("Inf")   # O(1)       
        s = sink # O(1)      
        path = [] # to color it  # O(1)  
        
        while s != source: # O(P)
            # stort path to color it
            path.append((parent[s], s))    # O(1)        
            # Find the minimum value in select path            
            path_flow = min(path_flow, residualGraph[parent[s]][s])  # O(1)             
            s = parent[s]  # O(1)        
        
        colorPath(path) # O(P)
        
        # Add path flow to overall flow
        max_flow += path_flow  # O(1)
        
        # update residual capacities of the edges  and reverse edges        
        v = sink
        while v != source: # O(P)
            u = parent[v]  # O(1)
            residualGraph[u][v] -= path_flow  # O(1)
            residualGraph[v][u] += path_flow  # O(1)
            lines[u][v].updateCapacity(residualGraph[u][v])  # O(1)
            v = parent[v]   # O(1)      
            
        clearPath(path) # O(P)
   
    return max_flow # O(1)
    
# --------------------------- Dinic Algorithm ---------------------------------

# assigns levels to nodes.
def BFS(residualGraph, source, sink): # O(V^2)
   
    level = [-1 for i in range(len(residualGraph))]  # O(V)
    
    level[source] = 0  # O(1)    
    queue = [source]   # O(1)     

    while queue: # O(V^2) 
       
        u = queue.pop(0)   # O(1)     
        
        # the neighbors of u
        for v in range(len(residualGraph)):  # O(V)  
            if u != v and level[v] < 0 and residualGraph[u][v] > 0:    # O(1)               
                level[v] = level[u] + 1;  # Level v is parent level + 1  # O(1)  
                queue.append(v)   # O(1)       
   
    return level # O(1)  

paths_D = {0: []} # it well filled by sendFlow function to color the path

# find the max flow in the current path using DFS
def sendFlow(residualGraph, level, count, u, sink, flow): # O(V * P)        
   
    if u == sink:  # O(1)  
        return flow   # O(1)   
    
    if count[u] == len(residualGraph):  # O(1)  
        return 0  # O(1)  
    
    for v in range(len(residualGraph)): # O(V)   
        
        if residualGraph[u][v] > 0: # O(1)  
            
            count[u] = count[u] + 1  # O(1)
            
            if level[v] == (level[u] + 1):    # O(1)                       
                curr_flow = min(flow, residualGraph[u][v])  # O(1)
                paths_D[v] = paths_D[u] + [(u,v)] # need this path to color # O(1)
                min_cap = sendFlow(residualGraph, level, count, v, sink, curr_flow) # O(P)
            
                if min_cap > 0:  # O(1)                 
                    residualGraph[u][v] -= min_cap # O(1)
                    residualGraph[v][u] += min_cap # O(1)                                                
                    return min_cap  # O(1)               
    return 0 # O(1)
	
 
def Dinic(graph, source, sink): 
    
    if source == sink: # O(1)  
        return -1

    max_flow = 0; # O(1)  
    residualGraph = copy.deepcopy(graph) # O(V^2)       

    # Augment the flow while there is path from source to sink
    while True:
        level = BFS(residualGraph, source, sink) # O(V^2)  
        
        # if sink level of sink doesn`t upedated, this means no path
        if level[sink] < 0: # O(1) 
            break
        colorLevel(level) # O(V) 
        # store how many neighbors are visited
        count = [0 for i in range(len(graph))] # O(V)       

        # while flow is not zero in graph from source to sink    
        while True:
            
            flow = sendFlow(residualGraph, level, count, source, sink, float('inf'))
                      
            if flow == 0:
                clearPath(paths_D[sink]) # O(P) 
                break
           
            colorPath(paths_D[sink]) # O(P)
            updatePathCapacity(residualGraph, paths_D[sink]) # O(P)
            max_flow += flow            
            clearPath(paths_D[sink])   # O(P) 
            
    return max_flow    
       
# ------------------- Some needed class for GUI -------------------------------
        
class Node:
    
    radius = 15       
    
    def __init__(self, x, y, value):
        self.Xcenter = x
        self.Ycenter = y
        self.circle = None  
        self.text = str(value)        
        
    def draw(self):
        # The points are left-top, right-bottom
        self.circle = canvas.create_oval(self.Xcenter - self.radius, 
                                        self.Ycenter - self.radius, 
                                        self.Xcenter + self.radius,
                                        self.Ycenter + self.radius, 
                                        fill= '#87a0fc', width= 1)        
        canvas.create_text(self.Xcenter, self.Ycenter, 
                           text= self.text, font=('ATC Pine Heavy', 13))
              
    def color(self):
        canvas.itemconfig(self.circle, fill='#f44068')
        
    
    def reColor(self):
        canvas.itemconfig(self.circle, fill='#87a0fc')
        
        
    def colorBlue(self):
        canvas.itemconfig(self.circle, fill= 'blue')
        
    def isColorBlue(self):
        return canvas.itemcget(self.circle, 'fill') == 'blue'
    
#------------------------------------------------------------------------------

class Line:
    def __init__(self, u, v, capacity):
        self.line = canvas.create_line(u.Xcenter, u.Ycenter, 
                                        v.Xcenter, v.Ycenter,
                                        width= 3, arrow= LAST, 
                                        arrowshape= (20, 25, 3))
        
        # determine the middle point of line, and slightly raise it 
        capacityPoistion = [(u.Xcenter + v.Xcenter) / 2,
                        (u.Ycenter + v.Ycenter) / 2 - 10] 
        
        # if line is Horizontal, slightly left it and down it
        if u.Xcenter ==  v.Xcenter: 
            capacityPoistion[0] -= 10
            capacityPoistion[1] += 10        
       
        # represent the capacity as text
        self.capacity = canvas.create_text(capacityPoistion, 
                                            fill= 'blue', 
                                            text= str(capacity),
                                            font=('Arial', 10))        
    
    def color(self):
        canvas.itemconfig(self.line, fill='#f44068')        
        
    def reColor(self):
        canvas.itemconfig(self.line, fill='black')        
        canvas.itemconfig(self.capacity, fill='blue')
        
    def updateCapacity(self, newValue):
        canvas.itemconfig(self.capacity, text= str(newValue))  
        if newValue == 0:
            self.flipArrowToFirt()
        
    def colorCapacity(self):
        canvas.itemconfig(self.capacity, fill='#f44068')    
        
    def flipArrowToFirt(self):
        canvas.itemconfig(self.line, arrow= FIRST, dash=(1, 1))  
        
    def flipArrowtoLast(self):
        canvas.itemconfig(self.line, arrow= LAST, dash= ())  
    
    # compare the capacity
    def isEqual(self, value):
        return canvas.itemcget(self.capacity, 'text') == value
    
    def isFlipped(self):
        return canvas.itemcget(self.line, 'arrow') == FIRST
 
# ---------------------- Some Function needed in GUI --------------------------

def drawGraph():    
    
    nodesG[0] = Node(80, 280, "s")     
    nodesG[4] = Node(150, 180, 4)
    nodesG[15] = Node(150, 390, 15)
    
    value = 1  
    for y in range(110, 490, 70):      
        for x in range(250, 620, 140):  
            if value == 4 or value == 15 or value == 8 or value == 19:
                value += 1           
            nodesG[value] = Node(x, y, value)                      
            value += 1 
    
    nodesG[8] = Node(630, 180, 8)
    nodesG[19] = Node(630, 390, 19)    
    nodesG[23] = Node(700, 280, "t")
    
    
    # draw the edges
    for i in range(len(theGraph)):
        for j in range(len(theGraph)):
            if theGraph[i][j] != 0:                
                lines[i][j] = Line(nodesG[i], nodesG[j], theGraph[i][j])
    
    # draw the verteces     
    for node in nodesG:
        node.draw()
        
        
maxFlowLabel = None

# the path will be a list of tuples [(u1, v1), (u2, v2), ...] 
def colorPath(path):     
    for u, v in path:
        nodesG[u].color()
        lines[u][v].color()
        
    nodesG[sink].color()    
    
    window.update() 
    time.sleep(1)       
    
def clearPath(path):    
    for u, v in path:
        nodesG[u].reColor()
        lines[u][v].reColor()
    nodesG[sink].reColor() 
    

def updatePathCapacity(residualGraph, path):         
    for u, v in path:       
        lines[u][v].updateCapacity(residualGraph[u][v])   
        

def colorLevel(level):
    for i in range(len(theGraph)):
        if level[i] != -1 and level[i] % 2 == 0:
            nodesG[i].colorBlue()       
   
    window.update() 
    time.sleep(1)  
    
def originGraph():
    maxFlowLabel.config(text= " ")  
    for i in range(len(theGraph)):
        
        if nodesG[i].isColorBlue():
            nodesG[i].reColor()
            
        for j in range(len(theGraph)):
            if theGraph[i][j] != 0: 
                if not lines[i][j].isEqual(theGraph[i][j]):                
                    lines[i][j].updateCapacity(theGraph[i][j])  
                    
                if lines[i][j].isFlipped():
                    lines[i][j].flipArrowtoLast()
                
    
    
def display(event):    
    canvas.delete(background, title, text)      
    drawGraph()       
       
    Button(canvas, 
            text= "Ford Fulkerson Algorithm",            
            bg= '#f98ba2',
            font=('Times', 10), 
            command= Ford_Fulkerson_Algorithm).place(x=50, y = 530)
       
    Button(canvas, 
            text= "Edmond-Karp Algorithm",            
            bg= '#f98ba2',
            font=('Times', 10), 
            command= Edmonds_Karp_Algorithm).place(x=250, y = 530)       
       
    Button(canvas, 
            text= "Dinic Algorithm",            
            bg= '#f98ba2',
            font=('Times', 10), 
            command= Dinic_Algorithm).place(x=450, y = 530)
   
    Button(canvas, 
            text= "Origenal Graph",            
            bg= '#f44068',
            font=('Times', 10), 
            command= originGraph).place(x= 600, y= 530)
   
    Label(canvas, font=('Times', 12, 'bold'), bg="#D3e0ff",
          text= 'The Max Flow is: ').place(x= 310, y = 30)   
   
    global maxFlowLabel
    maxFlowLabel = Label(canvas, font=('Times', 12, 'bold'), bg="#D3e0ff",
                         fg= "#015bfa", text= ' ')
    maxFlowLabel.place(x=440, y = 30)   

                
# The applied algrothm
def Ford_Fulkerson_Algorithm():    
    originGraph()    
    maxFlow = Ford_Fulkerson(theGraph, source, sink)    
    maxFlowLabel.config(text= str(maxFlow))  
       
 
def Edmonds_Karp_Algorithm():   
    originGraph()    
    maxFlow = Edmonds_Karp(theGraph, source, sink)  
    maxFlowLabel.config(text= str(maxFlow))           
    
def Dinic_Algorithm(): 
    originGraph()  
    maxFlow = Dinic(theGraph, source, sink)    
    maxFlowLabel.config(text= str(maxFlow))      

    
#--------------------------------- main ---------------------------------------
    
# The graph of 23 nodes to apply the algorithims 
theGraph = [
    [0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 5, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 6, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 7, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
 
source, sink = 0, 23

# The GUT representaion of nodes and edges 
nodesG = [ None for i in range(len(theGraph)) ]
lines = [[None] * len(theGraph) for i in range(len(theGraph))]   


#--------------------------------- GUI ----------------------------------------

window = Tk()

# window size and position
window.geometry('800x600+0+0')

# window title
window.title("Max Flow Algorithms")

# window icon in titlebar
icon = PhotoImage(file= "icon.png")
window.iconphoto(False, icon) 

# create the canvas to draw shapes
canvas = Canvas(window,  bg= '#D3e0ff')
canvas.pack(expand=True, fill= 'both')

# introduction background
backgroundImage = PhotoImage(file= "background.png" )
background = canvas.create_image(0, 0, image= backgroundImage, anchor=NW)

# introduction title
title = canvas.create_text(400, 50, # text poistion from center
                           text='Max Flow Algorithms',
                           font=('Times', 30, 'bold'), 
                           fill='#f44068', # font color
                           justify= CENTER)

# user guid to start the program
text = canvas.create_text(400, 510, # text poistion from center
                           text='Press space to start',
                           font=('Times', 10), 
                           fill='gray', # font color
                           justify= CENTER)

# when press space key, the graph and program will start
window.bind("<space >", display)

window.mainloop()   
