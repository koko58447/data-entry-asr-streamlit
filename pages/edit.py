import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import speech_recognition as sr
from pymongo import MongoClient
import pandas as pd

# Initialize session_state
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'father_name' not in st.session_state:
    st.session_state.father_name = ""
if 'mother_name' not in st.session_state:
    st.session_state.mother_name = ""
if 'nrc' not in st.session_state:
    st.session_state.nrc = ""
if 'address' not in st.session_state:
    st.session_state.address = ""
if 'note' not in st.session_state:
    st.session_state.note = ""

for field in ['name', 'father_name', 'mother_name', 'nrc', 'address', 'note']:
    if f"audio_key_{field}" not in st.session_state:
        st.session_state[f"audio_key_{field}"] = 0

# Function to handle recording and updating a specific field
def record_audio_and_update(field_name):
    audio = audio_recorder(
        text="",
        recording_color="#FF0000",
        neutral_color="#000000",
        icon_size="2x",
        key=f"audio_recorder_{field_name}_{st.session_state[f'audio_key_{field_name}']}"
    )

    if audio is not None:
        try:
            audio_file = BytesIO(audio)
            r = sr.Recognizer()

            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language="my-MM")
                st.session_state[field_name] = text

                # Refresh key to allow next recording
                st.session_state[f"audio_key_{field_name}"] += 1
                st.rerun()

        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")

# MongoDB Connection
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo"]["uri"])


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["voice_form_db"]
collection = db["users"]

# Load All Data from MongoDB
def load_from_mongodb():
    items = list(collection.find({}, {'_id': 0}))
    return pd.DataFrame(items)


# Update Record
def update_record(old_data, new_data):
    collection.update_one(old_data, {"$set": new_data})

st.title("🖋️ ပြင်ဆင်မည်")

df = load_from_mongodb()
if df.empty:
    st.warning("⚠️ ပြင်ဆင်ရန်အချက်အလက်မရှိပါ။")
else:
    selected_nrc = st.selectbox("ပြင်ဆင်မည့်မှတ်ပုံတင်အမှတ်ကိုရွေးပါ", df['nrc'].unique())

    original_data = df[df['nrc'] == selected_nrc].to_dict(orient='records')[0]

    # for key in original_data:
    #     # st.session_state[f"{key}_input"] = original_data[key]
    #     st.session_state[key] = original_data[key]

    # st.session_state.update({f"{key}": value for key, value in original_data.items()})

    for field, label in {
        "name": "အမည်",
        "father_name": "အဖအမည်",
        "mother_name": "အမိအမည်",
        "nrc": "မှတ်ပုံတင်အမှတ်",
        "address": "နေရပ်လိပ်စာ",
        "note": "မှတ်ချက်"
    }.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text_input(label, value=st.session_state[field], key=f"{field}_input")
        with col2:
            st.markdown('<div class="audio-recorder-wrapper">', unsafe_allow_html=True)
            record_audio_and_update(field)
            st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 ပြင်ဆင်သိမ်းဆည်းမည်"):
        updated_data = {
            "name": st.session_state.name,
            "father_name": st.session_state.father_name,
            "mother_name": st.session_state.mother_name,
            "nrc": st.session_state.nrc,
            "address": st.session_state.address,
            "note": st.session_state.note
        }
        update_record(original_data, updated_data)
        st.success("✅ ပြင်ဆင်ပြီးပြီ!")