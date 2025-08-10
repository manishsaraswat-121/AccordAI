import json
import time
from typing import List, Dict
import openai
from config import OPENROUTER_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, FEW_SHOT_EXAMPLES, CLAUSE_TYPES

client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

def extract_json_from_text(text: str) -> str:
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            json.loads(candidate)
            return candidate
        except Exception:
            return ''
    return ''

def llm_extract_clause(contract_id: str, context_chunks: List[str], clause_type: str) -> Dict[str, str]:
    example_pairs = []
    for ex in FEW_SHOT_EXAMPLES:
        example_pairs.append(f"EXCERPT:\n{ex['contract_excerpt'].strip()}\n\nEXTRACTIONS:\nTermination: {ex['termination_clause']}\nConfidentiality: {ex['confidentiality_clause']}\nLiability: {ex['liability_clause']}\n---")

    prefix = (
        "You are a legal-narrow LLM assistant. Given contract text excerpts, locate and extract the requested clause type. "
        "Return a JSON object with keys: 'raw_clause', 'normalized_clause', and 'found'. "
        "If multiple matches exist, return the most representative one. If not found, set 'found' to false and texts empty."
    )

    context_text = '\n\n---\n\n'.join([c.strip() for c in context_chunks])

    system_msg = {'role': 'system', 'content': 'You are a helpful legal assistant specialized in clause extraction.'}
    user_prompt = (
        f"{prefix}\n\nFEW-SHOT EXAMPLES:\n\n" + "\n\n".join(example_pairs) +
        f"\n\nCONTRACT ID: {contract_id}\n\nCONTEXT (most relevant chunks):\n{context_text}\n\nREQUEST: Extract the '{clause_type}' clause.\n\nRespond ONLY with a JSON object as specified."
    )
    messages = [system_msg, {'role': 'user', 'content': user_prompt}]

    try:
        resp = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )
        raw = resp.choices[0].message.content
        json_text = extract_json_from_text(raw)
        if json_text:
            return json.loads(json_text)
        else:
            return json.loads(raw)
    except Exception as e:
        return {'raw_clause': '', 'normalized_clause': '', 'found': False, 'error': str(e)}

def llm_extract_clause_multi(contract_id: str, context_chunks: List[str], clause_type: str) -> Dict[str, str]:
    best_result = {'raw_clause': '', 'normalized_clause': '', 'found': False}
    for chunk in context_chunks:
        res = llm_extract_clause(contract_id, [chunk], clause_type)
        if res.get('found', False):
            return res
        if len(res.get('raw_clause', '')) > len(best_result.get('raw_clause', '')):
            best_result = res
    return best_result

def llm_generate_summary(contract_id: str, context_chunks: List[str], extracted_clauses: Dict[str, Dict[str,str]]) -> str:
    clause_summaries = []
    for ct in CLAUSE_TYPES:
        info = extracted_clauses.get(ct, {})
        if info and info.get('found'):
            clause_summaries.append(f"{ct.title()} -> {info.get('normalized_clause','')}")
    clause_block = '\n'.join(clause_summaries)

    context_text = '\n\n'.join([c.strip() for c in context_chunks[:6]])

    system_msg = {'role': 'system', 'content': 'You are a concise contract summarizer. Produce 100-150 word summaries.'}
    user_prompt = (
        f"CONTRACT ID: {contract_id}\n\nCONTEXT (top chunks):\n{context_text}\n\nEXTRACTED_CLAUSES_SUMMARY:\n{clause_block}\n\n"
        "Write a concise 100-150 word summary that highlights: purpose, key obligations of each party, and notable risks/penalties. "
        "Return ONLY the summary text (no JSON)."
    )

    messages = [system_msg, {'role': 'user', 'content': user_prompt}]

    try:
        resp = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.3,
            max_tokens=300,
        )
        summary = resp.choices[0].message.content.strip()
        words = summary.split()
        if len(words) > 160:
            summary = ' '.join(words[:150])
        return summary
    except Exception as e:
        return f"[SUMMARY_GENERATION_FAILED] {e}"
