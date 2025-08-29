#!/usr/bin/env python3
"""
Extract features from IntelliJ refactorings for model testing
"""

import json
import pandas as pd
from pathlib import Path

def extract_basic_features(json_file):
    """Extract basic features from RefactoringMiner JSON"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    features = []
    for commit in data['commits']:
        for refactoring in commit['refactorings']:
            # Get file path from left side locations
            file_path = refactoring['leftSideLocations'][0]['filePath'] if refactoring['leftSideLocations'] else ''
            
            # Extract class and method names
            class_name = extract_class_name(file_path)
            method_name = extract_method_name(refactoring)
            
            # Calculate lines changed
            lines_changed = calculate_lines_changed(refactoring)
            
            features.append({
                'refactoring_type': refactoring['type'],
                'file_path': file_path,
                'method_name': method_name,
                'class_name': class_name,
                'lines_changed': lines_changed,
                'commit_sha': commit['sha1']
            })
    
    return pd.DataFrame(features)

def extract_class_name(file_path):
    """Extract class name from file path"""
    if not file_path:
        return ''
    return Path(file_path).stem

def extract_method_name(refactoring):
    """Extract method name from refactoring description"""
    desc = refactoring.get('description', '')
    # Simple extraction - look for method patterns
    if 'method' in desc.lower():
        parts = desc.split()
        for i, part in enumerate(parts):
            if part == 'method' and i + 1 < len(parts):
                return parts[i + 1].split('(')[0]
    return ''

def calculate_lines_changed(refactoring):
    """Calculate lines changed from refactoring locations"""
    total_lines = 0
    for location in refactoring.get('leftSideLocations', []) + refactoring.get('rightSideLocations', []):
        start = location.get('startLine', 0)
        end = location.get('endLine', 0)
        total_lines += max(0, end - start + 1)
    return total_lines

def main():
    # Extract features from IntelliJ data
    json_file = 'data/intellij-community_refactorings.json'
    df = extract_basic_features(json_file)
    
    print(f"Extracted {len(df)} refactoring instances")
    print(f"Refactoring types: {df['refactoring_type'].value_counts()}")
    
    # Save to CSV
    output_file = 'data/intellij_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
