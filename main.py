from uuid import uuid4

import streamlit as st
from streamlit_option_menu import option_menu

from utils.agent_with_memory import agent_with_chat_history as agent
from utils.helpers.stream import simulate_streaming as stream_response

st.set_page_config(page_title="Chat", page_icon="🗣️", initial_sidebar_state="collapsed")

if "current_page" not in st.session_state:
    st.session_state["current_page"] = None

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

option_page_map = {
    "Home": "./main.py",
    "Upload": "pages/File_Upload.py",
    "Settings": "pages/Settings.py",
}


navbar_options = option_menu(
    None,
    ["Home", "Upload", "Settings"],
    icons=["house", "cloud-upload", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    key="navbar",
)

if navbar_options:
    if st.session_state["current_page"] != navbar_options:
        st.session_state["current_page"] = navbar_options
        page = option_page_map.get(navbar_options, None)
        if page:
            st.switch_page(page)

st.markdown(f"# Langchain + Agent + RAG")


if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid4().hex

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything"):
    # Add user message to chat history and display it
    with st.chat_message("user"):
        user_message = st.empty()
        for _ in stream_response(text=prompt, obj_ref=user_message):
            pass
        user_message.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Getting answer.."):
        # Get agent response
        response = agent.invoke(
            {"input": prompt},
            config={"configurable": {"session_id": st.session_state["session_id"]}},
        )
        bot_message = response["output"]
        print(f"[Bot] {bot_message}")

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            assistant_message_text = st.empty()
            for _ in stream_response(text=bot_message, obj_ref=assistant_message_text):
                pass
            assistant_message_text.markdown(bot_message)
        st.session_state.messages.append({"role": "assistant", "content": bot_message})

st.button("📂")