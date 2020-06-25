from glob import glob
from pydub import AudioSegment
import pandas as pd
import numpy as np
import functools as ft
import os


base_path = "<source recording folder>"
base_path_output = "<KALDI_BASE>/egs/digits/data"


def to_playlist(files_list):
    signal_list = [[AudioSegment.from_wav(a), AudioSegment.silent()] for a in files_list]
    flatten = [item for sublist in signal_list for item in sublist]
    return ft.reduce(lambda x, y: x.append(y, crossfade=(20)), flatten)

def create_sentences_from_digits(number_of_samples, length, dataset_folder):
    files = [(a.split("/")[-1], a) for a in glob(base_path + "/**.wav")]
    df_files = pd.DataFrame(files)
    df = pd.concat([df_files, df_files[0].str.split("_", expand=True)], axis=1).iloc[:, 0:4]
    df.columns = ['file', 'file_path', 'digit', 'speaker']
    file_names = {}
    for i in range(number_of_samples):
        speaker = np.random.choice(df['speaker'].unique())
        to_sentence = df[df['speaker'] == speaker].sample(length)
        file_name = "{}_{}".format("_".join(to_sentence['digit'].tolist()), speaker)
        if file_name in file_names:
            file_names[file_name] += 1
        else:
            file_names[file_name] = 1
        path = os.path.join(base_path_output, dataset_folder,'recordings')
        os.makedirs(path,exist_ok=True)
        file_name_ex = "{}/{}_{}.wav".format(path, file_name, file_names[file_name])
        merged_audio = to_playlist(to_sentence['file_path'].tolist())
        with open(file_name_ex, 'wb') as out_f:
            merged_audio.export(out_f, format='wav')


if __name__ == "__main__":
    create_sentences_from_digits(1000, 3, 'train')
    create_sentences_from_digits(200, 3, 'test')
