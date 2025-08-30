#!/usr/bin/env python3
"""
Generate detailed classification reports for mixed domain training results
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import joblib

def load_and_analyze_domains():
    """Load all domains and generate detailed analysis"""
    
    # Load Apache Commons/Gson
    apache_df = pd.read_csv('data/enhanced_dataset.csv')
    apache_df['domain'] = 'apache_commons_gson'
    apache_df['class_encoded'] = pd.Categorical(apache_df['class_name'].fillna('')).codes
    apache_df['method_encoded'] = pd.Categorical(apache_df['method_name'].fillna('')).codes
    
    # Load other domains
    intellij_df = pd.read_csv('data/intellij_enhanced_dataset.csv')
    intellij_df['domain'] = 'intellij'
    
    mockito_df = pd.read_csv('data/mockito_enhanced_dataset.csv')
    mockito_df['domain'] = 'mockito'
    
    elasticsearch_df = pd.read_csv('data/elasticsearch_enhanced_dataset.csv')
    elasticsearch_df['domain'] = 'elasticsearch'
    
    domains = [
        ('apache_commons_gson', apache_df),
        ('intellij', intellij_df),
        ('mockito', mockito_df),
        ('elasticsearch', elasticsearch_df)
    ]
    
    # Create splits and train model
    train_parts = []
    test_parts = []
    
    for domain_name, df in domains:
        class_counts = df['refactoring_type'].value_counts()
        valid_classes = class_counts[class_counts >= 2].index
        df_filtered = df[df['refactoring_type'].isin(valid_classes)]
        
        train_df, test_df = train_test_split(
            df_filtered, test_size=0.3, random_state=42, 
            stratify=df_filtered['refactoring_type']
        )
        
        train_parts.append(train_df)
        test_parts.append((domain_name, test_df))
    
    # Train model
    combined_train = pd.concat(train_parts, ignore_index=True)
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X_train = combined_train[feature_cols].fillna(0)
    y_train = combined_train['refactoring_type']
    
    classes = np.unique(y_train)
    class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = dict(zip(classes, class_weights))
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weight_dict, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Generate detailed reports for each domain
    for domain_name, test_df in test_parts:
        print(f"\n{'='*60}")
        print(f"DETAILED ANALYSIS: {domain_name.upper()}")
        print(f"{'='*60}")
        
        X_test = test_df[feature_cols].fillna(0)
        y_test = test_df['refactoring_type']
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Dataset Size: {len(test_df)} instances")
        print(f"Accuracy: {accuracy:.1%}")
        print(f"Complexity Range: {test_df['cyclomatic_complexity'].min()}-{test_df['cyclomatic_complexity'].max()}")
        print(f"Nesting Range: {test_df['nesting_depth'].min()}-{test_df['nesting_depth'].max()}")
        print(f"Unique Refactoring Types: {len(test_df['refactoring_type'].unique())}")
        print(f"Unique Predictions: {len(set(y_pred))}")
        
        print(f"\nComplexity Statistics:")
        print(f"  Mean Complexity: {test_df['cyclomatic_complexity'].mean():.1f}")
        print(f"  Std Complexity: {test_df['cyclomatic_complexity'].std():.1f}")
        print(f"  Mean Nesting: {test_df['nesting_depth'].mean():.1f}")
        print(f"  Mean Lines Changed: {test_df['lines_changed'].mean():.1f}")
        
        print(f"\nComplete Classification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        # Top actual vs predicted
        print(f"\nTop 10 Actual Refactoring Types:")
        actual_counts = test_df['refactoring_type'].value_counts().head(10)
        for reftype, count in actual_counts.items():
            print(f"  {reftype}: {count} ({count/len(test_df)*100:.1f}%)")
        
        print(f"\nTop 10 Predicted Refactoring Types:")
        pred_counts = pd.Series(y_pred).value_counts().head(10)
        for reftype, count in pred_counts.items():
            print(f"  {reftype}: {count} ({count/len(y_pred)*100:.1f}%)")

if __name__ == "__main__":
    load_and_analyze_domains()
