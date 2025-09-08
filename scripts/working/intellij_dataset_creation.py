#!/usr/bin/env python3
"""
Create IntelliJ Single-Domain Dataset
"""

import json
import csv
from collections import defaultdict

def load_intellij_refactorings():
    """Load IntelliJ RefactoringMiner JSON"""
    with open('data/intellij_refactorings.json', 'r') as f:
        return json.load(f)

def create_intellij_dataset():
    """Create IntelliJ behavioral-ready dataset"""
    
    print("🚀 CREATING INTELLIJ SINGLE-DOMAIN DATASET")
    print("=" * 50)
    
    # Load refactoring data
    print("📊 Loading IntelliJ refactorings...")
    data = load_intellij_refactorings()
    
    # Extract features for each refactoring
    dataset = []
    
    for commit_idx, commit in enumerate(data['commits']):
        for ref_idx, refactoring in enumerate(commit['refactorings']):
            # Get file path
            file_path = None
            if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                file_path = refactoring['leftSideLocations'][0]['filePath']
            elif 'rightSideLocations' in refactoring and refactoring['rightSideLocations']:
                file_path = refactoring['rightSideLocations'][0]['filePath']
            
            if file_path:
                # Basic features
                lines_changed = 1
                if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                    location = refactoring['leftSideLocations'][0]
                    start_line = location.get('startLine', 1)
                    end_line = location.get('endLine', 1)
                    lines_changed = max(1, end_line - start_line + 1)
                
                # BEHAVIORAL VALIDATION METADATA
                row = {
                    'file_path': file_path,
                    'refactoring_type': refactoring['type'],
                    'lines_changed': lines_changed,
                    'cyclomatic_complexity': 1,
                    'nesting_depth': 1,
                    # KEY: Metadata for behavioral validation
                    'commit_sha': commit['sha1'],
                    'commit_idx': commit_idx,
                    'refactoring_idx': ref_idx,
                    'description': refactoring['description'],
                    'has_left_locations': len(refactoring.get('leftSideLocations', [])) > 0,
                    'has_right_locations': len(refactoring.get('rightSideLocations', [])) > 0
                }
                dataset.append(row)
    
    # Statistics
    type_counts = {}
    for row in dataset:
        ref_type = row['refactoring_type']
        type_counts[ref_type] = type_counts.get(ref_type, 0) + 1
    
    print(f"📊 IntelliJ dataset created:")
    print(f"   Total refactorings: {len(dataset)}")
    print(f"   Refactoring types: {len(type_counts)}")
    print(f"   Files: {len(set(row['file_path'] for row in dataset))}")
    
    print(f"\n📋 Top refactoring types:")
    for ref_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {ref_type}: {count}")
    
    # Check behavioral validation readiness
    testable = sum(1 for row in dataset if row['has_left_locations'] and row['has_right_locations'])
    print(f"\n🧪 Behavioral validation readiness:")
    print(f"   Potentially testable: {testable}/{len(dataset)} ({testable/len(dataset)*100:.1f}%)")
    
    # Save dataset
    fieldnames = [
        'file_path', 'refactoring_type', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth',
        'commit_sha', 'commit_idx', 'refactoring_idx', 'description', 
        'has_left_locations', 'has_right_locations'
    ]
    
    with open('data/intellij_behavioral_dataset.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
    
    print(f"\n💾 Dataset saved to: data/intellij_behavioral_dataset.csv")
    
    # Also save a simple version for ML
    simple_dataset = []
    for row in dataset:
        simple_row = {
            'file_path': row['file_path'],
            'refactoring_type': row['refactoring_type'],
            'lines_changed': row['lines_changed'],
            'cyclomatic_complexity': row['cyclomatic_complexity'],
            'nesting_depth': row['nesting_depth']
        }
        simple_dataset.append(simple_row)
    
    with open('data/intellij_simple_dataset.csv', 'w', newline='') as f:
        simple_fieldnames = ['file_path', 'refactoring_type', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
        writer = csv.DictWriter(f, fieldnames=simple_fieldnames)
        writer.writeheader()
        writer.writerows(simple_dataset)
    
    print(f"💾 Simple ML dataset saved to: data/intellij_simple_dataset.csv")
    
    return dataset

if __name__ == "__main__":
    create_intellij_dataset()
