README
======

This little program creates sentences from a provided text file using markov chains.

Your text file has to be one word per line. You can easily create a usable text file from any text file using *grep* from a terminal (started in the same folder as your text file) like this:
**grep -o '\w*' input.txt > output.txt** 
This transforms your text file to one word per line.

Optional additional commands:
**grep -i -E '[a-zA-Z]' input.txt > output.txt** 
This removes all lines not starting with alphabetic characters. You can expand it with symbolds you want to exclude.

**grep -i -v -E 'word1|word2|...|wordn' input.txt > output.txt**
This removes certain words from your text file if you have recurring words that would skew the generation.

You can specify a starting word (that has to be present in your text file) and a length for the generated sentences.
Furthermore, you can set the amount of words to use from your text file to save computing time (~100000 still gives quick results).
