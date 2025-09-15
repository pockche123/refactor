#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os

def load_datasets(domain):
    """Load train and test datasets for a domain"""
    try:
        train_df = pd.read_csv(f'data/{domain}_350_real_train.csv')
        test_df = pd.read_csv(f'data/{domain}_350_real_test.csv')
        return train_df, test_df
    except FileNotFoundError as e:
        print(f"Dataset not found for {domain}: {e}")
        return None, None

def prepare_features(train_df, test_df):
    """Prepare features and labels"""
    feature_cols = ['lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    
    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]
    
    # Combine train and test labels for consistent encoding
    all_labels = pd.concat([train_df['refactoring_type'], test_df['refactoring_type']])
    le = LabelEncoder()
    le.fit(all_labels)
    
    y_train = le.transform(train_df['refactoring_type'])
    y_test = le.transform(test_df['refactoring_type'])
    
    return X_train, X_test, y_train, y_test, le

def train_and_test_models(X_train, X_test, y_train, y_test, le, domain):
    """Train and test all models"""
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n=== {name} on {domain.upper()} ===")
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.3f}")
        
        # Classification report
        unique_labels = np.unique(np.concatenate([y_test, y_pred]))
        target_names = [le.classes_[i] for i in unique_labels]
        report = classification_report(y_test, y_pred, labels=unique_labels, target_names=target_names, zero_division=0)
        print("Classification Report:")
        print(report)
        
        # Store results
        results[name] = {
            'accuracy': accuracy,
            'predictions': y_pred,
            'true_labels': y_test,
            'label_names': le.inverse_transform(y_pred),
            'true_names': le.inverse_transform(y_test)
        }
    
    return results

def save_results(results, domain, test_df):
    """Save detailed results to CSV"""
    os.makedirs('results/ml_testing', exist_ok=True)
    
    for model_name, result in results.items():
        # Create detailed results DataFrame
        detailed_results = test_df.copy()
        detailed_results['predicted_type'] = result['label_names']
        detailed_results['correct'] = result['true_names'] == result['label_names']
        detailed_results['model'] = model_name
        
        # Save
        filename = f'results/ml_testing/{domain}_{model_name.lower()}_results.csv'
        detailed_results.to_csv(filename, index=False)
        print(f"Saved: {filename}")

def main():
    domains = ['commons_lang', 'spring', 'kafka', 'intellij', 'mockito']
    
    all_results = {}
    
    for domain in domains:
        print(f"\n{'='*50}")
        print(f"TESTING DOMAIN: {domain.upper()}")
        print(f"{'='*50}")
        
        # Load data
        train_df, test_df = load_datasets(domain)
        if train_df is None or test_df is None:
            print(f"Skipping {domain} - no data")
            continue
        
        print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")
        print(f"Unique types: {train_df['refactoring_type'].nunique()}")
        
        # Prepare features
        X_train, X_test, y_train, y_test, le = prepare_features(train_df, test_df)
        
        # Train and test
        results = train_and_test_models(X_train, X_test, y_train, y_test, le, domain)
        
        # Save results
        save_results(results, domain, test_df)
        
        all_results[domain] = results
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY OF ALL RESULTS")
    print(f"{'='*50}")
    
    for domain, domain_results in all_results.items():
        print(f"\n{domain.upper()}:")
        for model, result in domain_results.items():
            print(f"  {model}: {result['accuracy']:.3f}")

if __name__ == "__main__":
    main()
