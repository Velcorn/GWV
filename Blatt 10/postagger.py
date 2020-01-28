from collections import Counter
from random import random


# Gets a list of all word and tags from a tagged file.
def read_file(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = [tuple(line.rstrip('\n').split('\t')) for line in f if line != "\n"]
        words = [word for word, _ in lines]
        tags = [tag for _, tag in lines]

    return words, tags


# Takes user input from the command line.
def get_user_input():
    user_input = input('> ')
    return user_input


# Calculates the transition and emission probabilities from the tagged data.
def calculate_probabilities(words, tags):
    # Counts occurrences of tags.
    tag_counts = Counter(tag for tag in tags)

    # Creates a list of tag, previous tag tuples and gets their occurrences.
    transition_counts = Counter(transition for transition in list(zip(tags[1:], tags)))
    # Calculates probabilities from counts (count of tag, previous tag tuple / count of previous tag)
    transition_probabilities = [(transition_counts[trac] / tag_counts[trac[1]], trac)
                                for trac in transition_counts]

    # Creates a list of word, tag tuples and gets their occurrences.
    emission_counts = Counter(emission for emission in list(zip(words, tags)))
    # Calculates probabilities from counts (count of word, tag tuple / count of tag)
    emission_probabilities = [(emission_counts[ec] / tag_counts[ec[1]], ec)
                              for ec in emission_counts]

    return transition_probabilities, emission_probabilities


# Creates suffix trees for unknown words based on a frequency of <= 25 with a maximum suffix length of 5.
def build_suffix_trees(words, tags):
    upper_case_suffixes_tags = []
    lower_case_suffixes_tags = []

    word_counts = Counter(word for word in words)

    # Adds the suffix, tag tuples from unknown words to their corresponding suffix list.
    for i, word in enumerate(words):
        if word_counts[word] <= 25:
            suffix = word[-5:]

            if word[0].isupper():
                upper_case_suffixes_tags.append((suffix, tags[i]))
            else:
                lower_case_suffixes_tags.append((suffix, tags[i]))

    # Gets the tag and suffix, tag tuple counts.
    upper_case_tag_counts = Counter(st[1] for st in upper_case_suffixes_tags)
    upper_case_st_counts = Counter(st for st in upper_case_suffixes_tags)
    lower_case_tag_counts = Counter(st[1] for st in lower_case_suffixes_tags)
    lower_case_st_counts = Counter(st for st in lower_case_suffixes_tags)

    # Calculates the probabilities of the suffix, tag tuples.
    upper_case_probabilities = [(upper_case_st_counts[ucc] / upper_case_tag_counts[ucc[1]], ucc)
                                for ucc in upper_case_st_counts]
    lower_case_probabilities = [(lower_case_st_counts[lcc] / lower_case_tag_counts[lcc[1]], lcc)
                                for lcc in lower_case_st_counts]

    return upper_case_probabilities, lower_case_probabilities


# Calculates the most probable tag sequence using the viterbi algorithm.
def viterbi(words, transition_probabilities, emission_probabilities,
            upper_case_probabilities, lower_case_probabilities, user_input):
    return ""


# Generates a random tag sequence.
def random_sequence(tags, user_input):
    output = []

    tag_counts = Counter(tag for tag in tags)
    tag_probabilities = [(tag_counts[tc] / sum(tag_counts.values()), tc) for tc in tag_counts]

    for w in user_input:
        r = random()
        sum_of_probs = 0
        for t in tag_probabilities:
            sum_of_probs += t[0]
            if sum_of_probs >= r:
                tag = t[1]
                output.append(w + "\\" + tag)
                break

    print(" ".join(output))


# Tags user input based on hidden markov model (using the viterbi algorithm).
def create_tag_sequence():
    words, tags = read_file("hdt-1-10000-train.tags")
    transition_probabilities, emission_probabilities = calculate_probabilities(words, tags)
    upper_case_probabilities, lower_case_probabilities = build_suffix_trees(words, tags)

    while True:
        user_input = get_user_input()
        random_sequence(tags, user_input)
        # viterbi(words, transition_probabilities, emission_probabilities,
        #         upper_case_probabilities, lower_case_probabilities, user_input)


print(create_tag_sequence())
