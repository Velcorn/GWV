# Creates a wordlist from given words.
wordlist = ['add', 'ado', 'age', 'ago', 'aid', 'ail', 'aim', 'air',
            'and', 'any', 'ape', 'apt', 'arc', 'are', 'ark', 'arm',
            'art', 'ash', 'ask', 'auk', 'awe', 'awl', 'aye', 'bad',
            'bag', 'ban', 'bat', 'bee', 'boa', 'ear', 'eel', 'eft',
            'far', 'fat', 'fit', 'lee', 'oaf', 'rat', 'tar', 'tie']

# Creates empty crossword puzzle with 3 rows.
puzzle = [[],
          [],
          []]

# Assigns each row every word from the wordlist.
for w in wordlist:
    puzzle[0] = w
    for x in wordlist:
        puzzle[1] = x
        for y in wordlist:
            puzzle[2] = y

            # Specifies columns.
            col1 = (puzzle[0][0] + puzzle[1][0] + puzzle[2][0])
            col2 = (puzzle[0][1] + puzzle[1][1] + puzzle[2][1])
            col3 = (puzzle[0][2] + puzzle[1][2] + puzzle[2][2])

            # If every column is a word in the wordlist, print the solution.
            if all(col in wordlist for col in (col1, col2, col3)):
                for e in puzzle:
                    print("[" + e[0] + "]" + "[" + e[1] + "]" + "[" + e[2] + "]")
                print("\n")
