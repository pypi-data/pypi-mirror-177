from setuptools import setup
setup(name="ASRscsvmv",
version="0.1.2",
description="This package recognizes and translates your words",
long_description="""
INSTALL THIS PACKAGE USING 
pip install ASRscsvmv
to run this just type 
from ASRscsvmv import asrscsvmv
""",
author="SCSVMV 22-23 PROJECT 17",
packages=['ASRscsvmv'],
install_requires=['vosk','PySimpleGUI','argostranslate','streamlit','pyaudio'])