#!/usr/bin/env python3

import subprocess
import os
import tempfile

def get_and_save_real_code():
    """Get real code and save directly"""
    
    commit_sha = "6b93cbe15693055e50a7f8550bd2baa93fa7f870"
    file_path = "src/test/java/org/apache/commons/lang3/ValidateTest.java"
    repo_url = "https://github.com/apache/commons-lang.git"
    
    # Get current directory
    original_dir = os.getcwd()
    validation_dir = os.path.join(original_dir, 'commons_lang_real_validation_test')
    
    print("RETRIEVING REAL REFACTORED CODE")
    print("=" * 50)
    print(f"Commit: {commit_sha}")
    print(f"File: {file_path}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'commons-lang')
        
        # Clone repository
        print("\nCloning Commons Lang repository...")
        subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)
        
        # Change to repo directory for git operations
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
        
        # Return to original directory
        os.chdir(original_dir)
        
        # Ensure validation directories exist
        os.makedirs(f'{validation_dir}/before', exist_ok=True)
        os.makedirs(f'{validation_dir}/after', exist_ok=True)
        
        # Save BEFORE code
        before_file = f'{validation_dir}/before/ValidateTest.java'
        with open(before_file, 'w') as f:
            f.write(before_result.stdout)
        print(f"✓ Saved BEFORE code: {before_file}")
        
        # Save AFTER code
        after_file = f'{validation_dir}/after/ValidateTest.java'
        with open(after_file, 'w') as f:
            f.write(after_result.stdout)
        print(f"✓ Saved AFTER code: {after_file}")
        
        # Save diff
        diff_file = f'{validation_dir}/refactoring_diff.txt'
        with open(diff_file, 'w') as f:
            f.write(diff_result.stdout)
        print(f"✓ Saved diff: {diff_file}")
        
        # Quick analysis
        print(f"\n{'='*50}")
        print("BEHAVIORAL VALIDATION ANALYSIS")
        print(f"{'='*50}")
        
        before_lines = len(before_result.stdout.split('\n'))
        after_lines = len(after_result.stdout.split('\n'))
        
        print(f"Before refactoring: {before_lines} lines")
        print(f"After refactoring: {after_lines} lines")
        print(f"Lines difference: {after_lines - before_lines}")
        
        # Check for method extraction
        if 'assertNullPointerException' in before_result.stdout:
            if 'assertNullPointerException' not in after_result.stdout:
                print("✓ Method 'assertNullPointerException' removed from ValidateTest")
            else:
                print("? Method 'assertNullPointerException' still present")
        
        print(f"\nML Prediction: Extract And Move Method")
        print(f"Status: ✓ Real code retrieved for behavioral validation")

if __name__ == "__main__":
    get_and_save_real_code()
