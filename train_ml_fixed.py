import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import os

def train_and_test_ml(train_file, test_file, domain):
    """Train and test ML models with proper label handling"""
    
    # Load data
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    
    # Combine to get all possible labels
    all_df = pd.concat([train_df, test_df])
    
    # Features
    feature_cols = ['lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    
    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]
    
    # Encode labels using all data
    le = LabelEncoder()
    le.fit(all_df['refactoring_type'])
    
    y_train = le.transform(train_df['refactoring_type'])
    y_test = le.transform(test_df['refactoring_type'])
    
    # Models
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    results = {}
    
    print(f"\n🔬 {domain.upper()}")
    print(f"   Train: {len(X_train)} | Test: {len(X_test)} | Classes: {len(le.classes_)}")
    
    for name, model in models.items():
        try:
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            results[name] = accuracy
            
            print(f"   {name}: {accuracy:.1%}")
            
        except Exception as e:
            print(f"   {name}: Error - {e}")
            results[name] = 0.0
    
    return results

def main():
    data_dir = 'data'
    
    # Find train/test pairs
    domains = []
    for file in os.listdir(data_dir):
        if file.endswith('_350_real_train.csv'):
            domain = file.replace('_350_real_train.csv', '')
            train_file = os.path.join(data_dir, file)
            test_file = os.path.join(data_dir, f'{domain}_350_real_test.csv')
            
            if os.path.exists(test_file):
                domains.append((domain, train_file, test_file))
    
    print("🤖 ML BASELINE TRAINING")
    print("=" * 40)
    
    all_results = {}
    
    for domain, train_file, test_file in sorted(domains):
        results = train_and_test_ml(train_file, test_file, domain)
        all_results[domain] = results
    
    # Summary table
    print("\n" + "=" * 40)
    print("📊 SUMMARY")
    print("=" * 40)
    
    # Header
    models = ['RandomForest', 'LogisticRegression', 'SVM']
    print(f"{'Domain':<12} {'RF':<6} {'LR':<6} {'SVM':<6}")
    print("-" * 32)
    
    for domain, results in all_results.items():
        rf = results.get('RandomForest', 0)
        lr = results.get('LogisticRegression', 0) 
        svm = results.get('SVM', 0)
        print(f"{domain:<12} {rf:.1%} {lr:.1%} {svm:.1%}")
    
    print("\n✅ ML baseline complete! Ready for LLM comparison.")

if __name__ == "__main__":
    main()
