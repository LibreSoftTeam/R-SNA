#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import csv
import networkx as nx
import sys
import os
import matplotlib.pyplot as plt


node_file = open('test-graph2.csv', 'r')

dicc_nodes = {}

data_final = open('info-out.csv', 'w')
data_final.close()
data_final = open('info-out.csv', 'a')

viewed_lines = {}
temp_counter = 0

lines_node = node_file.readlines()
count = 0
dicc_nodes = {}
tri_format = False
ex_line = lines_node[0].split(',')

if len(ex_line) == 3:
    tri_format = True
    
    
for node in lines_node:

    if node not in viewed_lines.keys():
        viewed_lines[node] = 1
    else:
        temp_counter = viewed_lines[node]
        temp_counter += 1
        viewed_lines[node] = temp_counter
     
    nodes = node.split(",")
    node1 = nodes[0]
    node2 = nodes[1]
    if node1 not in dicc_nodes.keys():
        dicc_nodes[node1] = 1
    else:
        counter = dicc_nodes[node1]
        counter += 1
        dicc_nodes[node1] = counter

    if node2 not in dicc_nodes.keys():
        dicc_nodes[node2] = 1
    else:
        counter = dicc_nodes[node2]
        counter += 1
        dicc_nodes[node2] = counter


g = nx.Graph()

list_nodes = dicc_nodes.keys()

for node in viewed_lines.keys():
    nodes = node.split(",")
    node1 = nodes[0]
    node2 = nodes[1]
    if tri_format:
        g.add_edge(node1, node2, weight=float(nodes[2]))
    else:
        g.add_edge(node1, node2[:-1], weight=float(viewed_lines[node]))


print "==================\r\nNodes information: "
print g.nodes()
print "Degree:"
print nx.degree(g)
print "Density: "
print nx.density(g)

print "==================\r\nCentrality: "
print "Closeness Centrality: "
print nx.closeness_centrality(g)
print "Degree Centrality: "
print nx.degree_centrality(g)
print "Betweenness Centrality: "
print nx.betweenness_centrality(g)

print "Edge Betweenness: "
print nx.edge_betweenness(g)


nx.draw(g)

print "\r\nShowing graph... Close the window when you're done to finish"
plt.show()
data_final.close()
print "Fin del programa"
