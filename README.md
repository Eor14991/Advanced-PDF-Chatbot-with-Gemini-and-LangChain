# Advanced PDF Chatbot with Gemini and LangChain

## 📖 Overview

This project provides an advanced, modular, and efficient Streamlit application for chatting with multiple PDF documents. Users can upload PDFs, provide a Google AI API key, and ask questions about the document content. The backend leverages LangChain, Google's Gemini Pro model, and a FAISS vector store for retrieval-augmented generation (RAG).

The conversation history can be downloaded as a CSV file.

---

## ✨ Features

- **Multiple PDF Upload:** Upload and process several PDF files at once.
- **Efficient Processing:** PDFs are processed only when new files are uploaded, not on every question.
- **Stateful Conversations:** Remembers the context of the uploaded documents for a continuous chat session.
- **Downloadable Chat History:** Export the entire conversation to a CSV file.
- **Modular Architecture:** The code is separated into UI, utilities, and main application logic for better readability and maintenance.
- **Powered by Gemini:** Uses Google's powerful `gemini-2.0-flash` model for generating answers.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** LangChain, Google Generative AI
- **Embeddings:** Hugging Face `sentence-transformers`
- **Vector Store:** FAISS (Facebook AI Similarity Search)
- **PDF Processing:** PyPDF2

---

## 📂 Project Structure

```

pdf-chatbot/
│
├── faiss_index/              # Stores the local FAISS vector database
├── app.py                    # Main application logic and Chatbot class
├── ui.py                     # Streamlit user interface components
├── utils.py                  # Helper functions for PDF processing
├── requirements.txt          # Project dependencies
└── README.md                 # This file

````

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A Google AI API Key. You can get one from [Google AI Studio](https://ai.google.dev/).

### Installation

1. **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd pdf-chatbot
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2. **Use the web interface:**
    - Open your browser to the URL provided by Streamlit (e.g., `http://localhost:8501`).
    - Enter your Google AI API key in the sidebar.
    - Upload one or more PDF files.
    - Once the files are processed, you can start asking questions.

---

## 📄 Notes

- Only newly uploaded PDFs are processed to save time.
- Chat history can be downloaded as CSV for later reference.
- Make sure your Google AI API key has access to the `gemini-2.0-flash` model.

---
