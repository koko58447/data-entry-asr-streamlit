# # app.py

# import streamlit as st
# from module import record_audio_and_update

# # # st.session_state.name="input text"
# # # st.session_state.father_name="input text"

# # # Sample input field simulation
# # if "name" not in st.session_state:
# #     st.session_state.name = "input text"
# # if "father_name" not in st.session_state:
# #     st.session_state.father_name = "input text"

# # name=st.text_input("အမည်", value=st.session_state.name)
# # record_audio_and_update("name")  # field name ကိုပေးပါ
# # st.write(name)

# # father_name=st.text_area("အဖအမည်", value=st.session_state.father_name)
# # record_audio_and_update("father_name")  # field name ကိုပေးပါ
# # st.write(father_name)

import streamlit as st

# CSS နဲ့ input box ကို customize လုပ်
st.markdown("""
<style>
.input-container {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 4px 8px;
    width: 100%;
    max-width: 600px;
    background-color: #f9f9f9;
}

.input-container input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 16px;
    padding-left: 8px;
    background-color: transparent;
}

.input-container .icon {
    margin-right: 8px;
    font-size: 20px;
}

.input-container .mic-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([10, 1])  # 10:1 အချိုးနဲ့ columns ခွဲ

with col1:
    user_input = st.text_input("message", placeholder="Type your message...", key="custom_input", label_visibility="collapsed")

with col2:
    if st.button("🎙️", key="mic_button"):
        st.write("Mic clicked! (Not implemented yet)")

# မှတ်ချက် - သင့် input value ကို သုံးချင်ရင် user_input ကို အသုံးပြုပါ
if user_input:
    st.write(f"You typed: {user_input}")

user_input2 = st.text_input(" ", placeholder="👤 Type your message...", key="custom_input1")
if st.button("🎙️"):
    st.write("Mic clicked!")

# Custom CSS for input with icons on both sides
st.markdown("""
<style>
.input-wrapper {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 4px 12px;
    background-color: #f9f9f9;
    max-width: 600px;
    width: 100%;
    box-sizing: border-box;
}

.input-wrapper .icon-left {
    margin-right: 8px;
    font-size: 20px;
    color: #555;
}

.input-wrapper .icon-right {
    margin-left: 8px;
    font-size: 20px;
    color: #555;
    cursor: pointer;
}

.input-wrapper input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 16px;
    background-color: transparent;
    padding: 4px 0;
}
</style>
""", unsafe_allow_html=True)

# HTML + input ကို ပေါင်းထည့်
st.markdown("""
<div class="input-wrapper">
    <span class="icon-left">👤</span>
    <input type="text" id="customInput" placeholder="Type your message...">
    <span class="icon-right" title="Voice Input">🎙️</span>
</div>
""", unsafe_allow_html=True)