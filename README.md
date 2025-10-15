# Research Paper Analyzer 🔬

AI-powered research assistant using NVIDIA NIM and agentic workflows.

## Features
- 🤖 Autonomous query decomposition
- 📚 Automatic paper fetching from ArXiv
- 🧠 Multi-paper synthesis with citations
- 🔬 Methodology comparison
- 🎯 Research gap identification

## Tech Stack
- **LLM**: Llama-3.1-8B via NVIDIA NIM
- **Retrieval**: ArXiv API + PyPDF
- **Framework**: Streamlit
- **Deployment**: AWS (EKS/SageMaker)

## Installation
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Setup
Create `.env` file:
```
NVIDIA_API_KEY=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
```

## Run
```bash
streamlit run app.py
```

## Demo Video
[Link to your demo video]

## How It Works
1. User asks research question
2. Agent decomposes into sub-queries
3. Searches ArXiv for relevant papers
4. Downloads and processes PDFs
5. Synthesizes findings with citations
6. Compares methodologies & identifies gaps