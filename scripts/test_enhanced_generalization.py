#!/usr/bin/env python3
"""
Test model generalization with real complexity features
"""

import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score

def test_enhanced_model(dataset_file, project_name):
    """Test model on dataset with real complexity features"""
    # Load enhanced dataset
    df = pd.read_csv(dataset_file)
    
    # Prepare features (same as training)
    X = df[['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']].fillna(0)
    y_true = df['refactoring_type']
    
    # Load trained model
    model = joblib.load('models/enhanced_refactoring_classifier.pkl')
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    
    print(f"\n=== {project_name.upper()} ENHANCED RESULTS ===")
    print(f"Dataset: {len(df)} instances")
    print(f"Accuracy: {accuracy:.1%}")
    print(f"Complexity range: {df['cyclomatic_complexity'].min()}-{df['cyclomatic_complexity'].max()}")
    print(f"Nesting range: {df['nesting_depth'].min()}-{df['nesting_depth'].max()}")
    
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))
    
    return accuracy

def main():
    """Test all enhanced datasets"""
    datasets = [
        ('data/intellij_enhanced_dataset.csv', 'IntelliJ'),
        ('data/mockito_enhanced_dataset.csv', 'Mockito'),
        ('data/elasticsearch_enhanced_dataset.csv', 'Elasticsearch')
    ]
    
    results = {}
    
    for dataset_file, project_name in datasets:
        try:
            accuracy = test_enhanced_model(dataset_file, project_name)
            results[project_name] = accuracy
        except Exception as e:
            print(f"Error testing {project_name}: {e}")
    
    print("\n=== ENHANCED GENERALIZATION SUMMARY ===")
    for project, accuracy in results.items():
        print(f"{project}: {accuracy:.1%}")

if __name__ == "__main__":
    main()
