from VAD import VAD
from pydub import AudioSegment
from pathlib import Path  # For writing videos into the data folder

def split_vad(audio_file, name):
  
  # create a folder to hold processed files
  path = f"./finished/{name}"
  Path(path).mkdir( exist_ok=True)

  # run analysis
  vad_results = VAD(audio_file)
  
  audio = AudioSegment.from_wav(audio_file)
  
  # Split on detections 

  # get timestamps of activations and deactivatins
  timestamp = []
  for i,swap in enumerate(vad_results["change"]):
    if swap != 0:
      timestamp.append(vad_results.iloc[i]["time"])
  
  # split on the time stamps
  names = []
  for  i in range(0,len(timestamp)+1,2):
      #break loop if at last element of list
      if i == len(timestamp)-1:
        audio_chunk=audio[timestamp[i]*1000:timestamp[-1]]
        audio_chunk.export( f"{path}/vad{i}.wav", format="wav")
        names.append(f"{path}/vad{i}.wav")
      elif i != len(timestamp):
        audio_chunk=audio[timestamp[i]*1000:timestamp[i+1]*1000]
        audio_chunk.export( f"{path}/vad{i}.wav", format="wav")
        names.append(f"{path}/vad{i}.wav")
  
  #recombine to get the full version
  to_join = [AudioSegment.from_file(file) for file in names ]
  joined_file = sum(to_join)
  joined_file.export(f"{path}/full.wav", format="wav")

pathlist = Path("C:/Users/Paige/Documents/VAD/K3r3TKmWZkA").glob('**/*.wav')
for i,path in enumerate(pathlist):
    split_vad(str(path),f"K3r3TKmWZkA_{i+21}")
