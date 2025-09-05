#!/usr/bin/env python3
"""
Train and test on Mockito dataset (70/30 split)
"""

import csv
import random
from collections import defaultdict

def load_dataset():
    """Load the simple dataset"""
    dataset = []
    with open('data/mockito_simple_dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['lines_changed'] = int(row['lines_changed'])
            row['cyclomatic_complexity'] = int(row['cyclomatic_complexity'])
            row['nesting_depth'] = int(row['nesting_depth'])
            dataset.append(row)
    return dataset

def stratified_split(dataset, test_size=0.3, random_seed=42):
    """Split dataset maintaining class distribution"""
    random.seed(random_seed)
    
    # Group by refactoring type
    by_type = defaultdict(list)
    for row in dataset:
        by_type[row['refactoring_type']].append(row)
    
    train_set = []
    test_set = []
    
    for ref_type, rows in by_type.items():
        random.shuffle(rows)
        n_test = max(1, int(len(rows) * test_size))  # At least 1 for test
        n_train = len(rows) - n_test
        
        train_set.extend(rows[:n_train])
        test_set.extend(rows[n_train:])
    
    return train_set, test_set

def simple_classifier_predict(train_set, test_instance):
    """Simple majority class classifier"""
    # Count refactoring types in training set
    type_counts = defaultdict(int)
    for row in train_set:
        type_counts[row['refactoring_type']] += 1
    
    # Return most common type
    return max(type_counts.items(), key=lambda x: x[1])[0]

def evaluate_predictions(test_set, predictions):
    """Evaluate predictions"""
    correct = 0
    total = len(test_set)
    
    for i, test_instance in enumerate(test_set):
        if predictions[i] == test_instance['refactoring_type']:
            correct += 1
    
    accuracy = correct / total
    return accuracy, correct, total

def train_and_test():
    """Train and test on Mockito dataset"""
    
    print("🚀 Training and Testing on Mockito Dataset")
    print("=" * 50)
    
    # Load dataset
    dataset = load_dataset()
    print(f"📊 Dataset loaded: {len(dataset)} refactorings")
    
    # Split 70/30
    train_set, test_set = stratified_split(dataset, test_size=0.3)
    
    print(f"📊 Split completed:")
    print(f"   Training set: {len(train_set)} ({len(train_set)/len(dataset)*100:.1f}%)")
    print(f"   Test set: {len(test_set)} ({len(test_set)/len(dataset)*100:.1f}%)")
    
    # Train (simple majority classifier)
    print(f"\n🧠 Training simple classifier...")
    
    # Test
    print(f"🧪 Testing on {len(test_set)} instances...")
    predictions = []
    for test_instance in test_set:
        prediction = simple_classifier_predict(train_set, test_instance)
        predictions.append(prediction)
    
    # Evaluate
    accuracy, correct, total = evaluate_predictions(test_set, predictions)
    
    print(f"\n📊 Results:")
    print(f"   Accuracy: {accuracy:.1%} ({correct}/{total})")
    
    # Save test results with predictions
    test_results = []
    for i, test_instance in enumerate(test_set):
        result = test_instance.copy()
        result['predicted'] = predictions[i]
        result['correct'] = predictions[i] == test_instance['refactoring_type']
        test_results.append(result)
    
    # Save results
    with open('results/mockito_test_results.csv', 'w', newline='') as f:
        fieldnames = ['file_path', 'refactoring_type', 'predicted', 'correct', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_results)
    
    print(f"💾 Test results saved to: results/mockito_test_results.csv")
    
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
    train_and_test()
