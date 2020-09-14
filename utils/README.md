# Processing and Training on Large Datasets - An Example

Initial dataset in the format :-
```
bpe_codes
vocab
|
data/
|  mono/
|  |  lg1.mono
|  |  lg2.mono
|  |  ...
|  |  
|  para/
|     lg1-lg2.lg1
|     lg1-lg2.lg2
|     ...
|     
splitted/
processed/
binarized/
```
Note that , if there ```lg1-lg2``` is a prefix of any file name in ```para/``` , then ```lg1``` must be alphabetically smaller than ```lg2``` .

**Don't keep any unnecessary files in ```data/``` folder , or they will be processed in the same way as the rest too.**

1.) Shuffle dataset if needed. Only datasets with ```.mono``` extension will be shuffled. Files are shuffled in-place.

```
python3 shuffler.py --data_dir ../data/
```

2.) Split the data files into train, valid, test sets.  
```
python3 splitter.py ../splitted/ ../data/ --split_bigfiles 20 --delete_old
```
Due to the above command, all files in folder ```../data/``` (and in its subfolders too, recursively) are splitted and stored in ```../splitted/``` folder directly, 
or under a ```split-i/``` folder. Any file bigger than 1000000 lines is split into 20 equal parts which are stored in ```split0/, split1/, ... split19/``` folders.
The original files in ```../data/``` are deleted as ```--delete_old``` flag is there. Files(in ```../data/```) having 'train.', 'test.', 'valid.', 'dev.' in their front, are not splitted, and just moved.  

File format after splitting :
```
bpe_codes
vocab
|
data/
|  mono/
|  para/
|
splitted/
|  split0/
|  |  train.lg1.mono
|  |  train.lg2.mono
|  |  ... 
|  split1/
|  |  train.lg1.mono
|  |  train.lg2.mono
|  |  ...
|  ...
|  split19/
|  |  train.lg1.mono
|  |  train.lg2.mono
|  |  ...
|  train.lg1-lg2.lg1
|  train.lg1-lg2.lg2
|  valid.lg1-lg2.lg1
|  valid.lg1-lg2.lg2
|  test.lg1-lg2.lg1
|  test.lg1-lg2.lg2
|  ... 
| 
processed/
binarized/
```
To chage the number of lines in test/valid sets, edit here .

3.) **Apply BPE using proper codes to all the splitted files.** 
```
python3 applybpe --fast_path ../tools/FastBPE/fast --out_path ../processed/ --bpe_path ../bpe_codes --data_path ../splitted/ --maintain_fs --delete_old
```
The ```--maintain_fs``` flag ensures that the data files aren't all put directly in ```../processed``` folder, and that the file structure remains the same as in ```../splitted/```.
```--fast_path``` is used to provide the path to the ```FastBPE```'s script. See [here](https://github.com/deterministic-algorithms-lab/Large-XLM#1-preparing-the-data).

4.) **Binarize all the splitted files , in one go.** 
```
python3 binarize.py --in_path ../processed/ --out_path ../binarized/ --vocab_path ../vocab --xlm_path ../XLM/ --delete_old
```
All files in ```../processed/``` are binarized(==pickled), and put into ```../binarized/``` . Initial file structure, before this command, must folllow the splitted format,
or should have all files directly under ```../processed/```.

5.) **Do split-wise training for big files which have been splitted.**

The usual training command( see [here](https://github.com/deterministic-algorithms-lab/Large-XLM/#1-preparing-the-data) )
is provided in the ```--command``` argument.
In the command below, we first train on data in ```split0/``` + data directly under the ```data_path``` provided in the command that is provided in ```--command``` argument,
then on data in ```split1/``` + data directly under the ```data_path``` provided in the command that is provided in ```--command``` argument , and  so on uptil ```splitn/```.
This process is repeated ```--n_reps``` times.

```
python3 ../split_trainer.py --command "usual-command(CUDA_VISIBLE_DEVICES=0,1 python ../train.py all usual arguments)" --n_reps 4
```
```--data_path``` in original command must correspond to directory having binarized data in format of the splitted file tree. Currently, early stopping, based on ```n_reps```
is not supported, but will be in future.

**It is best to comment all ```execute()/os.system()``` calls first, and see all the commands printed; confirm their correct-ness, and then uncomment the ```execute()/os.system()``` calls, and execute the files. Especially if you are using ```--delete_path``` .**


## Making Vocabularies For Large Multi-Lingual Datasets

1.) **Learns BPE codes(from mono files), split files, apply BPE to all files using corresponding BPE codes, make vocabularies. All language wise.**

```
python3 make_bpe_vocab.py --data_path ../data --n_codes <num of BPE codes to learn> --fast_path ../tools/fastBPE/fast --codes_dir ../data/codes \
                          --vocab_dir ../data/vocab/ --delete_old
```
Modify [this line](https://github.com/deterministic-algorithms-lab/Large-XLM/blob/35a957727e338537fed70a8d21d7d03dd0d1927f/utils/make_bpe_vocab.py#L27) to modify how splitting is done. And [this one](https://github.com/deterministic-algorithms-lab/Large-XLM/blob/35a957727e338537fed70a8d21d7d03dd0d1927f/utils/make_bpe_vocab.py#L33) for changing how BPE is applied.

2.) **Join together the various vocabularies into single one.**

```
python3 join_vocab --vocab_path ../data/vocab/ --final_vocab_path ../vocab --top_k 20000
```
The above commands joins vocabularies of all languages seperately & top 20000 words from each language make into the final vocabulary stored in the file name given in ```---final_vocab_path``` argument. If ```--absolute_top_k``` flag had been added, then top 20000 most frequent words, in the combination of vocabularies of all languages would have been chosen. 

```
python3 join_vocab --vocab_path ../data/vocab/ --final_vocab_path ../vocab --top_k 25000 --lg_k_dict 'en-20000-de-21000'
```
If the above command is used, then top 25000 most frequent words of each language, except English and German, are stored in the final vocabulary. For English , only top 20000 most frequent words make into the final vocabulary and similarly only top 21000 for German.

Note :- The final bpe_codes for the entire multilingual dataset can be found by concatenating bpe_code files of all languages, using the ```cat``` command.
