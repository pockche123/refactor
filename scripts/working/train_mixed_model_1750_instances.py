#!/usr/bin/env python3
"""
Train Mixed Model on ALL 1,750 instances (5 projects × 350 instances each)
Cross-domain refactoring prediction analysis
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    print("🚀 MIXED MODEL ML TRAINING (1,750 INSTANCES)")
    print("=" * 65)
    print("Training on ALL 5 projects: Commons Lang + IntelliJ + Kafka + Spring + Mockito")
    
    # Load all 350-instance datasets
    print("📊 Loading all 350-instance datasets...")
    
    # Load individual datasets
    commons_lang_df = pd.read_csv('data/commons_lang_simple_dataset_350.csv')
    commons_lang_df['project'] = 'commons_lang'
    
    intellij_df = pd.read_csv('data/intellij_simple_dataset_350.csv')
    intellij_df['project'] = 'intellij'
    
    kafka_df = pd.read_csv('data/kafka_simple_dataset_350.csv')
    kafka_df['project'] = 'kafka'
    
    spring_df = pd.read_csv('data/spring_simple_dataset_350.csv')
    spring_df['project'] = 'spring'
    
    mockito_df = pd.read_csv('data/mockito_simple_dataset_350.csv')
    mockito_df['project'] = 'mockito'
    
    # Combine all datasets
    mixed_df = pd.concat([commons_lang_df, intellij_df, kafka_df, spring_df, mockito_df], ignore_index=True)
    
    print(f"   Commons Lang: {len(commons_lang_df)} instances")
    print(f"   IntelliJ: {len(intellij_df)} instances")
    print(f"   Kafka: {len(kafka_df)} instances")
    print(f"   Spring: {len(spring_df)} instances")
    print(f"   Mockito: {len(mockito_df)} instances")
    print(f"   TOTAL MIXED: {len(mixed_df)} instances")
    
    # Prepare features
    print("🔧 Preparing features...")
    le_file = LabelEncoder()
    le_project = LabelEncoder()
    
    mixed_df['file_path_encoded'] = le_file.fit_transform(mixed_df['file_path'])
    mixed_df['project_encoded'] = le_project.fit_transform(mixed_df['project'])
    
    # Feature columns (including project as a feature)
    feature_columns = ['file_path_encoded', 'project_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X = mixed_df[feature_columns]
    y = mixed_df['refactoring_type']
    
    print(f"   Features: {len(feature_columns)} (including project domain)")
    print(f"   Unique refactoring types: {len(y.unique())}")
    print(f"   Projects: {mixed_df['project'].unique()}")
    
    # Split data (70-30)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=mixed_df['project'])
    
    print(f"   Training set: {len(X_train)} instances")
    print(f"   Test set: {len(X_test)} instances")
    
    # Train Random Forest
    print("🤖 Training Mixed Random Forest model...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"   ✅ Mixed model trained with {test_accuracy:.1%} test accuracy")
    
    # Full dataset predictions
    print("🔮 Making predictions on full mixed dataset...")
    y_pred_full = rf.predict(X)
    full_accuracy = accuracy_score(y, y_pred_full)
    correct_predictions = (y == y_pred_full).sum()
    
    print(f"   Full dataset accuracy: {full_accuracy:.1%}")
    print(f"   Correct predictions: {correct_predictions}/{len(mixed_df)}")
    
    # Per-project analysis
    print("\n📊 Per-Project Performance Analysis:")
    for project in mixed_df['project'].unique():
        project_mask = mixed_df['project'] == project
        project_data = mixed_df[project_mask]
        project_X = X[project_mask]
        project_y = y[project_mask]
        project_pred = rf.predict(project_X)
        project_accuracy = accuracy_score(project_y, project_pred)
        project_correct = (project_y == project_pred).sum()
        
        print(f"   {project.upper()}: {project_accuracy:.1%} accuracy ({project_correct}/{len(project_data)} correct)")
    
    # Save model and encoders
    print("💾 Saving mixed model...")
    joblib.dump(rf, 'models/mixed_rf_model_1750.pkl')
    joblib.dump(le_file, 'models/mixed_file_encoder_1750.pkl')
    joblib.dump(le_project, 'models/mixed_project_encoder_1750.pkl')
    print("   ✅ models/mixed_rf_model_1750.pkl")
    print("   ✅ models/mixed_file_encoder_1750.pkl")
    print("   ✅ models/mixed_project_encoder_1750.pkl")
    
    # Save predictions
    results_df = mixed_df.copy()
    results_df['predicted_type'] = y_pred_full
    results_df['correct_prediction'] = (y == y_pred_full)
    
    results_file = 'results/working/mixed_ml_test_results_1750.csv'
    results_df.to_csv(results_file, index=False)
    print(f"   ✅ {results_file}")
    
    # Detailed results
    print(f"\n📈 MIXED MODEL 1,750-INSTANCE RESULTS:")
    print(f"   Dataset size: {len(mixed_df)} refactorings (5 projects)")
    print(f"   Test accuracy: {test_accuracy:.1%}")
    print(f"   Full dataset accuracy: {full_accuracy:.1%}")
    print(f"   Correct predictions: {correct_predictions}")
    print(f"   Ready for behavioral validation: {correct_predictions} test cases")
    
    # Top refactoring types across all projects
    print(f"\n📊 Top 10 Refactoring Types (Cross-Domain):")
    type_counts = mixed_df['refactoring_type'].value_counts()
    for i, (ref_type, count) in enumerate(type_counts.head(10).items()):
        percentage = (count / len(mixed_df)) * 100
        print(f"   {i+1:2d}. {ref_type}: {count} ({percentage:.1f}%)")
    
    # Project distribution
    print(f"\n📊 Project Distribution:")
    project_counts = mixed_df['project'].value_counts()
    for project, count in project_counts.items():
        percentage = (count / len(mixed_df)) * 100
        print(f"   {project.upper()}: {count} instances ({percentage:.1f}%)")
    
    # Compare with individual model accuracies
    print(f"\n📊 Mixed vs Individual Model Comparison:")
    individual_accuracies = {
        'commons_lang': 96.3,
        'intellij': 78.9,
        'kafka': 73.7,
        'spring': 69.4,
        'mockito': 56.9
    }
    
    print("   Project        | Individual | Mixed | Difference")
    print("   ---------------|------------|-------|----------")
    for project in mixed_df['project'].unique():
        project_mask = mixed_df['project'] == project
        project_X = X[project_mask]
        project_y = y[project_mask]
        project_pred = rf.predict(project_X)
        mixed_acc = accuracy_score(project_y, project_pred) * 100
        individual_acc = individual_accuracies[project]
        diff = mixed_acc - individual_acc
        
        print(f"   {project.upper():14s} | {individual_acc:8.1f}% | {mixed_acc:5.1f}% | {diff:+6.1f}%")
    
    # Classification report
    print(f"\n📊 Mixed Model Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()
