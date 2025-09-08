#!/usr/bin/env python3
"""
Create Commons Lang dataset from RefactoringMiner JSON
Following same methodology as Mockito/IntelliJ
"""

import json
import csv
from collections import defaultdict

def load_commons_lang_refactorings():
    """Load Commons Lang RefactoringMiner JSON"""
    with open('data/commons_lang_refactorings.json', 'r') as f:
        return json.load(f)

def extract_features(refactoring, commit_idx, ref_idx, commit_sha):
    """Extract features from refactoring following existing methodology"""
    
    # Get file path from locations
    file_path = None
    if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
        file_path = refactoring['leftSideLocations'][0]['filePath']
    elif 'rightSideLocations' in refactoring and refactoring['rightSideLocations']:
        file_path = refactoring['rightSideLocations'][0]['filePath']
    
    if not file_path:
        return None
    
    # Calculate lines changed
    lines_changed = 1  # Default
    if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
        location = refactoring['leftSideLocations'][0]
        start_line = location.get('startLine', 1)
        end_line = location.get('endLine', 1)
        lines_changed = max(1, end_line - start_line + 1)
    
    # Basic features (same as Mockito/IntelliJ methodology)
    features = {
        'file_path': file_path,
        'refactoring_type': refactoring['type'],
        'lines_changed': lines_changed,
        'cyclomatic_complexity': 1,  # Default (same as Mockito)
        'nesting_depth': 1,  # Default (same as Mockito)
        'commit_sha': commit_sha,
        'commit_idx': commit_idx,
        'refactoring_idx': ref_idx,
        'description': refactoring['description'],
        'has_left_locations': 'leftSideLocations' in refactoring and len(refactoring['leftSideLocations']) > 0,
        'has_right_locations': 'rightSideLocations' in refactoring and len(refactoring['rightSideLocations']) > 0
    }
    
    return features

def create_commons_lang_dataset():
    """Create Commons Lang behavioral-ready dataset"""
    
    print("🚀 CREATING COMMONS LANG DATASET")
    print("=" * 50)
    
    # Load refactoring data
    print("📊 Loading Commons Lang refactorings...")
    data = load_commons_lang_refactorings()
    
    # Extract features for each refactoring
    dataset = []
    refactoring_types = defaultdict(int)
    
    for commit_idx, commit in enumerate(data['commits']):
        for ref_idx, refactoring in enumerate(commit['refactorings']):
            features = extract_features(refactoring, commit_idx, ref_idx, commit['sha1'])
            if features:
                dataset.append(features)
                refactoring_types[refactoring['type']] += 1
    
    print(f"📈 Dataset Statistics:")
    print(f"   Total refactorings: {len(dataset)}")
    print(f"   Unique refactoring types: {len(refactoring_types)}")
    print(f"   Commits analyzed: {len(data['commits'])}")
    
    print(f"\n📋 Top 10 Refactoring Types:")
    sorted_types = sorted(refactoring_types.items(), key=lambda x: x[1], reverse=True)
    for i, (ref_type, count) in enumerate(sorted_types[:10]):
        percentage = (count / len(dataset)) * 100
        print(f"   {i+1:2d}. {ref_type:<30} {count:3d} ({percentage:5.1f}%)")
    
    # Save behavioral dataset
    print(f"\n💾 Saving datasets...")
    
    # Behavioral dataset (same format as Mockito/IntelliJ)
    with open('data/commons_lang_behavioral_dataset.csv', 'w', newline='') as f:
        if dataset:
            writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
            writer.writeheader()
            writer.writerows(dataset)
    
    # Simple dataset (same format as Mockito/IntelliJ)
    simple_dataset = []
    for item in dataset:
        simple_item = {
            'file_path': item['file_path'],
            'refactoring_type': item['refactoring_type'],
            'lines_changed': item['lines_changed'],
            'cyclomatic_complexity': item['cyclomatic_complexity'],
            'nesting_depth': item['nesting_depth']
        }
        simple_dataset.append(simple_item)
    
    with open('data/commons_lang_simple_dataset.csv', 'w', newline='') as f:
        if simple_dataset:
            writer = csv.DictWriter(f, fieldnames=simple_dataset[0].keys())
            writer.writeheader()
            writer.writerows(simple_dataset)
    
    print(f"   ✅ commons_lang_behavioral_dataset.csv ({len(dataset)} refactorings)")
    print(f"   ✅ commons_lang_simple_dataset.csv ({len(simple_dataset)} refactorings)")
    
    print(f"\n🎯 Ready for ML training with 70-30 split!")
    
    return dataset

if __name__ == "__main__":
    create_commons_lang_dataset()
