from random import randint

# TODO: Specify starting word and length of generated sentences
word = "hallo".lower()
length = 20


# Gets all words that start with an alphabetic character from a given text file.
with open("ggcc-one-word-per-line.txt", "r", encoding="utf-8") as f:
    words = []
    for line in f:
        if line[0].isalpha():
            words.append(line.strip("\n").lower())


# Creates a sentence of given length based on a chosen starting word using bigrams.
def markov_bigrams(word, length):
    # If the word is not in the word list, let the user know.
    if word not in words:
        return "Invalid word!" + "\n" + "Word has to start with a-z or äöü." + "\n" +\
               "Maybe it's not in the provided file or not processed." + "\n"

    # Create the bigram database and initiate the sentence with chosen starting word.
    bigram_db = [[words[i], words[i+1]] for i in range(len(words)-2)]
    sentence = [word]

    for i in range(length-1):
        # Gets indices of the bigrams for the current word.
        indices = [i for i, x in enumerate(bigram_db) if x[0] == word]

        # Randomly picks an element from the bigram database
        # for the current word, appends the sentence with it
        # and updates word to the next word.
        r = randint(0, len(indices)-1)
        sentence.append(bigram_db[r][1])
        word = bigram_db[r][1]

    return "Bigram:" + "\n" + " ".join(sentence) + "\n"


# Creates a sentence of given length based on a chosen starting word using trigrams.
def markov_trigrams(word, length):
    if word not in words:
        return "Invalid word!" + "\n" + "Word has to start with either a-z or äöü." + "\n" +\
               "Maybe it's not in the provided file or not processed." + "\n"

    trigram_db = [[words[i], words[i+1], words[i+2]] for i in range(len(words)-3)]
    sentence = [word]

    for i in range(length - 1):
        indices = [i for i, x in enumerate(trigram_db) if x[0] == word]
        r = randint(0, len(indices) - 1)
        sentence.append(trigram_db[r][1])
        word = trigram_db[r][1]

    return "Trigram:" + "\n" + " ".join(sentence) + "\n"


def markov_quadrograms(word, length):
    if word not in words:
        return "Invalid word!" + "\n" + "Word has to start with either a-z or äöü." + "\n" +\
               "Maybe it's not in the provided file or not processed." + "\n"

    quadrogram_db = [[words[i], words[i+1], words[i+2], words[i+3]] for i in range(len(words)-4)]
    sentence = [word]

    for i in range(length - 1):
        indices = [i for i, x in enumerate(quadrogram_db) if x[0] == word]
        r = randint(0, len(indices) - 1)
        sentence.append(quadrogram_db[r][1])
        word = quadrogram_db[r][1]

    return "Quadrogram:" + "\n" + " ".join(sentence) + "\n"


print(markov_bigrams(word, length))
print(markov_trigrams(word, length))
print(markov_quadrograms(word, length))
