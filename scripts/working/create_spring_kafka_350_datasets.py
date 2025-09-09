#!/usr/bin/env python3
"""
Create 350-instance datasets from scaled refactoring extractions
"""

import json
import csv
import random
from collections import defaultdict

def create_spring_350_dataset():
    """Create 350-instance dataset from Spring's 3,555 refactorings"""
    
    print("📊 Processing Spring Framework (3,555 → 350)...")
    
    # Load Spring refactorings
    with open('data/spring_refactorings.json', 'r') as f:
        data = json.load(f)
    
    # Extract all refactorings
    all_refactorings = []
    for commit_idx, commit in enumerate(data['commits']):
        commit_sha = commit['sha1']
        for ref_idx, refactoring in enumerate(commit['refactorings']):
            # Extract features
            file_path = None
            if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                file_path = refactoring['leftSideLocations'][0]['filePath']
            elif 'rightSideLocations' in refactoring and refactoring['rightSideLocations']:
                file_path = refactoring['rightSideLocations'][0]['filePath']
            
            if file_path:
                lines_changed = 1
                if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                    location = refactoring['leftSideLocations'][0]
                    start_line = location.get('startLine', 1)
                    end_line = location.get('endLine', 1)
                    lines_changed = max(1, end_line - start_line + 1)
                
                all_refactorings.append({
                    'file_path': file_path,
                    'refactoring_type': refactoring['type'],
                    'lines_changed': lines_changed,
                    'cyclomatic_complexity': 1,
                    'nesting_depth': 1,
                    'commit_sha': commit_sha
                })
    
    print(f"   Extracted {len(all_refactorings)} refactorings")
    
    # Randomly sample 350
    random.seed(42)  # For reproducibility
    sampled_refactorings = random.sample(all_refactorings, min(350, len(all_refactorings)))
    
    # Save datasets
    save_datasets(sampled_refactorings, 'spring')
    
    return len(sampled_refactorings)

def create_kafka_350_dataset():
    """Create 350-instance dataset from Kafka's 1,123 refactorings"""
    
    print("📊 Processing Kafka (1,123 → 350)...")
    
    # Load Kafka refactorings
    with open('data/kafka_refactorings.json', 'r') as f:
        data = json.load(f)
    
    # Extract all refactorings
    all_refactorings = []
    for commit_idx, commit in enumerate(data['commits']):
        commit_sha = commit['sha1']
        for ref_idx, refactoring in enumerate(commit['refactorings']):
            # Extract features
            file_path = None
            if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                file_path = refactoring['leftSideLocations'][0]['filePath']
            elif 'rightSideLocations' in refactoring and refactoring['rightSideLocations']:
                file_path = refactoring['rightSideLocations'][0]['filePath']
            
            if file_path:
                lines_changed = 1
                if 'leftSideLocations' in refactoring and refactoring['leftSideLocations']:
                    location = refactoring['leftSideLocations'][0]
                    start_line = location.get('startLine', 1)
                    end_line = location.get('endLine', 1)
                    lines_changed = max(1, end_line - start_line + 1)
                
                all_refactorings.append({
                    'file_path': file_path,
                    'refactoring_type': refactoring['type'],
                    'lines_changed': lines_changed,
                    'cyclomatic_complexity': 1,
                    'nesting_depth': 1,
                    'commit_sha': commit_sha
                })
    
    print(f"   Extracted {len(all_refactorings)} refactorings")
    
    # Randomly sample 350
    random.seed(42)  # For reproducibility
    sampled_refactorings = random.sample(all_refactorings, min(350, len(all_refactorings)))
    
    # Save datasets
    save_datasets(sampled_refactorings, 'kafka')
    
    return len(sampled_refactorings)

def save_datasets(refactorings, project_name):
    """Save behavioral and simple datasets"""
    
    # Behavioral dataset
    behavioral_file = f'data/{project_name}_behavioral_dataset_350.csv'
    with open(behavioral_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file_path', 'refactoring_type', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth', 'commit_sha'])
        writer.writeheader()
        writer.writerows(refactorings)
    
    # Simple dataset (without commit_sha)
    simple_data = [{k: v for k, v in r.items() if k != 'commit_sha'} for r in refactorings]
    simple_file = f'data/{project_name}_simple_dataset_350.csv'
    with open(simple_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file_path', 'refactoring_type', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth'])
        writer.writeheader()
        writer.writerows(simple_data)
    
    print(f"   ✅ {behavioral_file}")
    print(f"   ✅ {simple_file}")

def main():
    print("🚀 CREATING 350-INSTANCE DATASETS")
    print("=" * 50)
    
    total_instances = 0
    
    # Create Spring 350 dataset
    spring_count = create_spring_350_dataset()
    total_instances += spring_count
    
    # Create Kafka 350 dataset  
    kafka_count = create_kafka_350_dataset()
    total_instances += kafka_count
    
    print(f"\n📈 DATASET CREATION SUMMARY:")
    print(f"   Spring Framework: {spring_count} instances")
    print(f"   Kafka: {kafka_count} instances")
    print(f"   Total: {total_instances} instances")
    print(f"   Target per project: 350 instances")
    
    print(f"\n✅ Ready for ML training on 350-instance datasets")

if __name__ == "__main__":
    main()
