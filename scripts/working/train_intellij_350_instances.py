#!/usr/bin/env python3
"""
Train IntelliJ ML model on 350-instance dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    print("🚀 INTELLIJ ML TRAINING (350 INSTANCES)")
    print("=" * 55)
    
    # Load 350-instance dataset
    print("📊 Loading IntelliJ 350-instance dataset...")
    df = pd.read_csv('data/intellij_simple_dataset_350.csv')
    print(f"   Loaded {len(df)} refactoring instances")
    
    # Prepare features
    print("🔧 Preparing features...")
    le_file = LabelEncoder()
    df['file_path_encoded'] = le_file.fit_transform(df['file_path'])
    
    # Feature columns
    feature_columns = ['file_path_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X = df[feature_columns]
    y = df['refactoring_type']
    
    print(f"   Features: {len(feature_columns)}")
    print(f"   Unique refactoring types: {len(y.unique())}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train Random Forest
    print("🤖 Training Random Forest model...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"   ✅ Model trained with {test_accuracy:.1%} test accuracy")
    
    # Full dataset predictions
    print("🔮 Making predictions on full dataset...")
    y_pred_full = rf.predict(X)
    full_accuracy = accuracy_score(y, y_pred_full)
    correct_predictions = (y == y_pred_full).sum()
    
    print(f"   Full dataset accuracy: {full_accuracy:.1%}")
    print(f"   Correct predictions: {correct_predictions}/{len(df)}")
    
    # Save model and encoder
    print("💾 Saving model...")
    joblib.dump(rf, 'models/intellij_rf_model_350.pkl')
    joblib.dump(le_file, 'models/intellij_file_encoder_350.pkl')
    print("   ✅ models/intellij_rf_model_350.pkl")
    print("   ✅ models/intellij_file_encoder_350.pkl")
    
    # Save predictions
    results_df = df.copy()
    results_df['predicted_type'] = y_pred_full
    results_df['correct_prediction'] = (y == y_pred_full)
    
    results_file = 'results/working/intellij_ml_test_results_350.csv'
    results_df.to_csv(results_file, index=False)
    print(f"   ✅ {results_file}")
    
    # Detailed results
    print(f"\n📈 INTELLIJ 350-INSTANCE RESULTS:")
    print(f"   Dataset size: {len(df)} refactorings")
    print(f"   Test accuracy: {test_accuracy:.1%}")
    print(f"   Full dataset accuracy: {full_accuracy:.1%}")
    print(f"   Correct predictions: {correct_predictions}")
    print(f"   Ready for behavioral validation: {correct_predictions} test cases")
    
    # Top refactoring types
    print(f"\n📊 Top 5 Refactoring Types:")
    type_counts = df['refactoring_type'].value_counts()
    for i, (ref_type, count) in enumerate(type_counts.head().items()):
        percentage = (count / len(df)) * 100
        print(f"   {i+1}. {ref_type}: {count} ({percentage:.1f}%)")
    
    # Classification report
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()
