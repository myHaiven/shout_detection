import librosa
import soundfile as sf
import matlab.engine
from pathlib import Path
import os
import pandas as pd
from pydub import AudioSegment
import numpy as np

def VAD(file):
  eng = matlab.engine.start_matlab()
  
  # lower the sampling rate for VAD
  new_rate, sr = librosa.load(file, sr = 16000 )
  sf.write('./data/stereo_file.wav', new_rate, 16000)
  
  # extract features
  extracted = eng.vad_func('./data/stereo_file.wav', nargout=3)
  
  mode = 2          # 0 : ACAM3, 1 : bDNN, 2 : DNN, 3 : LSTM
  threshold = 0.4   # threshold for hard decision
  output_type = 1   # 0 : frame based prediction, 1: sample based prediction
  is_default = 1    # 0 : use trained model, 1: use default model
  
  Path('./result').mkdir(exist_ok=True)
  
  # run features though DNN
  os.system(f'python3 ./lib/python/VAD_test.py -m {mode} -l {int(extracted[0])} -d {is_default} --data_dir=./sample_data --model_dir=./saved_model --norm_dir=./norm_data')
  
  # plot the predictions and return a binary classification
  results = eng.plot_preds('./data/stereo_file.wav', threshold, output_type, extracted[1], extracted[2])
  
  results = np.array(results._data)
  
  newResults = []
  
  # replace true values with int equlvalents
  for i,result in enumerate(results):
    if result == True:
      newResults.append(1)
    else:
      newResults.append(0)
  
  # calculate the points at which the signal moved from activated to deactivated, vice versa
  swap_points = []
  for i,label in enumerate(newResults):
    if i == len(newResults)-1:
        swap_points.append(0)
        break
    if newResults[i] == 0 and newResults[i+1] == 1:
        swap_points.append(1)
    elif newResults[i] == 1 and newResults[i+1] == 0:
        swap_points.append(2)
    else:
        swap_points.append(0)
  
  audio = AudioSegment.from_file('./data/stereo_file.wav')
  
  time = np.linspace(0,audio.duration_seconds,len(newResults))
  
  vocal_activity_df = pd.DataFrame(
      {'activity': newResults,
       'change': swap_points,
       'time': time
      })
  
  return(vocal_activity_df)