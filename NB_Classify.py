import csv
import math
from twitter_specials import *

my_dict = {}
my_cats = ["positive", "negative", "neutral", "irrelevant"]
my_prob = {}
my_totes = [0, 0, 0, 0]

each_counted = []
multi_word = []
total = 0
for w, count in my_dict.items():
    if count > 1:
        multi_word.append((count, w))
for count, w in multi_word:
    each_counted.append(w)

with open("labeled_corpus.tsv", encoding="utf-8") as lf:
    readCSV = csv.reader(lf, delimiter='\t')
    for row in readCSV:
        total += 1
        line_arr = list(row)

        tweet = line_arr[0]
        category = line_arr[1]
        tweet = clean_tweet(tweet, emo_repl_order, emo_repl, re_repl)

        words = tweet.split()
        words_set = set()
        for w in words:
            if '#' not in w and '@' not in w:
                words_set.add(w)
        for w in each_counted:
            if w in words_set:
                if w not in my_prob:
                    my_prob[w] = [0, 0, 0, 0]
                for i in range(4):
                    if my_cats[i] == category:
                        my_prob[w][i] += 1
for w in my_prob:
    for i in range(4):
        my_prob[w][i] = my_prob[w][i] / my_totes[i]
classed = []

with open("labeled_corpus.tsv", encoding="utf-8") as lf:
    readCSV = csv.reader(lf, delimiter='\t')
    for row in readCSV:
        line_arr = list(row)

        tweet = line_arr[0]
        category = line_arr[1]
        for i in range(4):
            if category == my_cats[i]:
                my_totes[i] += 1
        tweet = clean_tweet(tweet, emo_repl_order, emo_repl, re_repl)

        words = tweet.split()
        words_set = set()
        for w in words:
            if '#' not in w and '@' not in w:
                words_set.add(w)

        for w in words_set:
            if w not in my_dict:
                my_dict[w] = 0
            my_dict[w] += 1

with open('geo_twits_squares.tsv', encoding="utf-8") as gf:

    readCSV = csv.reader((line.replace('\0', '') for line in gf), delimiter='\t')

    for row in readCSV:
        converted_cats = {"positive": 0, "negative": 0, "neutral": 0, "irrelevant": 0}
        for i in range(4):
            converted_cats[my_cats[i]] = math.log2(my_totes[i] / total)
        line_arr = list(row)
        lat = line_arr[0]
        long = line_arr[1]
        tweet = line_arr[2]
        tweet = clean_tweet(tweet, emo_repl_order, emo_repl, re_repl)
        words = tweet.split()
        words_set = set()
        for w in words:
            if '#' not in w and '@' not in w and w in my_prob:
                words_set.add(w)
        for w in words_set:
            for i in range(4):
                # print(classifier[w][i])
                if my_prob[w][i] != 0:
                    converted_cats[my_cats[i]] += math.log2(my_prob[w][i])
        at_most = converted_cats[my_cats[0]]
        for i in range(4):
            if converted_cats[my_cats[i]] > at_most:
                at_most = converted_cats[my_cats[i]]
        final = list(converted_cats.keys())[list(converted_cats.values()).index(at_most)]
        classed.append((lat, long, final))

with open('locations_classified.tsv', 'w') as lt:
    writer = csv.writer(lt, delimiter='\t', lineterminator='\n')
    for i in classed:
        writer.writerow(i)
