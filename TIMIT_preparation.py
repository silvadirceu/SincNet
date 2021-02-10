#!/usr/bin/env python3

# TIMIT_preparation 
# Mirco Ravanelli 
# Mila - University of Montreal 

# July 2018

# Description: 
# This code prepares TIMIT for the following speaker identification experiments. 
# It removes start and end silences according to the information reported in the *.wrd files and normalizes the amplitude of each sentence.
 
# How to run it:
# python TIMIT_preparation.py $TIMIT_FOLDER $OUTPUT_FOLDER data_lists/TIMIT_all.scp 

# NOTE: This script expects filenames in lowercase (e.g, train/dr1/fcjf0/si1027.wav" rather than "TRAIN/DR1/FCJF0/SI1027.WAV)


import shutil
import os
import soundfile as sf
import numpy as np
import sys

def createDirectory(path):
	try:
		os.makedirs(path, exist_ok=True)
		return True
	except OSError:
		print ("Creation of the directory %s failed" % path)
		return False

def getPathFileNameExt(filepath):

	path = []
	filename = []
	basename = []
	ext = []

	if isinstance(filepath, str):
		path, filename = os.path.split(filepath)
		basename,ext = os.path.splitext(filename)
	else:
		for file in filepath:
			p,f = os.path.split(file)
			b,e = os.path.splitext(f)

			path.append(p)
			filename.append(f)
			basename.append(b)
			ext.append(e)

	return path,filename,basename,ext

def sph2wav(timitpath="./timit/train/", ext='*.wav'):
 import glob
 from sphfile import SPHFile

 path_timit=os.path.join(timitpath, ext)
 files = glob.glob(path_timit,recursive=True)

 #files = [files[3]]

 for wav_file in files:

     print(wav_file)
     # create fileout
     path,filename,basename,ext = getPathFileNameExt(wav_file)
     root_ext = path.split("/")
     root = os.path.join(*root_ext[:-4])
     #dirbase = os.path.join(*root_ext[-3:])
     filetemp = os.path.join(*['/',root,'temp.wav'])

     #dirout = os.path.join(root_ext[-4]+'2',dirbase)
     #fileout = os.path.join(*['/',root,dirout,filename])
     #ok = createDirectory(dirout)
     #print(ok)

     sph = SPHFile(wav_file)
     '''
     sph.format = {  'sample_rate': 8000,
                     'channel_count': 1,
                     'sample_byte_format': '01',
                     'sample_n_bytes': 2,
                     'sample_sig_bits': 16,
                     'sample_coding': 'pcm'
                   }
     '''

     sr = (sph.format)['sample_rate']
     txt_file = wav_file[:-3] + "txt"
     print(txt_file)

     f = open(txt_file,'r')
     for line in f:
         words = line.split(" ")
         start_time = int(words[0])/sr
         end_time   = int(words[1])/sr
     f.close()

     print("writing file ", filetemp)
     print("start = %.2f - end = %.2f"%(int(words[0]), int(words[1])))
     print("start = %.2f - end = %.2f"%(start_time, end_time))

     sph.write_wav(filetemp,start_time,end_time)
     os.remove(wav_file)
     shutil.move(filetemp,wav_file)


def ReadList(list_file):
 f=open(list_file,"r")
 lines=f.readlines()
 list_sig=[]
 for x in lines:
    list_sig.append(x.rstrip())
 f.close()
 return list_sig

def copy_folder(in_folder,out_folder):
 if not(os.path.isdir(out_folder)):
  shutil.copytree(in_folder, out_folder, ignore=ig_f)

def ig_f(dir, files):
 return [f for f in files if os.path.isfile(os.path.join(dir, f))]

def prepare(in_folder,out_folder,list_file):
    # Read List file
    list_sig = ReadList(list_file)

    # Replicate input folder structure to output folder
    copy_folder(in_folder, out_folder)

    # Speech Data Reverberation Loop
    for i in range(len(list_sig)):
        # Open the wav file
        wav_file = in_folder + '/' + list_sig[i]
        [signal, fs] = sf.read(wav_file)
        signal = signal.astype(np.float64)

        # Signal normalization
        signal = signal / np.max(np.abs(signal))

        # Read wrd file
        wrd_file = wav_file.replace(".wav", ".wrd")
        wrd_sig = ReadList(wrd_file)
        beg_sig = int(wrd_sig[0].split(' ')[0])
        end_sig = int(wrd_sig[-1].split(' ')[1])

        # Remove silences
        signal = signal[beg_sig:end_sig]

        # Save normalized speech
        file_out = out_folder + '/' + list_sig[i]

        sf.write(file_out, signal, fs)

        print("Done %s" % (file_out))


if __name__ == "__main__":

    in_folder=sys.argv[1]
    out_folder=sys.argv[2]
    list_file=sys.argv[3]

    sph2wav(timitpath=in_folder, ext='**/*.wav')

    #prepare(in_folder,out_folder,list_file)