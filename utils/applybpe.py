#Applies BPE to files in a folder, recursive-ly.
#Usage python3 applybpe --xlm_path ./XLM --out_path ./bpe/ --bpe_path ../bpe_codes --data_path ./data --delete_old

import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--xlm_path', default='./XLM', help='Path to XLM repo.')
parser.add_argument('--out_path', default='./processed', help='Path to directory where byte pair encoded files are to be written')
parser.add_argument('--bpe_path', default='./processed/codes', help='Path to file having BPE codes')
parser.add_argument('--data_path',default='./data', help='Path to folder having txts which are to be byte pair encoded. All files in sub-folders are BPE-ed recursively.')
parser.add_argument('--delete_old', action='store_true', help='If this flag is provided, original files are deleted.')

args = parser.parse_args()

cmd_initial = os.path.join(args.xlm_path, '/fastBPE/fast/')+" applybpe "+args.out_path
cmd_final = " "+args.bpe_path
data_dir = args.data_path

for root, dirs, files in os.walk(data_dir) :
    for filename in files :
        if not (filename[-1]=='z' and filename[-2]=='g') :
            command = cmd_initial + filename +' '+os.path.join(root, filename)+cmd_final
            print(command)
            os.system(command)
            
            if args.delete_old :
                command = 'rm '+os.path.join(root, filename)
                print(command)
                os.system(command)