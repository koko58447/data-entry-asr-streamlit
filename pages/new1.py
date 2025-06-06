import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import speech_recognition as sr
from pymongo import MongoClient
import os
import module as md

# ဓာတ်ပုံသိမ်းမယ့် folder ဖန်တီး
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize session_state
for field in ['name', 'father_name', 'mother_name', 'nrc', 'address', 'note']:
    if field not in st.session_state:
        st.session_state[field] = ""
    if f"audio_key_{field}" not in st.session_state:
        st.session_state[f"audio_key_{field}"] = 0

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["voice_form_db"]
collection = db["users"]

# Save Data to MongoDB
def save_to_mongodb(data):
    collection.insert_one(data)

def clean_text():
    for field in ['name', 'father_name', 'mother_name', 'nrc', 'address', 'note']:
        st.session_state[field] = ""
    # Image widgets တွေကို reset (မဖျက်ဘဲ session_state မှာမရှိရင် skip လုပ်)
    if "camera_input" in st.session_state:
        del st.session_state["camera_input"]
    if "upload_input" in st.session_state:
        del st.session_state["upload_input"]
    if "img" in st.session_state:
        del st.session_state["img"]

    # Rerun
    st.rerun()
    

# UI Layout
st.subheader("🎙️ Voice Form - New Entry")

updated_data = {}

labels = {
    "name": "အမည်",
    "father_name": "အဖအမည်",
    "mother_name": "အမိအမည်",
    "nrc": "မှတ်ပုံတင်အမှတ်",
    "address": "နေရပ်လိပ်စာ",
    "note": "မှတ်ချက်"
}

cola, colb = st.columns([3, 2])

with cola:
    for field, label in labels.items():
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(label, value=st.session_state[field], key=f"{field}_input",icon="♻️")
            updated_data[field] = user_input
        with col2:
            st.write("<br>", unsafe_allow_html=True)
            md.record_audio_and_update(field)

    if st.button("💾 သိမ်းဆည်းမည်"):
        # img ကို sidebar ကနေယူ
        img = st.session_state.get("img", None)

        pic_path = None

        # Image ရှိလားစစ်
        if img is not None:
            filename = f"{st.session_state.name.replace(' ', '_')}.jpg" if st.session_state.name else "image.jpg"
            pic_path = os.path.join(UPLOAD_FOLDER, filename)

            # Image ကိုသိမ်း
            with open(pic_path, "wb") as f:
                f.write(img.getvalue())

            # Add to data
            updated_data["pic_path"] = pic_path

            st.success(f"📸 ဓာတ်ပုံကို `{pic_path}` သို့သိမ်းပြီးပြီ!")

        if updated_data is None:
            st.error("⚠️ အမည် ထည့်ပေးပါ။")           
        else:
             # Save to MongoDB
            save_to_mongodb(updated_data)
            clean_text()
            st.success("✅ သိမ်းဆည်းပြီးပြီ။")



       

with st.sidebar:
    st.header("📷 ဓာတ်ပုံရိုက်ခြင်း")
    with st.expander("Photo"):

    
        pic = st.camera_input("📷 ဓာတ်ပုံရိုက်ရန်", key="camera_input")
        bro = st.file_uploader("📷 ဓာတ်ပုံတင်ရန်", type=["jpg", "jpeg", "png"], key="upload_input")

        # ဓာတ်ပုံကို img ထဲသို့သိမ်း
        img = None
        if pic:
            img = pic
        elif bro:
            img = bro

        st.session_state['img'] = img  # session_state မှာသိမ်းထား

with colb:
    if 'img' in st.session_state and st.session_state.img is not None:
        st.image(st.session_state.img, caption="ဓာတ်ပုံ", use_container_width=True)
        st.success("📷 ဓာတ်ပုံကိုဘယ်သို့သိမ်းပြီးပြီ။")
    else:
        st.info("⚠️ ဓာတ်ပုံမရှိပါ။")