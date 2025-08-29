#!/usr/bin/env python3
"""
Test model generalization on Spring Boot refactorings
"""

import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support

def main():
    # Load Spring Boot dataset
    df = pd.read_csv('data/spring-boot_dataset.csv')
    print(f"Spring Boot dataset: {len(df)} instances")
    print(f"Refactoring types: {len(df['refactoring_type'].unique())} unique types")
    
    # Load trained model
    model = joblib.load('models/enhanced_refactoring_classifier.pkl')
    print("Using enhanced model (81.8% accuracy on training data)")
    
    # Prepare features (add missing enhanced features with defaults)
    df['class_encoded'] = pd.Categorical(df['class_name'].fillna('')).codes
    df['method_encoded'] = pd.Categorical(df['method_name'].fillna('')).codes
    df['cyclomatic_complexity'] = 2  # Default complexity
    df['nesting_depth'] = 1  # Default nesting
    
    X = df[['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']].fillna(0)
    y_true = df['refactoring_type']
    
    # Predict
    y_pred = model.predict(X)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    baseline = y_true.value_counts().iloc[0] / len(y_true)
    
    print(f"\n=== SPRING BOOT GENERALIZATION RESULTS ===")
    print(f"Dataset: Spring Boot Framework ({len(df)} instances)")
    print(f"Refactoring types: {len(y_true.unique())} unique types")
    print(f"\n--- PERFORMANCE METRICS ---")
    print(f"Accuracy:  {accuracy:.3f} ({accuracy:.1%})")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-Score:  {f1:.3f}")
    print(f"\nBaseline (most frequent): {baseline:.3f} ({baseline:.1%})")
    print(f"Improvement over baseline: {(accuracy - baseline):+.1%}")
    print(f"Performance drop from training: {(0.818 - accuracy):+.1%}")
    
    # Detailed classification report
    print(f"\n--- DETAILED CLASSIFICATION REPORT ---")
    print(classification_report(y_true, y_pred, zero_division=0))
    
    # Domain shift analysis
    print(f"\n--- DOMAIN SHIFT ANALYSIS ---")
    print("Top 5 actual refactorings in Spring Boot:")
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
    results_df.to_csv('results/springboot_generalization_results.csv', index=False)
    print(f"\nDetailed results saved to results/springboot_generalization_results.csv")

if __name__ == "__main__":
    main()
