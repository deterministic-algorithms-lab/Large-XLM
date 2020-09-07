# Binarizes all files given directly in a folder or in the format of file tree produced by splitter.py
# Usage :-
# python3 binarize.py --in_path ./splitted/ --out_path ./binarized/ --vocab_path ./data/xlm_100_vocab --delete_old

import os
import shutil
import argparse

def execute(command) :
    x = os.system(command)
    if x>>8!=0 : 
        exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--in_path', help='Path to directory have splitted(train, test , valid) files') 
parser.add_argument('--out_path', help='Path to output directory, where binarized files are to be stored')
parser.add_argument('--vocab_path', help='Path to vocabulary file')
parser.add_argument('--xlm_path', help='Path to XLM cloned repo')
parser.add_argument('--delete_old', action='store_true', help='If this flag is provided, original files are deleted.')

args = parser.parse_args()

cmd_initial = "python3 "+os.path.join(args.xlm_path,"preprocess.py")+" "

if os.path.isdir(os.path.join(args.in_path, 'split'+str(0))) :
    is_splitted=True
else :
    is_splitted=False
    
for root, dirs, files in os.walk(args.in_path) :
    for filename in files :
            
        #removing '.mono' from end of filename
        if filename.split('.')[-1]=='mono' :
            rectified_filename = '.'.join(filename.split('.')[:-1])
        else :
            rectified_filename = filename
        
        #Figuring out destination for storing binarized file. 
        if is_splitted and root.split('/')[-1][0:5] == 'split' :
            out_split_dir = os.path.join( args.out_path, root.split('/')[-1] )
            if not os.path.isdir(out_split_dir) :
                os.mkdir(out_split_dir) 
            dest_path = os.path.join(out_split_dir, rectified_filename)
        else :
            dest_path = os.path.join(args.out_path, rectified_filename)
            
        #Only Make binarized file if it doesn't already exist
        if not os.path.isfile(dest_path+'.pth') :
               
            command = cmd_initial+args.vocab_path+' '+os.path.join(root, filename)+' '+dest_path
                
            print(command)
            execute(command)

            if args.delete_old :    
                command = 'rm '+os.path.join(root, filename)
                print(command)
                execute(command)