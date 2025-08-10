# Contract Analysis Pipeline

A modular pipeline to analyze contract PDFs using semantic search and large language models (LLMs).

---

## Overview

This pipeline allows you to:

- Extract and normalize text from contract PDFs
- Split text into chunks for processing
- Generate embeddings with `sentence-transformers` and build a FAISS semantic search index
- Use an OpenRouter/OpenAI-compatible LLM to:
  - Extract specific contract clauses (Termination, Confidentiality, Liability) using few-shot prompting
  - Generate concise contract summaries
- Save results in JSON and CSV formats

---

## Project Structure

- contract_analysis_pipeline/
  - config.py               : Configuration and constants
  - pdf_utils.py            : PDF text extraction and normalization utilities
  - embedding_utils.py      : Embeddings model and FAISS index building functions
  - llm_utils.py            : LLM prompt construction and API calls for clause extraction & summarization
  - pipeline.py             : Main processing pipeline to handle contracts end-to-end
  - main.py                 : CLI entrypoint to run the pipeline with user-specified parameters
  - docs/developer_docs.md  : Project Documentation
  - /dataset                : dataset directory


## 🚀 Installation

```bash
git clone <https://github.com/manishsaraswat-121/AccordAI.git >
cd project_root
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## 🛠 Usage

1. Place contracts in `dataset`.
2. Change the input data and desired output file path in  `config.py`
2. Run:
```bash
 python main.py 
```
3. Output is saved to `output/contracts_output.json`.

## 🔑 Environment Variables

| Variable             | Description                  |
|----------------------|------------------------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key       |

## 📦 Requirements

- Python 3.8+
- Dependencies in `requirements.txt`
