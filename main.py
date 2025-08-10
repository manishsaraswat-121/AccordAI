import json
import pandas as pd
from pathlib import Path
from pipeline import run_pipeline
from config import OUTPUT_DIR

def save_results(results, output_dir=OUTPUT_DIR):
    out_json = output_dir / 'contracts_output.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    rows = []
    for r in results:
        rows.append({
            'contract_id': r['contract_id'],
            'summary': r['summary'],
            'termination_clause': r['termination_clause'].get('normalized_clause', '') if isinstance(r['termination_clause'], dict) else '',
            'confidentiality_clause': r['confidentiality_clause'].get('normalized_clause', '') if isinstance(r['confidentiality_clause'], dict) else '',
            'liability_clause': r['liability_clause'].get('normalized_clause', '') if isinstance(r['liability_clause'], dict) else '',
            'source_path': r.get('source_path', '')
        })

    df = pd.DataFrame(rows)
    out_csv = output_dir / 'contracts_output.csv'
    df.to_csv(out_csv, index=False)

    print(f"Saved JSON to {out_json} and CSV to {out_csv}")

if __name__ == '__main__':
    results = run_pipeline()
    save_results(results)
