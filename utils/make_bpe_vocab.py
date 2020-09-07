# Learns BPE codes(from mono files), splits files, applies BPE, finds vocabulary. All language wise. 

import argparse
import os
from applybpe import ensure_exists, get_lang

def execute(command) :
    x = os.system(command)
    if x>>8!=0 : 
        exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default='../data/', help='Path to data. It must be in the standard format provided in README.md')
parser.add_argument('--n_codes', type=int, default='20000', help='Number of BPE codes for each language')
parser.add_argument('--fast_path', default='../tools/FastBPE/fast', help='Path to \'fast\' program')
parser.add_argument('--codes_dir', default='../data/codes/', help='Directory to store BPE files')
parser.add_argument('--vocab_dir', default='../data/vocab/', help='Directory to store vocab files')
args = parser.parse_args()

learn_bpe_command = args.fast_path+' '+'learnbpe'+' '+args.n_codes+' '

#Learning BPE codes
for filename in os.listdir(os.path.join(args.data_path, 'mono/')) :
    if filename.endswith('.mono') :
        command = learn_bpe_command + os.path.join(args.data_path, filename) + ' > '+os.path.join(args.codes_dir, 'codes.'+filename[:-5])
        print(command)
        execute(command)

#Splitting files
splitted_path = os.path.join(args.data_path, '..', 'splitted/')
command = 'python3 splitter.py '+splitted_path+' '+args.data_path+' '+'--split_bigfiles --delete_old'
print(command)
execute(command)

#Applying BPE
bped_files_path = os.path.join(args.data_path, '..', 'processed/')
command = 'python3 applybpe.py --fast_path '+args.fast_path+' --out_path '+bped_files_path+' --data_path '+splitted_path+' --maintain_fs --delete_old --codes_path '+args.codes_dir
print(command)
execute(command)

#Getting Vocabularies
for root, dirs, files in os.walk(bped_files_path) :
    for filename in files :
        vocab_filename = 'vocab.'+filename
        cur_file_path = os.path.join(root, vocab_filename)
        nested_vocab_path = os.path.relpath(cur_file_path, bped_files_path)
        ensure_exists(nested_vocab_path, args.vocab_path)
        
        command = args.fast_path+' getvocab '+os.path.join(root, filename)+' > '+os.path.join(args.vocab_path, nested_vocab_path)
        print(command)
        execute(command)