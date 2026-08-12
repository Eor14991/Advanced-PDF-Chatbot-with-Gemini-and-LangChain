# 📄 Advanced PDF Chatbot with Gemini & LangChain

An intelligent, modular Streamlit application that allows users to engage in context-aware conversations with multiple PDF documents. Powered by **Google Gemini Pro**, **LangChain**, and **FAISS**, this tool transforms static documents into an interactive knowledge base.

## 🚀 Key Features
- **Multi-PDF Support:** Upload and process multiple PDF files simultaneously.
- **Stateful Conversations:** Maintains chat history for a continuous, context-aware dialogue.
- **Efficient Retrieval:** Uses **HuggingFace Embeddings** and **FAISS** for high-speed semantic search.
- **Downloadable History:** Export your entire conversation as a CSV file for future reference.
- **Modular Design:** Clean separation between UI logic, PDF processing, and RAG pipelines.

## 🛠 Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Orchestration:** [LangChain](https://www.langchain.com/)
- **LLM:** [Google Gemini 2.0 Flash](https://aistudio.google.com/)
- **Vector Store:** [FAISS](https://github.com/facebookresearch/faiss)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **PDF Parsing:** PyPDF2

## 📋 Prerequisites
- Python 3.8+
- Google AI API Key (Get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

## ⚙️ Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Eor14991/Advanced-PDF-Chatbot-with-Gemini-and-LangChain.git
   cd Advanced-PDF-Chatbot-with-Gemini-and-LangChain
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Usage
1. **Run the app:**
   ```bash
   streamlit run app.py
   ```
2. **Enter your API Key** in the sidebar.
3. **Upload your PDFs** and click "Submit & Process".
4. **Start chatting** with your documents!
