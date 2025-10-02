# Deep Research Agent

## Overview
This project implements a deep research agent designed to process and analyze PDF documents for in-depth research. The agent leverages advanced embeddings and a vector store to enable efficient information retrieval and analysis. The primary data source is a PDF file located in the `data` directory, which is processed to create a vector store for research queries.

## Objectives
- Ingest and process PDF documents for research purposes.
- Create a vector store using Chroma DB for efficient data retrieval.
- Enable a research agent to perform deep analysis on the ingested content.
- Provide a modular codebase for extensibility and further development.

## Project Structure
```
├── data
│   └── AI Engineering Building Applications with Foundation Models (Chip Huyen) (Z-Library).pdf
├── images
│   └── deep_research_agent.png
├── LICENSE
├── markdowns
│   ├── PRD.md              # Product Requirements Document
│   └── research.md         # Research notes or documentation
├── notebooks
│   └── deep-research-agent.ipynb  # Jupyter notebook for exploratory analysis
├── README.md              # Project overview (this file)
├── requirements.txt       # Python dependencies
├── scripts
│   ├── ingest_data.py     # Script to ingest PDF and create vector store
│   ├── __init__.py
│   └── __pycache__        # Compiled Python files
├── services
│   ├── database_service.py  # Database-related functionality
│   ├── embedding_service.py # Embedding generation for documents
│   ├── __init__.py
│   └── __pycache__         # Compiled Python files
├── src
│   ├── agent.py           # Core research agent logic
│   ├── config.py          # Configuration settings
│   ├── core
│   │   ├── models.py      # Model definitions
│   │   ├── nodes.py       # Node definitions for agent workflow
│   │   ├── prompts.py     # Prompt templates for the agent
│   │   ├── __init__.py
│   │   └── __pycache__    # Compiled Python files
│   ├── main.py            # Main entry point for running the agent
│   ├── utils.py           # Utility functions
│   ├── __init__.py
│   └── __pycache__        # Compiled Python files
├── utils
│   ├── pdf_utils.py       # PDF processing utilities
│   ├── __init__.py
│   └── __pycache__        # Compiled Python files
└── vector_store
    └── chroma_db          # Chroma DB vector store
        ├── chroma.sqlite3
        └── 6190c0e5-ce37-42bf-9028-041d47aa1ede
            ├── data_level0.bin
            ├── header.bin
            ├── index_metadata.pickle
            ├── length.bin
            └── link_lists.bin
```

## Prerequisites
- Python 3.8+
- A PDF file placed in the `data` directory (e.g., `AI Engineering Building Applications with Foundation Models (Chip Huyen) (Z-Library).pdf`).
- API keys for Google, Tavily, LangSmith, and Chroma (Hugging Face).

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/deep-research-agent.git
   cd deep-research-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with the following content:
   ```plaintext
   GOOGLE_API_KEY=your_google_api_key
   TAVILY_API_KEY=your_tavily_api_key
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGCHAIN_PROJECT=your_langchain_project_name
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_TRACING=true
   CHROMA_HUGGINGFACE_API_KEY=your_huggingface_api_key
   ```
   Replace `your_*` placeholders with your actual API keys and project details.

5. **Place the PDF file**:
   Ensure the PDF file you want to research (e.g., `AI Engineering Building Applications with Foundation Models (Chip Huyen) (Z-Library).pdf`) is placed in the `data` directory.

## Usage
1. **Ingest the PDF and create the vector store**:
   Run the ingestion script to process the PDF and generate a vector store in the `vector_store/chroma_db` directory:
   ```bash
   python3 -m scripts.ingest_data
   ```

2. **Run the research agent**:
   Execute the main script to start the research agent:
   ```bash
   python3 -m src.main
   ```

3. **Explore with Jupyter notebook**:
   Use the `notebooks/deep-research-agent.ipynb` notebook for interactive analysis or experimentation.

## Notes
- The `ingest_data.py` script processes the PDF in the `data` directory and creates a Chroma DB vector store for efficient querying.
- The `src/main.py` script runs the core research agent, utilizing the vector store and embeddings for analysis.
- Ensure all API keys are correctly configured in the `.env` file before running the scripts.
- The `utils/pdf_utils.py` script contains helper functions for PDF processing, and `services` contains modules for database and embedding operations.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or collaboration inquiries, open an issue on GitHub.