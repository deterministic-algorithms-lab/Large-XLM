# Joins together codes of various splitted files and langauages to obtain a common one.

import argparse
from collections import Counter
from general import execute, get_lang
import os

def get_lg_k_dict(args, lg_dict) :
    
    out_lg_k_dict = {}

    if not args.absolute_top_k :
        for lg, value in lg_dict.items() :
            out_lg_k_dict[lg] = args.top_k
        
    if args.lg_k_dict is not None :
        lg_k_lis = args.lg_k_dict.split('-')
        for i in range(0,len(lg_k_lis),2) :
            if lg_k_lis[i] not in out_lg_k_dict :
                raise ValueError('No files corresponding to language '+lg_k_lis[i])
            out_lg_k_dict[lg_k_lis[i]] = int(lg_k_lis[i+1])
    
    return out_lg_k_dict

def read_dic_file(codes_path, counts={}) :
    skipped = 0
    assert os.path.isfile(codes_path), codes_path

    with open(codes_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if '\u2028' in line:
                skipped += 1
                continue
            line = line.rstrip().split()
            if len(line) != 3:
                skipped += 1
                continue
            assert len(line) == 3, (i, line)
            assert line[2].isdigit(), (i, line)
            key = line[0]+' '+line[1]
            if key in counts :
                counts[key] += int(line[2])
            else :
                counts[key] = int(line[2])
    
    print("Skipped "+str(skipped)+" lines. ")
    return counts

def write_dic_file(codes_counter, write_path) :
    with open(write_path, 'w+', encoding='utf-8') as f :
        for elem in codes_counter.most_common() :
            f.write(str(elem[0])+' '+str(elem[1])+'\n')

parser = argparse.ArgumentParser()
parser.add_argument('--codes_path', help='Path to directory having codes files.')
parser.add_argument('--final_codes_path', help='Path where final codes file will be stored.')
parser.add_argument('--top_k', type=int, default=20000, help='Top k words will be chosen from codes of each language.')
parser.add_argument('--lg_k_dict', help='Dictionary of language wise k, of the form \"lg-k-lg-k\". The languages not in dictionary would be assigned top_k value.')
parser.add_argument('--absolute_top_k', action='store_true', help='If this flag is provided, top_k elements are chosen from combination of codes of all languages.')

args = parser.parse_args()

lg_wise_file_dict = {}

for root, dirs, files in os.walk(args.codes_path) :
    for filename in files :
        try :
            lg = get_lang(filename)
        except ValueError :
            continue
        if lg not in lg_wise_file_dict :
            lg_wise_file_dict[lg] = []
        lg_wise_file_dict[lg].append(os.path.join(root, filename))

lg_to_codes_size_dict = get_lg_k_dict(args, lg_wise_file_dict)

lg_wise_counts = Counter()
for lg, files in lg_wise_file_dict.items() :
    counts = {}
    for f in files :
        counts = read_dic_file(f, counts)
    sorted_word_counts_lis = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    
    if not args.absolute_top_k :
        lg_codes_sz = lg_to_codes_size_dict[lg]
        sorted_word_counts_lis = sorted_word_counts_lis[:lg_codes_sz]
    
    lg_wise_counts.update({k: v for k, v in sorted_word_counts_lis})

if args.absolute_top_k :
    lg_wise_counts = Counter(dict(lg_wise_counts.most_common(args.top_k)))

write_dic_file(lg_wise_counts, args.final_codes_path)