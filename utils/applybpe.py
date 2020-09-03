# Applies BPE to files in a folder, recursive-ly.
# Usage python3 applybpe --fast_path ./FastBPE/fast --out_path ./bpe/ --bpe_path ../bpe_codes --data_path ./data --delete_old

import os
import subprocess
import argparse

def ensure_exists(filepath, search_in) :
    if filepath.find('/')==-1 :
        return 
    
    dir_to_search = '/'.join(filepath.split('/')[:-1])
    dir_to_search = os.path.join(search_in, dir_to_search)
    
    if not os.path.isdir(dir_to_search) :
        print("Making directory : ", dir_to_search)
        os.makedirs(dir_to_search)

parser = argparse.ArgumentParser()
parser.add_argument('--fast_path', default='./fastBPE/fast', help='Path to fast tool for BPE.') 
parser.add_argument('--out_path', default='./processed', help='Path to directory where byte pair encoded files are to be written')
parser.add_argument('--bpe_path', default='./processed/codes', help='Path to file having BPE codes')
parser.add_argument('--data_path',default='./data', help='Path to folder having txts which are to be byte pair encoded. All files in sub-folders are BPE-ed recursively.')
parser.add_argument('--maintain_fs', action='store_true', help='If this flag is provided the original file structure is maintained')
parser.add_argument('--delete_old', action='store_true', help='If this flag is provided, original files are deleted.')

args = parser.parse_args()

cmd_initial = args.fast_path+" applybpe " 
cmd_final = " "+args.bpe_path
data_dir = args.data_path

for root, dirs, files in os.walk(data_dir) :
    for filename in files :
        if not filename.endswith('.gz') :
            cur_file_path = os.path.join(root, filename)
            
            if args.maintain_fs :
                rectified_filename = os.path.relpath(cur_file_path, data_dir)
                ensure_exists(rectified_filename, args.out_path)
            else :
                rectified_filename = filename
            
            if not os.path.isfile(os.path.join(args.out_path, rectified_filename)) :
                
                command = cmd_initial + os.path.join(args.out_path, rectified_filename) + ' ' + cur_file_path + cmd_final
                print(command)
                os.system(command)
                
                if args.delete_old :
                    command = 'rm '+cur_file_path
                    print(command)
                    os.system(command)