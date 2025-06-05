# Caprae Capital AI-Readiness Challenge – Project Report

**Project:** Lead Scoring + Export Tool  
**Name:** Rofi Nastain  
**Duration:** ~5 hours  

---

## 💡 Approach
The goal was to build a lightweight tool to help sales teams prioritize company leads. I chose to focus on a rules-based scoring model (Quality First approach) that could be extended with AI in the future.

This tool allows users to upload CSV files containing lead data. The app then automatically scores each lead based on predefined business logic and lets users export the result.

---

## 🧠 Model Selection
Instead of a full ML model, I used **simple rule-based logic** for interpretability and speed. This choice fits the 5-hour constraint and aligns with the real-world requirement of easily explainable scoring:

| Criteria                  | Score |
|---------------------------|-------|
| Revenue > $3M             | +3    |
| Employees > 15            | +3    |
| Industry: Fintech, Edtech, Healthtech | +2    |
| Location in major cities  | +2    |

Total score is mapped into:
- **High (6+)**
- **Medium (3–5)**
- **Low (0–2)**

---

## 🧹 Data Preprocessing
- Cleaned `Revenue ($M)` and `Employees` columns with `pd.to_numeric(...)`
- Dropped rows with missing values in key columns
- Reset DataFrame index and generated custom `No.` column
- Filtered by lead quality (selectbox in UI)

Sample datasets were provided:
- `sample_leads.csv` (5 rows)
- `sample_leads_1000.csv` (1000 dummy companies)

---

## 📊 Performance Evaluation
As this is a rule-based demo, performance is evaluated **qualitatively** based on clarity, UX, and business relevance. Future improvements may include:
- AI model for predictive lead scoring
- Company description summarization via LLM (e.g., OpenAI, HuggingFace Transformers)
- CRM integration

---

## ✅ Rationale
This solution is simple, fast, and practical. It solves the real problem of lead overload by enabling non-technical users to prioritize targets instantly. It's ready for business use and easily extensible with AI.
