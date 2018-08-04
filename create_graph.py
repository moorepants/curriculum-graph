from textwrap import wrap

import yaml
import networkx
from networkx.drawing.nx_agraph import to_agraph

COLORSCHEME = 'paired12'
NODE_WIDTH = 0.5

with open('courses.yml') as f:
    courses = yaml.load(f)

graph = networkx.DiGraph()

graph.graph['graph'] = {
                        'splines': True,
                        'ranksep': 1.6,
                        'nodesep': 0.8,
                        'rankdir': 'LR',
                        'rank': 'min',
                        'ratio': 1.0,
                       }
graph.graph['node'] = {
                       'shape': 'square',
                      }

group_colors = {}
group_color_nums = [str(n) for n in range(20, 0, -1)]

for course, data in courses.items():
    group = data['group']
    if group not in group_colors:
        group_colors[group] = group_color_nums.pop()

for course, data in courses.items():

    prereqs = data['prereqs']

    group = data['group']

    if data['title'] is not None:
        title = '\n' + '\n'.join(wrap(data['title'], width=20))
    else:
        title = ''

    # Strictly required courses should have thick solid edges. Courses where
    # the students has a choice between more than one option for the
    # requirement should be thick dashed edges. Courses that are not required
    # are thin solid edges.
    if data['required'] is not None and 'EME' in data['required']:
        graph.add_node(course, penwidth=10, style='filled',
                       colorscheme=COLORSCHEME, fillcolor=group_colors[group],
                       label=course + title, width=NODE_WIDTH)
    elif data['required-choice'] is not None and 'EME' in data['required-choice']:
        graph.add_node(course, penwidth=10, style='filled,dashed',
                       colorscheme=COLORSCHEME, fillcolor=group_colors[group],
                       label=course + title, width=NODE_WIDTH)
    else:
        graph.add_node(course, label=course + title, width=NODE_WIDTH)

    if prereqs is not None:
        for prereq in prereqs:
            if 'or' in prereq:  # set of choices
                choices = [p.strip() for p in prereq.split('or')]
                for choice in choices:
                    if choice not in graph:
                        graph.add_node(choice, width=NODE_WIDTH)
                    try:
                        color = group_colors[courses[choice]['group']]
                    except KeyError:
                        color = 'black'
                    graph.add_edge(choice, course, colorscheme=COLORSCHEME,
                                   penwidth=5, style='dashed', arrowsize=2,
                                   color=color)
            else:
                if prereq not in graph:
                    graph.add_node(prereq, width=NODE_WIDTH)
                graph.add_edge(prereq, course, penwidth=5, arrowsize=2)

graphviz_graph = to_agraph(graph)
graphviz_graph.layout('dot')
graphviz_graph.draw('eme-curriculum-map.png')

print('Longest path in the graph:')
print(networkx.algorithms.dag.dag_longest_path(graph))

print('Courses sorted by number of prerequisites.')
# TODO : Need to account for choice prereqs.
for course, num in sorted(dict(graph.in_degree()).items(), key=lambda kv: kv[1]):
    print('{}: {}'.format(course, num))

print('Courses sorted by number of courses that depend on them.')
for course, num in sorted(dict(graph.out_degree()).items(), key=lambda kv: kv[1]):
    print('{}: {}'.format(course, num))
