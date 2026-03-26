<<<<<<< HEAD
# PrecisionReg Navigator

PrecisionReg Navigator is an agentic FDA regulatory intelligence application for oncology in vitro diagnostics, tumor profiling assays, liquid biopsy concepts, and companion diagnostics.

It combines product concept classification, FDA guidance retrieval, structured precedent search, evidence-gap assessment, and memo generation into a practical workflow for early regulatory strategy evaluation.

## Why this project exists

Regulatory strategy for oncology diagnostics is rarely a pure document-search problem. Teams need to understand how intended use, biomarker scope, specimen type, platform, therapy linkage, and software components affect likely regulatory pathways and evidence expectations.

PrecisionReg Navigator was built to make those early assessments more structured, more transparent, and more grounded in FDA guidance and precedent.

## Current scope

This version is intentionally narrow and focused on FDA-regulated oncology diagnostics.

Included in scope:
- oncology IVD concepts
- NGS-based tumor profiling assays
- liquid biopsy concepts
- companion diagnostics
- FDA guidance retrieval
- structured FDA precedent search
- draft regulatory memo generation

Not yet included:
- EU IVDR
- Health Canada
- PMDA
- automated web ingestion
- full standards mapping
- full study-risk determination workflows
- production deployment controls

## Core capabilities

- classify a product concept as likely tumor profiling, CDx, or general IVD
- retrieve relevant FDA guidance excerpts from a curated source set
- retrieve structured FDA precedents from a local database
- identify likely evidence gaps and development risks
- generate a draft FDA-focused regulatory assessment memo
- provide a simple Streamlit interface for interactive exploration

## Example use cases

- NSCLC tissue NGS assay intended to support therapy selection
- NSCLC liquid biopsy assay for actionable genomic alterations in plasma
- pan-tumor profiling assay intended for molecular characterization rather than direct therapy selection
- early concept evaluation for oncology companion diagnostic strategy

## Current FDA source set

The current prototype uses a focused set of FDA source documents, including:
- NGS analytical validation guidance
- public variant database clinical validity guidance
- investigational IVDs in oncology trials study-risk guidance
- oncology CDx group labeling guidance
- companion diagnostics overview
- precision medicine overview

## Architecture

PrecisionReg Navigator currently uses:

- Python
- Streamlit
- Anthropic API for reasoning
- sentence-transformers for embeddings
- FAISS for vector search
- SQLite for structured FDA precedents
- Pydantic for typed outputs

### Workflow

1. user enters a product concept
2. the app classifies the concept
3. the app retrieves relevant FDA guidance
4. the app retrieves structured precedent records
5. the app generates a regulatory assessment with evidence gaps and recommended next steps

## Repository structure

```text
precisionreg-navigator/
├── README.md
├── requirements.txt
├── .env
├── app.py
├── data/
│   ├── raw/
│   │   ├── guidance/
│   │   └── precedents/
│   ├── processed/
│   └── sqlite/
├── src/
├── scripts/
└── tests/
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_real_key_here
OPENAI_API_KEY=
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTORSTORE_INDEX=data/processed/faiss.index
VECTORSTORE_METADATA=data/processed/faiss_metadata.pkl
SQLITE_PATH=data/sqlite/fda_precedents.db
data/raw/guidance/
PYTHONPATH=. python3 scripts/load_guidance.py
PYTHONPATH=. python3 scripts/build_vectorstore.py
PYTHONPATH=. python3 scripts/build_precedents_db.py
PYTHONPATH=. streamlit run app.py

## 2. Add `.gitignore`

```bash
cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.DS_Store
.env
data/processed/*.index
data/processed/*.pkl
data/sqlite/*.db
.streamlit/
=======
# precisionreg-navigator
Agentic FDA regulatory intelligence for oncology IVDs, tumor profiling, liquid biopsy, and companion diagnostics. Combines guidance retrieval, structured precedent search, product classification, evidence-gap analysis, and memo generation into a practical early regulatory strategy workflow.
>>>>>>> 775f24adcd741acb80429e9d11b103cb727c4f75
