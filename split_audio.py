import torchaudio
import glob, tqdm

for fi in tqdm.tqdm(glob.glob("AUDIO/*")):
     if "Silent" in fi or "others" in fi:
          continue
     w, sr = torchaudio.load(fi)
     segment = int(w.size(1)/(sr*3))
     for i in range(segment):
          audio = w[:,i*sr*3:(i+1)*sr*3]
          torchaudio.save(fi.replace("AUDIO","AUDIO3S").replace(".wav", "_" + str(i) + ".wav").replace(",","").replace(" ","_"), audio, 16000)