#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# girvan-newman.py - LibreSoft, July 2015

"""
A different implementation of the Girvan-Newman algorithm
to detect subcommunities in a given graph.
"""

import csv
import networkx as nx
import sys
import os
import matplotlib.pyplot as plt

usage = "python net.py <input_graph.csv>"


class GN:
    """
    Main class
    """

    def __init__(self):
        """
        Initial values for program variables
        """
        self.dicc_nodes = {}
        self.viewed_lines = {}
        self.data_final = open('info-out.csv', 'w')
        self.data_final.close()
        self.data_final = open('info-out.csv', 'a')
        self.temp_counter = 0
        self.count = 0
        self.tri_format = False
        self.g = nx.Graph()

    def check_startup(self):
        """
        Checks if the program can run properly with the given arguments
        """
        input_opt = sys.argv
        if len(input_opt) != 2:
            print usage
            raise SystemExit
        else:
            try:
                filename = input_opt[1]
                node_file = open(filename, 'r')
                self.lines_node = node_file.readlines()
                node_file.close()
            except IOError:
                print "Check input file"
                print usage
                raise SystemExit

    def my_draw(self, g):
        """
        Draws a given graph with many specified options
        """
        elarg = [(u, v) for (u, v, d)
                 in g.edges(data=True) if d['weight'] > 0.5]
        esmall = [(u, v) for (u, v, d)
                  in g.edges(data=True) if d['weight'] <= 0.5]

        pos = nx.nx.spring_layout(g)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(g, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(g, pos, edgelist=elarg,
                               width=6)
        nx.draw_networkx_edges(g, pos, edgelist=esmall,
                               width=6, alpha=0.5, edge_color='b',
                               style='dashed')

        # labels
        nx.draw_networkx_labels(g, pos, font_size=20, font_family='sans-serif')

        plt.axis('off')
        # plt.savefig("weighted_graph.png") # save as png
        plt.show()  # display

    def build_graph(self):
        """
        Builds a graph from a given CSV file, looking first at the kind of
        graph (If it is weighed o not)
        """

        ex_line = self.lines_node[0].split(',')
        if len(ex_line) == 3:
            tri_format = True

        for node in self.lines_node:

            if node not in self.viewed_lines.keys():
                self.viewed_lines[node] = 1
            else:
                self.temp_counter = self.viewed_lines[node]
                self.temp_counter += 1
                self.viewed_lines[node] = self.temp_counter

            nodes = node.split(",")
            node1 = nodes[0]
            node2 = nodes[1]
            if node1 not in self.dicc_nodes.keys():
                self.dicc_nodes[node1] = 1
            else:
                self.counter = self.dicc_nodes[node1]
                self.counter += 1
                self.dicc_nodes[node1] = self.counter

            if node2 not in self.dicc_nodes.keys():
                self.dicc_nodes[node2] = 1
            else:
                self.counter = self.dicc_nodes[node2]
                self.counter += 1
                self.dicc_nodes[node2] = self.counter

        g = nx.Graph()

        list_nodes = self.dicc_nodes.keys()

        for node in self.viewed_lines.keys():
            nodes = node.split(",")
            node1 = nodes[0]
            node2 = nodes[1]
            if tri_format:
                g.add_edge(node1, node2, weight=float(nodes[2]))
            else:
                g.add_edge(node1, node2[:-1], weight=float(viewed_lines[node]))

        return g

    def graphic_girvan_newman(self, g):
        """
        Main algorithm that iterates in the builded graph and plotting
        the result in each iteration
        """
        copyg = g
        dicc2 = {}
        num = 0
        while nx.number_of_edges(copyg) > 0:
            print nx.number_of_edges(copyg)
            new_g = nx.edge_betweenness(copyg)
            dicc2 = {}
            list_g = []
            for edge in new_g.keys():
                num = str(new_g[edge])
                num_list = num.split(".")
                num2 = num_list[1]
                if len(num2) > 12:
                    num2 = num2[:11]
                newnum = str(num_list[0]) + "." + str(num2)
                dicc2[edge] = float(newnum)
                list_g.append(dicc2[edge])

            maxvalue = 0.0
            for value in list_g:
                if float(value) > float(maxvalue):
                    maxvalue = float(value)

            maxedge = ""
            for edge in dicc2.keys():
                if (dicc2[edge] == maxvalue):
                    maxedge = edge
            print maxedge
            node1 = maxedge[0]
            node2 = maxedge[1]
            copyg.remove_edge(*maxedge)  # Unpacks edge tuple
            self.my_draw(copyg)


if __name__ == "__main__":

    print "Starting 'girvan-newman.py'..."
    my_gn = GN()
    my_gn.check_startup()
    my_gn.g = my_gn.build_graph()
    my_gn.my_draw(my_gn.g)
    my_gn.graphic_girvan_newman(my_gn.g)
    my_gn.data_final.close()
    print "End of 'girvan-newman.py'"
