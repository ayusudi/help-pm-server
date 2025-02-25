import streamlit as st
from functions.header import header
from functions.chat_stream import chat_stream
from functions.cortex_search_implementation import cortex_search, prompting_llm

header("👥", "PM Assistant")

st.session_state.selected_cortex_search_service = "SEARCH_EMPLOYEE"
if "messages" not in st.session_state or st.session_state.messages is None:
    st.session_state.messages = []

# Layout for model selection and max_tokens slider
col1, col2 = st.columns((3, 2))
col1.info(f"Trigger our Posterio RAG as a PM Assistant by starting a chat with **/RAG** then continue with your prompt.\n\n**/RAG** I'm planning to build an inventory management system. Who would you recommend from our IT talent to develop this app?")

with col2:
    max_tokens = col2.slider(
        "Max Tokens:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=32768,
        value=32768,
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: 32.768",
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

prompt = st.chat_input("Chat with PM Assistant")
if type(prompt) == str and prompt.lower().startswith("/rag"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)
    try:
        user_question = prompt[5:-1]
        pm_email = st.session_state.user_info["email"]
        with st.spinner("Thinking..."):
            list = cortex_search(query=user_question, filter_pm_email=pm_email) 
            response = prompting_llm(list, user_question)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)
    except Exception as e:
        st.error(e, icon="🚨")
elif type(prompt) == str and len(prompt) > 0:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)
    chat_stream(max_tokens)
