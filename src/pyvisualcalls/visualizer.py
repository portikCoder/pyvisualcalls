import logging

from dataclasses import dataclass
from graphviz import Digraph, nohtml

from data_node_holder import DataStructure_ToHoldCallsAndCallees


def visualize_demo():
    dot = Digraph(comment='The Round Table')
    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')
    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')
    print(dot)
    dot.render('test-output/round-table.gv', view=True)


def visualize_demo_real_sample():
    dot = Digraph(comment='Real data')
    dot.node('main.py', 'Start of execution')
    dot.node('module_1', 'module_1.test_fnc_1(None)')
    dot.node('module_1', 'module_1.test_fnc_2(None)')
    dot.node('module_2', 'module_2.test_fnc_1(None)')
    # dot.edges(['mainpy:module_1', 'mainpy:module_2'])
    dot.edge('main.py', 'module_1')
    dot.edge('main.py', 'module_2')
    dot.edge('module_1', 'module_2')
    print(dot)
    dot.render('test-output/real-sample.gv', view=True)


if __name__ == '__main__':
    # visualize_demo()
    visualize_demo_real_sample()


class AutoCounter(object):
    def __init__(self, counter: int):
        self._counter = counter - 1

    @property
    def counter(self):
        self._counter += 1
        return self._counter


def visualize(project_name: str, calls_with_calees: DataStructure_ToHoldCallsAndCallees, view_only: bool = True):
    if not calls_with_calees:
        raise ValueError("Empty data cannot be visualized!")

    logging.info(f"Visualize ONLY files, with their functions/methods, of the project: {project_name}")
    dot = Digraph(name=project_name)
    dot = Digraph(name=project_name, node_attr={'shape': 'record', 'height': '.1'})

    # dot.attr('node', shape='box')
    cluster_counter = AutoCounter(0)
    for key, call_with_calee in calls_with_calees.modules.items():
        # functions = key + ':\t\t' + ';\t\n'.join([key for key, _ in call_with_calee.items()])
        join_counter = AutoCounter(0)
        path = key.replace("\\", "\\\\")
        functions = f'<f{join_counter.counter}> {path} |' + ' | '.join(
            [f"<f{join_counter.counter}> {key} " for key, _ in call_with_calee.items()])

        with dot.subgraph(name=f"cluster_{cluster_counter.counter}") as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            {c.node(name=key,label=key) for key in call_with_calee}
            # c.node(name=key, label=nohtml(functions))
            # c.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
            c.attr(label=path)
        # dot.node(name=key, label=nohtml(functions))

    out_f_name = f"{project_name}_graph.gv"
    out_path_w_file = f"out/{out_f_name}"
    logging.info(f"Visualization is done, outputting: {out_f_name}")

    if view_only:
        dot.view()
    else:
        dot.render(out_path_w_file, view=True)

    return None
