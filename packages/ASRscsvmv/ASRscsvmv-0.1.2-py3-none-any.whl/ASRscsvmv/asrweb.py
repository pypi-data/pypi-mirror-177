import argostranslate.package, argostranslate.translate
import pyaudio
import streamlit as st
from vosk import KaldiRecognizer, Model


FRAMES_PER_BUFFER = 8196
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
model = Model(model_name="vosk-model-small-en-in-0.4")
rec = KaldiRecognizer(model, RATE)
mic = pyaudio.PyAudio()

stream = mic.open(rate = RATE,channels = CHANNELS,format = FORMAT,input=True,frames_per_buffer=8192)
stream.start_stream()

import argostranslate.translate,argostranslate.package

from_code = "en"
to_code = "hi"
argostranslate.package.update_package_index()
# Download and install Argos Translate package
available_packages = argostranslate.package.get_available_packages()
available_package = list(filter(lambda x: x.from_code == from_code and x.to_code == to_code, available_packages))[0]
download_path = available_package.download()
argostranslate.package.install_from_path(download_path)

# Translate
installed_languages = argostranslate.translate.get_installed_languages()
from_lang = list(filter(lambda x: x.code == from_code,installed_languages))[0]
to_lang = list(filter(lambda x: x.code == to_code,installed_languages))[0]
translation = from_lang.get_translation(to_lang)

def start_listening():
	st.session_state['run'] = True
	st.write("start speaking")
	while True:
		
		data = stream.read(15000)
		if rec.AcceptWaveform(data):
			text = rec.Result()[14:-3]
			st.write(text)
			translatedText = translation.translate(text)
			st.write(translatedText)

def stop_listening():
	st.session_state['run'] = False
	


st.title('Get real-time transcription')

start, stop = st.columns(2)
start.button('Start listening', on_click=start_listening)

stop.button('Stop listening', on_click=stop_listening)
