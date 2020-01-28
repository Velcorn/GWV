import os
from timeit import default_timer
from collections import deque

# The environments.
blatt3 = "blatt3_environment.txt"  # Standard
blatt4b = "blatt4_environment_b.txt"  # Portals
blatt5 = "blatt5_environment.txt"  # No path
blatt5b = "blatt5_environment_b.txt"  # More goals


# Splits a string into a list of its characters.
def split(word):
    return [char for char in word]


# Transforms the maze to an array,
# replacing spaces with 0s for better handling.
def create_maze():
    # TODO: Select environment to use!
    with open(blatt4b, "r") as f:
        maze = [split(line.replace(" ", "0").strip("\n")) for line in f]
    return maze


# Searches for the coordinates of a node in the maze.
def find(maze, char):
    for row in maze:
        if char in row:
            return [[maze.index(row), row.index(char)]]


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


# Saves the maze to file again.
def save_maze(maze, env):
    # Appends the maze to the text file, first removing blanks and then replacing 0s with blanks again.
    with open(env, "a", encoding="utf-8") as f:
        for line in maze:
            f.write(" ".join(line).replace(" ", "").replace("0", " ") + "\n")
        f.write("\n")


# Saves found path(s) to file.
def save_path(path, env):
    with open(env, "a", encoding="utf-8") as f:
        f.write("Path: " + str(path) + "\n" + "\n")


# Saves the performance of the search in terms of expansions of the queue
# and maximum number of nodes in queue.
def save_performance(expansions, max_nodes, env):
    with open(env, "a", encoding="utf-8") as f:
        f.write("Performance: " + "\n")
        f.write("Expansions of queue: " + str(expansions) + "\n")
        f.write("Max number of nodes in queue: " + str(max_nodes) + "\n")


# Breadth-first search
def bfs():
    # Tracks time taken.
    begin = default_timer()

    # Reads the maze into the program from a text file.
    maze = create_maze()

    # Gets start node, queue for nodes/paths to check,
    # visited for already visited nodes and portals for portals.
    start = find(maze, "s")
    queue = deque([start])
    visited = set()
    portals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Keep track of queue expansions and maximum number of nodes in queue.
    expansions = 1
    max_nodes = 1

    # Remove the previous environment text before appending.
    env = "bfs_environment.txt"
    if os.path.exists(env):
        os.remove(env)

    # While the queue isn't empty, check all neighbors of the current node,
    # add them to the queue and add the current node to visited.
    # Repeat until the goal is found or there are no further nodes to check.
    while queue:
        # Calculate the maximum number of nodes in the queue in each iteration.
        max_nodes = max(sum(len(nodes) for nodes in queue), max_nodes)
        # FIFO queue, so pop first element.
        path = queue.popleft()
        node = path[-1]

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

            # Marks visited nodes with a plus.
            if maze[node[0]][node[1]] == "0":
                maze[node[0]][node[1]] = "+"

        # If current node equals goal node,
        # print the path, mark it in the environment and add it into the text file.
        # Otherwise, go through the neighbors, add them to the path,
        # add the resulting path to the queue, add the current node to visited nodes
        # and add the environment to the text file.
        if maze[node[0]][node[1]] == "g":
            mark_path(maze, path)
            save_maze(maze, env)
            save_path(path, env)
            save_performance(expansions, max_nodes, env)
            # Returns time taken to find path(s). All other info in the text file(s).
            end = default_timer()
            return "Found BFS path in " + str(round(end-begin, 2)) + " seconds."
        else:
            # If current node isn't the goal,
            # add each reachable neighbors to a path (and visited)
            # and then append them to the queue.
            for n in get_neighbors(maze, node, visited):
                if n not in path and (node[0], node[1]) not in visited:
                    expansions += 1
                    new_path = path + [n]
                    queue.append(new_path)

        # Add current node to visited and save current maze to file.
        visited.add((node[0], node[1]))
        save_maze(maze, env)

    save_performance(expansions, max_nodes, env)
    return "No BFS path found :("


# Depth-first search
def dfs():
    begin = default_timer()
    maze = create_maze()

    start = find(maze, "s")
    queue = deque([start])
    visited = set()
    portals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    expansions = 1
    max_nodes = 1

    env = "dfs_environment.txt"
    if os.path.exists(env):
        os.remove(env)

    while queue:
        max_nodes = max(sum(len(nodes) for nodes in queue), max_nodes)
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
            mark_path(maze, path)
            save_maze(maze, env)
            save_path(path, env)
            save_performance(expansions, max_nodes, env)
            end = default_timer()
            return "Found DFS path in " + str(round(end - begin, 2)) + " seconds."
        else:
            # Reverses neighbor list to have priorities in the correct order for DFS
            for n in reversed(get_neighbors(maze, node, path)):
                if n not in path and (node[0], node[1]) not in visited:
                    expansions += 1
                    new_path = path + [n]
                    queue.append(new_path)

        visited.add((node[0], node[1]))
        save_maze(maze, env)

    save_performance(expansions, max_nodes, env)
    return "No DFS path found :("


# Calculates f(n) = g(n) + h(n).
def heuristic(goal, path):
    # Distance between current node and start node.
    g = len(path)
    # Manhattan distance.
    h = abs(goal[0][0] - path[-1][0]) + abs(goal[0][1] - path[-1][1])
    f = g + h
    return f


# Calculates f(n) = g(n) + h(n), taking portals into account.
def heuristic_portal(maze, goal, portals, path):
    portal_coords = []
    for p in portals:
        if find(maze, p):
            coord1 = find(maze, p)
            portal_coords.append(coord1)
            maze[coord1[0][0]][coord1[0][1]] = "0"
            coord2 = find(maze, p)
            portal_coords.append(coord2)
            maze[coord1[0][0]][coord1[0][1]] = str(p)

    # Distance between current node and start node.
    g = len(path)
    # Manhattan distance, including portals
    possible_hs = [abs(goal[0][0] - path[-1][0]) + abs(goal[0][1] - path[-1][1])]
    for i, c in enumerate(portal_coords):
        if i < len(portal_coords)-1:
            next = portal_coords[i+1]
        if i > 0:
            previous = portal_coords[i-1]
        if i % 2 == 0:
            possible_hs.append(abs(c[0][0] - path[-1][0]) + abs(c[0][1] - path[-1][1]) +
                               abs(goal[0][0] - next[-1][0]) + abs(goal[0][1] - next[-1][1]))
        else:
            possible_hs.append(abs(previous[0][0] - path[-1][0]) + abs(previous[0][1] - path[-1][1]) +
                               abs(goal[0][0] - c[-1][0]) + abs(goal[0][1] - c[-1][1]))

    h = sorted(possible_hs, key=int)[0]
    f = g + h
    return f


# A* search.
def a_star():
    begin = default_timer()
    maze = create_maze()

    start = find(maze, "s")

    # List of all goals
    goals = []
    # Searches for all goals and adds them to the list.
    # Overrides goals temporarily to get all of them.
    while find(maze, "g"):
        goal = find(maze, "g")
        goals.append(goal)
        maze[goal[0][0]][goal[0][1]] = "0"

    # Calculate which goal is the nearest and restore it in the maze.
    distances = []
    for g in goals:
        distances.append((abs(start[0][0] - g[0][0]) + abs(start[0][1] - g[0][1]), g[0]))
    nearest_goal = sorted(distances, key=lambda int: int[0])[0]
    maze[nearest_goal[1][0]][nearest_goal[1][1]] = "g"

    queue = ([start])
    visited = set()
    portals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    expansions = 1
    max_nodes = 1

    env = "a_star_environment.txt"
    if os.path.exists(env):
        os.remove(env)

    while queue:
        max_nodes = max(sum(len(nodes) for nodes in queue), max_nodes)
        # Priority "queue", so pop first element.
        path = queue[0]
        # Manually delete "popped" element.
        del queue[0]
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
            mark_path(maze, path)
            save_maze(maze, env)
            save_path(path, env)
            save_performance(expansions, max_nodes, env)
            end = default_timer()
            return "Found A* path(s) in " + str(round(end - begin, 2)) + " seconds."
        else:
            for n in get_neighbors(maze, node, visited):
                if n not in path and (node[0], node[1]) not in visited:
                    expansions += 1
                    new_path = path + [n]
                    queue.append(new_path)
                    # Sorts queue according to f value from lowest to highest.
                    queue = sorted(queue, key=lambda p: heuristic_portal(maze, goal, portals, p))

        visited.add((node[0], node[1]))
        save_maze(maze, env)

    save_performance(expansions, max_nodes, env)
    return "No A* path found :("


print(bfs())
print(dfs())
print(a_star())
