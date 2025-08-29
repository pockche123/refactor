#!/usr/bin/env python3
"""
Mixed Domain Training: Combine 70% from all projects for training, test on 30% splits
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import joblib

def load_and_split_datasets():
    """Load all datasets and create 70-30 splits per domain"""
    
    datasets = {
        'intellij': 'data/intellij_enhanced_dataset.csv',
        'mockito': 'data/mockito_enhanced_dataset.csv', 
        'elasticsearch': 'data/elasticsearch_enhanced_dataset.csv'
    }
    
    train_parts = []
    test_parts = []
    
    for domain_name, file_path in datasets.items():
        try:
            df = pd.read_csv(file_path)
            df['domain'] = domain_name
            
            # Filter out classes with only 1 instance for stratification
            class_counts = df['refactoring_type'].value_counts()
            valid_classes = class_counts[class_counts >= 2].index
            df_filtered = df[df['refactoring_type'].isin(valid_classes)]
            
            print(f"{domain_name}: {len(df)} total, {len(df_filtered)} after filtering rare classes")
            
            # 70-30 split for this domain
            train_df, test_df = train_test_split(
                df_filtered, 
                test_size=0.3, 
                random_state=42, 
                stratify=df_filtered['refactoring_type']
            )
            
            train_parts.append(train_df)
            test_parts.append(test_df)
            
            print(f"  Split: {len(train_df)} train, {len(test_df)} test")
            
        except Exception as e:
            print(f"Could not load {domain_name}: {e}")
    
    if not train_parts:
        raise ValueError("No datasets loaded successfully!")
    
    # Combine all 70% portions into one training set
    combined_train = pd.concat(train_parts, ignore_index=True)
    
    print(f"\nCOMBINED TRAINING SET: {len(combined_train)} instances")
    print(f"Training domains: {combined_train['domain'].value_counts().to_dict()}")
    print(f"Training classes: {len(combined_train['refactoring_type'].unique())} unique refactoring types")
    
    return combined_train, test_parts

def train_mixed_model(train_df):
    """Train on combined 70% from all domains"""
    
    # Prepare features
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X_train = train_df[feature_cols].fillna(0)
    y_train = train_df['refactoring_type']
    
    print(f"\nClass distribution in combined training set:")
    class_counts = y_train.value_counts()
    print(f"Total classes: {len(class_counts)}")
    print(f"Top 5 classes: {class_counts.head().to_dict()}")
    print(f"Most balanced: {class_counts.tail().to_dict()}")
    
    # Calculate balanced class weights
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
    
    # Training performance
    train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_pred)
    print(f"\nTraining accuracy on combined data: {train_accuracy:.1%}")
    
    return model

def test_on_domains(model, test_parts):
    """Test model on each domain's 30% and combined 30%"""
    
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    
    domain_results = {}
    all_test_X = []
    all_test_y = []
    all_test_pred = []
    
    print(f"\n=== TESTING ON INDIVIDUAL DOMAINS ===")
    
    for test_df in test_parts:
        domain = test_df['domain'].iloc[0]
        
        X_test = test_df[feature_cols].fillna(0)
        y_test = test_df['refactoring_type']
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        domain_results[domain] = accuracy
        
        # Store for combined analysis
        all_test_X.extend(X_test.values.tolist())
        all_test_y.extend(y_test.tolist())
        all_test_pred.extend(y_pred.tolist())
        
        print(f"\n{domain.upper()}:")
        print(f"  Accuracy: {accuracy:.1%}")
        print(f"  Test size: {len(X_test)}")
        print(f"  Unique predictions: {len(set(y_pred))}")
        print(f"  Top predictions: {pd.Series(y_pred).value_counts().head(3).to_dict()}")
    
    # Combined test performance
    combined_accuracy = accuracy_score(all_test_y, all_test_pred)
    
    print(f"\n=== COMBINED TEST SET PERFORMANCE ===")
    print(f"Overall accuracy: {combined_accuracy:.1%}")
    print(f"Total test instances: {len(all_test_y)}")
    
    print(f"\nCombined Classification Report:")
    print(classification_report(all_test_y, all_test_pred, zero_division=0))
    
    return domain_results, combined_accuracy

def main():
    """Execute mixed domain training"""
    
    print("=== MIXED DOMAIN TRAINING ===")
    print("Strategy: Combine 70% from all domains for training")
    print("Testing: Individual 30% per domain + combined 30%\n")
    
    # Load and split datasets
    combined_train, test_parts = load_and_split_datasets()
    
    # Train on combined 70%
    model = train_mixed_model(combined_train)
    
    # Test on 30% splits
    domain_results, combined_accuracy = test_on_domains(model, test_parts)
    
    # Save model
    model_path = 'models/mixed_domain_classifier.pkl'
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    
    # Final summary
    print(f"\n=== FINAL RESULTS ===")
    print(f"Combined test accuracy: {combined_accuracy:.1%}")
    print("Per-domain results:")
    for domain, accuracy in domain_results.items():
        print(f"  {domain}: {accuracy:.1%}")

if __name__ == "__main__":
    main()
