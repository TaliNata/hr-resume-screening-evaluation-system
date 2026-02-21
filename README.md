# Overview
This project is a production-style LLM system for automated HR resume screening.
It evaluates candidate resumes against job descriptions using a multi-stage
prompt architecture with strict input/output contracts and LLM-based evaluation.

---

## Features
- Multi-layer prompt system (system / role / instructions);
- Strict JSON input and output schemas;
- Hallucination control;
- LLM-as-Judge evaluation step;
- Prompt versioning;
- Deterministic scoring (temperature = 0).

---

## Architecture
```
INPUT (JSON)
↓
Schema Validation
↓
LLM Screening (Prompt System)
↓
Output Schema Validation
↓
LLM Evaluation (Judge)
```
---

## Project Structure
hr-llm-system/
├─ core/
├─ prompts/
│ └─ v1/
├─ schemas/
├─ pipeline.py
├─ run.py
└─ README.md

---

## Example Output

Match score (0–100):
1. Matched skills;
2. Missing skills;
3. Hiring risks;
4. Final recommendation;
5. Evaluation (PASS / FAIL).

---

## Why This Is Not a Simple Prompt

This system demonstrates production-level prompt engineering:
1. Separation of concerns;
2. Reproducibility;
3. Schema enforcement;
4. Evaluation pipeline.
