
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import io
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import speech_recognition as sr
import module as md

def delete_session():
    for key in ['name', 'father_name', 'mother_name', 'nrc', 'address', 'note','img']:
            if key in st.session_state:
                del st.session_state[key]

for field in ['name', 'father_name', 'mother_name', 'nrc', 'address', 'note']:
    if f"audio_key_{field}" not in st.session_state:
        st.session_state[f"audio_key_{field}"] = 0



# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["voice_form_db"]
collection = db["users"]

# Load Data
def load_data():
    items = list(collection.find({}, {"_id": 1, "name": 1, "father_name": 1, "mother_name": 1, "nrc": 1, "address": 1, "note": 1}))
    return pd.DataFrame(items)

# Update document in MongoDB
def update_data(doc_id, data):
    collection.update_one({"_id": doc_id}, {"$set": data})

# Export to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Session State
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
    st.session_state.selected_id = None

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 8px;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
    }
    .stDataFrame {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px;
    }
            
    .button-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .stButton button {
        width: 100% !important;
        padding: 0.5em 1em !important;
        text-align: center;
        border-radius: 6px !important;
    }
    .stDownloadButton button {
        width: 100% !important;
        padding: 0.5em 1em !important;
        text-align: center;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

st.subheader("📊 သိမ်းဆည်းထားသောအချက်အလက်များ")

# Auto-refresh toggle
auto_refresh = st.checkbox("🔄 အလိုအလျောက် Refresh လုပ်မည်")
if auto_refresh:
    st.rerun()

if not st.session_state.edit_mode:
    df = load_data()

    if not df.empty:
        # Add No and Select columns
        df.insert(0, "စဉ်", range(1, len(df) + 1))
        df.insert(1, "ရွေးပါ", False)
        df.columns = [
            "စဉ်",
            "ရွေးပါ",
            "_id",
            "အမည်",
            "အဖအမည်",
            "အမိအမည်",
            "မှတ်ပုံတင်အမှတ်",
            "လိပ်စာ",
            "မှတ်ချက်",
        ]

        # Search / Filter
        filter_col = st.selectbox("🔍 ရှာဖွေရန် Column", df.columns.tolist())
                # Initialize session_state
        if 'search' not in st.session_state:
            st.session_state.search = ""
        col11,col22=st.columns([4,1])
        with col11:            
            filter_val = st.text_input("🔍 ရှာဖွေရန် စာလုံး", value=st.session_state["search"],icon="🔍")
        with col22:
            st.write("<br>",unsafe_allow_html=True)
            md.record_audio_and_update("search")
        
        if filter_val:
            df = df[df[filter_col].astype(str).str.contains(filter_val, case=False, na=False)]

        # Show DataFrame with all columns
        edited_df = st.data_editor(
            df[["စဉ်", "ရွေးပါ", "အမည်", "အဖအမည်", "အမိအမည်", "မှတ်ပုံတင်အမှတ်", "လိပ်စာ", "မှတ်ချက်"]],
            disabled=["စဉ်", "အမည်", "အဖအမည်", "အမိအမည်", "မှတ်ပုံတင်အမှတ်", "လိပ်စာ", "မှတ်ချက်"],
            use_container_width=True,
            hide_index=True,
        )

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        with col1:
            st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
            edit_btn = st.button("📝 ပြင်မည်")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
            delete_btn = st.button("🗑️ ဖျက်မည်")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            csv = md.convert_df_to_csv(df.drop(columns=["ရွေးပါ", "_id"]))
            st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
            st.download_button(label="📄 CSV", data=csv, file_name='data.csv', mime='text/csv')
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            excel = md.convert_df_to_excel(df.drop(columns=["ရွေးပါ", "_id"]))
            st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
            st.download_button(label="📘 Excel", data=excel, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        if edit_btn:
            delete_session()
            selected_rows = df.loc[edited_df["ရွေးပါ"], :]
            if len(selected_rows) == 1:
                st.session_state.edit_mode = True
                st.session_state.selected_id = selected_rows.iloc[0]["_id"]
                st.rerun()
            else:
                st.warning("⚠️ တစ်ခုတည်းကိုသာရွေးပါ။")

        if delete_btn:
            selected_ids = df.loc[edited_df["ရွေးပါ"], "_id"].tolist()
            if selected_ids:
                collection.delete_many({"_id": {"$in": selected_ids}})
                st.success(f"✅ {len(selected_ids)} ကြိမ်ဖျက်ပြီးပြီ။")
                st.rerun()
            else:
                st.warning("⚠️ ဖျက်မယ့်ဒေတာကိုရွေးပါ။")

    else:
        st.info("⚠️ အချက်အလက်မရှိပါ။")

else:
    # Edit Mode
    doc_id = st.session_state.selected_id
    data = collection.find_one({"_id": doc_id})
    

    if data:
        st.subheader("🖋️ အချက်အလက်ပြင်ဆင်ခြင်း")
        
        if 'name' not in st.session_state:
            st.session_state.name =  data.get("name", "")
        if 'father_name' not in st.session_state:
            st.session_state.father_name =  data.get("father_name", "")
        if 'mother_name' not in st.session_state:
            st.session_state.mother_name = data.get("mother_name", "")
        if 'nrc' not in st.session_state:
            st.session_state.nrc =  data.get("nrc", "")
        if 'address' not in st.session_state:
            st.session_state.address = data.get("address", "")
        if 'note' not in st.session_state:
            st.session_state.note =  data.get("note", "")
        if 'img' not in st.session_state:
            st.session_state.img =  data.get("pic_path", None)
                
        

        labels = {
            "name": "အမည်",
            "father_name": "အဖအမည်",
            "mother_name": "အမိအမည်",
            "nrc": "မှတ်ပုံတင်အမှတ်",
            "address": "နေရပ်လိပ်စာ",
            "note": "မှတ်ချက်"
        }

        # Create a dictionary to hold the updated values
        updated_data = {}

        cola, colb = st.columns([3, 2])
        with cola:
            for field, label in labels.items():
                col1, col2 = st.columns([4, 1])
                with col1:
                    initial_value = data.get(field, "")
                    session_key = f"{field}_input"
                    user_input = st.text_input(label, value=st.session_state.get(field, initial_value), key=f"{field}_input",icon="♻️")
                    updated_data[field] = user_input
                with col2:
                    st.write("<br>", unsafe_allow_html=True)
                    md.record_audio_and_update(field)  # Optional: ASR အတွက် function
                
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
                if st.button("💾 သိမ်းမည်"):
                        # Update to MongoDB using the input values directly
                        collection.update_one(
                            {"_id": doc_id},
                            {"$set": updated_data}
                        )
                        delete_session()
                        st.success("✅ ပြင်ပြီးပြီ။")
                        st.session_state.edit_mode = False
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
                if st.button("🔙 နောက်သို့"):
                    st.session_state.edit_mode = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        with colb:
        
           if 'img' in st.session_state and st.session_state.img is not None:
                st.image(st.session_state.img, caption="ဓာတ်ပုံ", use_container_width=True)           
           else:
                st.info("⚠️ ဓာတ်ပုံမရှိပါ။")

        

    