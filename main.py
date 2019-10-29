from Graph import Graph



if __name__ == '__main__':
    my_graph = Graph()

    start_ver = "start"
    end_ver = "finish"
    #creatinh vertexs
    my_graph.add_vertex(start_ver, 0)
    my_graph.add_vertex(end_ver, 0)
    my_graph.add_vertex('b', 5)
    my_graph.add_vertex('c', 6)
    my_graph.add_vertex('d', 12)
    my_graph.add_vertex('temp', 2)
    my_graph.add_vertex('isolated', 89)

    my_graph.add_edge(start_ver, 'b')
    my_graph.add_edge(start_ver, 'd')
    my_graph.add_edge('b', 'c')
    my_graph.add_edge('c', 'isolated')
    my_graph.add_edge('c', end_ver)
    my_graph.add_edge('d', 'temp')
    my_graph.add_edge('temp', end_ver)

    # print the graph:
    print(my_graph)

    # removing temp vertex
    my_graph.remove_edge('temp')
    print("print the graph after delete temp vertex \n")
    print(my_graph)
    print("\n")

    isolated_ver = my_graph.find_isolate()
    print("the isolated vertexs: \n")
    print(isolated_ver)
    print("\n")
    empty_temp = []

    # find all path in graph from start to finish
    all_pathes = my_graph.find_all_paths(start_ver, end_ver, empty_temp)

    # before finding critical path have to check if have a cycle
    # for now there is no cycle
    graph_simple = my_graph.get_graph_simplified()
    cycles = [[node] + path for node in graph_simple for path in my_graph.dfs(graph_simple, node, node)]
    is_cycle = my_graph.check_cycle(cycles)

    # finding critical path
    critical_path = my_graph.find_critical_path(all_pathes, is_cycle)
    print("the critical path: \n")
    print(critical_path)
    print("\n")

    time_slack = my_graph.slack_time(start_ver, end_ver, is_cycle)
    print("the slack time without critical path vertexs: \n")
    print(time_slack)
    print("\n")

    print("the project time is : %s" % (my_graph.project_duration))
    print("\n")

    # create cycle
    my_graph.add_vertex('cycle_x', 1)
    my_graph.add_vertex('cycle_y', 1)
    my_graph.add_edge('b', 'cycle_x')
    my_graph.add_edge('cycle_x', 'cycle_y')
    my_graph.add_edge('cycle_y', 'b')

    # finding cycle in graph
    graph_simple = my_graph.get_graph_simplified()
    cycles = [[node] + path for node in graph_simple for path in my_graph.dfs(graph_simple, node, node)]
    is_cycle = my_graph.check_cycle(cycles)
    print("the cycle paths : \n")
    print(cycles)
