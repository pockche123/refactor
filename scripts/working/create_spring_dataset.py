#!/usr/bin/env python3
"""
Create Spring Framework dataset from RefactoringMiner JSON
Following same methodology as Commons Lang/Mockito/IntelliJ
"""

import json
import csv
from collections import defaultdict

def load_spring_refactorings():
    """Load Spring Framework RefactoringMiner JSON"""
    with open('data/spring_refactorings.json', 'r') as f:
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
    
    # Basic features (same as other projects methodology)
    features = {
        'file_path': file_path,
        'refactoring_type': refactoring['type'],
        'lines_changed': lines_changed,
        'cyclomatic_complexity': 1,  # Default (same as other projects)
        'nesting_depth': 1,  # Default (same as other projects)
        'commit_sha': commit_sha,
        'commit_idx': commit_idx,
        'refactoring_idx': ref_idx,
        'description': refactoring['description'],
        'has_left_locations': 'leftSideLocations' in refactoring and len(refactoring['leftSideLocations']) > 0,
        'has_right_locations': 'rightSideLocations' in refactoring and len(refactoring['rightSideLocations']) > 0
    }
    
    return features

def main():
    print("🚀 SPRING FRAMEWORK DATASET CREATION")
    print("=" * 50)
    
    # Load refactorings
    print("📊 Loading Spring Framework refactorings...")
    data = load_spring_refactorings()
    
    # Extract features from all refactorings
    all_features = []
    refactoring_types = defaultdict(int)
    
    for commit_idx, commit in enumerate(data['commits']):
        commit_sha = commit['sha1']
        
        for ref_idx, refactoring in enumerate(commit['refactorings']):
            features = extract_features(refactoring, commit_idx, ref_idx, commit_sha)
            if features:
                all_features.append(features)
                refactoring_types[features['refactoring_type']] += 1
    
    print(f"   Extracted {len(all_features)} refactoring features")
    
    # Create behavioral dataset (same format as other projects)
    print("📝 Creating behavioral dataset...")
    
    behavioral_data = []
    for features in all_features:
        behavioral_data.append({
            'file_path': features['file_path'],
            'refactoring_type': features['refactoring_type'],
            'lines_changed': features['lines_changed'],
            'cyclomatic_complexity': features['cyclomatic_complexity'],
            'nesting_depth': features['nesting_depth'],
            'commit_sha': features['commit_sha'],
            'description': features['description']
        })
    
    # Save behavioral dataset
    behavioral_file = 'data/spring_behavioral_dataset.csv'
    with open(behavioral_file, 'w', newline='') as f:
        if behavioral_data:
            writer = csv.DictWriter(f, fieldnames=behavioral_data[0].keys())
            writer.writeheader()
            writer.writerows(behavioral_data)
    
    print(f"   ✅ {behavioral_file}")
    
    # Create simple dataset (same format as other projects)
    print("📝 Creating simple dataset...")
    
    simple_data = []
    for features in all_features:
        simple_data.append({
            'file_path': features['file_path'],
            'refactoring_type': features['refactoring_type'],
            'lines_changed': features['lines_changed'],
            'cyclomatic_complexity': features['cyclomatic_complexity'],
            'nesting_depth': features['nesting_depth']
        })
    
    # Save simple dataset
    simple_file = 'data/spring_simple_dataset.csv'
    with open(simple_file, 'w', newline='') as f:
        if simple_data:
            writer = csv.DictWriter(f, fieldnames=simple_data[0].keys())
            writer.writeheader()
            writer.writerows(simple_data)
    
    print(f"   ✅ {simple_file}")
    
    # Summary statistics
    print(f"\n📈 DATASET SUMMARY:")
    print(f"   Total refactorings: {len(all_features)}")
    print(f"   Unique types: {len(refactoring_types)}")
    print(f"   Top 5 types:")
    
    sorted_types = sorted(refactoring_types.items(), key=lambda x: x[1], reverse=True)
    for ref_type, count in sorted_types[:5]:
        percentage = (count / len(all_features)) * 100
        print(f"     {ref_type}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
