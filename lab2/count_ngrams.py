"""
Counting n-grams of any size: N
Usage: python count_ngrams.py N < corpus.txt
"""
__author__ = "Pierre Nugues"
import itertools
import sys

import regex


def tokenize(text):
    words = regex.findall('\p{L}+', text)
    return words


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    frequencies = {}
    for bigram in bigrams:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies


def count_ngrams(words, n):
    ngrams = [tuple(words[inx:inx + n])
              for inx in range(len(words) - n + 1)]
    # "\t".join(words[inx:inx + n])
    frequencies = {}
    for ngram in ngrams:
        if ngram in frequencies:
            frequencies[ngram] += 1
        else:
            frequencies[ngram] = 1
    return frequencies


import math


def nCr(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n - r)

if __name__ == '__main__':
    n = 2
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    text = sys.stdin.read().lower()
    words = tokenize(text)
    iterable = set([word.lower() for word in words])
    #print(len(iterable))
    #print(nCr(len(iterable), 4))
    frequency = count_ngrams(words, n)
    for word in sorted(frequency, key=frequency.get, reverse=True):
        print(word, '\t', frequency[word])    #for f in frequency:
    print(len(frequency))
    #    print(f + frequency[f])
    #for word in sorted(frequency, key=frequency.get, reverse=True):
    #    print(word, '\t', frequency[word])