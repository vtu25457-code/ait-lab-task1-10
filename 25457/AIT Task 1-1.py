def dfs(graph, start):
    stack, visited = [start], set()
    print("DFS:", end=" ")
    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    print()
graph = {
    4: [5, 6],
    5: [4, 7, 8],
    6: [4, 9],
    7: [5],
    8: [5, 9],
    9: [6, 8]
}
dfs(graph, 4)