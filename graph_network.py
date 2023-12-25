import random
import lpsolve55 as lp
import json


class GraphNetwork:
    def __init__(self):
        self.__edges, self.__weights, self.__vertiсes = [], [], []

    def genGraph(self):
        self.__edges.clear()
        self.__vertiсes.clear()
        self.__weights.clear()

        n = random.randint(4, 9)
        temp_list = list(range(1, n + 1))
        random.shuffle(temp_list)
        self.__vertiсes = ['s'] + temp_list + ['d']
        n += 2

        for i in range(0, n - 2):
            for j in range(i + 1, n - 1):
                self.__edges.append((self.__vertiсes[i], self.__vertiсes[j]))
            if i != n - 3:
                self.__edges.pop(len(self.__edges) - random.randint(1, n - 3 - i))
        self.__edges.append((self.__vertiсes[n - 2], self.__vertiсes[n - 1]))
        for i in range(1, n - 2):
            if random.randint(0, 1):
                self.__edges.append((self.__vertiсes[i], self.__vertiсes[n - 1]))
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
                   [1] * (len(self.__vertiсes) - 3) + [0] * (len(self.__edges) - len(self.__vertiсes) + 3))
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

        lp.lpsolve('write_lp', dlp, 'task1.lp')
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
