import sys
import pickle
import regex as re
import os
import math

def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files


def create_master_index():
    files = get_files("Selma", "txt")
    master_index = {}
    for book in files:
        with open("Selma/" + book, "r") as f:
            unchanged_text = f.read().lower()
            words = re.findall("\p{L}+", unchanged_text)

        for word in words:
            if word not in master_index.keys():
                master_index[word] = {}
            if book not in master_index[word].keys():
                matches = re.finditer("\W" + word + "\W", unchanged_text)
                positions = []

                for match in matches:
                    positions.append(match.span()[0] + 1)   # To compensate for the \W.

                master_index[word][book] = positions

    return master_index


def get_word_count():
    wc = {}
    files = get_files("Selma", "txt")
    for file in files:
        with open("Selma/" + file, "r") as f:
            wc[file] = len(re.findall("\p{L}+", f.read()))
    return wc


def get_tf(term, document, master_index, master_wc):   # term = t, document = d, master_index
    total_count = master_wc[document]
    if document in master_index[term].keys():
        word_count = len(master_index[term][document])
        return word_count / total_count

    return 0


def get_idf(term, master_index): # term = t, master_index
    D = get_files("Selma", "txt")
    N = len(D)
    n_term = len(master_index[term])
    return math.log(float(N)/n_term, 10)


def cos_sim(doc_1, doc_2, master_index, master_wc):     # Numpy + Scipy: dot product.
    qd_sum = d_square = q_square = 0                    # Scikit learn och numpy har cos similarity färdig.
    for word in master_index.keys():                    # Scikit learn tfidf har färdig.
        sub_list = master_index[word]
        q_i = d_i = 0

        if doc_1 in sub_list.keys():
            q_i = tfidf(word, doc_1, master_index, master_wc)
        if doc_2 in sub_list.keys():
            d_i = tfidf(word, doc_2, master_index, master_wc)

        qd_sum += q_i * d_i
        q_square += q_i * q_i
        d_square += d_i * d_i
    return qd_sum / (math.sqrt(q_square)*math.sqrt(d_square))


def file_combo_used(used_combo, file, file2):
    for combo in used_combo:
        if (file and file2) in combo:
            return True
    return False


def find_most_sim(master_wc):       # vinkeln mellan dem närmst
    indx = open_pickle()
    sim_score = 0
    sim_bad = 1
    files = get_files("Selma", "txt")
    used_combo = []
    for file in files:
        for file2 in files:
            if file != file2 and not file_combo_used(used_combo, file, file2):
                used_combo.append([file, file2])
                sim_temp = cos_sim(file, file2, indx, master_wc)
                if sim_temp > sim_score:
                    sim_score = cos_sim(file, file2, indx, master_wc)
                    win_1 = file
                    win_2 = file2
                if sim_temp < sim_bad:
                    sim_bad = cos_sim(file, file2, indx, master_wc)
                    loss_1 = file
                    loss_2 = file2
            else:
                print(file, file2)
    print("%s and %s is most similar (%s)" % (win_1, win_2, sim_score))
    print("%s and %s is least similar (%s)" % (loss_1, loss_2, sim_bad))


"""def create_index(filename):
    indices = {}
    with open(filename, "r") as f:
        unchanged_text = f.read().lower()
        words = re.findall("\p{L}+", unchanged_text)

    for word in words:
        if word not in indices.keys():
            matches = re.finditer(word, unchanged_text)
            positions = []

            for match in matches:
                positions.append(match.span()[0])

            indices[word] = positions
    return indices
"""


def create_matrix():
    #           word1 ... wordn
    # book1
    # book2
    # ..
    # bookn
    master_index = open_pickle()
    master_wc = get_word_count()
    files = get_files("Selma", "txt")
    words = list(master_index.keys())
    words = words[58:61]
    print('\t'.join(['\t\t'] + ["%s  " % word for word in words]))       # print header
    for book in files:
        to_print = '\t\t'.join([book] + ["%s" % round(tfidf(x, book, master_index, master_wc), 8) for x in words])
        print(to_print)




def write_pickle(index_dict):
    pickle.dump(index_dict, open("indices.p", "wb"))


def tfidf(term, book, master_index, master_wc):
    tf = get_tf(term, book, master_index, master_wc)
    idf = get_idf(term, master_index)
    return tf*idf


def open_pickle():
    return pickle.load(open("indices.p", "rb"))


def print_master_index():
    master_index = open_pickle()
    to_print = ""
    for word in master_index:
        to_print = word + ':'
        for book in master_index[word]:
            to_print = ' '.join([to_print, book] + [str(x) for x in master_index[word][book]])
        print(to_print)

if __name__ == "__main__":
    ##indexx = open_pickle()
    #master_wc = get_word_count()
    #find_most_sim(master_wc)
    create_matrix()
    #for words in indexx.keys():
    #    tf_sc = tfidf(words, "nils.txt", indexx, master_wc)

        #if tf_sc > 0:
        #    print("%s: %s" % (words, tf_sc))
            