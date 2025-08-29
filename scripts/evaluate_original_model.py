#!/usr/bin/env python3
"""
Comprehensive evaluation of model on original training data
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder

def main():
    # Load original enhanced dataset
    df = pd.read_csv('data/enhanced_dataset.csv')
    print(f"Original dataset: {len(df)} instances")
    
    # Prepare features (same as training)
    le_class = LabelEncoder()
    le_method = LabelEncoder()
    
    df['class_encoded'] = le_class.fit_transform(df['class_name'].fillna(''))
    df['method_encoded'] = le_method.fit_transform(df['method_name'].fillna(''))
    
    X = df[['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']]
    y = df['refactoring_type']
    
    # Same split as training (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Load trained model
    model = joblib.load('models/enhanced_refactoring_classifier.pkl')
    
    # Predict on test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
    baseline = y_test.value_counts().iloc[0] / len(y_test)
    
    print(f"\n=== ORIGINAL MODEL EVALUATION ===")
    print(f"Dataset: Enhanced Commons/Gson ({len(X_test)} test instances)")
    print(f"Refactoring types: {len(y_test.unique())} unique types")
    print(f"\n--- PERFORMANCE METRICS ---")
    print(f"Accuracy:  {accuracy:.3f} ({accuracy:.1%})")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-Score:  {f1:.3f}")
    print(f"\nBaseline (most frequent): {baseline:.3f} ({baseline:.1%})")
    print(f"Improvement over baseline: {(accuracy - baseline):+.1%}")
    
    # Detailed classification report
    print(f"\n--- DETAILED CLASSIFICATION REPORT ---")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Top refactoring types
    print(f"\n--- REFACTORING TYPE DISTRIBUTION ---")
    print("Top 5 refactoring types in test set:")
    test_counts = y_test.value_counts().head()
    for reftype, count in test_counts.items():
        print(f"  {reftype}: {count} ({count/len(y_test):.1%})")
    
    # Save results
    results_df = pd.DataFrame({
        'actual': y_test,
        'predicted': y_pred,
        'correct': y_test == y_pred
    })
    results_df.to_csv('results/original_model_evaluation.csv', index=False)
    print(f"\nDetailed results saved to results/original_model_evaluation.csv")

if __name__ == "__main__":
    main()
