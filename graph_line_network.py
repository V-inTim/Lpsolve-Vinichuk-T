import random
import lpsolve55 as lp
import json


class GraphNetwork:
    def __init__(self):
        self.__edges, self.__vertiсes, self.__weights = [], [], []

    def genGraph(self):
        self.__edges.clear()
        self.__vertiсes.clear()
        self.__weights.clear()

        n = random.randint(4, 4)
        m = random.randint(3, 3)
        self.__vertiсes = [str(i) for i in range(1, n * m + 1)]

        for i in range(0, m):
            for j in range(i * n + 1, (i + 1) * n):
                self.__edges.append((j, j + 1))
                if j % n != 1:
                    if not (i == 0 or i == m - 1):
                        b = random.randint(-1, 2)
                        if b == 1 or b == -1:
                            self.__edges.append((j, j + b * n + 1))
                        elif b == 2:
                            self.__edges.append((j, j + n + 1))
                            self.__edges.append((j, j - n + 1))
                    else:
                        b = random.randint(0, 1)
                        if b:
                            self.__edges.append((j, j + (n if i == 0 else -n) + 1))

        for i in range(0, m):
            b = random.randint(1, 1)
            for j in range(1, b + 1):
                self.__vertiсes.append(str(len(self.__vertiсes) + 1))
                self.__edges.append((i * n + n, len(self.__vertiсes)))
        self.__vertiсes += ['s', 'd']

        for i in range(0, m):
            self.__edges.append(('s', i * n + 1))

        for i in range(n * m + 1, len(self.__vertiсes) - 1):
            self.__edges.append((i, 'd'))

        for i in range(0, len(self.__edges)):
            self.__weights.append(random.randint(5, 30))

    def getEdges(self):
        return self.__edges

    def getVertiсes(self):
        return self.__vertiсes

    def lpSolve(self):
        edge_names = ['E' + str(ed[0]) + ',' + str(ed[1]) for ed in self.__edges]

        dlp = lp.lpsolve('make_lp', 0, len(self.__edges))
        lp.lpsolve('set_verbose', dlp, 'IMPORTANT')

        for i in range(len(edge_names)):
            lp.lpsolve('set_col_name', dlp, i + 1, edge_names[i])

        lp.lpsolve('set_obj_fn', dlp,
                   [1 if ed[0] == 's' else 0 for ed in self.__edges])
        lp.lpsolve('set_maxim', dlp)

        for i in range(1, len(self.__vertiсes) - 1):
            coe = []
            for ed in self.__edges:
                if ed[0] == i:
                    coe.append(-1)
                elif ed[1] == i:
                    coe.append(1)
                else:
                    coe.append(0)
            lp.lpsolve('add_constraint', dlp, coe, 'EQ', 0.0)

        for i in range(len(self.__edges)):
            lp.lpsolve('set_upbo', dlp, i + 1, self.__weights[i])

        lp.lpsolve('write_lp', dlp, 'task2.lp')
        lp.lpsolve('solve', dlp)
        self.__task_result = str(lp.lpsolve('get_objective', dlp))
        lp.lpsolve('delete_lp', dlp)

        return self.__task_result

    def saveGraph(self, name_file):

        graph = {
            "vertiсes": self.__vertiсes,
            "edges": self.__edges,
            "weights": self.__weights
        }

        graph_json = json.dumps(graph)

        with open(name_file, "w") as my_file:
            my_file.write(graph_json)

    def readGraph(self, name_file):
        with open(name_file, "r") as my_file:
            graph_json = my_file.read()

        graph = json.loads(graph_json)
        self.__vertiсes = graph["vertiсes"]
        self.__edges = graph["edges"]
        self.__weights = graph["weights"]
