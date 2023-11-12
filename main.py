import graph_mixin

if __name__ == '__main__':
    graph_raw = ['network1.txt', 'network2.txt']
    for i in range(len(graph_raw)):
        file_name = graph_raw[i]
        gm = graph_mixin.GraphMixin(file_name)
        gm.visualize()