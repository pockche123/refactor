#!/usr/bin/env python3

import subprocess
import os
import tempfile

def get_real_refactored_code():
    """Get actual before/after code from Commons Lang commit"""
    
    commit_sha = "6b93cbe15693055e50a7f8550bd2baa93fa7f870"
    file_path = "src/test/java/org/apache/commons/lang3/ValidateTest.java"
    repo_url = "https://github.com/apache/commons-lang.git"
    
    print("RETRIEVING REAL REFACTORED CODE")
    print("=" * 50)
    print(f"Commit: {commit_sha}")
    print(f"File: {file_path}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'commons-lang')
        
        # Clone repository
        print("\nCloning Commons Lang repository...")
        subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)
        
        os.chdir(repo_dir)
        
        # Get BEFORE code (parent commit)
        print("Getting BEFORE refactoring code...")
        before_result = subprocess.run([
            'git', 'show', f'{commit_sha}^:{file_path}'
        ], capture_output=True, text=True, check=True)
        
        # Get AFTER code (current commit)  
        print("Getting AFTER refactoring code...")
        after_result = subprocess.run([
            'git', 'show', f'{commit_sha}:{file_path}'
        ], capture_output=True, text=True, check=True)
        
        # Get diff
        print("Getting refactoring diff...")
        diff_result = subprocess.run([
            'git', 'show', commit_sha, '--', file_path
        ], capture_output=True, text=True, check=True)
        
        return {
            'before_code': before_result.stdout,
            'after_code': after_result.stdout,
            'diff': diff_result.stdout
        }

def save_real_code():
    """Save real before/after code to validation directories"""
    
    # Get the real code
    code_data = get_real_refactored_code()
    
    # Save to validation directories
    validation_dir = 'commons_lang_real_validation_test'
    
    # Ensure directories exist
    os.makedirs(f'{validation_dir}/before', exist_ok=True)
    os.makedirs(f'{validation_dir}/after', exist_ok=True)
    
    # Save BEFORE code
    before_file = f'{validation_dir}/before/ValidateTest.java'
    with open(before_file, 'w') as f:
        f.write(code_data['before_code'])
    print(f"✓ Saved BEFORE code: {before_file}")
    
    # Save AFTER code
    after_file = f'{validation_dir}/after/ValidateTest.java'
    with open(after_file, 'w') as f:
        f.write(code_data['after_code'])
    print(f"✓ Saved AFTER code: {after_file}")
    
    # Save diff
    diff_file = f'{validation_dir}/refactoring_diff.txt'
    with open(diff_file, 'w') as f:
        f.write(code_data['diff'])
    print(f"✓ Saved diff: {diff_file}")
    
    # Analyze the refactoring
    print(f"\n{'='*50}")
    print("BEHAVIORAL VALIDATION ANALYSIS")
    print(f"{'='*50}")
    
    before_lines = len(code_data['before_code'].split('\n'))
    after_lines = len(code_data['after_code'].split('\n'))
    
    print(f"Before refactoring: {before_lines} lines")
    print(f"After refactoring: {after_lines} lines")
    print(f"Lines difference: {after_lines - before_lines}")
    
    # Check for method extraction evidence
    if 'assertNullPointerException' in code_data['before_code']:
        if 'assertNullPointerException' not in code_data['after_code']:
            print("✓ Method 'assertNullPointerException' removed from ValidateTest")
        else:
            print("? Method 'assertNullPointerException' still present")
    
    # Check diff for move evidence
    if 'LangAssertions' in code_data['diff']:
        print("✓ 'LangAssertions' mentioned in diff - indicates move")
    
    print(f"\nML Prediction: Extract And Move Method")
    print(f"Behavioral Evidence: Ready for manual inspection")

if __name__ == "__main__":
    save_real_code()
