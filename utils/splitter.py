# Splits files int train test and valid files. 
# Large files can be split into many train files each of which are used one by one for training in split_train.py

'''
Usage :-  
python3 splitter.py ./splitted/ ./data/ --split_bigfiles 20  
All files in folder ./data/ (and in its subfolders too, recursively) are splitted and stored in ./splitted/ folder directly, or under a split-i/ folder.
Any file bigger than 1000000 lines is split into 20 equal parts which are stored in split0/, split1/, ... split19/ folders.
Files(in ./data/) having 'train.', 'test.', 'valid.', 'dev.' in their front, are not splitted, and just copied/moved.  
'''

import os
import shutil
import argparse
from general import execute

def make_dirs(outdir, n) :
    for i in range(n) :
        dir_path = os.path.join(outdir, 'split'+str(i)+'/')
        if not os.path.isdir(dir_path) :
            print("Making directory ", dir_path)
            os.makedirs(dir_path)         

def is_bigfile(filepath) :
    with open(filepath, 'r') as f :
        for i, l in enumerate(f) :
            pass
        if i+1>10000 :
            return i+1
        print(filepath, " has ", i+1, " lines ")
        return 0

def split(filepath, train_path, valid_path, test_path, split_bigfiles) :
    if split_bigfiles > 0 :
        n_lines = is_bigfile(filepath)
        if n_lines>0 : 
            print(filepath, " has ", n_lines, " lines ")
    
    n_test_valid_lines = 50
    
    with open(filepath) as f :
        
        i = 0
        if not os.path.isfile(test_path) :
            with open(test_path, 'w+') as test_file :      
                print("Making test file : ", test_path, "with ", n_test_valid_lines, " lines.")
                while i< n_test_valid_lines :
                    line = f.readline()
                    test_file.write(line)
                    i+=1
            
        if not os.path.isfile(valid_path) :
            with open(valid_path, 'w+') as valid_file :
                print("Making valid file : ", valid_path, "with ", n_test_valid_lines, " lines.")
                while i< 2*n_test_valid_lines :
                    line = f.readline()
                    valid_file.write(line)
                    i+=1
                
        if split_bigfiles>0 and n_lines>0 :

            path_elems = train_path.split('/')
            root, filename = '/'.join(path_elems[:-1]), path_elems[-1]                          #Finding Root ,filename to access split directories properly 
                    
            for i in range(split_bigfiles) :
                    
                j=0

                #Write n_lines/split_bigfiles in each split directory                        
                train_path = os.path.join(root, 'split'+str(i), filename)

                if not os.path.isfile(train_path) :
                    
                    with open(train_path, 'w+') as train_file :
                            
                        while j<n_lines/split_bigfiles :
                            line = f.readline()
                            if line == '' :
                                break
                            j=j+1
                            train_file.write(line)
                            
                        print("Made train file : ", train_path, "with ", j, " lines.")
                            
                        if line=='' :
                            break
                else :

                    while j<n_lines/split_bigfiles :
                        line = f.readline()
                        if line == '' :
                            break
                        j=j+1
                    print("skipped to ", i*j, "th line.")
                        
        else :

            if not os.path.isfile(train_path) :    
                
                with open(train_path, 'w+') as train_file :
                    while True :
                        line = f.readline()
                        i+=1
                        if line == '' :
                            break
                        train_file.write(line)
                print("Made Train file ", train_path, " with : ", i-2*n_test_valid_lines, " lines.")        
                

def already_splitted(filename) :
    if len(filename)>6 and filename[0:6]=='train.' : return True
    if len(filename)>6 and filename[0:6]=='valid.' : return True
    if len(filename)>5 and filename[0:5]=='test.'  : return True
    if len(filename)>4 and filename[0:4]=='dev.'   : return True 
    return False


parser = argparse.ArgumentParser() 
parser.add_argument('outdir', metavar='-o', nargs=1, help='directory where to write files')
parser.add_argument('indir', metavar='-i', nargs=1, help='directory where to read files from')
parser.add_argument('--split_bigfiles', metavar='-s', type=int, default=0, help='the no. of parts into which any file with >1000000 lines is to be split')
parser.add_argument('--delete_old', action='store_true', help='If this flag is provided, original files are deleted.')

args = parser.parse_args()

args.indir = args.indir[0]
args.outdir = args.outdir[0]

if args.split_bigfiles>0 :
    make_dirs(args.outdir, args.split_bigfiles)
    
for root, dirs, files in os.walk(args.indir) :
    for filename in files :
        filepath = os.path.join(root, filename)

        if not filename.endswith('.gz') and not filename.startswith('codes.') :
            if not already_splitted(filename) :
                
                train_path = os.path.join(args.outdir, 'train.'+filename) 
                valid_path = os.path.join(args.outdir, 'valid.'+filename)
                test_path = os.path.join(args.outdir, 'test.'+filename)

                split(filepath, train_path, valid_path, test_path, args.split_bigfiles)                
                    
                if args.delete_old :
                    command = 'rm '+filepath
                    execute(command)
                    
            else : 
                copy_or_cut = "mv " if args.delete_old else "cp "
                command = copy_or_cut+filepath+' '+os.path.join(args.outdir, filename)
                execute(command)    
