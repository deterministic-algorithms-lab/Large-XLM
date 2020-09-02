# Does split-wise training for big files which have been splitted.
# data_path in original command must correspond to directory having binarized data in format of splitted file tree.
# Usage :- python3 split_trainer.py --command "python train.py ....." --n_reps 4
# The above command loops 4 times through all splits ; each time running command provided with --command
 
import os
import argparse
from train import get_parser

def replace_data_path(train_command, cur_dp) :
    parts = train.command.split('--data_path')
    assert len(parts) == 2
    before_dp, after_dp = parts[0], parts[1]
    after_parts_lis = [cur_dp+' ']+after_dp.split('--')[1:]
    modified_command = before_dp+'--'.join(after_parts_lis)
    return modified_command

def shift_files(source_dir, dest_dir, file_lis=[]) :
    shift_from = file_lis if len(file_lis)>0 else os.listdir(source_dir)
    shifted_files = []
    for filename in  shift_from :
        command = "mv "+os.path.join(source_dir, filename)+' '+os.path.join(dest_dir, filename)
        shift_files.append(filename)
    return shifted_files


parser = argparse.ArgumentParser()
parser.add_argument('--command', help='Command to execute for training.')
parser.add_argument('--n_reps', type=int, help='Number of times to loop through all splits. One split+common files are used in a single run')

args = parser.parse_args()

train_parser = get_parser()
train_command = args.command
initial_command, train_command = train_command.split('--', 1)
train_command = '--'+train_command
train_args = train_parser.parse(train_command)
original_dp = train_args.data_path

cur_dp = './cur_data_path/'
train_command = replace_data_path(train_command, cur_dp)

if not os.path.isdir(cur_dp):
    os.mkdir(cur_dp)
    
common_files = shift_files(original_dp, cur_dp)

for _ in range(args.n_reps) :
    i=0
    while True :
        if i!=0 :
            shift_files(cur_dp, split_file_dir, split_i_files)
        split_file_dir = os.path.join(original_dp, 'split'+str(i))
        if not os.path.isdir(split_file_dir) :
            break
        split_i_files = shift_files(split_file_dir, cur_dp)
        os.system(train_command)
        i=i+1
    
shift_files(cur_dp, original_dp, common_files)

