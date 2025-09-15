import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import os

def train_and_test_ml(train_file, test_file, domain):
    """Train and test ML models on a domain"""
    
    # Load data
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    
    # Features (same as original research)
    feature_cols = ['lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    
    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]
    
    # Encode target labels
    le = LabelEncoder()
    y_train = le.fit_transform(train_df['refactoring_type'])
    y_test = le.transform(test_df['refactoring_type'])
    
    # Models to test
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(random_state=42)
    }
    
    results = {}
    
    print(f"\n🔬 Training ML models for {domain}")
    print(f"   Train: {len(X_train)} samples, Test: {len(X_test)} samples")
    print(f"   Features: {feature_cols}")
    print(f"   Classes: {len(le.classes_)} refactoring types")
    
    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = accuracy
        
        print(f"   {name}: {accuracy:.3f} accuracy")
    
    return results, le.classes_

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
    
    print("🤖 ML Model Training & Testing")
    print("=" * 50)
    
    all_results = {}
    
    for domain, train_file, test_file in sorted(domains):
        try:
            results, classes = train_and_test_ml(train_file, test_file, domain)
            all_results[domain] = results
            
        except Exception as e:
            print(f"❌ {domain}: Error - {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ML RESULTS SUMMARY")
    print("=" * 50)
    
    for domain, results in all_results.items():
        print(f"\n{domain.upper()}:")
        for model, accuracy in results.items():
            print(f"  {model}: {accuracy:.1%}")
    
    print("\n✅ ML baseline established! Ready for LLM comparison.")

if __name__ == "__main__":
    main()
