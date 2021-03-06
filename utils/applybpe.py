# Applies BPE to files in a folder, recursive-ly.
# Usage python3 applybpe --fast_path ./FastBPE/fast --out_path ./bpe/ --bpe_path ../bpe_codes --data_path ./data --delete_old

import os
import subprocess
import argparse
import re 
from general import ensure_exists, get_lang, execute

def get_bpe_path(filename, codes_path) :
    lg = get_lang(filename)    
    return ' '+os.path.join(codes_path, 'codes.'+lg)
    

parser = argparse.ArgumentParser()
parser.add_argument('--fast_path', default='./fastBPE/fast', help='Path to fast tool for BPE.') 
parser.add_argument('--out_path', default='./processed', help='Path to directory where byte pair encoded files are to be written')
parser.add_argument('--bpe_path', default='./processed/codes', help='Path to file having BPE codes')
parser.add_argument('--data_path',default='./data', help='Path to folder having txts which are to be byte pair encoded. All files in sub-folders are BPE-ed recursively.')
parser.add_argument('--maintain_fs', action='store_true', help='If this flag is provided the original file structure is maintained')
parser.add_argument('--delete_old', action='store_true', help='If this flag is provided, original files are deleted.')
parser.add_argument('--codes_path', help='If different BPE code files per language are there, then you need to provide path to directory having all those codes files. Filename must be of form : codes.lg')

args = parser.parse_args()

cmd_initial = args.fast_path+" applybpe " 
cmd_final = " "+args.bpe_path if args.bpe_path is not None else ''
data_dir = args.data_path

for root, dirs, files in os.walk(data_dir) :
    for filename in files :
        if not filename.endswith('.gz') :

            if args.codes_path is not None :
                cmd_final = get_bpe_path(filename, args.codes_path)

            cur_file_path = os.path.join(root, filename)

            if args.maintain_fs :
                rectified_filename = os.path.relpath(cur_file_path, data_dir)
                ensure_exists(rectified_filename, args.out_path)
            else :
                rectified_filename = filename
            
            if not os.path.isfile(os.path.join(args.out_path, rectified_filename)) :
                
                command = cmd_initial + os.path.join(args.out_path, rectified_filename) + ' ' + cur_file_path + cmd_final
                print(command)
                execute(command)
                
                if args.delete_old :
                    command = 'rm '+cur_file_path
                    print(command)
                    execute(command)