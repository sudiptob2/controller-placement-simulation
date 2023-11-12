import graph_mixin

if __name__ == '__main__':
    graph_raw = ['network1', 'network2']
    for i in range(len(graph_raw)):
        file_name = graph_raw[i]+'.txt'
        gm = graph_mixin.GraphMixin(file_name)
        gm.visualize()