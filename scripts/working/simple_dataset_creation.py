#!/usr/bin/env python3
"""
Simple Mockito dataset creation without pandas
"""

import json
import csv

def create_simple_dataset():
    """Create simple CSV dataset from JSON"""
    
    print("🔄 Creating Mockito dataset...")
    
    # Load refactoring data
    with open('data/mockito_refactorings.json', 'r') as f:
        data = json.load(f)
    
    # Extract refactorings
    dataset = []
    
    for commit in data['commits']:
        for refactoring in commit['refactorings']:
            # Get file path
            file_path = None
            if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                file_path = refactoring['leftSideLocations'][0]['filePath']
            elif 'rightSideLocations' in refactoring and refactoring['rightSideLocations']:
                file_path = refactoring['rightSideLocations'][0]['filePath']
            
            if file_path:
                # Simple features
                lines_changed = 1
                if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                    location = refactoring['leftSideLocations'][0]
                    start_line = location.get('startLine', 1)
                    end_line = location.get('endLine', 1)
                    lines_changed = max(1, end_line - start_line + 1)
                
                row = {
                    'file_path': file_path,
                    'refactoring_type': refactoring['type'],
                    'lines_changed': lines_changed,
                    'cyclomatic_complexity': 1,  # Default
                    'nesting_depth': 1  # Default
                }
                dataset.append(row)
    
    # Count refactoring types
    type_counts = {}
    for row in dataset:
        ref_type = row['refactoring_type']
        type_counts[ref_type] = type_counts.get(ref_type, 0) + 1
    
    print(f"📊 Dataset created:")
    print(f"   Total refactorings: {len(dataset)}")
    print(f"   Refactoring types: {len(type_counts)}")
    
    print(f"\n📋 Refactoring type distribution:")
    for ref_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {ref_type}: {count}")
    
    # Save as CSV
    with open('data/mockito_dataset.csv', 'w', newline='') as f:
        fieldnames = ['file_path', 'refactoring_type', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
    
    print(f"\n💾 Dataset saved to: data/mockito_dataset.csv")
    return dataset

if __name__ == "__main__":
    create_simple_dataset()
