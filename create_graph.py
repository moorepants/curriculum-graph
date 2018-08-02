import yaml
import networkx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt
import pygraphviz as pgv

with open('courses.yml') as f:
    courses = yaml.load(f)

graph = networkx.DiGraph()

for course, prerequisites in courses.items():
    if course not in graph:
        graph.add_node(course)
    colors = ['orange', 'purple', 'green', 'blue', 'red']
    if prerequisites is not None:
        for prereq in prerequisites:
            if 'or' in prereq:  # set of choices
                choices = [p.strip() for p in prereq.split('or')]
                color = colors.pop()
                for choice in choices:
                    if choice not in graph:
                        graph.add_node(choice)
                    graph.add_edge(choice, course, style='dashed', color=color)
            else:
                if prereq not in graph:
                    graph.add_node(prereq)
                graph.add_edge(prereq, course)

#networkx.draw(graph, with_labels=True)

graph.graph['graph']={'rankdir':'TD'}
graph.graph['node']={'shape':'circle'}

A = to_agraph(graph)
A.layout('dot')
A.draw('abcd.png')
