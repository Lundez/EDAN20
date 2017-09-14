import regex as re
from mutual_info import count_unigrams, count_bigrams

def accuracy_dot(text):
    dots = re.findall("\.", text)
    others = re.findall("(\!|\?)", text)
    print(len(dots) / (len(dots) + len(others)))

def insert_delimeters(text):
    match_list = re.finditer("[\p{Lu}][^\.]*(\.|\?|\!)", text)  # Bättre med Lu, Unicode.
    match_list = ['<s> ' +
                  re.sub('(\p{P}|\t|\n|\r|\f)', ' ', match.group().lower()) +
                  ' </s> ' for match in match_list]

    return match_list

def compute_likelihood_by_unigram(sentence, text):
    sentence = insert_delimeters(sentence)[0].split()
    unigram_dict = count_unigrams(text)
    result = 1
    print_unigram_header()
    for word in sentence:
        if(word in '<s>'):
            continue
        result = result * (unigram_dict[word]/len(text))
        print_table_word(word, unigram_dict, text)
    entropy_unigram = entropy(result, sentence)
    perplexity_unigram = perplexity(entropy_unigram)
    print("======================================================")
    print("Prob. unigrams:\t %s" % result)
    print("Entropy rate: \t %s" % entropy_unigram)
    print("Perplexity: \t %s" % perplexity_unigram)
    return result

def print_unigram_header():
    print("Unigram model")
    print("======================================================")
    print('\t'.join(['wi', 'C(wi)', '#words', 'P(wi)']))


def print_table_word(word, unigram_dict, text):
    to_print = '\t'.join([word, str(unigram_dict[word]), str(len(text)), str(unigram_dict[word]/len(text))])
    print(to_print)

def print_table_bigram(bigram, unigram_dict, bigram_dict, perc):
    b1 = bigram[0]
    b2 = bigram[1]
    to_print = '\t'.join([b1+"\t", b2+"\t", str(bigram_dict.get(bigram, 0)), str(unigram_dict[b1]), perc])
    print(to_print)


def compute_likelihood_by_bigram(sentence, text):
    bigram_dict = count_bigrams(text)
    unigram_dict = count_unigrams(text)
    sentence = insert_delimeters(sentence)[0].split()
    result = 1
    print("Bigram model")
    print("======================================================")
    print('\t'.join(['wi\t', 'wi+1\t', 'Ci,i+1', 'C(i)', 'P(wi+1|wi)']))
    for x in range(1, len(sentence)):
        bigram = (sentence[x-1], sentence[x])

        if bigram in bigram_dict.keys():
            perc = bigram_dict[bigram]/unigram_dict[sentence[x-1]]
            result = result * perc
        else:
            perc = unigram_dict[sentence[x]]/len(text)
            result = result * perc
            perc = '*backoff: %s' % perc

        print_table_bigram(bigram, unigram_dict, bigram_dict, str(perc))
    entropy_bigram = entropy(result, sentence)
    perplexity_bigram = perplexity(entropy_bigram)
    print("======================================================")
    print("Prob. bigrams: \t %s" % result)
    print("Entropy rate: \t %s" % entropy_bigram)
    print("Perplexity: \t %s" % perplexity_bigram)
    return result


def entropy(result, sentence):
    return (-1)*math.log(result, 2)/len(sentence)


def perplexity(hl):
    return 2**hl


import math
def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)

import sys
if __name__ == '__main__':
    book = "Selma.txt"
    text = sys.stdin.read().strip()
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = insert_delimeters(text)
    text = ''.join(text).split()
    compute_likelihood_by_unigram("Det var en gång en katt som hette Nils.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("Det var en gång en katt som hette Nils.", text)
"""
    compute_likelihood_by_unigram("Det är en sanning, att is alltid är trolös och ingenting att lita på.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("Det är en sanning, att is alltid är trolös och ingenting att lita på.", text)

    compute_likelihood_by_unigram("Därför bugade han sig för mamsell Broström.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("Därför bugade han sig för mamsell Broström.", text)

    compute_likelihood_by_unigram("De hade ingen brådska.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("De hade ingen brådska.", text)

    compute_likelihood_by_unigram("Den lille Ruster var eldfängd och stolt.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("Den lille Ruster var eldfängd och stolt.", text)

    compute_likelihood_by_unigram("Elden slog just då ut genom tak och fönster, och hettan var förfärlig.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("Elden slog just då ut genom tak och fönster, och hettan var förfärlig.", text)

    compute_likelihood_by_unigram("Sigurd däremot satt orörlig och bara lyssnade.", text)
    print("\n======================================================\n")
    compute_likelihood_by_bigram("Sigurd däremot satt orörlig och bara lyssnade.", text)
"""