import time
from pathlib import Path
from typing import Dict
from pdf_utils import extract_text_from_pdf, normalize_text, chunk_text
from embedding_utils import build_embeddings_model, embed_texts, build_faiss_index, retrieve_top_k
from llm_utils import llm_extract_clause_multi, llm_generate_summary
from config import DATA_DIR, CLAUSE_TYPES

def process_contract(path: Path, embed_model) -> Dict:
    contract_id = path.stem
    raw_text = extract_text_from_pdf(path)
    if not raw_text:
        print(f"Empty extraction for {path}")
    text = normalize_text(raw_text)
    chunks = chunk_text(text)

    emb = embed_texts(embed_model, chunks)
    faiss_index = build_faiss_index(emb)

    extracted = {}
    for clause in CLAUSE_TYPES:
        query = f"Find the {clause} clause in this contract."
        q_emb = embed_texts(embed_model, [query])
        D, I = retrieve_top_k(faiss_index, q_emb, k=min(8, len(chunks)))
        contexts = [chunks[i] for i in I if i < len(chunks)]
        res = llm_extract_clause_multi(contract_id, contexts, clause)
        extracted[clause] = res
        time.sleep(0.2)

    query = "Summarize the purpose and key obligations of this contract."
    q_emb = embed_texts(embed_model, [query])
    D, I = retrieve_top_k(faiss_index, q_emb, k=min(10, len(chunks)))
    contexts = [chunks[i] for i in I if i < len(chunks)]
    summary = llm_generate_summary(contract_id, contexts, extracted)

    return {
        'contract_id': contract_id,
        'summary': summary,
        'termination_clause': extracted.get('termination', {}),
        'confidentiality_clause': extracted.get('confidentiality', {}),
        'liability_clause': extracted.get('liability', {}),
        'source_path': str(path)
    }

def run_pipeline():
    files = sorted(DATA_DIR.glob('*.pdf'))[:50]
    if not files:
        raise ValueError(f'No PDF files found in {DATA_DIR}. Place up to 50 CUAD PDFs there.')

    embed_model = build_embeddings_model('all-MiniLM-L6-v2')
    results = []

    from tqdm import tqdm
    for p in tqdm(files, desc='Processing contracts'):
        try:
            out = process_contract(p, embed_model)
            results.append(out)
        except Exception as e:
            print(f"Failed on {p}: {e}")

    return results
