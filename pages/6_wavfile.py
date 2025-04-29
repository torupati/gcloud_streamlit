import streamlit as st
#import librosa
#import librosa.display
import wave
import matplotlib.pyplot as plt
import numpy as np

def plot_waveform(audio_file):
    """Plot wave form of audil file"""
    try:
        with wave.open(audio_file, "rb") as wf:
            num_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            frame_rate = wf.getframerate()
            num_frames = wf.getnframes()
            frames = wf.readframes(num_frames)

            # データを数値に変換
            if sample_width == 2:
                audio_data = np.frombuffer(frames, dtype=np.int16)
            elif sample_width == 1:
                audio_data = np.frombuffer(frames, dtype=np.uint8) - 128
            else:
                st.error(f"not supported {sample_width=}")
                return

            if num_channels == 2:
                audio_data = audio_data[::2]

            time = np.arange(0, num_frames) / frame_rate

            fig, ax = plt.subplots()
            ax.plot(time, audio_data)
            ax.set(xlabel="Time (s)", ylabel="Amplitude", title="Waveform")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"{e=}")

#def plot_waveform(audio_file):
#    """plot wave form of audio file"""
#    try:
#        y, sr = librosa.load(audio_file)
#        fig, ax = plt.subplots()
#        librosa.display.waveshow(y, sr=sr, ax=ax)
#        ax.set(title='Waveform')
#        st.pyplot(fig)
#    except Exception as e:
#        st.error(f"Error：{e=}")

if "user" not in st.session_state:
    st.warning("Please login")
    #st.markdown("[login page](/)") # link to app.py
    st.stop()
else:
    st.title("WAVE file")

    uploaded_file = st.file_uploader("Upload wav file", type=["wav"])

    if uploaded_file is not None:
        plot_waveform(uploaded_file)

