from __future__ import division
import matplotlib.pyplot as plt
import networkx as nx
from model_3 import ClauseGraph


def do_something(node, node_string=None):
    if node_string:
        label = node_string
    else:
        label = node.cargo.tags[0]
    if not G.has_node(label):
        G.add_node(label)
    if node.parents:
        for parent in node.parents:
            G.add_edge(node_string, parent.cargo.tag[0])
            for daughter in node.daughters:
                do_something(daughter)


G = nx.Graph()
# Add nodes and edges
G.add_node("Head")
clause_graph = ClauseGraph()
do_something(clause_graph.head, "Head")
nx.draw(G, with_labels=True)
plt.savefig('labels.png')
nx.draw(G, with_labels=True)
