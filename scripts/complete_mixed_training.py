#!/usr/bin/env python3
"""
Complete Mixed Domain Training: Include Apache Commons/Gson in 70-30 split
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import joblib

def load_all_domains_with_splits():
    """Load all 4 domains and create 70-30 splits"""
    
    domains_data = []
    
    # 1. Apache Commons/Gson (original training data) - needs encoding
    apache_df = pd.read_csv('data/enhanced_dataset.csv')
    apache_df['domain'] = 'apache_commons_gson'
    # Add missing encoded columns
    apache_df['class_encoded'] = pd.Categorical(apache_df['class_name'].fillna('')).codes
    apache_df['method_encoded'] = pd.Categorical(apache_df['method_name'].fillna('')).codes
    domains_data.append(('apache_commons_gson', apache_df))
    
    # 2. Other domains (already have encoded columns)
    other_domains = [
        ('intellij', 'data/intellij_enhanced_dataset.csv'),
        ('mockito', 'data/mockito_enhanced_dataset.csv'),
        ('elasticsearch', 'data/elasticsearch_enhanced_dataset.csv')
    ]
    
    for domain_name, file_path in other_domains:
        try:
            df = pd.read_csv(file_path)
            df['domain'] = domain_name
            domains_data.append((domain_name, df))
        except Exception as e:
            print(f"Could not load {domain_name}: {e}")
    
    # Create 70-30 splits for each domain
    train_parts = []
    test_parts = []
    
    print("=== DOMAIN SPLITS ===")
    for domain_name, df in domains_data:
        # Filter rare classes for stratification
        class_counts = df['refactoring_type'].value_counts()
        valid_classes = class_counts[class_counts >= 2].index
        df_filtered = df[df['refactoring_type'].isin(valid_classes)]
        
        # 70-30 split
        train_df, test_df = train_test_split(
            df_filtered, 
            test_size=0.3, 
            random_state=42, 
            stratify=df_filtered['refactoring_type']
        )
        
        train_parts.append(train_df)
        test_parts.append((domain_name, test_df))
        
        print(f"{domain_name}: {len(df)} total → {len(train_df)} train, {len(test_df)} test")
    
    # Combine all 70% for training
    combined_train = pd.concat(train_parts, ignore_index=True)
    
    print(f"\nCOMBINED TRAINING: {len(combined_train)} instances from all domains")
    print(f"Training distribution: {combined_train['domain'].value_counts().to_dict()}")
    
    return combined_train, test_parts

def train_complete_model(train_df):
    """Train on combined 70% from all 4 domains"""
    
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X_train = train_df[feature_cols].fillna(0)
    y_train = train_df['refactoring_type']
    
    print(f"\nTRAINING DATA ANALYSIS:")
    print(f"Total instances: {len(X_train)}")
    print(f"Unique classes: {len(y_train.unique())}")
    print(f"Top 5 classes: {y_train.value_counts().head().to_dict()}")
    
    # Balanced class weights
    classes = np.unique(y_train)
    class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = dict(zip(classes, class_weights))
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight=class_weight_dict,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Training accuracy
    train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_pred)
    print(f"Training accuracy: {train_accuracy:.1%}")
    
    return model

def test_all_domains(model, test_parts):
    """Test on all domain 30% splits + combined"""
    
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    
    print(f"\n=== INDIVIDUAL DOMAIN RESULTS ===")
    
    domain_results = {}
    all_test_data = []
    
    for domain_name, test_df in test_parts:
        X_test = test_df[feature_cols].fillna(0)
        y_test = test_df['refactoring_type']
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        domain_results[domain_name] = accuracy
        
        # Store for combined analysis
        all_test_data.extend(list(zip(X_test.values, y_test, y_pred)))
        
        print(f"\n{domain_name.upper()}:")
        print(f"  Accuracy: {accuracy:.1%}")
        print(f"  Test size: {len(X_test)}")
        print(f"  Unique predictions: {len(set(y_pred))}")
        
        # Show top predictions
        pred_counts = pd.Series(y_pred).value_counts().head(3)
        print(f"  Top predictions: {pred_counts.to_dict()}")
    
    # Combined test performance
    all_X = [item[0] for item in all_test_data]
    all_y_true = [item[1] for item in all_test_data]
    all_y_pred = [item[2] for item in all_test_data]
    
    combined_accuracy = accuracy_score(all_y_true, all_y_pred)
    
    print(f"\n=== COMBINED TEST RESULTS ===")
    print(f"Overall accuracy: {combined_accuracy:.1%}")
    print(f"Total test instances: {len(all_y_true)}")
    
    return domain_results, combined_accuracy

def main():
    """Execute complete mixed domain training with all 4 domains"""
    
    print("=== COMPLETE MIXED DOMAIN TRAINING ===")
    print("Including: Apache Commons/Gson + IntelliJ + Mockito + Elasticsearch")
    print("Strategy: 70% from each domain → combined training")
    print("Testing: 30% from each domain individually + combined\n")
    
    # Load all domains with splits
    combined_train, test_parts = load_all_domains_with_splits()
    
    # Train on combined 70%
    model = train_complete_model(combined_train)
    
    # Test on all 30% splits
    domain_results, combined_accuracy = test_all_domains(model, test_parts)
    
    # Save model
    model_path = 'models/complete_mixed_domain_classifier.pkl'
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    
    # Final summary
    print(f"\n=== FINAL RESULTS SUMMARY ===")
    print(f"Combined test accuracy: {combined_accuracy:.1%}")
    print("\nPer-domain results:")
    for domain, accuracy in sorted(domain_results.items()):
        print(f"  {domain}: {accuracy:.1%}")

if __name__ == "__main__":
    main()
