from random import random

# TODO: Specify amount of words to process, starting word and length of generated sentences
amount = 100000
word = "hallo".lower()
length = 20


# Gets all words that start with an alphabetic character from a given text file.
with open("ggcc-one-word-per-line.txt", "r", encoding="utf-8") as f:
    words = []
    for line in f:
        if line[0].isalpha():
            words.append(line.strip("\n").lower())
            if len(words) == amount:
                break


# Creates a list of bigrams for a given word, calculates their probability,
# sorts the list and adds them to a set of bigrams.
def bigrams(word):
    # Creates the bigram list for the current word.
    bigram_list = [[words[i], words[i+1]]
                   for i, x in enumerate(words) if x == word and i < len(words)-1]

    # Calculates the probability of a bigram, inserts it into the list
    # and adds the element into a bigram set.
    bigram_set = set()
    for w in bigram_list:
        occurrences = bigram_list.count(w)
        probability = occurrences/len(bigram_list)
        w.insert(0, str(probability))
        bigram_set.add((w[0], w[1], w[2]))

    return bigram_set


def trigrams(word):
    trigram_list = [[words[i], words[i+1], words[i+2]]
                    for i, x in enumerate(words) if x == word and i < len(words)-2]

    trigram_set = set()
    for w in trigram_list:
        occurrences = trigram_list.count(w)
        probability = occurrences / len(trigram_list)
        w.insert(0, str(probability))
        trigram_set.add((w[0], w[1], w[2], w[3]))

    return trigram_set


def quadrograms(word):
    quadrogram_list = [[words[i], words[i+1], words[i+2], words[i+3]]
                       for i, x in enumerate(words) if x == word and i < len(words)-3]

    quadrogram_set = set()
    for w in quadrogram_list:
        occurrences = quadrogram_list.count(w)
        probability = occurrences / len(quadrogram_list)
        w.insert(0, str(probability))
        quadrogram_set.add((w[0], w[1], w[2], w[3], w[4]))

    return quadrogram_set


# Creates a sentence of given length based on a chosen starting word using bigrams.
def markov_bigrams(word, length):
    # If the word is not in the word list, let the user know.
    if word not in words:
        return "Invalid word!" + "\n" + "Word has to start with a-z or äöü." + "\n" +\
               "Maybe it's not in the provided file or not processed." + "\n"

    # Initializes sentence with starting word.
    sentence = [word]

    for i in range(length-1):
        bigram_set = bigrams(word)

        # Randomly picks an element from the bigram set.
        # Copied and adjusted code from the hint.
        r = random.random()
        sop = 0
        for w in bigram_set:
            sop += float(w[0])
            if sop >= r:
                # Appends the sentence with the word that exceeded the threshold.
                sentence.append(w[2])
                # Updates word to next word.
                word = w[2]
                break

    return "Bigram:" + "\n" + " ".join(sentence) + "\n"


# Creates a sentence of given length based on a chosen starting word using trigrams.
def markov_trigrams(word, length):
    if word not in words:
        return "Invalid word!" + "\n" + "Word has to start with either a-z or äöü." + "\n" +\
               "Maybe it's not in the provided file or not processed." + "\n"

    sentence = [word]

    for i in range(length-1):
        trigram_set = trigrams(word)
        r = random()
        sop = 0
        for w in trigram_set:
            sop += float(w[0])
            if sop >= r:
                sentence.append(w[2])
                word = w[2]
                break

    return "Trigram:" + "\n" + " ".join(sentence) + "\n"


def markov_quadrograms(word, length):
    if word not in words:
        return "Invalid word!" + "\n" + "Word has to start with either a-z or äöü." + "\n" +\
               "Maybe it's not in the provided file or not processed." + "\n"

    sentence = [word]

    for i in range(length-1):
        quadrogram_set = quadrograms(word)
        r = random.random()
        sop = 0
        for w in quadrogram_set:
            sop += float(w[0])
            if sop >= r:
                sentence.append(w[2])
                word = w[2]
                break

    return "Quadrogram:" + "\n" + " ".join(sentence) + "\n"


print(markov_bigrams(word, length))
print(markov_trigrams(word, length))
print(markov_quadrograms(word, length))
