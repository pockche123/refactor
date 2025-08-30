#!/usr/bin/env python3
"""
Extract real complexity features from Java source code for refactoring analysis
"""

import json
import pandas as pd
import subprocess
import os
from pathlib import Path
import re

def calculate_cyclomatic_complexity(file_path, start_line, end_line):
    """Calculate cyclomatic complexity for code section"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Extract relevant code section
        code_section = ''.join(lines[start_line-1:end_line])
        
        # Count decision points (simplified McCabe complexity)
        complexity = 1  # Base complexity
        
        # Decision keywords that increase complexity
        decision_keywords = ['if', 'else', 'while', 'for', 'case', 'catch', '&&', '||', '?']
        
        for keyword in decision_keywords:
            if keyword in ['&&', '||', '?']:
                complexity += code_section.count(keyword)
            else:
                # Use word boundaries for keywords
                complexity += len(re.findall(r'\b' + keyword + r'\b', code_section))
        
        return complexity
    except:
        return 2  # Default fallback

def calculate_nesting_depth(file_path, start_line, end_line):
    """Calculate maximum nesting depth for code section"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        code_section = ''.join(lines[start_line-1:end_line])
        
        max_depth = 0
        current_depth = 0
        
        for char in code_section:
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth = max(0, current_depth - 1)
        
        return max(1, max_depth)  # Minimum depth of 1
    except:
        return 1  # Default fallback

def extract_complexity_features(json_file, project_path):
    """Extract complexity features from RefactoringMiner JSON"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    features = []
    
    for commit in data['commits']:
        for refactoring in commit['refactorings']:
            # Get primary location for analysis
            location = None
            if refactoring.get('leftSideLocations'):
                location = refactoring['leftSideLocations'][0]
            elif refactoring.get('rightSideLocations'):
                location = refactoring['rightSideLocations'][0]
            
            if not location:
                continue
            
            file_path = os.path.join(project_path, location['filePath'])
            start_line = location.get('startLine', 1)
            end_line = location.get('endLine', start_line)
            
            # Calculate real complexity metrics
            complexity = calculate_cyclomatic_complexity(file_path, start_line, end_line)
            nesting = calculate_nesting_depth(file_path, start_line, end_line)
            
            # Extract other features
            class_name = Path(location['filePath']).stem
            method_name = extract_method_name(refactoring)
            lines_changed = max(1, end_line - start_line + 1)
            
            features.append({
                'refactoring_type': refactoring['type'],
                'class_name': class_name,
                'method_name': method_name,
                'lines_changed': lines_changed,
                'cyclomatic_complexity': complexity,
                'nesting_depth': nesting,
                'file_path': location['filePath'],
                'commit_sha': commit['sha1']
            })
    
    return pd.DataFrame(features)

def extract_method_name(refactoring):
    """Extract method name from refactoring description"""
    desc = refactoring.get('description', '')
    if 'method' in desc.lower():
        parts = desc.split()
        for i, part in enumerate(parts):
            if part == 'method' and i + 1 < len(parts):
                return parts[i + 1].split('(')[0]
    return ''

def process_project(project_name, json_file, project_path):
    """Process a single project and extract complexity features"""
    print(f"Processing {project_name}...")
    
    df = extract_complexity_features(json_file, project_path)
    
    # Encode categorical features
    df['class_encoded'] = pd.Categorical(df['class_name'].fillna('')).codes
    df['method_encoded'] = pd.Categorical(df['method_name'].fillna('')).codes
    
    print(f"Extracted {len(df)} instances")
    print(f"Complexity range: {df['cyclomatic_complexity'].min()}-{df['cyclomatic_complexity'].max()}")
    print(f"Nesting range: {df['nesting_depth'].min()}-{df['nesting_depth'].max()}")
    
    # Save enhanced dataset
    output_file = f'data/{project_name}_enhanced_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}\n")
    
    return df

def main():
    """Process all projects with real complexity extraction"""
    projects = [
        ('intellij', 'data/intellij-community_refactorings.json', 'complex_projects/intellij-community'),
        ('springboot', 'data/spring-boot_refactorings.json', 'complex_projects/spring-boot'),
        ('mockito', 'data/mockito_refactorings.json', 'complex_projects/mockito'),
        ('elasticsearch', 'data/elasticsearch_refactorings.json', 'complex_projects/elasticsearch')
    ]
    
    for project_name, json_file, project_path in projects:
        if os.path.exists(json_file) and os.path.exists(project_path):
            process_project(project_name, json_file, project_path)
        else:
            print(f"Skipping {project_name} - files not found")

if __name__ == "__main__":
    main()
