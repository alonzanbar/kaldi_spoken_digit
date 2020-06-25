# kaldi_spoken_digit

#### Simple scripts to create a toy dataset for experimenting KALDI 

1. git clone git@github.com:Jakobovski/free-spoken-digit-dataset.git to some folder outside the repo
2. change :
    - modify : prepare_dataset.py
        - base_path = "<source recording folder>"
        - base_path_output = "<KALDI_BASE>/egs/digits/data"
    - run python prepare_dataset.py
    - review the files created in the <KALDI_BASE>/egs/digits/data/train/recording , 
    <KALDI_BASE>/egs/digits/data/test/recording
    - modify prepate_metadata.py
        - base_path = "<KALDI_BASE>/egs/digits"
    - run pyton prepate_metadata.py
    
