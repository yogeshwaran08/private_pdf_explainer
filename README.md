# PDF Chat Assistant

A powerful local AI-powered PDF reader that lets you have intelligent conversations with your documents - completely private and offline!

## The Story

Imagine having a personal AI assistant that can read through hundreds of pages of PDFs and answer your questions instantly. That's exactly what this application does!

Built with modern AI technologies, this PDF Chat Assistant transforms the way you interact with documents. Instead of manually searching through pages, you simply upload your PDF and ask questions in natural language. The AI understands the context, finds relevant information, and provides accurate answers - all running locally on your machine.

### How It Works

1. **Upload**: You upload any PDF document (research papers, books, manuals, reports)
2. **Process**: The app breaks down the PDF into smart chunks and creates semantic embeddings
3. **Store**: These embeddings are stored in a local vector database for lightning-fast retrieval
4. **Chat**: Ask questions naturally, and the AI searches through the content to provide contextual answers
5. **Learn**: The more you ask, the better you understand your documents

### The Magic Behind the Scenes

- **LangChain**: Orchestrates the entire AI pipeline
- **Ollama**: Runs powerful language models locally on your computer
- **ChromaDB**: Stores document embeddings for semantic search
- **Streamlit**: Provides a beautiful, interactive web interface

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- At least 8GB RAM (16GB recommended for larger models)
- 10GB+ free disk space

### Step 1: Install Ollama

Ollama allows you to run large language models locally on your machine.

#### For Windows:

1. Download Ollama from [https://ollama.ai/download](https://ollama.ai/download)
2. Run the installer
3. Open PowerShell and verify installation:
   ```powershell
   ollama --version
   ```

#### For macOS:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### For Linux:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Download Required Models

Pull the models needed for the application:

```bash
# Language model for answering questions (8B parameters, ~4.7GB)
ollama pull llama3:8b

# Embedding model for semantic search (~274MB)
ollama pull nomic-embed-text
```

**Note**: The first download will take some time depending on your internet speed.

Verify models are installed:

```bash
ollama list
```

### Step 3: Install Python Dependencies

Clone or download this project, then install required packages:

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run the Application

Make sure Ollama is running (it should start automatically, but you can check):

```bash
ollama serve
```

In a new terminal (with your virtual environment activated), start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 💡 How to Use

1. **Upload a PDF**: Click "Choose a PDF file" in the sidebar
2. **Process**: Click the "Process PDF" button and wait for the magic to happen
3. **Ask Questions**: Type your questions in the chat input at the bottom
4. **Get Answers**: The AI will provide contextual answers based on your PDF content

### Example Questions You Can Ask:

- "What is the main topic of this document?"
- "Summarize the key findings in chapter 3"
- "What does the author say about [specific topic]?"
- "List all the recommendations mentioned in the report"
- "Explain [concept] mentioned in the document"

## Features

- ✅ **100% Local & Private**: All processing happens on your machine
- ✅ **Fast Semantic Search**: Find relevant information instantly
- ✅ **Context-Aware Answers**: AI understands the document context
- ✅ **Chat History**: Keep track of your conversation
- ✅ **Easy to Use**: Simple, clean interface
- ✅ **Free & Open Source**: No API costs, no subscriptions

## ⚙️ Configuration

You can customize the application by modifying these parameters in `app.py`:

```python
# Chunk size for text splitting
chunk_size=500          # Smaller = more precise, Larger = more context
chunk_overlap=50        # Overlap between chunks

# Number of relevant chunks to retrieve
search_kwargs={"k": 3}  # Increase for more context in answers

# Change models
model="llama3:8b"       # Options: llama3:8b, llama3:70b, mistral, etc.
embedding="nomic-embed-text"
```

## 🔧 Troubleshooting

### Issue: "Connection refused" error

**Solution**: Make sure Ollama is running with `ollama serve`

### Issue: Slow responses

**Solution**:

- Use a smaller model like `llama3:8b` instead of `llama3:70b`
- Reduce the number of chunks retrieved (set `k=2` instead of `k=3`)
- Ensure you have enough RAM available

### Issue: Out of memory

**Solution**:

- Close other applications
- Use a smaller model
- Reduce chunk size in the configuration

### Issue: Model not found

**Solution**: Pull the required models:

```bash
ollama pull llama3:8b
ollama pull nomic-embed-text
```

## Advanced: Using Different Models

Want to try different models? Here are some options:

```bash
# Faster, smaller model (3B parameters)
ollama pull llama3:3b

# More powerful model (70B parameters, requires 64GB+ RAM)
ollama pull llama3:70b

# Alternative models
ollama pull mistral
ollama pull mixtral
ollama pull phi3
```

Update the model name in `app.py`:

```python
llm = Ollama(model="mistral")  # Change here
```

## Technical Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Ollama (nomic-embed-text)
- **LLM**: Ollama (llama3:8b)
- **PDF Processing**: PyPDF

## Contributing

Feel free to fork this project and add your own features! Some ideas:

- Support for multiple PDFs
- Export chat history
- Custom prompt templates
- Support for other document formats (DOCX, TXT)
- Better error handling
- Document summarization
- Citation tracking

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Ollama team for making local LLMs accessible
- LangChain for the amazing framework
- Streamlit for the beautiful UI toolkit
- The open-source AI community

---

**Happy PDF Chatting!**

For questions or issues, please open an issue on the repository.
