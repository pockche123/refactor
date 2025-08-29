#!/usr/bin/env python3
"""
Test model generalization: trained on Commons/Gson, tested on IntelliJ
"""

import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
import numpy as np

def main():
    # Load IntelliJ data
    intellij_df = pd.read_csv('data/intellij_dataset.csv')
    print(f"IntelliJ dataset: {len(intellij_df)} instances")
    print(f"Refactoring types: {len(intellij_df['refactoring_type'].unique())}")
    
    # Load trained model
    try:
        model = joblib.load('models/enhanced_refactoring_classifier.pkl')
        print("Using enhanced model (92.1% accuracy on training data)")
    except:
        print("Error: No enhanced model found.")
        return
    
    # Prepare features (add missing enhanced features with defaults)
    intellij_df['class_encoded'] = pd.Categorical(intellij_df['class_name'].fillna('')).codes
    intellij_df['method_encoded'] = pd.Categorical(intellij_df['method_name'].fillna('')).codes
    intellij_df['cyclomatic_complexity'] = 2  # Default complexity
    intellij_df['nesting_depth'] = 1  # Default nesting
    
    X = intellij_df[['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']].fillna(0)
    y_true = intellij_df['refactoring_type']
    
    # Predict
    y_pred = model.predict(X)
    
    # Results
    accuracy = accuracy_score(y_true, y_pred)
    baseline = y_true.value_counts().iloc[0] / len(y_true)
    
    # Calculate precision, recall, F1-score
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    
    print(f"\n=== GENERALIZATION TEST RESULTS ===")
    print(f"Dataset: IntelliJ Community ({len(intellij_df)} instances)")
    print(f"Refactoring types: {len(y_true.unique())} unique types")
    print(f"\n--- PERFORMANCE METRICS ---")
    print(f"Accuracy:  {accuracy:.3f} ({accuracy:.1%})")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-Score:  {f1:.3f}")
    print(f"\nBaseline (most frequent): {baseline:.3f} ({baseline:.1%})")
    print(f"Improvement over baseline: {(accuracy - baseline):+.1%}")
    
    # Detailed classification report
    print(f"\n--- DETAILED CLASSIFICATION REPORT ---")
    print(classification_report(y_true, y_pred, zero_division=0))
    
    # Domain shift analysis
    print(f"\n--- DOMAIN SHIFT ANALYSIS ---")
    print("Top 5 actual refactorings in IntelliJ:")
    actual_counts = y_true.value_counts().head()
    for reftype, count in actual_counts.items():
        print(f"  {reftype}: {count} ({count/len(y_true):.1%})")
    
    print(f"\nTop 5 predicted refactorings:")
    pred_counts = pd.Series(y_pred).value_counts().head()
    for reftype, count in pred_counts.items():
        print(f"  {reftype}: {count} ({count/len(y_pred):.1%})")
    
    # Save results
    results_df = pd.DataFrame({
        'actual': y_true,
        'predicted': y_pred,
        'correct': y_true == y_pred
    })
    results_df.to_csv('results/intellij_generalization_results.csv', index=False)
    print(f"\nDetailed results saved to results/intellij_generalization_results.csv")

if __name__ == "__main__":
    main()
