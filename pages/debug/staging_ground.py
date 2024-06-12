import streamlit as st


btn, user_input = st.columns([1,7])

btn.button(label="Send")

if prompt := user_input.chat_input("Ask me anything"):
    st.write("Hello how are you?")