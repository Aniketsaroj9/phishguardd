"""PhishGuard ML Model Training Script

Trains a TF-IDF + Logistic Regression pipeline for SMS/email scam detection.
Uses the SMS Spam Collection dataset (5,574 labeled messages).

Usage:
    cd backend
    python ml/train_model.py

Output:
    - ml/model.pkl       (full sklearn Pipeline: TF-IDF + LogisticRegression)
    - ml/vectorizer.pkl  (standalone TF-IDF vectorizer for feature inspection)
"""

import os
import re
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import joblib


# ========================
# Configuration
# ========================

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset', 'SMSSpamCollection.tsv')
MODEL_OUTPUT = os.path.join(os.path.dirname(__file__), 'model.pkl')
VECTORIZER_OUTPUT = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

# Model parameters
TFIDF_PARAMS = {
    'ngram_range': (1, 2),
    'max_features': 5000,
    'stop_words': 'english'
}

LR_PARAMS = {
    'max_iter': 1000,
    'random_state': 42
}

# Split parameters
TEST_SIZE = 0.2
RANDOM_STATE = 42


# ========================
# Preprocessing
# ========================

def preprocess_text(text):
    """Clean and preprocess message text.
    
    Args:
        text: Raw message string
    
    Returns:
        Cleaned lowercase text with punctuation removed
    """
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ========================
# Main Training Pipeline
# ========================

def load_dataset():
    """Load and validate the SMS Spam Collection dataset."""
    print("=" * 60)
    print("  PhishGuard ML Model Training")
    print("=" * 60)
    print()
    
    print(f"[1/5] Loading dataset from: {DATASET_PATH}")
    
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        print("Please download SMS Spam Collection from UCI/Kaggle")
        sys.exit(1)
    
    # Load tab-separated dataset (no header)
    df = pd.read_csv(
        DATASET_PATH,
        sep='\t',
        header=None,
        names=['label', 'message'],
        encoding='latin-1'
    )
    
    print(f"  Total messages: {len(df)}")
    print(f"  Label distribution:")
    label_counts = df['label'].value_counts()
    for label, count in label_counts.items():
        pct = count / len(df) * 100
        print(f"    {label}: {count} ({pct:.1f}%)")
    print()
    
    return df


def preprocess_dataset(df):
    """Preprocess the dataset: clean text and encode labels."""
    print("[2/5] Preprocessing text...")
    
    # Clean message text
    df['cleaned'] = df['message'].apply(preprocess_text)
    
    # Encode labels: ham=0 (Safe), spam=1 (Scam)
    df['label_encoded'] = df['label'].map({'ham': 0, 'spam': 1})
    
    # Check for any unmapped labels
    if df['label_encoded'].isna().any():
        print("  WARNING: Some labels could not be mapped!")
        print(df[df['label_encoded'].isna()]['label'].unique())
    
    print(f"  Preprocessing complete. Sample:")
    print(f"    Original: '{df['message'].iloc[0][:60]}...'")
    print(f"    Cleaned:  '{df['cleaned'].iloc[0][:60]}...'")
    print()
    
    return df


def split_data(df):
    """Split data into training and test sets with stratification."""
    print(f"[3/5] Splitting data ({int((1-TEST_SIZE)*100)}/{int(TEST_SIZE*100)} stratified split)...")
    
    X = df['cleaned']
    y = df['label_encoded']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    print(f"  Training set: {len(X_train)} messages")
    print(f"  Test set:     {len(X_test)} messages")
    print()
    
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """Train the TF-IDF + Logistic Regression pipeline."""
    print("[4/5] Training model...")
    print(f"  TF-IDF: ngram_range={TFIDF_PARAMS['ngram_range']}, max_features={TFIDF_PARAMS['max_features']}")
    print(f"  Classifier: LogisticRegression(max_iter={LR_PARAMS['max_iter']})")
    
    # Create sklearn Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(**TFIDF_PARAMS)),
        ('classifier', LogisticRegression(**LR_PARAMS))
    ])
    
    # Train
    pipeline.fit(X_train, y_train)
    
    print("  Training complete!")
    print()
    
    return pipeline


def evaluate_model(pipeline, X_test, y_test):
    """Evaluate the trained model and print metrics."""
    print("[5/5] Evaluating model...")
    print()
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    
    # Check minimum bar
    if accuracy >= 0.80:
        print(f"  [PASS] PASSED minimum accuracy threshold (80%+)")
    else:
        print(f"  [WARN] BELOW minimum accuracy threshold (80%+)")
    
    print()
    
    # Classification Report
    print("  Classification Report:")
    print("  " + "-" * 55)
    report = classification_report(
        y_test, y_pred,
        target_names=['Safe (ham)', 'Scam (spam)']
    )
    for line in report.split('\n'):
        print(f"  {line}")
    
    print()
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("  Confusion Matrix:")
    print(f"                    Predicted Safe  Predicted Scam")
    print(f"    Actual Safe     {cm[0][0]:>13}  {cm[0][1]:>14}")
    print(f"    Actual Scam     {cm[1][0]:>13}  {cm[1][1]:>14}")
    print()
    
    return accuracy


def save_model(pipeline):
    """Serialize the trained model and vectorizer."""
    print("  Saving model artifacts...")
    
    # Save full pipeline (TF-IDF + LR together)
    joblib.dump(pipeline, MODEL_OUTPUT)
    print(f"    Pipeline saved: {MODEL_OUTPUT}")
    
    # Save vectorizer separately (useful for feature inspection)
    vectorizer = pipeline.named_steps['tfidf']
    joblib.dump(vectorizer, VECTORIZER_OUTPUT)
    print(f"    Vectorizer saved: {VECTORIZER_OUTPUT}")
    
    # File sizes
    model_size = os.path.getsize(MODEL_OUTPUT) / 1024
    vec_size = os.path.getsize(VECTORIZER_OUTPUT) / 1024
    print(f"    Model size: {model_size:.1f} KB")
    print(f"    Vectorizer size: {vec_size:.1f} KB")
    print()


def main():
    """Run the complete training pipeline."""
    # Load
    df = load_dataset()
    
    # Preprocess
    df = preprocess_dataset(df)
    
    # Split
    X_train, X_test, y_train, y_test = split_data(df)
    
    # Train
    pipeline = train_model(X_train, y_train)
    
    # Evaluate
    accuracy = evaluate_model(pipeline, X_test, y_test)
    
    # Save
    save_model(pipeline)
    
    # Summary
    print("=" * 60)
    print("  Training Complete!")
    print(f"  Accuracy: {accuracy*100:.1f}%")
    print(f"  Model: {MODEL_OUTPUT}")
    print(f"  Vectorizer: {VECTORIZER_OUTPUT}")
    print("=" * 60)
    
    return accuracy


if __name__ == '__main__':
    main()
