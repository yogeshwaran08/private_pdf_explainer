import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

st.set_page_config(page_title="PDF Chat Assistant", layout="wide")
st.title("PDF Chat Assistant")
st.markdown("Upload a PDF and ask questions about its content!")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Process PDF", type="primary"):
            with st.spinner("Processing PDF..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    st.info("Loading PDF...")
                    loader = PyPDFLoader(tmp_path)
                    documents = loader.load()
                    st.success(f"Loaded {len(documents)} pages")
                    
                    st.info("Splitting into chunks...")
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=500,
                        chunk_overlap=50
                    )
                    chunks = splitter.split_documents(documents)
                    st.success(f"Created {len(chunks)} chunks")
                    
                    st.info("Creating embeddings...")
                    embeddings = OllamaEmbeddings(model="nomic-embed-text")
                    
                    temp_db_dir = tempfile.mkdtemp()
                    vectorstore = Chroma.from_documents(
                        documents=chunks,
                        embedding=embeddings,
                        persist_directory=temp_db_dir
                    )
                    
                    llm = Ollama(model="llama3:8b")
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
                    )
                    
                    st.session_state.vectorstore = vectorstore
                    st.session_state.qa_chain = qa_chain
                    st.session_state.pdf_processed = True
                    st.session_state.chat_history = []
                    
                    os.unlink(tmp_path)
                    
                    st.success("PDF processed successfully! You can now ask questions.")
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
    
    if st.session_state.pdf_processed:
        st.success("PDF is ready for questions!")
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

if not st.session_state.pdf_processed:
    st.info("Please upload and process a PDF from the sidebar to start chatting.")
else:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if question := st.chat_input("Ask a question about the PDF..."):
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.qa_chain.invoke(question)
                    answer = response['result']
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
