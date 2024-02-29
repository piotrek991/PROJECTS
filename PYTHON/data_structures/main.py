import networkx as nx
import matplotlib.pyplot as plt


aggraph = nx.Graph()

graph = {'A': ['B', 'C'],
'B': ['A', 'C', 'D'],
'C': ['A', 'B', 'D', 'E'],
'D': ['B', 'C', 'E', 'F'],
'E': ['C', 'D', 'F'],
'F': ['D', 'E']}
 
for node in graph:
    aggraph.add_node(node)
    for edge in graph[node]:
        aggraph.add_edge(node,edge)

pos = { 'A': [0.00, 0.50], 'B': [0.25, 0.75],
'C': [0.25, 0.25], 'D': [0.75, 0.75],
'E': [0.75, 0.25], 'F': [1.00, 0.50]}

nx.draw(aggraph,pos, with_labels=True)
nx.draw_networkx(aggraph,pos)
plt.show()