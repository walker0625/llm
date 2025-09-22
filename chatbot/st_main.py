# uv add openai python-dotenv streamlit
import streamlit as st 

pages = [
    st.Page(
        page='pages/components.py',
        title='basic',
        icon='📂',
        default=True
    ),
    st.Page(
        page='pages/chat.py',
        title='Chat',
        icon='📝',
    )
]

nav = st.sidebar.radio(pages)