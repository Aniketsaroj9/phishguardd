# Phase 2: ML Model Training & Evaluation - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Train a TF-IDF + Logistic Regression pipeline on the SMS Spam Collection dataset, evaluate it, and serialize the trained model + vectorizer to .pkl files in `backend/ml/`. This is a reference/learning project — not production deployment.

</domain>

<decisions>
## Implementation Decisions

### Project Scope
- **D-01:** This is a reference/learning project, not production deployment. Use sensible defaults everywhere. Don't over-engineer.

### Dataset & Preprocessing
- **D-02:** (Agent's Discretion) Use SMS Spam Collection dataset from UCI/Kaggle (5,574 labeled messages)
- **D-03:** (Agent's Discretion) Standard preprocessing: lowercase, remove punctuation, tokenize, remove stopwords. No stemming needed for simplicity.

### Model Configuration
- **D-04:** (Agent's Discretion) TF-IDF with unigrams + bigrams (`ngram_range=(1, 2)`), `max_features=5000`, `stop_words='english'`
- **D-05:** (Agent's Discretion) Logistic Regression with `max_iter=1000`, default C=1.0, no hyperparameter tuning

### Evaluation
- **D-06:** (Agent's Discretion) 80/20 stratified train/test split
- **D-07:** (Agent's Discretion) Report Accuracy, Precision, Recall, F1-score. Target 80%+ accuracy.
- **D-08:** (Agent's Discretion) Print confusion matrix and classification report

### Training Script
- **D-09:** (Agent's Discretion) Standalone Python script (`train_model.py`), not Jupyter notebook
- **D-10:** (Agent's Discretion) Script prints evaluation metrics to console and saves model artifacts
- **D-11:** Model artifacts saved to `backend/ml/model.pkl` and `backend/ml/vectorizer.pkl` (from Phase 1 config)

### Agent's Discretion
All technical decisions deferred to agent — user confirmed this is a reference project, use recommended defaults for everything.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Core value, constraints, key decisions
- `.planning/REQUIREMENTS.md` — ML-01 through ML-05 requirement details
- `.planning/ROADMAP.md` — Phase 2 success criteria

### Prior Phases
- `.planning/phases/01-database-backend-foundation/01-CONTEXT.md` — D-05: ML artifacts in `backend/ml/`
- `backend/config.py` — ML_CONFIG with model paths

### Research
- `.planning/research/STACK.md` — scikit-learn, NLTK versions and usage
- `.planning/research/PITFALLS.md` — ML overfitting prevention, model file paths

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/config.py` — ML_CONFIG with MODEL_PATH and VECTORIZER_PATH
- `backend/ml/` — Directory already exists (created in Phase 1)

### Established Patterns
- Phase 1 established modular file structure in `backend/`
- Config values imported from `config.py`

### Integration Points
- Phase 4 (Message Analyzer) will load the serialized model from `backend/ml/model.pkl`
- Paths configured in `backend/config.py` ML_CONFIG

</code_context>

<specifics>
## Specific Ideas

- User confirmed: reference/learning project — use defaults, don't over-engineer
- Dataset can be downloaded programmatically or bundled in the repo

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-ml-model-training-evaluation*
*Context gathered: 2026-05-19*
