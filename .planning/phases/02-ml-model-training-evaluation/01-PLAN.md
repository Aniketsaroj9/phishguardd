---
phase: 2
plan: 01
title: "Train TF-IDF + Logistic Regression SMS Spam Classifier"
wave: 1
depends_on: []
files_modified:
  - backend/ml/train_model.py
  - backend/ml/model.pkl
  - backend/ml/vectorizer.pkl
  - backend/ml/dataset/SMSSpamCollection.tsv
requirements:
  - ML-01
  - ML-02
  - ML-03
  - ML-04
  - ML-05
autonomous: true
---

# Plan 01: Train TF-IDF + Logistic Regression SMS Spam Classifier

<objective>
Download the SMS Spam Collection dataset, preprocess it, train a TF-IDF + Logistic Regression pipeline, evaluate with Precision/Recall/F1, and serialize model artifacts to backend/ml/.
</objective>

<must_haves>
- SMS Spam Collection dataset loaded and preprocessed
- TF-IDF + Logistic Regression pipeline trained with stratified 80/20 split
- Model achieves 80%+ accuracy with metrics documented
- Trained model serialized to backend/ml/model.pkl
- TF-IDF vectorizer serialized to backend/ml/vectorizer.pkl
- Training script is reproducible and committed
</must_haves>

## Tasks

<task id="01.1" title="Create training script with dataset loading, preprocessing, training, evaluation, and serialization">
<read_first>
- backend/config.py (ML_CONFIG paths)
- .planning/phases/02-ml-model-training-evaluation/02-CONTEXT.md (all decisions)
- .planning/research/PITFALLS.md (ML overfitting section)
</read_first>

<action>
Create `backend/ml/train_model.py` — a standalone training script that:

1. **Loads dataset** — SMS Spam Collection (tab-separated, columns: label, message)
2. **Preprocesses** — lowercase, remove punctuation, basic cleaning
3. **Splits** — 80/20 stratified train/test split
4. **Trains** — scikit-learn Pipeline with TfidfVectorizer + LogisticRegression
5. **Evaluates** — prints accuracy, classification report, confusion matrix
6. **Serializes** — saves pipeline to model.pkl and vectorizer separately

The script should handle the dataset being in `backend/ml/dataset/SMSSpamCollection.tsv`.

Key parameters:
- TfidfVectorizer: `ngram_range=(1, 2)`, `max_features=5000`, `stop_words='english'`
- LogisticRegression: `max_iter=1000`
- train_test_split: `test_size=0.2`, `random_state=42`, `stratify=y`

The script should print clear output showing dataset info, training progress, and evaluation metrics.
</action>

<acceptance_criteria>
- `backend/ml/train_model.py` contains `TfidfVectorizer`
- `backend/ml/train_model.py` contains `LogisticRegression`
- `backend/ml/train_model.py` contains `train_test_split`
- `backend/ml/train_model.py` contains `classification_report`
- `backend/ml/train_model.py` contains `confusion_matrix`
- `backend/ml/train_model.py` contains `joblib.dump`
- `backend/ml/train_model.py` contains `ngram_range=(1, 2)`
- `backend/ml/train_model.py` contains `max_features=5000`
- `backend/ml/train_model.py` contains `stratify`
- Running the script produces model.pkl and vectorizer.pkl in backend/ml/
</acceptance_criteria>
</task>

<verification>
1. `backend/ml/train_model.py` exists and is a valid Python script
2. Running the script downloads/loads dataset and trains model
3. Model achieves 80%+ accuracy on test set
4. `backend/ml/model.pkl` and `backend/ml/vectorizer.pkl` exist after training
5. Evaluation metrics (Precision, Recall, F1) are printed
</verification>
