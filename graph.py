import queue


def bfs(start_vertex, graph):
    queue_ = queue.Queue()
    queue_.put_nowait(start_vertex)
    was = list(False for x in range(len(graph)))
    was[start_vertex] = True
    distance = list("Inf" for x in range(len(graph)))
    distance[start_vertex] = 0

    while not queue_.empty():
        vertex = queue_.get_nowait()
        for incidence_vertex in graph[vertex]:
            if not was[incidence_vertex]:
                was[incidence_vertex] = True
                distance[incidence_vertex] = distance[vertex] + 1
                queue_.put_nowait(incidence_vertex)

    return distance


def dfs_step(vertex, graph, was):
    was[vertex] = True
    for incidence_vertex in graph[vertex]:
        if not was[incidence_vertex]:
            dfs_step(incidence_vertex, graph, was)


def dfs(graph):
    was = list(False for x in range(len(graph)))
    for vertex in range(len(graph)):
        dfs_step(vertex, graph, was)


def main():
    graph = dict()
    in_file = open("input.txt")
    number_of_vertices = int(in_file.readline())
    for x in range(number_of_vertices):
        vertex_id = x
        incidence_tuple = tuple(int(x) for x in in_file.readline().split())
        graph[vertex_id] = incidence_tuple

    dfs(graph)
    distance = bfs(0, graph)
    print(distance)


if __name__ == '__main__':
    main()