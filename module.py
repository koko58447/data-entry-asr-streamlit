# mymodule/audio_utils.py

import streamlit as st
from pymongo import MongoClient
import pandas as pd
import io
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import speech_recognition as sr

def record_audio_and_update(field_name):
      # Ensure session_state keys exist
    if f"audio_key_{field_name}" not in st.session_state:
        st.session_state[f"audio_key_{field_name}"] = 0

    # Audio Recorder UI
    audio = audio_recorder(
        text="",
        recording_color="#FF0000",
        neutral_color="#1B7B3DFF",
        icon_size="3x",
        key=f"audio_recorder_{field_name}_{st.session_state[f'audio_key_{field_name}']}"
    )

    if audio is not None:
        try:
            # Convert audio bytes to file-like object
            audio_file = BytesIO(audio)
            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            # Recognize Myanmar language
            text = recognizer.recognize_google(audio_data, language="my-MM")

            # Update session_state and increment key to reset recorder
            st.session_state[field_name] = text
            st.session_state[f"audio_key_{field_name}"] += 1

            # Rerun to reflect changes
            st.rerun()

        except sr.UnknownValueError:
            st.error("⚠️ error။")
        except sr.RequestError as e:
            st.error(f"⚠️ error: {e}")
            
# Export to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# export to excel
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

#delete session

def delete_session():
    for key in ['name', 'father_name', 'mother_name', 'nrc', 'address', 'note','img']:
            if key in st.session_state:
                del st.session_state[key]