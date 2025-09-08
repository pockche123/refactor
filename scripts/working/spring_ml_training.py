#!/usr/bin/env python3
"""
Spring Framework ML Training
Following same methodology as Commons Lang/IntelliJ/Mockito
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def load_spring_dataset():
    """Load Spring Framework dataset"""
    return pd.read_csv('data/spring_simple_dataset.csv')

def prepare_features(df):
    """Prepare features for ML training (same as other projects)"""
    
    # Encode file paths
    le_file = LabelEncoder()
    df['file_path_encoded'] = le_file.fit_transform(df['file_path'])
    
    # Feature columns (same as other projects)
    feature_columns = ['file_path_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X = df[feature_columns]
    
    # Target variable
    y = df['refactoring_type']
    
    return X, y, le_file

def train_model(X, y):
    """Train Random Forest model (same as other projects)"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    return rf, accuracy, y_test, y_pred, X_test

def main():
    print("🚀 SPRING FRAMEWORK ML TRAINING")
    print("=" * 50)
    
    # Load dataset
    print("📊 Loading Spring Framework dataset...")
    df = load_spring_dataset()
    print(f"   Loaded {len(df)} refactoring instances")
    
    # Check if we have enough data for ML
    if len(df) < 10:
        print("⚠️  Warning: Very small dataset - ML results may not be reliable")
    
    # Prepare features
    print("🔧 Preparing features...")
    X, y, le_file = prepare_features(df)
    
    # Train model
    print("🤖 Training Random Forest model...")
    rf, accuracy, y_test, y_pred, X_test = train_model(X, y)
    
    print(f"   ✅ Model trained with {accuracy:.1%} accuracy")
    
    # Detailed results
    print(f"\n📈 TRAINING RESULTS:")
    print(f"   Dataset size: {len(df)} refactorings")
    print(f"   Test accuracy: {accuracy:.1%}")
    print(f"   Unique refactoring types: {len(df['refactoring_type'].unique())}")
    
    # Classification report
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and encoder
    print("💾 Saving model...")
    joblib.dump(rf, 'models/spring_rf_model.pkl')
    joblib.dump(le_file, 'models/spring_file_encoder.pkl')
    print("   ✅ models/spring_rf_model.pkl")
    print("   ✅ models/spring_file_encoder.pkl")
    
    # Make predictions on full dataset
    print("🔮 Making predictions on full dataset...")
    y_pred_full = rf.predict(X)
    
    # Calculate accuracy on full dataset
    full_accuracy = accuracy_score(y, y_pred_full)
    correct_predictions = (y == y_pred_full).sum()
    
    print(f"   Full dataset accuracy: {full_accuracy:.1%}")
    print(f"   Correct predictions: {correct_predictions}/{len(df)}")
    
    # Save predictions
    results_df = df.copy()
    results_df['predicted_type'] = y_pred_full
    results_df['correct_prediction'] = (y == y_pred_full)
    
    results_file = 'results/working/spring_ml_test_results.csv'
    results_df.to_csv(results_file, index=False)
    print(f"   ✅ {results_file}")
    
    # Summary for comparison with other projects
    print(f"\n🎯 SPRING FRAMEWORK ML SUMMARY:")
    print(f"   Total refactorings: {len(df)}")
    print(f"   ML accuracy: {full_accuracy:.1%}")
    print(f"   Correct predictions: {correct_predictions}")
    print(f"   Ready for behavioral validation: {correct_predictions} test cases")

if __name__ == "__main__":
    main()
