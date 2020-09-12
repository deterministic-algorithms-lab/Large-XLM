import re
import os

def ensure_exists(filepath, search_in) :
    if filepath.find('/')==-1 :
        return 
    
    dir_to_search = '/'.join(filepath.split('/')[:-1])
    dir_to_search = os.path.join(search_in, dir_to_search)
    
    if not os.path.isdir(dir_to_search) :
        print("Making directory : ", dir_to_search)
        os.makedirs(dir_to_search)

def remove_split(filename) :
    if filename.startswith('train.') or filename.startswith('valid.'):
        filename = filename[6:]
    elif filename.startswith('test.') :
        filename = filename[5:]
    elif filename.startswith('dev.') :
        filename = filename[4:]
    return filename

def get_lang(filename) :
    if len(filename)>=8 and bool(re.match('..-..\...',filename[-8:])) :
        return filename[-2]+filename[-1]
    elif len(filename)>=7 and bool(re.match('..\.mono', filename[-7:])) :
        return filename[-7]+filename[-6]
    else :
        raise ValueError('Filename '+filename+' should end with a string of form \'lg.mono\' or \'lg-lg.lg\' to be applied BPE on.')

def execute(command) :
    x = os.system(command)
    if x>>8!=0 : 
        exit(1)
