import numpy as np


# Splits a string into a list of its characters.
def split(word):
    return [char for char in word]


# Transforms the maze to an array,
# replacing spaces with 0s for better handling.
with open("blatt3_environment.txt", "r") as f:
    maze = np.array([split((line.replace(" ", "0").strip("\n"))) for line in f])
print(maze)


# Get start and goal position.
start = i, j = np.where(maze == "s")
goal = x, y = np.where(maze == "g")


# Robot moving in one of the four directions, stopping at borders.
# Path is represented by pluses.
# Move forward by one.
if maze[i-1, j] == "0":
    maze[i-1, j] = "+"
    # print(maze)
    i -= 1


# Save maze to file again.
def save_to_file(maze):
    # Generate a new text file with the current environment
    np.savetxt("current_environment.txt", maze, fmt="%s")

    # Remove spaces from text file and replace 0s with blanks again.
    with open("current_environment.txt", "r") as f:
        lines = f.readlines()
        lines = [line.replace(" ", "") for line in lines]
        lines = [line.replace("0", " ") for line in lines]
    with open("current_environment.txt", "w") as f:
        f.writelines(lines)


save_to_file(maze)
