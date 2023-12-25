# This is a sample Python script.
import graph_network as gn
import graph_line_network as gln

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gr_lnet = gln.GraphNetwork()
    print(gr_lnet.getEdges())
    res = gr_lnet.lpSolve()
    print(res)

    gr_lnet.saveGraph("graph_task2.json")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
