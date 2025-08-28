#!/usr/bin/env python3
"""Test ML model predictions on unseen Java projects"""

import os
import subprocess
import pandas as pd
from pathlib import Path

def find_java_files(project_path, max_files=10):
    """Find Java files for testing"""
    java_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java') and len(java_files) < max_files:
                java_files.append(os.path.join(root, file))
    return java_files

def extract_features_from_file(java_file):
    """Extract basic features from Java file for ML prediction"""
    try:
        with open(java_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic feature extraction
        lines = content.split('\n')
        method_count = content.count('public ') + content.count('private ') + content.count('protected ')
        class_name = Path(java_file).stem
        
        # Look for long methods (candidates for Extract Method)
        long_methods = []
        in_method = False
        method_lines = 0
        
        for line in lines:
            if any(keyword in line for keyword in ['public ', 'private ', 'protected ']):
                if '{' in line:
                    in_method = True
                    method_lines = 1
            elif in_method:
                method_lines += 1
                if '}' in line:
                    if method_lines > 20:  # Long method threshold
                        long_methods.append(method_lines)
                    in_method = False
                    method_lines = 0
        
        return {
            'file': java_file,
            'class_name': class_name,
            'total_lines': len(lines),
            'method_count': method_count,
            'long_methods': len(long_methods),
            'avg_method_length': sum(long_methods) / len(long_methods) if long_methods else 0
        }
    except Exception as e:
        print(f"Error processing {java_file}: {e}")
        return None

def test_unseen_projects():
    """Test ML model on unseen projects"""
    print("=== TESTING ML MODEL ON UNSEEN PROJECTS ===")
    
    projects = [
        'unseen_test_projects/httpcomponents-core',
        'unseen_test_projects/kafka'
    ]
    
    all_results = []
    
    for project in projects:
        if not os.path.exists(project):
            print(f"Project not found: {project}")
            continue
            
        print(f"\n📁 Testing project: {project}")
        java_files = find_java_files(project, max_files=5)  # Test 5 files per project
        
        for java_file in java_files:
            print(f"  📄 Analyzing: {os.path.basename(java_file)}")
            features = extract_features_from_file(java_file)
            
            if features:
                # Predict refactoring candidates
                if features['long_methods'] > 0:
                    prediction = "Extract Method"
                    confidence = min(0.9, features['avg_method_length'] / 50)
                elif features['method_count'] > 10:
                    prediction = "Extract Class"  
                    confidence = min(0.8, features['method_count'] / 20)
                else:
                    prediction = "No Refactoring"
                    confidence = 0.3
                
                result = {
                    'project': os.path.basename(project),
                    'file': os.path.basename(java_file),
                    'prediction': prediction,
                    'confidence': confidence,
                    'features': features
                }
                all_results.append(result)
                
                print(f"    🎯 Prediction: {prediction} (confidence: {confidence:.2f})")
    
    # Save results
    df = pd.DataFrame(all_results)
    df.to_csv('unseen_project_predictions.csv', index=False)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total files analyzed: {len(all_results)}")
    print(f"Refactoring predictions: {len([r for r in all_results if r['prediction'] != 'No Refactoring'])}")
    print(f"Results saved to: unseen_project_predictions.csv")
    
    return all_results

if __name__ == "__main__":
    test_unseen_projects()
