import streamlit as st
from pymongo import MongoClient
import pandas as pd

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

# Delete Record
def delete_record(data):
    collection.delete_one(data)

st.title("🗑️ ဖျက်မည်")

df = load_from_mongodb()
if df.empty:
    st.warning("⚠️ ဖျက်ရန်အချက်အလက်မရှိပါ။")
else:
    selected_nrc = st.selectbox("ဖျက်မည့်မှတ်ပုံတင်အမှတ်ကိုရွေးပါ", df['nrc'].unique())
    confirm = st.checkbox("ဖျက်ရန်သေချာပါသလား?")

    if confirm and st.button("❌ ဖျက်မည်"):
        target = df[df['nrc'] == selected_nrc].to_dict(orient='records')[0]
        delete_record(target)
        st.success("✅ ဖျက်ပြီးပြီ!")