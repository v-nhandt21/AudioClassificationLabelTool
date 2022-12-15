from ast import keyword
from re import S
from numpy import place
import streamlit as st
import random
import glob, os
from annotated_text import annotated_text
import json, random
from PIL import Image
# from streamlit import caching

# st.set_page_config(layout="wide")

# if "visibility" not in st.session_state:
st.session_state.visibility = "visible"
st.session_state.horizontal = True

cur_dir = os.path.dirname(os.path.realpath(__file__))

audios_total = glob.glob(cur_dir + "/AUDIO3S/*.wav")

if 'audios' not in st.session_state:
     st.session_state.audios = []
else:
     st.session_state.audios = []

user_file = cur_dir + "/Database/data.json"

if not os.path.isfile(user_file):
     user_data = {}
     for audio in audios_total:
          idx = audio
          user_data[idx] ={"event": "", "labeled": 0}
     with open(user_file, 'w+', encoding='utf-8') as fw:
          json.dump(user_data, fw, ensure_ascii=False, indent=4)

f = open(user_file)
user_data = json.load(f)

count = 0
for k, v in user_data.items():
     if v['labeled'] == 0 and count<50:
          count += 1
          st.session_state.audios.append(k)
     else:
          continue
     f.close()


st.title("Sound Event Testset")

event_Mapping = {'Motor vehicle (road)': 0, 'Screaming': 1, 'Explosion': 2, 'Female speech': 3, 'Male speech': 4, 'Breaking': 5, 'Crowd': 6, 'Crying, sobbing': 7, 'Siren': 8, 'Gunshot, gunfire': 9, "Remove":10,"":11}

finish = False

if not finish:

     for no, audio in enumerate(st.session_state.audios):

          # image = Image.open('/home/nhandt23/Desktop/TTS/08_Evaluation/DCASE/IMAGE/image.png')

          idx = audio
          text_id = idx.split("/")[-1].replace(".wav","")

          if text_id.split("-")[0] == "Male_speech" or text_id.split("-")[0] == "Female_speech":
               continue 

          st.markdown("""---""")

          col0, col1 = st.columns([20,4])

          # st.image(image)
          annotated_text(st,("Default: " + text_id.split("-")[0], "", "#f7eb0a"))
          
          col0.audio(audio, format="audio/wav", start_time=0)

          user_data[idx]["event"] = st.radio("Event: ", tuple(event_Mapping.keys()), horizontal=True, key=str(no)+"event", index=event_Mapping[user_data[idx]["event"]])

          col0, col1, col2 = st.columns([20,13,7])
          if user_data[idx]["event"] != "":
               annotated_text(col0,("Labeled", "", "#02cf13"))
               user_data[idx]["labeled"] = 1
          else:
               annotated_text(col0,("Unlabeled", "", "#fc2c03"))

     if st.button('Submit / Save'):
          with open("Database/data.json", 'w+', encoding='utf-8') as fw:
               json.dump(user_data, fw, ensure_ascii=False, indent=4)
          fw.close()
          finish =True
          # st.experimental_rerun()

if finish:
     annotated_text(st,("Save! Thank you", "", "#00ff00"))
     count = 0
     for audio in sorted(st.session_state.audios)[:]:
          idx = audio

          if user_data[idx]["labeled"] != 0:
               count+= 1
     annotated_text(st,(str(count) + " labeled audios - " + str(len(st.session_state.audios)-count) + " audios left", "", "#eb500e"))