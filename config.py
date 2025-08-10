import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path('./dataset')
OUTPUT_DIR = Path('./outputs')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
EMBEDDING_DIM = 384

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError('Set OPENROUTER_API_KEY in environment before running')

LLM_MODEL = 'mistralai/mistral-7b-instruct'
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 800

CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

CLAUSE_TYPES = ['termination', 'confidentiality', 'liability']

FEW_SHOT_EXAMPLES = [
    {
        'contract_excerpt': """
This Agreement may be terminated by either party upon thirty (30) days' prior written notice to the other party if the other party materially breaches any representation, warranty or covenant under this Agreement and fails to cure such breach within thirty (30) days following receipt of written notice describing the breach.
""",
        'termination_clause': "This Agreement may be terminated by either party upon 30 days' written notice if the other party materially breaches and fails to cure within 30 days.",
        'confidentiality_clause': "N/A",
        'liability_clause': "N/A",
    },
    {
        'contract_excerpt': """
The Receiving Party agrees to hold in confidence all Confidential Information disclosed by the Disclosing Party and shall not use such Confidential Information except for the purpose of performing under this Agreement. Disclosure is permitted only to employees on a need-to-know basis and who are bound by similar confidentiality obligations.
""",
        'termination_clause': "N/A",
        'confidentiality_clause': "Receiving Party must keep Confidential Information confidential and use it only to perform the Agreement; disclosures limited to need-to-know employees bound by similar obligations.",
        'liability_clause': "N/A",
    },
    {
        'contract_excerpt': """
In no event shall either party be liable to the other for any indirect, special, incidental or consequential damages, including loss of profits, even if advised of the possibility of such damages. The aggregate liability of each party for claims arising out of this Agreement shall not exceed the fees paid in the twelve (12) months preceding the claim.
""",
        'termination_clause': "N/A",
        'confidentiality_clause': "N/A",
        'liability_clause': "No indirect or consequential damages; aggregate liability capped at fees paid in prior 12 months.",
    },
]
