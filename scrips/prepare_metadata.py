import os
from metadata import metadata
from glob import glob
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


digit_text = ['zero','one','two','three','four','five','six','seven','eight','nine']

base_path = "<KALDI_BASE>/egs/digits"
data_folder = "data"
recording_folder = "recordings"
spk2gender_file = "spk2gender"
ut_id_to_wav_file ="wav.scp"
text_file = "text"
ut2psk_file = "utt2spk"
corpus_file = "corpus.txt"
local_folder = "local"



def prepare_gender(dataset_folder):
    file_path = os.path.join(base_path,data_folder,dataset_folder,spk2gender_file)
    with open(file_path,'w') as f:
        for k,v in metadata.items():
            f.write("{} {}\n".format(k,v['gender'][0]))

def prepare_utterence_id(dataset_folder):
    wav_folder = os.path.join(base_path,data_folder,dataset_folder,recording_folder)
    root.info(wav_folder)
    files = glob(wav_folder+"/**.wav")
    files = sorted(files)
    file_path = os.path.join(base_path, data_folder, dataset_folder, ut_id_to_wav_file)
    with open(file_path, 'w') as f:
        for wav_file in files:
            f.write("{} {}\n".format(wav_file.split("/")[-1].split(".")[0], wav_file))

def prepare_text(dataset_folder):
    id_to_wav_file_path = os.path.join(base_path, data_folder, dataset_folder, ut_id_to_wav_file)
    ids = [a.split(" ")[0] for a in open(id_to_wav_file_path).read().strip("\n").split("\n")]
    text_file_path = os.path.join(base_path, data_folder, dataset_folder, text_file)
    with open(text_file_path, 'w') as f:
        for id in ids:
            sentence = " ".join([digit_text[int(d)] for d in  id.split("-")[1].split("_")])
            f.write("{} {}\n".format(id,sentence))


def ut2psk(dataset_folder):
    id_to_wav_file_path = os.path.join(base_path, data_folder, dataset_folder, ut_id_to_wav_file)
    ids = [a.split(" ")[0] for a in open(id_to_wav_file_path).read().strip("\n").split("\n")]
    ut2psk_file_path = os.path.join(base_path, data_folder, dataset_folder, ut2psk_file)
    with open(ut2psk_file_path, 'w') as f:
        for id in ids:
            speaker = id.split("-")[0].split("_")[0]
            f.write("{} {}\n".format(id, speaker))
def create_corpus(dataset_folder):
    text_file_path = os.path.join(base_path, data_folder, dataset_folder, text_file)
    utts = [a[a.find(" ")+1:] for a in open(text_file_path).read().strip("\n").split("\n")]
    corpus_file_path  = os.path.join(base_path, data_folder,local_folder, corpus_file)
    with open(corpus_file_path, 'a') as f:
        for ut in utts:
            f.write(ut+"\n")

def main():
    prepare_gender('train')
    prepare_gender('test')
    prepare_utterence_id('train')
    prepare_utterence_id('test')
    prepare_text('train')
    prepare_text('test')
    ut2psk('train')
    ut2psk('test')
    corpus_file_path = os.path.join(base_path, data_folder, local_folder, corpus_file)
    if os.path.exists(corpus_file_path):
        os.remove(corpus_file_path)
    create_corpus('train')
    create_corpus('test')

if __name__=="__main__":
    main()