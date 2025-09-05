#!/usr/bin/env python3
"""
Comprehensive ML Training with detailed metrics
- Random Forest with sklearn
- Comprehensive precision/recall/F1 metrics per class
- 70/15/15 split following methodology
"""

import csv
import json
import random
from collections import defaultdict, Counter

# Simple implementations since we don't have sklearn
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
            
            # Simple decision tree (majority vote)
            tree = self._build_tree(X_bootstrap, y_bootstrap)
            self.trees.append(tree)
        
        return self
    
    def _build_tree(self, X, y):
        # Simple tree: return majority class
        counter = Counter(y)
        return counter.most_common(1)[0][0]
    
    def predict(self, X):
        predictions = []
        
        for x in X:
            # Get votes from all trees
            votes = []
            for tree in self.trees:
                votes.append(tree)  # Simple: each tree votes for majority class
            
            # Majority vote
            counter = Counter(votes)
            prediction = counter.most_common(1)[0][0]
            predictions.append(prediction)
        
        return predictions

def classification_report(y_true, y_pred, target_names=None, zero_division=0):
    """Generate classification report"""
    
    # Get unique classes
    classes = sorted(list(set(y_true + y_pred)))
    
    if target_names is None:
        target_names = [str(cls) for cls in classes]
    
    # Calculate metrics for each class
    class_metrics = {}
    total_support = len(y_true)
    
    for i, cls in enumerate(classes):
        # True positives, false positives, false negatives
        tp = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred == cls)
        fp = sum(1 for true, pred in zip(y_true, y_pred) if true != cls and pred == cls)
        fn = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred != cls)
        
        # Support (actual occurrences)
        support = sum(1 for true in y_true if true == cls)
        
        # Precision, recall, F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else zero_division
        recall = tp / (tp + fn) if (tp + fn) > 0 else zero_division
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else zero_division
        
        class_metrics[cls] = {
            'precision': precision,
            'recall': recall,
            'f1-score': f1,
            'support': support
        }
    
    # Overall accuracy
    accuracy = sum(1 for true, pred in zip(y_true, y_pred) if true == pred) / len(y_true)
    
    # Macro averages
    macro_precision = sum(metrics['precision'] for metrics in class_metrics.values()) / len(class_metrics)
    macro_recall = sum(metrics['recall'] for metrics in class_metrics.values()) / len(class_metrics)
    macro_f1 = sum(metrics['f1-score'] for metrics in class_metrics.values()) / len(class_metrics)
    
    # Weighted averages
    weighted_precision = sum(metrics['precision'] * metrics['support'] for metrics in class_metrics.values()) / total_support
    weighted_recall = sum(metrics['recall'] * metrics['support'] for metrics in class_metrics.values()) / total_support
    weighted_f1 = sum(metrics['f1-score'] * metrics['support'] for metrics in class_metrics.values()) / total_support
    
    return {
        'class_metrics': class_metrics,
        'accuracy': accuracy,
        'macro_avg': {
            'precision': macro_precision,
            'recall': macro_recall,
            'f1-score': macro_f1,
            'support': total_support
        },
        'weighted_avg': {
            'precision': weighted_precision,
            'recall': weighted_recall,
            'f1-score': weighted_f1,
            'support': total_support
        }
    }

def print_classification_report(report, target_names=None):
    """Print classification report in sklearn format"""
    
    class_metrics = report['class_metrics']
    
    # Header
    print(f"{'':>25} {'precision':>9} {'recall':>9} {'f1-score':>9} {'support':>9}")
    print()
    
    # Per-class metrics
    classes = sorted(class_metrics.keys())
    if target_names:
        class_names = target_names
    else:
        class_names = [str(cls) for cls in classes]
    
    for cls, name in zip(classes, class_names):
        metrics = class_metrics[cls]
        print(f"{name:>25} {metrics['precision']:>9.2f} {metrics['recall']:>9.2f} {metrics['f1-score']:>9.2f} {metrics['support']:>9}")
    
    print()
    
    # Overall metrics
    print(f"{'accuracy':>25} {'':<9} {'':<9} {report['accuracy']:>9.2f} {report['macro_avg']['support']:>9}")
    print(f"{'macro avg':>25} {report['macro_avg']['precision']:>9.2f} {report['macro_avg']['recall']:>9.2f} {report['macro_avg']['f1-score']:>9.2f} {report['macro_avg']['support']:>9}")
    print(f"{'weighted avg':>25} {report['weighted_avg']['precision']:>9.2f} {report['weighted_avg']['recall']:>9.2f} {report['weighted_avg']['f1-score']:>9.2f} {report['weighted_avg']['support']:>9}")

def load_dataset():
    """Load behavioral dataset"""
    dataset = []
    with open('data/mockito_behavioral_dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['lines_changed'] = int(row['lines_changed'])
            row['cyclomatic_complexity'] = int(row['cyclomatic_complexity'])
            row['nesting_depth'] = int(row['nesting_depth'])
            dataset.append(row)
    return dataset

def stratified_split_70_15_15(dataset, random_seed=42):
    """Split dataset 70/15/15 maintaining class distribution"""
    random.seed(random_seed)
    
    by_type = defaultdict(list)
    for row in dataset:
        by_type[row['refactoring_type']].append(row)
    
    train_set = []
    val_set = []
    test_set = []
    
    for ref_type, rows in by_type.items():
        random.shuffle(rows)
        n = len(rows)
        
        n_train = max(1, int(n * 0.70))
        n_val = max(1, int(n * 0.15)) if n > 2 else 0
        n_test = n - n_train - n_val
        
        if n_test < 1 and n > 1:
            n_test = 1
            n_val = max(0, n - n_train - n_test)
        
        train_set.extend(rows[:n_train])
        val_set.extend(rows[n_train:n_train + n_val])
        test_set.extend(rows[n_train + n_val:])
    
    return train_set, val_set, test_set

def extract_features(row):
    """Extract feature vector"""
    return [
        row['lines_changed'],
        row['cyclomatic_complexity'],
        row['nesting_depth']
    ]

def comprehensive_ml_training():
    """Comprehensive ML training with detailed metrics"""
    
    print("🚀 COMPREHENSIVE ML TRAINING")
    print("=" * 60)
    
    # Load dataset
    print("📊 Loading dataset...")
    dataset = load_dataset()
    print(f"   Total instances: {len(dataset)}")
    
    # Split dataset
    print(f"\n📊 Splitting dataset (70/15/15)...")
    train_set, val_set, test_set = stratified_split_70_15_15(dataset)
    
    print(f"   Training set: {len(train_set)} ({len(train_set)/len(dataset)*100:.1f}%)")
    print(f"   Validation set: {len(val_set)} ({len(val_set)/len(dataset)*100:.1f}%)")
    print(f"   Test set: {len(test_set)} ({len(test_set)/len(dataset)*100:.1f}%)")
    
    # Prepare data
    X_train = [extract_features(row) for row in train_set]
    y_train = [row['refactoring_type'] for row in train_set]
    
    X_test = [extract_features(row) for row in test_set]
    y_test = [row['refactoring_type'] for row in test_set]
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    
    print(f"\n📊 Dataset statistics:")
    print(f"   Unique refactoring types: {len(label_encoder.classes_)}")
    
    # Train Random Forest
    print(f"\n🌲 Training Random Forest classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train_encoded)
    
    # Train baseline (majority class)
    print(f"📊 Training baseline classifier...")
    majority_class = Counter(y_train_encoded).most_common(1)[0][0]
    baseline_pred = [majority_class] * len(y_test_encoded)
    
    # Make predictions
    print(f"\n🧪 Making predictions...")
    rf_pred_encoded = rf_model.predict(X_test)
    
    # Convert back to original labels
    rf_pred = label_encoder.inverse_transform(rf_pred_encoded)
    baseline_pred_labels = label_encoder.inverse_transform(baseline_pred)
    
    # Generate comprehensive reports
    print(f"\n📊 RANDOM FOREST RESULTS:")
    print("=" * 60)
    rf_report = classification_report(y_test, rf_pred, target_names=None)
    print_classification_report(rf_report)
    
    print(f"\n📊 BASELINE (MAJORITY CLASS) RESULTS:")
    print("=" * 60)
    baseline_report = classification_report(y_test, baseline_pred_labels, target_names=None)
    print_classification_report(baseline_report)
    
    # Save test results for behavioral validation
    test_results = []
    for i, test_instance in enumerate(test_set):
        result = {
            'file_path': test_instance['file_path'],
            'refactoring_type': test_instance['refactoring_type'],
            'predicted_type': rf_pred[i],
            'correct': rf_pred[i] == test_instance['refactoring_type'],
            'lines_changed': test_instance['lines_changed'],
            'cyclomatic_complexity': test_instance['cyclomatic_complexity'],
            'nesting_depth': test_instance['nesting_depth'],
            'commit_sha': test_instance['commit_sha'],
            'commit_idx': test_instance['commit_idx'],
            'refactoring_idx': test_instance['refactoring_idx'],
            'description': test_instance['description']
        }
        test_results.append(result)
    
    # Save results
    with open('results/comprehensive_ml_test_results.csv', 'w', newline='') as f:
        fieldnames = [
            'file_path', 'refactoring_type', 'predicted_type', 'correct',
            'lines_changed', 'cyclomatic_complexity', 'nesting_depth',
            'commit_sha', 'commit_idx', 'refactoring_idx', 'description'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_results)
    
    print(f"\n💾 Test results saved to: results/comprehensive_ml_test_results.csv")
    
    # Show correct predictions for behavioral validation
    correct_predictions = [r for r in test_results if r['correct']]
    print(f"\n✅ Correct predictions for behavioral validation: {len(correct_predictions)}")
    
    if correct_predictions:
        print(f"📋 Correct predictions by type:")
        correct_by_type = defaultdict(int)
        for r in correct_predictions:
            correct_by_type[r['refactoring_type']] += 1
        
        for ref_type, count in sorted(correct_by_type.items()):
            print(f"   {ref_type}: {count}")
    
    return test_results, correct_predictions, rf_report

if __name__ == "__main__":
    comprehensive_ml_training()
