import io
import os
import streamlit as st
import requests
import glob
import time
from PIL import Image
from gtts import gTTS
from googletrans import Translator
from model import get_caption_model, generate_caption


translator = Translator()
try:
    os.mkdir("temp")
except:
    pass


@st.cache(allow_output_mutation=True)
def get_model():
    return get_caption_model()

caption_model = get_model()


def predict():
    
    text = generate_caption('tmp.jpg', caption_model)

    st.markdown('#### Predicted Captions:')
    st.write(text)

    out_lang = st.selectbox("Select your output language",
    ("English", "Hindi", "Bengali", "korean", "Chinese", "Japanese"),)
    if out_lang == "English":
        output_language = "en"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "korean":
        output_language = "ko"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Japanese":
        output_language = "ja"

    def text_to_speech(output_language, text):
        translation = translator.translate(text, src='en', dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language,slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    if st.button("convert"):
        result, output_text = text_to_speech(output_language, text)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

    display_output_text = st.checkbox("Display output text")

    if display_output_text:
        st.markdown(f"## Output text:")
        st.write(f" {output_text}")
   
st.title('Image Captioner')

img_upload = st.file_uploader(label='Upload Image', type=['jpg', 'png', 'jpeg'])

if img_upload != None:
    img = img_upload.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert('RGB')
    img.save('tmp.jpg')
    st.image(img)
    predict()
    os.remove('tmp.jpg')

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)