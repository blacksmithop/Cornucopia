import streamlit as st
from utils.stream_message import stream_chat
from utils.memory_manager import with_message_history as ask_llm
from uuid import uuid4

st.title("Identify Speakers from text")

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
        for _ in stream_chat(text=prompt, obj_ref=user_message):
            pass
        user_message.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get assistant response
    response = ask_llm.invoke(
        {"input": prompt},
        {"configurable": {"session_id": st.session_state["session_id"]}},
    )
    print(type(response))
    print(f"[Bot] {response}")

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        assistant_message_text = st.empty()
        for _ in stream_chat(text=response, obj_ref=assistant_message_text):
            pass
        assistant_message_text.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
