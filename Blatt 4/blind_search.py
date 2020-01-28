import os
from collections import deque


# The environments.
blatt3 = "blatt3_environment.txt"
blatt4a = "blatt4_environment_a.txt"  # Environment without a solution.
blatt4b = "blatt4_environment_b.txt"
blatt4c = "blatt4_environment_c.txt"  # Environment favoring BFS.
blatt4d = "blatt4_environment_d.txt"  # Environment favoring DFS.


# Splits a string into a list of its characters.
def split(word):
    return [char for char in word]


# Transforms the maze to an array,
# replacing spaces with 0s for better handling.
def create_maze():
    # TODO: Select environment to use!
    with open(blatt3, "r") as f:
        maze = [split(line.replace(" ", "0").strip("\n")) for line in f]
    return maze


# Searches for the coordinates of a node in the maze.
def find(maze, char):
    for row in maze:
        if char in row:
            return [[maze.index(row), row.index(char)]]


# Saves the maze to file again.
def save_to_file(maze, env):
    # Appends the maze to the text file, first removing blanks and then replacing 0s with blanks again.
    with open(env, "a", encoding="utf-8") as f:
        for line in maze:
            f.write(" ".join(line).replace(" ", "").replace("0", " ") + "\n")
        f.write("\n")


# Finds the neighbors of a node in the maze.
def get_neighbors(maze, node, visited):
    # Lists potential neighbors in order: up, right, down, left.
    potential_neighbors = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    # Neighbors that aren't an "x" or already visited.
    reachable_neighbors = []

    # Filters for reachable neighbors according to the properties.
    for pn in potential_neighbors:
        y = node[0]+pn[0]
        x = node[1]+pn[1]
        if maze[y][x] != "x" and not (y, x) in visited:
            reachable_neighbors += [[y, x]]

    return reachable_neighbors


# Marks the path with the direction taken for the next step.
def mark_path(maze, path):
    # Enumerates over all nodes in the path.
    for i, yx in enumerate(path):
        # Gets successor
        if i < len(path) - 1:
            next_xy = path[i + 1]
            # If node isn't start, goal or a portal,
            # mark it with the direction.
            if maze[yx[0]][yx[1]] == "+":
                direction = [next_xy[0] - yx[0], next_xy[1] - yx[1]]
                if direction == [-1, 0]:
                    maze[yx[0]][yx[1]] = "▲"
                elif direction == [0, 1]:
                    maze[yx[0]][yx[1]] = "►"
                elif direction == [1, 0]:
                    maze[yx[0]][yx[1]] = "▼"
                else:
                    maze[yx[0]][yx[1]] = "◄"


# Breadth-first search
def bfs():
    maze = create_maze()

    # Gets start node, queue for nodes/paths to check,
    # visited for already visited nodes and portals for portals.
    start = find(maze, "s")
    queue = deque([start])
    visited = set()
    portals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Remove the previous environment text before appending.
    env = "bfs_environment.txt"
    if os.path.exists(env):
        os.remove(env)

    # While the queue isn't empty, check all neighbors of the current node,
    # add them to the queue and add the current node to visited.
    # Repeat until the goal is found or there are no further nodes to check.
    while queue:
        # FIFO queue, so pop first element.
        path = queue.popleft()
        node = path[-1]

        # Marks visited nodes with a plus.
        if maze[node[0]][node[1]] not in ["s", "g"]:
            # Teleports from one number to the other.
            # Saves the portal number, overwrites it to find the other one,
            # restores the number of the first portal
            # and sets the node's position to that of the second portal.
            if maze[node[0]][node[1]] in portals:
                portal = maze[node[0]][node[1]]
                maze[node[0]][node[1]] = "0"
                pos = find(maze, str(portal))[0]
                maze[node[0]][node[1]] = portal
                node = pos

            if maze[node[0]][node[1]] == "0":
                maze[node[0]][node[1]] = "+"

        # If current node equals goal node,
        # print the path, mark it in the environment and add it into the text file.
        # Otherwise, go through the neighbors, add them to the path,
        # add the resulting path to the queue, add the current node to visited nodes
        # and add the environment to the text file.
        if maze[node[0]][node[1]] == "g":
            print("Found BFS path: ")
            mark_path(maze, path)
            save_to_file(maze, env)
            return str(path) + "\n"
        else:
            for n in get_neighbors(maze, node, visited):
                if n not in path and (node[0], node[1]) not in visited:
                    new_path = path + [n]
                    queue.append(new_path)

        visited.add((node[0], node[1]))
        save_to_file(maze, env)

    return "No BFS path found :(" + "\n"


# Depth-first search
def dfs():
    maze = create_maze()

    start = find(maze, "s")
    queue = deque([start])
    visited = set()
    portals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    env = "dfs_environment.txt"
    if os.path.exists(env):
        os.remove(env)

    while queue:
        # FILO queue, so pop last element.
        path = queue.pop()
        node = path[-1]

        if maze[node[0]][node[1]] not in ["s", "g"]:
            if maze[node[0]][node[1]] in portals:
                portal = maze[node[0]][node[1]]
                maze[node[0]][node[1]] = "0"
                pos = find(maze, str(portal))[0]
                maze[node[0]][node[1]] = portal
                node = pos

            if maze[node[0]][node[1]] == "0":
                maze[node[0]][node[1]] = "+"

        if maze[node[0]][node[1]] == "g":
            print("Found DFS path: ")
            mark_path(maze, path)
            save_to_file(maze, env)
            return str(path) + "\n"
        else:
            # Reverses neighbor list to have priorities in the correct order for DFS
            for n in reversed(get_neighbors(maze, node, path)):
                if n not in path and (node[0], node[1]) not in visited:
                    new_path = path + [n]
                    queue.append(new_path)

        visited.add((node[0], node[1]))
        save_to_file(maze, env)

    return "No DFS path found :(" + "\n"


print(bfs())
print(dfs())
