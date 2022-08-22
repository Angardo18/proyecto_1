from graph.Graph import Graph

sources = [1, 2, 3, 0, 5, 1, 1, 3]
targets = [0, 0, 0, 5, 0, 2, 3, 1]
weights = [2, 2, 4, 1, 1, 3, 2, 2]

graph = Graph(sources, targets, weights)
graph.print_r()
graph.draw(with_weight=False)