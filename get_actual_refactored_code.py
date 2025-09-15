#!/usr/bin/env python3

import pandas as pd
import subprocess
import tempfile
import os

def get_refactored_code(repo_url, commit_sha, file_path):
    """Get actual before/after code from commit SHA"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone repository
            print(f"Cloning {repo_url}...")
            subprocess.run(['git', 'clone', '--depth', '100', repo_url, temp_dir], 
                          check=True, capture_output=True)
            
            os.chdir(temp_dir)
            
            # Get code BEFORE refactoring (parent commit)
            before_result = subprocess.run(['git', 'show', f'{commit_sha}^:{file_path}'], 
                                         capture_output=True, text=True)
            
            # Get code AFTER refactoring (current commit)
            after_result = subprocess.run(['git', 'show', f'{commit_sha}:{file_path}'], 
                                        capture_output=True, text=True)
            
            # Get the diff
            diff_result = subprocess.run(['git', 'show', commit_sha, '--', file_path], 
                                       capture_output=True, text=True)
            
            if before_result.returncode == 0 and after_result.returncode == 0:
                return {
                    'success': True,
                    'before_code': before_result.stdout,
                    'after_code': after_result.stdout,
                    'diff': diff_result.stdout,
                    'commit_sha': commit_sha,
                    'file_path': file_path
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to retrieve code: before={before_result.returncode}, after={after_result.returncode}'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

def demonstrate_actual_refactoring():
    """Demonstrate getting actual refactored code from our ML predictions"""
    
    # Load a sample of correct predictions
    df = pd.read_csv('results/ml_testing/commons_lang_randomforest_results.csv')
    correct_predictions = df[df['correct'] == True].head(2)
    
    repo_url = 'https://github.com/apache/commons-lang.git'
    
    for idx, row in correct_predictions.iterrows():
        print(f"\n{'='*80}")
        print(f"ACTUAL REFACTORING EXAMPLE {idx+1}")
        print(f"{'='*80}")
        print(f"Predicted Type: {row['predicted_type']}")
        print(f"Actual Type: {row['refactoring_type']}")
        print(f"File: {row['file_path']}")
        print(f"Commit: {row['commit_sha']}")
        print(f"Lines Changed: {row['lines_changed']}")
        
        # Get the actual refactored code
        result = get_refactored_code(repo_url, row['commit_sha'], row['file_path'])
        
        if result['success']:
            print(f"\n✓ Successfully retrieved actual refactored code!")
            
            # Show code statistics
            before_lines = len(result['before_code'].split('\n'))
            after_lines = len(result['after_code'].split('\n'))
            
            print(f"Before refactoring: {before_lines} lines")
            print(f"After refactoring: {after_lines} lines")
            print(f"Lines difference: {after_lines - before_lines}")
            
            # Show a sample of the diff
            diff_lines = result['diff'].split('\n')
            print(f"\nActual code changes (first 20 lines of diff):")
            print("-" * 60)
            for line in diff_lines[:20]:
                if line.startswith('+') or line.startswith('-'):
                    print(line)
            print("-" * 60)
            
            # Save the actual code for inspection
            os.makedirs('results/actual_code', exist_ok=True)
            
            # Save before code
            with open(f'results/actual_code/before_{idx+1}.java', 'w') as f:
                f.write(result['before_code'])
            
            # Save after code  
            with open(f'results/actual_code/after_{idx+1}.java', 'w') as f:
                f.write(result['after_code'])
                
            # Save diff
            with open(f'results/actual_code/diff_{idx+1}.txt', 'w') as f:
                f.write(result['diff'])
            
            print(f"✓ Saved actual code files:")
            print(f"  - results/actual_code/before_{idx+1}.java")
            print(f"  - results/actual_code/after_{idx+1}.java") 
            print(f"  - results/actual_code/diff_{idx+1}.txt")
            
        else:
            print(f"✗ Failed to retrieve code: {result['error']}")

def show_commit_info():
    """Show what commit SHAs we have available"""
    
    domains = ['commons_lang', 'spring', 'kafka', 'intellij', 'mockito']
    
    print("AVAILABLE COMMIT SHAs FOR BEHAVIORAL VALIDATION:")
    print("=" * 60)
    
    for domain in domains:
        try:
            df = pd.read_csv(f'data/{domain}_350_real_test.csv')
            unique_commits = df['commit_sha'].nunique()
            sample_commits = df['commit_sha'].unique()[:3]
            
            print(f"\n{domain.upper()}:")
            print(f"  Total test cases: {len(df)}")
            print(f"  Unique commits: {unique_commits}")
            print(f"  Sample commit SHAs:")
            for commit in sample_commits:
                print(f"    {commit}")
                
        except FileNotFoundError:
            print(f"\n{domain.upper()}: No test data found")

if __name__ == "__main__":
    print("DEMONSTRATING ACTUAL REFACTORED CODE RETRIEVAL")
    print("=" * 80)
    
    # First show what commits we have
    show_commit_info()
    
    # Then demonstrate getting actual refactored code
    print(f"\n\nDEMONSTRATING ACTUAL CODE RETRIEVAL:")
    demonstrate_actual_refactoring()
