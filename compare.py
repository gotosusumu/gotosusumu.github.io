#!/usr/bin/env python3
import argparse
import Levenshtein
import pickle
import itertools
import sys

with open('benchmark.pkl', 'rb') as f:  # Open file in read-binary mode
    bds = pickle.load(f)

all_comparisons = bds[168]['compare']
just_one_response = bds[168]['compare']['llamallama2-70b']
original_prompt = bds[168]['conversation'][0]['content']
original_response = bds[168]['conversation'][1]['content']

print(f'Query No.\tModel1\tModel2\tDistance\tLen1\tLen2\tSimilarity')
for i in range(0, len(bds)):
    all_comparisons = bds[i]['compare']
    original_prompt = bds[i]['conversation'][0]['content']
    original_response = bds[i]['conversation'][1]['content']
    all_comparisons['original'] = original_response
    if (i == 8199 or all_comparisons == {}):
        continue

# Query 8199 includes some strange characters, so skipped    
#    for model in all_comparisons:
#        print(model)
#        print(all_comparisons[model])
#        if (all_comparisons[model] == ""):
#            print(i, model)
# Checked cases where a model returned nothing
# There are 317 cases: 140 prompts for 13 models, mostly llama-70b


    for (model1, model2) in itertools.combinations(all_comparisons, 2):
        text1 = all_comparisons[model1]
        text2 = all_comparisons[model2]
        distance = Levenshtein.distance(text1, text2)
        len1 = len(text1)
        len2 = len(text2)
        if (len1 == 0 or len2 == 0):
            continue
        max_len = max(len1, len2)
        similarity = 1 - (distance / max_len)
        print(f'{i}\t{model1}\t{model2}\t{distance}\t{len1}\t{len2}\t{similarity}')
    

