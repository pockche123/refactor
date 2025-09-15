#!/usr/bin/env python3

import pandas as pd
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

def clone_repository(repo_url, temp_dir):
    """Clone repository to temporary directory"""
    try:
        subprocess.run(['git', 'clone', repo_url, temp_dir], 
                      check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {repo_url}: {e}")
        return False

def get_code_changes(repo_path, commit_sha, file_path):
    """Get before/after code for a specific file in a commit"""
    try:
        os.chdir(repo_path)
        
        # Get the code after the refactoring (current commit)
        after_result = subprocess.run(['git', 'show', f'{commit_sha}:{file_path}'], 
                                    capture_output=True, text=True)
        
        # Get the code before the refactoring (parent commit)
        before_result = subprocess.run(['git', 'show', f'{commit_sha}^:{file_path}'], 
                                     capture_output=True, text=True)
        
        if after_result.returncode == 0 and before_result.returncode == 0:
            return {
                'before': before_result.stdout,
                'after': after_result.stdout,
                'success': True
            }
        else:
            return {'success': False, 'error': 'File not found in commit'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def validate_refactoring_prediction(before_code, after_code, predicted_type, actual_type):
    """Validate if the predicted refactoring type matches the actual changes"""
    
    # Simple heuristics for common refactoring types
    validation_rules = {
        'Rename Method': lambda b, a: check_method_rename(b, a),
        'Extract Method': lambda b, a: check_method_extraction(b, a),
        'Add Parameter': lambda b, a: check_parameter_addition(b, a),
        'Remove Parameter': lambda b, a: check_parameter_removal(b, a),
        'Add Parameter Annotation': lambda b, a: check_annotation_addition(b, a),
        'Rename Variable': lambda b, a: check_variable_rename(b, a),
        'Change Parameter Type': lambda b, a: check_parameter_type_change(b, a),
        'Change Return Type': lambda b, a: check_return_type_change(b, a)
    }
    
    # Check if prediction matches actual
    prediction_correct = predicted_type == actual_type
    
    # Try to validate the actual refactoring occurred
    behavioral_validation = False
    if actual_type in validation_rules:
        try:
            behavioral_validation = validation_rules[actual_type](before_code, after_code)
        except:
            behavioral_validation = None  # Validation failed
    
    return {
        'prediction_correct': prediction_correct,
        'behavioral_validation': behavioral_validation,
        'code_retrieved': True
    }

def check_method_rename(before, after):
    """Check if method was renamed"""
    # Simple check: different method names but similar structure
    before_methods = extract_method_names(before)
    after_methods = extract_method_names(after)
    return len(before_methods.symmetric_difference(after_methods)) > 0

def check_method_extraction(before, after):
    """Check if method was extracted"""
    # Simple check: more methods in after than before
    before_count = before.count('public ') + before.count('private ') + before.count('protected ')
    after_count = after.count('public ') + after.count('private ') + after.count('protected ')
    return after_count > before_count

def check_parameter_addition(before, after):
    """Check if parameter was added"""
    # Simple check: more parameters in method signatures
    return after.count(',') > before.count(',') or ('(' in after and after.count('(') >= before.count('('))

def check_parameter_removal(before, after):
    """Check if parameter was removed"""
    # Simple check: fewer parameters in method signatures
    return before.count(',') > after.count(',')

def check_annotation_addition(before, after):
    """Check if annotation was added"""
    # Simple check: more @ symbols in after
    return after.count('@') > before.count('@')

def check_variable_rename(before, after):
    """Check if variable was renamed"""
    # Simple check: different variable patterns
    return len(set(before.split()) - set(after.split())) > 0

def check_parameter_type_change(before, after):
    """Check if parameter type changed"""
    # Simple check: different type keywords
    types = ['String', 'int', 'boolean', 'List', 'Map', 'Object']
    before_types = sum(before.count(t) for t in types)
    after_types = sum(after.count(t) for t in types)
    return before_types != after_types

def check_return_type_change(before, after):
    """Check if return type changed"""
    # Simple check: different return type patterns
    return 'return ' in before and 'return ' in after and before != after

def extract_method_names(code):
    """Extract method names from code (simple regex-free approach)"""
    methods = set()
    lines = code.split('\n')
    for line in lines:
        if any(modifier in line for modifier in ['public ', 'private ', 'protected ']):
            if '(' in line and ')' in line:
                # Extract potential method name
                parts = line.split('(')[0].split()
                if len(parts) > 0:
                    methods.add(parts[-1])
    return methods

def validate_ml_predictions(domain, model_name, repo_url, max_samples=10):
    """Validate ML predictions for a domain using behavioral testing"""
    
    print(f"\n=== Behavioral Validation: {domain.upper()} - {model_name.upper()} ===")
    
    # Load ML results
    results_file = f'results/ml_testing/{domain}_{model_name}_results.csv'
    try:
        df = pd.read_csv(results_file)
    except FileNotFoundError:
        print(f"Results file not found: {results_file}")
        return None
    
    # Filter to correct predictions for validation
    correct_predictions = df[df['correct'] == True].head(max_samples)
    print(f"Validating {len(correct_predictions)} correct predictions...")
    
    # Create temporary directory for repository
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = os.path.join(temp_dir, 'repo')
        
        # Clone repository
        if not clone_repository(repo_url, repo_path):
            print("Failed to clone repository")
            return None
        
        validation_results = []
        
        for idx, row in correct_predictions.iterrows():
            print(f"Validating {idx+1}/{len(correct_predictions)}: {row['predicted_type']}")
            
            # Get code changes
            changes = get_code_changes(repo_path, row['commit_sha'], row['file_path'])
            
            if changes['success']:
                # Validate the refactoring
                validation = validate_refactoring_prediction(
                    changes['before'], 
                    changes['after'],
                    row['predicted_type'],
                    row['refactoring_type']
                )
                
                validation_results.append({
                    'commit_sha': row['commit_sha'],
                    'file_path': row['file_path'],
                    'predicted_type': row['predicted_type'],
                    'actual_type': row['refactoring_type'],
                    'ml_correct': row['correct'],
                    'code_retrieved': validation['code_retrieved'],
                    'behavioral_validation': validation['behavioral_validation'],
                    'lines_before': len(changes['before'].split('\n')),
                    'lines_after': len(changes['after'].split('\n'))
                })
            else:
                print(f"  Failed to retrieve code: {changes.get('error', 'Unknown error')}")
                validation_results.append({
                    'commit_sha': row['commit_sha'],
                    'file_path': row['file_path'],
                    'predicted_type': row['predicted_type'],
                    'actual_type': row['refactoring_type'],
                    'ml_correct': row['correct'],
                    'code_retrieved': False,
                    'behavioral_validation': None,
                    'error': changes.get('error', 'Unknown error')
                })
    
    return pd.DataFrame(validation_results)

def main():
    # Repository URLs for each domain
    repositories = {
        'commons_lang': 'https://github.com/apache/commons-lang.git',
        'spring': 'https://github.com/spring-projects/spring-framework.git',
        'kafka': 'https://github.com/apache/kafka.git',
        'intellij': 'https://github.com/JetBrains/intellij-community.git',
        'mockito': 'https://github.com/mockito/mockito.git'
    }
    
    # Test with best performing models first
    test_cases = [
        ('commons_lang', 'randomforest'),  # 91.4% accuracy
        ('intellij', 'logisticregression'),  # 63.2% accuracy
        ('spring', 'randomforest'),  # 48.6% accuracy
    ]
    
    os.makedirs('results/behavioral_validation', exist_ok=True)
    
    for domain, model in test_cases:
        if domain in repositories:
            print(f"\nStarting behavioral validation for {domain} - {model}")
            
            results = validate_ml_predictions(
                domain, 
                model, 
                repositories[domain], 
                max_samples=5  # Start with 5 samples per domain
            )
            
            if results is not None:
                # Save results
                output_file = f'results/behavioral_validation/{domain}_{model}_behavioral.csv'
                results.to_csv(output_file, index=False)
                print(f"✓ Saved: {output_file}")
                
                # Summary
                total = len(results)
                code_retrieved = results['code_retrieved'].sum()
                behavioral_valid = results['behavioral_validation'].sum() if 'behavioral_validation' in results else 0
                
                print(f"Summary: {code_retrieved}/{total} code retrieved, {behavioral_valid}/{total} behaviorally validated")
            else:
                print(f"✗ Failed validation for {domain}")

if __name__ == "__main__":
    main()
