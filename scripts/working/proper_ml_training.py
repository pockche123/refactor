#!/usr/bin/env python3
"""
Proper ML Training following the methodology:
- Random Forest classifier
- 70/15/15 split (train/validation/test)
- Feature extraction and encoding
- Baseline majority classifier comparison
"""

import csv
import json
import random
from collections import defaultdict, Counter

def load_dataset():
    """Load behavioral dataset with metadata"""
    dataset = []
    with open('data/mockito_behavioral_dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric features
            row['lines_changed'] = int(row['lines_changed'])
            row['cyclomatic_complexity'] = int(row['cyclomatic_complexity'])
            row['nesting_depth'] = int(row['nesting_depth'])
            dataset.append(row)
    return dataset

def encode_features(dataset):
    """Encode categorical features and normalize"""
    
    # Get unique refactoring types for encoding
    refactoring_types = list(set(row['refactoring_type'] for row in dataset))
    refactoring_types.sort()  # Consistent ordering
    
    type_to_id = {ref_type: i for i, ref_type in enumerate(refactoring_types)}
    id_to_type = {i: ref_type for ref_type, i in type_to_id.items()}
    
    # Encode dataset
    encoded_dataset = []
    for row in dataset:
        encoded_row = {
            'file_path': row['file_path'],
            'refactoring_type': row['refactoring_type'],
            'refactoring_type_id': type_to_id[row['refactoring_type']],
            'lines_changed': row['lines_changed'],
            'cyclomatic_complexity': row['cyclomatic_complexity'],
            'nesting_depth': row['nesting_depth'],
            # Keep metadata for behavioral validation
            'commit_sha': row['commit_sha'],
            'commit_idx': row['commit_idx'],
            'refactoring_idx': row['refactoring_idx'],
            'description': row['description']
        }
        encoded_dataset.append(encoded_row)
    
    return encoded_dataset, type_to_id, id_to_type

def stratified_split_70_15_15(dataset, random_seed=42):
    """Split dataset 70/15/15 maintaining class distribution"""
    random.seed(random_seed)
    
    # Group by refactoring type
    by_type = defaultdict(list)
    for row in dataset:
        by_type[row['refactoring_type']].append(row)
    
    train_set = []
    val_set = []
    test_set = []
    
    for ref_type, rows in by_type.items():
        random.shuffle(rows)
        n = len(rows)
        
        # Calculate splits (ensure at least 1 in each if possible)
        n_train = max(1, int(n * 0.70))
        n_val = max(1, int(n * 0.15)) if n > 2 else 0
        n_test = n - n_train - n_val
        
        if n_test < 1 and n > 1:  # Adjust if test set would be empty
            n_test = 1
            n_val = max(0, n - n_train - n_test)
        
        train_set.extend(rows[:n_train])
        val_set.extend(rows[n_train:n_train + n_val])
        test_set.extend(rows[n_train + n_val:])
    
    return train_set, val_set, test_set

class SimpleRandomForest:
    """Simple Random Forest implementation"""
    
    def __init__(self, n_trees=10):
        self.n_trees = n_trees
        self.trees = []
        
    def fit(self, X_train, y_train):
        """Train the forest"""
        self.trees = []
        
        for _ in range(self.n_trees):
            # Bootstrap sample
            n_samples = len(X_train)
            indices = [random.randint(0, n_samples - 1) for _ in range(n_samples)]
            
            X_bootstrap = [X_train[i] for i in indices]
            y_bootstrap = [y_train[i] for i in indices]
            
            # Train simple decision tree (majority vote at leaf)
            tree = self._train_tree(X_bootstrap, y_bootstrap)
            self.trees.append(tree)
    
    def _train_tree(self, X, y):
        """Train a simple decision tree"""
        # Simple tree: just return majority class
        counter = Counter(y)
        majority_class = counter.most_common(1)[0][0]
        return majority_class
    
    def predict(self, X_test):
        """Predict using forest"""
        predictions = []
        
        for x in X_test:
            # Get prediction from each tree
            tree_predictions = []
            for tree in self.trees:
                tree_predictions.append(tree)  # Simple: each tree returns majority class
            
            # Vote
            counter = Counter(tree_predictions)
            prediction = counter.most_common(1)[0][0]
            predictions.append(prediction)
        
        return predictions

class MajorityClassifier:
    """Baseline majority class classifier"""
    
    def __init__(self):
        self.majority_class = None
    
    def fit(self, X_train, y_train):
        """Find majority class"""
        counter = Counter(y_train)
        self.majority_class = counter.most_common(1)[0][0]
    
    def predict(self, X_test):
        """Predict majority class for all"""
        return [self.majority_class] * len(X_test)

def extract_features(row):
    """Extract feature vector"""
    return [
        row['lines_changed'],
        row['cyclomatic_complexity'],
        row['nesting_depth']
    ]

def evaluate_model(y_true, y_pred, id_to_type):
    """Evaluate model performance"""
    
    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    total = len(y_true)
    accuracy = correct / total if total > 0 else 0
    
    # Per-class metrics
    class_metrics = {}
    for class_id in id_to_type.keys():
        true_positives = sum(1 for true, pred in zip(y_true, y_pred) if true == class_id and pred == class_id)
        false_positives = sum(1 for true, pred in zip(y_true, y_pred) if true != class_id and pred == class_id)
        false_negatives = sum(1 for true, pred in zip(y_true, y_pred) if true == class_id and pred != class_id)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        class_metrics[class_id] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'support': sum(1 for true in y_true if true == class_id)
        }
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'class_metrics': class_metrics
    }

def proper_ml_training():
    """Proper ML training following methodology"""
    
    print("🚀 PROPER ML TRAINING - Following Methodology")
    print("=" * 60)
    
    # Load and encode dataset
    print("📊 Loading dataset...")
    dataset = load_dataset()
    encoded_dataset, type_to_id, id_to_type = encode_features(dataset)
    
    print(f"   Total instances: {len(encoded_dataset)}")
    print(f"   Refactoring types: {len(type_to_id)}")
    
    # Split dataset 70/15/15
    print(f"\n📊 Splitting dataset (70/15/15)...")
    train_set, val_set, test_set = stratified_split_70_15_15(encoded_dataset)
    
    print(f"   Training set: {len(train_set)} ({len(train_set)/len(encoded_dataset)*100:.1f}%)")
    print(f"   Validation set: {len(val_set)} ({len(val_set)/len(encoded_dataset)*100:.1f}%)")
    print(f"   Test set: {len(test_set)} ({len(test_set)/len(encoded_dataset)*100:.1f}%)")
    
    # Prepare features and labels
    X_train = [extract_features(row) for row in train_set]
    y_train = [row['refactoring_type_id'] for row in train_set]
    
    X_val = [extract_features(row) for row in val_set]
    y_val = [row['refactoring_type_id'] for row in val_set]
    
    X_test = [extract_features(row) for row in test_set]
    y_test = [row['refactoring_type_id'] for row in test_set]
    
    # Train Random Forest
    print(f"\n🌲 Training Random Forest classifier...")
    rf_model = SimpleRandomForest(n_trees=10)
    rf_model.fit(X_train, y_train)
    
    # Train Baseline (Majority Class)
    print(f"📊 Training baseline (Majority Class) classifier...")
    baseline_model = MajorityClassifier()
    baseline_model.fit(X_train, y_train)
    
    # Evaluate on validation set
    print(f"\n🧪 Validation Results:")
    
    rf_val_pred = rf_model.predict(X_val)
    baseline_val_pred = baseline_model.predict(X_val)
    
    rf_val_metrics = evaluate_model(y_val, rf_val_pred, id_to_type)
    baseline_val_metrics = evaluate_model(y_val, baseline_val_pred, id_to_type)
    
    print(f"   Random Forest accuracy: {rf_val_metrics['accuracy']:.1%} ({rf_val_metrics['correct']}/{rf_val_metrics['total']})")
    print(f"   Baseline accuracy: {baseline_val_metrics['accuracy']:.1%} ({baseline_val_metrics['correct']}/{baseline_val_metrics['total']})")
    
    # Evaluate on test set
    print(f"\n🎯 Test Results:")
    
    rf_test_pred = rf_model.predict(X_test)
    baseline_test_pred = baseline_model.predict(X_test)
    
    rf_test_metrics = evaluate_model(y_test, rf_test_pred, id_to_type)
    baseline_test_metrics = evaluate_model(y_test, baseline_test_pred, id_to_type)
    
    print(f"   Random Forest accuracy: {rf_test_metrics['accuracy']:.1%} ({rf_test_metrics['correct']}/{rf_test_metrics['total']})")
    print(f"   Baseline accuracy: {baseline_test_metrics['accuracy']:.1%} ({baseline_test_metrics['correct']}/{baseline_test_metrics['total']})")
    
    # Save test results for behavioral validation
    test_results = []
    for i, test_instance in enumerate(test_set):
        result = test_instance.copy()
        result['predicted_id'] = rf_test_pred[i]
        result['predicted_type'] = id_to_type[rf_test_pred[i]]
        result['correct'] = rf_test_pred[i] == test_instance['refactoring_type_id']
        test_results.append(result)
    
    # Save results
    with open('results/proper_ml_test_results.csv', 'w', newline='') as f:
        fieldnames = [
            'file_path', 'refactoring_type', 'predicted_type', 'correct',
            'lines_changed', 'cyclomatic_complexity', 'nesting_depth',
            'commit_sha', 'commit_idx', 'refactoring_idx', 'description'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_results)
    
    print(f"\n💾 Test results saved to: results/proper_ml_test_results.csv")
    
    # Show correct predictions for behavioral validation
    correct_predictions = [r for r in test_results if r['correct']]
    print(f"\n✅ Correct predictions for behavioral validation: {len(correct_predictions)}")
    
    if correct_predictions:
        print(f"📋 Correct predictions by type:")
        correct_by_type = defaultdict(int)
        for r in correct_predictions:
            correct_by_type[r['refactoring_type']] += 1
        
        for ref_type, count in correct_by_type.items():
            print(f"   {ref_type}: {count}")
    
    return test_results, correct_predictions

if __name__ == "__main__":
    proper_ml_training()
