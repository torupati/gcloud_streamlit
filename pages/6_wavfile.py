import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def plot_waveform(audio_file):
    """plot wave form of audio file"""
    try:
        y, sr = librosa.load(audio_file)
        fig, ax = plt.subplots()
        librosa.display.waveshow(y, sr=sr, ax=ax)
        ax.set(title='Waveform')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error：{e=}")

if "user" not in st.session_state:
    st.warning("Please login")
    #st.markdown("[login page](/)") # link to app.py
    st.stop()
else:
    st.title("WAVE file")

    uploaded_file = st.file_uploader("Upload wav file", type=["wav"])

    if uploaded_file is not None:
        plot_waveform(uploaded_file)

