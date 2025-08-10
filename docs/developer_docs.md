Certainly! Here’s your nicely formatted developer documentation as a single snippet you can copy-paste in one go:

```markdown
# Contract Analysis Pipeline - Developer Documentation

## Project Overview

This project implements a contract analysis pipeline that uses semantic search and large language models (LLMs) to analyze PDF contracts. It extracts specific clauses (Termination, Confidentiality, Liability) and generates a concise summary for each contract.

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
  - dataset                  : dataset directory


### File Descriptions

- **config.py**  
  Contains all configuration constants like model names, directories, API keys, chunk sizes, few-shot examples, user inputs (input folder, output files) and clause types.

- **pdf_utils.py**  
  Utility functions for extracting and normalizing text from PDFs.

- **embedding_utils.py**  
  Functions related to embedding text using sentence-transformers and building/searching FAISS indices.

- **llm_utils.py**  
  Functions to interact with the LLM, including clause extraction and summary generation using few-shot prompting.

- **pipeline.py**  
  Core pipeline logic to process each contract:  
  - Extract text  
  - Normalize and chunk  
  - Compute embeddings & build FAISS index (if needed)  
  - Retrieve relevant chunks using semantic search  
  - Extract clauses with LLM calls  
  - Generate summaries  
  - Aggregate and return results

- **main.py**  
  Entry point script that:   
  - Initializes models and environment  
  - Runs the pipeline  
  - Saves outputs (JSON and CSV)

---

## How To Use

1. **Prepare Input Data**  
   Place up to 50 PDF contract files in a folder (default is `./data/contracts`).

2. **Set Environment Variables**  
   Set your OpenRouter API key as environment variable `OPENROUTER_API_KEY`.

3. **Run the Pipeline**  
   Execute the `main.py` script, specifying input/output paths in the script `config.py` or command line if applicable:

   ```bash
   python main.py
````

---

## Key Components

### PDF Utilities

* `extract_text_from_pdf(path: Path) -> str`
  Extracts text content from a PDF file using PyMuPDF.

* `normalize_text(text: str) -> str`
  Cleans and normalizes extracted text, removing headers, footers, and redundant whitespace.

* `chunk_text(text: str, size: int, overlap: int) -> List[str]`
  Splits text into overlapping chunks for embedding and retrieval.

### Embeddings & FAISS

* Uses sentence-transformers model `'all-MiniLM-L6-v2'` for local embedding generation.
* FAISS `IndexFlatIP` is used for approximate nearest neighbor search with cosine similarity.
* Embeddings are normalized before adding to the index and before searching.

### LLM Utilities

* Few-shot prompt examples included to guide clause extraction.
* `llm_extract_clause` uses a prompt with context chunks to extract specific clauses and returns a JSON with:

  * `raw_clause`: exact extracted text
  * `normalized_clause`: short summary
  * `found`: boolean flag
* `llm_generate_summary` generates a concise summary (100-150 words) of the contract based on extracted clauses and context.

---

## Pipeline Flow

For each contract:

* Extract and normalize text
* Chunk text and generate embeddings
* Build FAISS index (if not already built)
* For each clause type, query and extract using LLM
* Generate summary using LLM
* Aggregate results and save to JSON and CSV files

---

## Configuration Highlights (`config.py`)

* `DATA_DIR`, `OUTPUT_DIR` - paths for input and output files.
* `EMBEDDING_MODEL_NAME`, `LLM_MODEL`, `LLM_TEMPERATURE`, `LLM_MAX_TOKENS` - model configurations.
* `CHUNK_SIZE`, `CHUNK_OVERLAP` - text chunking parameters.
* `FEW_SHOT_EXAMPLES` - example clauses for LLM prompting.
* `CLAUSE_TYPES` - list of clause categories to extract.

---

## Dependencies

* Python 3.8+
* `openai` or `openrouter-client`
* `pdfminer.six`
* `PyMuPDF` (fitz)
* `sentence-transformers`
* `faiss-cpu`
* `pandas`
* `tqdm`
* `python-dotenv`

Install via:

```bash
pip install openai pdfminer.six PyMuPDF sentence-transformers faiss-cpu pandas tqdm python-dotenv
```

---

## Notes & Tips

* Ensure the environment variable `OPENROUTER_API_KEY` is set before running.
* The chunk size and overlap can be tuned for performance vs. context coverage.
* FAISS index can be cached and reused for faster processing of multiple contracts.
* Few-shot examples can be extended or customized in `config.py` for better extraction accuracy.
* Handle large documents carefully to avoid LLM token limits (chunk and query accordingly).

---

## Contact & Contribution

For issues or contributions, please open a GitHub issue or pull request in the project repository.

