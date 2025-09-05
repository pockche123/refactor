#!/usr/bin/env python3
"""
Create Mockito dataset from RefactoringMiner JSON
"""

import json
import pandas as pd
import os
from pathlib import Path

MOCKITO_PATH = "/Users/parjalrai/Workspace/mockito"

def extract_features(file_path, refactoring_data):
    """Extract basic features from refactoring"""
    
    # Basic features
    features = {
        'file_path': file_path,
        'refactoring_type': refactoring_data['type'],
        'lines_changed': 1,  # Default
        'cyclomatic_complexity': 1,  # Default  
        'nesting_depth': 1,  # Default
    }
    
    # Try to get lines changed from locations
    if 'leftSideLocations' in refactoring_data and refactoring_data['leftSideLocations']:
        location = refactoring_data['leftSideLocations'][0]
        start_line = location.get('startLine', 1)
        end_line = location.get('endLine', 1)
        features['lines_changed'] = max(1, end_line - start_line + 1)
    
    return features

def create_mockito_dataset():
    """Create Mockito dataset from JSON"""
    
    print("🔄 Creating Mockito dataset...")
    
    # Load refactoring data
    with open('data/mockito_refactorings.json', 'r') as f:
        data = json.load(f)
    
    # Extract features for each refactoring
    dataset = []
    
    for commit in data['commits']:
        for refactoring in commit['refactorings']:
            # Get file path from locations
            file_path = None
            if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                file_path = refactoring['leftSideLocations'][0]['filePath']
            elif 'rightSideLocations' in refactoring and refactoring['rightSideLocations']:
                file_path = refactoring['rightSideLocations'][0]['filePath']
            
            if file_path:
                features = extract_features(file_path, refactoring)
                dataset.append(features)
    
    # Create DataFrame
    df = pd.DataFrame(dataset)
    
    print(f"📊 Dataset created:")
    print(f"   Total refactorings: {len(df)}")
    print(f"   Refactoring types: {df['refactoring_type'].nunique()}")
    print(f"   Files: {df['file_path'].nunique()}")
    
    print(f"\n📋 Refactoring type distribution:")
    print(df['refactoring_type'].value_counts().head(10))
    
    # Save dataset
    df.to_csv('data/mockito_dataset.csv', index=False)
    print(f"\n💾 Dataset saved to: data/mockito_dataset.csv")
    
    return df

if __name__ == "__main__":
    create_mockito_dataset()
