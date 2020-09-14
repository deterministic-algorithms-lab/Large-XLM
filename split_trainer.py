# Does split-wise training for big files which have been splitted.
# data_path in original command must correspond to directory having binarized data in format of splitted file tree.
# Usage :- python3 split_trainer.py --command "python train.py ....." --n_reps 4
# The above command loops 4 times through all splits ; each time running command provided with --command
 
import os
import argparse
from train import get_parser
from utils.general import execute

def replace_arg(train_command, cur_value, arg) :
    parts = train_command.split(arg)
    if len(parts)==1 :
        parts[0] = parts[0]+' '
        parts.append('')
    before_arg, after_arg = parts[0]+arg, parts[1]
    after_arg_lis = [' '+cur_value+' ']+after_arg.split('--')[1:]
    modified_command = before_arg+'--'.join(after_arg_lis)
    return modified_command

def get_arg(train_command, arg) :
    parts = train_command.split(arg)
    if len(parts)==1 :
        return None
    return parts[1].split('--')[0].rstrip().lstrip()
 
def shift_files(source_dir, dest_dir, file_lis=[]) :
    shift_from = file_lis if len(file_lis)>0 else [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    shifted_files = []
    for filename in  shift_from :
        command = "mv "+os.path.join(source_dir, filename)+' '+os.path.join(dest_dir, filename)
        print(command)
        execute(command)
        shifted_files.append(filename)
    return shifted_files

def get_new_dump(train_command, i, delete_old) :
 
    #Changing dump_path to that of next run
    dump_path = get_arg(train_command, '--dump_path')
    new_dump_path = os.path.join(os.path.split(dump_path)[0], 'run'+str(i))
    train_command = replace_arg(train_command, new_dump_path, '--dump_path')
    
    if not os.path.isdir(new_dump_path) :
        os.makedirs(new_dump_path)
    
    #Changing checkpoint to load model from. 
    dump_dirs = [f.path for f in os.scandir(dump_path) if f.is_dir()]
    dump_dirs.sort()
    checkpoint_path = os.path.join(dump_dirs[0] if len(dump_dirs)>0 else dump_path, 'checkpoint.pth')
    #assert os.path.isfile(checkpoint_path)
    train_command = replace_arg(train_command, checkpoint_path, '--reload_model')
    
    #Removing useless directories of previous run. 
    for j in range(1, len(dump_dirs)) :
        command = 'rm -r '+dump_dirs[j]
        if delete_old :
           print(command)
           execute(command)
    
    return train_command

   
parser = argparse.ArgumentParser()
parser.add_argument('--command', help='Path to file having the command to execute for training.')
parser.add_argument('--n_reps', type=int, help='Number of times to loop through all splits. One split+common files are used in a single "run".')
parser.add_argument('--delete_old', action='store_true', help='If this flag is provided, all folders in --dump_path except the one for the first GPU , are deleted for all the previous runs.')

args = parser.parse_args()

with open(args.command) as f :
    train_command = f.read()
    print(train_command)
    train_command = train_command.strip()
    train_command = train_command.replace('\\\n','')
    print(train_command)

train_parser = get_parser()
initial_command, train_command = train_command.split('--',1)
train_command = '--'+train_command
print(train_command)
train_args = train_parser.parse_args(train_command.split())
original_dp = train_args.data_path

#Assigning new data path where all common files+files from one split will be stored, in each run.
#This directory stays same the --data_path; new files are brought in and old files removed each run.
cur_dp = './cur_data_path/'
train_command = replace_arg(train_command, cur_dp, '--data_path')
if not os.path.isdir(cur_dp):
    os.mkdir(cur_dp)

common_files = shift_files(original_dp, cur_dp)

#Making new run-wise dump paths for experiment. Nested within the dump_path provided in command.
#E.g. :- --dump_path/run0/ , --dump_path/run1/ .. and so on.
new_dump_path = os.path.join(get_arg(train_command, '--dump_path'), 'run0')
train_command = replace_arg(train_command, new_dump_path, '--dump_path')
if not os.path.isdir(new_dump_path) :
    os.makedirs(new_dump_path)
    
tot_splits = 0
for j in range(args.n_reps) :
    i=0
    while True :
        if i!=0 :
            shift_files(cur_dp, split_file_dir, split_i_files)
        split_file_dir = os.path.join(original_dp, 'split'+str(i))
        
        if not os.path.isdir(split_file_dir) :
            if j==0 :
                tot_splits = i
            break
        
        split_i_files = shift_files(split_file_dir, cur_dp)
        if i!=0 or j!=0 :
            train_command = get_new_dump(train_command, i+j*tot_splits, args.delete_old)
            
        final_command = initial_command+train_command
        print(final_command)
        execute(final_command)
        i=i+1
    
shift_files(cur_dp, original_dp, common_files)

