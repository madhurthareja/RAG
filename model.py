import streamlit as st
from chat import generate_response
from embeddings import generate_embedding
from supabase_db import store_document, supabase_client
from dotenv import load_dotenv
import os
import chardet
import PyPDF2

load_dotenv()

st.title("Retrieval Augmented Generation based Chatbot")

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file:
    raw_data = uploaded_file.read()

    # Detect encoding
    result = chardet.detect(raw_data)
    encoding = result["encoding"] if result["encoding"] else "utf-8"

    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = " ".join([page.extract_text() for page in pdf_reader.pages])
        else:
            text = raw_data.decode(encoding)

        st.success(f"File successfully read with encoding: {encoding}")

        # Generate embedding & store
        embedding = generate_embedding(text)
        print(f"Generated embedding: {embedding[:10]}...")  # Print first 10 elements of the embedding
        store_document(uploaded_file.name, text, embedding)

    except UnicodeDecodeError:
        st.error("Could not decode file. Try converting it to UTF-8 format.")
    
# Chat Input
user_input = st.text_input("Ask a question:")

if user_input:
    query_embedding = generate_embedding(user_input)
    print(f"Generated query embedding: {query_embedding[:10]}...")  # Print first 10 elements of the query embedding
    response = generate_response(query_embedding) 

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

    # Display Chat History
    for speaker, text in st.session_state.chat_history:
        with st.expander(f"**{speaker}:**", expanded=True):
            st.markdown(f"<div style='font-family: monospace; border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>{text}</div>", unsafe_allow_html=True)

