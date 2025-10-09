# -------------------- Fix OpenBLAS / OpenMP hang --------------------
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# -------------------- Imports --------------------
import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import base64
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import asyncio

# Setup asyncio loop for Streamlit
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# ---------------- PDF Processing ----------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

# ---------------- Vector Store ----------------
def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

# ---------------- Conversational Chain ----------------
def get_conversational_chain(api_key):
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the context, say "answer is not available in the context". 

    Context:\n{context}
    Question:\n{question}
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# ---------------- User Input ----------------
def user_input(user_question, api_key, pdf_docs):
    if not pdf_docs or not api_key:
        st.warning("Please upload PDF files and provide Google API key.")
        return

    # Process PDF & build FAISS
    text_chunks = get_text_chunks(get_pdf_text(pdf_docs))
    get_vector_store(text_chunks)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = vector_db.similarity_search(user_question)

    chain = get_conversational_chain(api_key)
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    response_output = response['output_text']

    pdf_names = [pdf.name for pdf in pdf_docs]
    st.session_state.conversation_history.append(
        (user_question, response_output, "Google AI", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ", ".join(pdf_names))
    )

    # ---------------- Display conversation ----------------
    st.markdown("""
    <style>
    .chat-message {padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: flex-start;}
    .chat-message.user {background-color: #1f2937; color: #fff;}
    .chat-message.bot {background-color: #374151; color: #fff;}
    .chat-message .avatar {width: 10%; margin-right: 10px;}
    .chat-message .avatar img {width: 50px; height: 50px; border-radius: 50%;}
    .chat-message .message {width: 90%; padding: 0.5rem; word-wrap: break-word;}
    </style>
    """, unsafe_allow_html=True)

    for question, answer, model, timestamp, pdf_name in reversed(st.session_state.conversation_history):
        st.markdown(
            f"""
            <div class="chat-message user">
                <div class="avatar"><img src="https://i.ibb.co/NFhMdWd/user.png"></div>
                <div class="message">{question}</div>
            </div>
            <div class="chat-message bot">
                <div class="avatar"><img src="https://i.ibb.co/1r2YZ8V/ai.png"></div>
                <div class="message">{answer}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- CSV Download ----------------
    if st.session_state.conversation_history:
        df = pd.DataFrame(st.session_state.conversation_history,
                          columns=["Question", "Answer", "Model", "Timestamp", "PDF Name"])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="conversation_history.csv"><button>Download conversation history</button></a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

# ---------------- Main App ----------------
def main():
    st.set_page_config(page_title="Chat with PDFs", page_icon=":books:")
    st.header("Chat with multiple PDFs :books:")

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Sidebar
    st.sidebar.header("Settings")
    api_key = st.sidebar.text_input("Enter your Google API Key")
    st.sidebar.markdown("Get it from [Google AI](https://ai.google.dev/)")
    pdf_docs = st.sidebar.file_uploader("Upload PDF files", accept_multiple_files=True)

    if st.sidebar.button("Reset"):
        st.session_state.conversation_history = []

    user_question = st.text_input("Ask a question from the PDFs:")
    if user_question:
        user_input(user_question, api_key, pdf_docs)

if __name__ == "__main__":
    main()
