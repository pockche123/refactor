#!/usr/bin/env python3
"""
Commons Lang ML Training with 70-30 split
Following same methodology as Mockito/IntelliJ
"""

import csv
import json
import random
from collections import defaultdict, Counter

# Simple implementations (same as your existing scripts)
class LabelEncoder:
    def __init__(self):
        self.classes_ = []
        self.class_to_id = {}
        
    def fit(self, y):
        unique_classes = sorted(list(set(y)))
        self.classes_ = unique_classes
        self.class_to_id = {cls: i for i, cls in enumerate(unique_classes)}
        return self
    
    def transform(self, y):
        return [self.class_to_id[cls] for cls in y]
    
    def fit_transform(self, y):
        return self.fit(y).transform(y)
    
    def inverse_transform(self, y_encoded):
        return [self.classes_[i] for i in y_encoded]

class RandomForestClassifier:
    def __init__(self, n_estimators=100, random_state=42):
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.trees = []
        
    def fit(self, X, y):
        random.seed(self.random_state)
        self.trees = []
        
        for _ in range(self.n_estimators):
            # Bootstrap sampling
            n_samples = len(X)
            indices = [random.randint(0, n_samples - 1) for _ in range(n_samples)]
            
            X_bootstrap = [X[i] for i in indices]
            y_bootstrap = [y[i] for i in indices]
            
            # Simple decision tree (majority class)
            tree = Counter(y_bootstrap).most_common(1)[0][0]
            self.trees.append(tree)
        
        return self
    
    def predict(self, X):
        predictions = []
        for _ in X:
            # Vote from all trees
            votes = Counter(self.trees)
            prediction = votes.most_common(1)[0][0]
            predictions.append(prediction)
        return predictions

def load_commons_lang_dataset():
    """Load Commons Lang behavioral dataset"""
    dataset = []
    with open('data/commons_lang_behavioral_dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append({
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'lines_changed': int(row['lines_changed']),
                'cyclomatic_complexity': int(row['cyclomatic_complexity']),
                'nesting_depth': int(row['nesting_depth']),
                'commit_sha': row['commit_sha'],
                'commit_idx': int(row['commit_idx']),
                'refactoring_idx': int(row['refactoring_idx']),
                'description': row['description']
            })
    return dataset

def stratified_split_70_30(dataset, random_seed=42):
    """Split dataset 70-30 maintaining class distribution"""
    random.seed(random_seed)
    
    # Group by refactoring type
    type_groups = defaultdict(list)
    for item in dataset:
        type_groups[item['refactoring_type']].append(item)
    
    train_set = []
    test_set = []
    
    for refactoring_type, rows in type_groups.items():
        random.shuffle(rows)
        n = len(rows)
        
        n_train = max(1, int(n * 0.70))
        n_test = n - n_train
        
        train_set.extend(rows[:n_train])
        test_set.extend(rows[n_train:])
    
    return train_set, test_set

def calculate_metrics(y_true, y_pred, label_encoder):
    """Calculate comprehensive metrics"""
    
    # Convert back to class names
    y_true_names = label_encoder.inverse_transform(y_true)
    y_pred_names = label_encoder.inverse_transform(y_pred)
    
    # Overall accuracy
    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    accuracy = correct / len(y_true)
    
    # Per-class metrics
    classes = label_encoder.classes_
    class_metrics = {}
    
    for cls in classes:
        # True positives, false positives, false negatives
        tp = sum(1 for true, pred in zip(y_true_names, y_pred_names) if true == cls and pred == cls)
        fp = sum(1 for true, pred in zip(y_true_names, y_pred_names) if true != cls and pred == cls)
        fn = sum(1 for true, pred in zip(y_true_names, y_pred_names) if true == cls and pred != cls)
        
        # Precision, Recall, F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        # Support
        support = sum(1 for true in y_true_names if true == cls)
        
        class_metrics[cls] = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'support': support
        }
    
    return accuracy, class_metrics

def main():
    print("🚀 COMMONS LANG ML TRAINING")
    print("=" * 50)
    
    # Load dataset
    print("📊 Loading Commons Lang dataset...")
    dataset = load_commons_lang_dataset()
    
    print(f"   Total refactorings: {len(dataset)}")
    
    # Count refactoring types
    type_counts = Counter(item['refactoring_type'] for item in dataset)
    print(f"   Refactoring types: {len(type_counts)}")
    
    print(f"\n📋 Top 5 refactoring types:")
    for i, (ref_type, count) in enumerate(type_counts.most_common(5)):
        percentage = (count / len(dataset)) * 100
        print(f"   {i+1}. {ref_type:<30} {count:3d} ({percentage:5.1f}%)")
    
    # Split dataset (70-30)
    print(f"\n📊 Splitting dataset (70-30)...")
    train_set, test_set = stratified_split_70_30(dataset)
    
    print(f"   Training set: {len(train_set)} ({len(train_set)/len(dataset)*100:.1f}%)")
    print(f"   Test set: {len(test_set)} ({len(test_set)/len(dataset)*100:.1f}%)")
    
    # Prepare features and labels
    print(f"\n🔧 Preparing features...")
    
    # Training data
    X_train = []
    y_train = []
    for item in train_set:
        features = [item['lines_changed'], item['cyclomatic_complexity'], item['nesting_depth']]
        X_train.append(features)
        y_train.append(item['refactoring_type'])
    
    # Test data
    X_test = []
    y_test = []
    test_items = []
    for item in test_set:
        features = [item['lines_changed'], item['cyclomatic_complexity'], item['nesting_depth']]
        X_test.append(features)
        y_test.append(item['refactoring_type'])
        test_items.append(item)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    
    print(f"   Features: lines_changed, cyclomatic_complexity, nesting_depth")
    print(f"   Classes: {len(label_encoder.classes_)}")
    
    # Train model
    print(f"\n🤖 Training Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train_encoded)
    
    # Make predictions
    print(f"\n🎯 Making predictions...")
    y_pred_encoded = model.predict(X_test)
    
    # Calculate metrics
    accuracy, class_metrics = calculate_metrics(y_test_encoded, y_pred_encoded, label_encoder)
    
    print(f"\n📈 RESULTS:")
    print(f"   Overall Accuracy: {accuracy:.1%} ({sum(1 for true, pred in zip(y_test_encoded, y_pred_encoded) if true == pred)}/{len(y_test)})")
    
    # Save detailed results
    print(f"\n💾 Saving results...")
    
    # Save test results with predictions
    results = []
    y_pred_names = label_encoder.inverse_transform(y_pred_encoded)
    
    for i, item in enumerate(test_items):
        result = {
            'file_path': item['file_path'],
            'refactoring_type': item['refactoring_type'],
            'predicted_type': y_pred_names[i],
            'correct': item['refactoring_type'] == y_pred_names[i],
            'lines_changed': item['lines_changed'],
            'cyclomatic_complexity': item['cyclomatic_complexity'],
            'nesting_depth': item['nesting_depth'],
            'commit_sha': item['commit_sha'],
            'commit_idx': item['commit_idx'],
            'refactoring_idx': item['refactoring_idx'],
            'description': item['description']
        }
        results.append(result)
    
    # Save results
    with open('results/working/commons_lang_ml_test_results.csv', 'w', newline='') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"   ✅ results/working/commons_lang_ml_test_results.csv")
    
    # Show per-class performance for top classes
    print(f"\n📊 Per-Class Performance (Top 5):")
    sorted_classes = sorted(class_metrics.items(), key=lambda x: x[1]['support'], reverse=True)
    
    for cls, metrics in sorted_classes[:5]:
        print(f"   {cls:<30} P:{metrics['precision']:.2f} R:{metrics['recall']:.2f} F1:{metrics['f1_score']:.2f} S:{metrics['support']}")
    
    # Count correct predictions
    correct_predictions = [r for r in results if r['correct']]
    print(f"\n🎯 Correct Predictions: {len(correct_predictions)}")
    
    if correct_predictions:
        print(f"   Ready for behavioral validation!")
        
        # Show correct prediction types
        correct_types = Counter(r['refactoring_type'] for r in correct_predictions)
        print(f"\n📋 Correct Predictions by Type:")
        for ref_type, count in correct_types.most_common():
            print(f"   {ref_type:<30} {count}")
    
    print(f"\n✅ Commons Lang ML training complete!")
    print(f"   Next: Behavioral validation of {len(correct_predictions)} correct predictions")

if __name__ == "__main__":
    main()
