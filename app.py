
import streamlit as st

pages={
    "Data Entry": [
        st.Page("pages/new1.py", title="New Page", icon="🎙️"),
        st.Page("pages/show.py", title="Show Page", icon="📊"),
    ],
    "ASR": [
        st.Page("pages/asr.py", title="ASR Test", icon="🎙️"),
        st.Page("pages/new.py", title="New Test Page", icon="🖋️"),
        st.Page("audiotest.py",title="Audio",icon="🎙️")
    ],
}

st.logo("images/MLLIP.png",size="large", )

with st.sidebar:
    st.image("images/mllip-logo.jpg")
# Set up navigation
pg = st.navigation(pages)

# Run the selected page
pg.run()