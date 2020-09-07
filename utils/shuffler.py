#Shuffles all files in a directory
#Use as :- python3 shuffler.py --data_dir './data/'

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', default='./data/', help='The directory, each of whose files is to be shuffled')
args = parser.parse_args()

data_dir = args.data_dir

files = os.listdir(data_dir)
print(files)
for filename in files :
    if filename.endswith('.mono') :     
        new_filename = 'shuf'+filename
        command = 'shuf '+os.path.join(data_dir, filename)+' > '+os.path.join(data_dir, new_filename)
        print(command)
        os.system(command)
        
        command = 'rm '+os.path.join(data_dir, filename)
        print(command)
        os.system(command)
        
        command = 'mv '+os.path.join(data_dir, new_filename)+' '+os.path.join(data_dir, filename)
        print(command)
        os.system(command)
        