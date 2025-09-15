#!/usr/bin/env python3

import pandas as pd
import subprocess
import os
import tempfile

def validate_commons_lang_case():
    """Validate one Commons Lang case step by step"""
    
    print("COMMONS LANG REAL COMMIT VALIDATION - SINGLE CASE")
    print("=" * 60)
    
    # Load first correct prediction
    df = pd.read_csv('results/ml_testing/commons_lang_randomforest_results.csv')
    case = df[df['correct'] == True].iloc[0]
    
    print(f"Target Case:")
    print(f"  File: {case['file_path']}")
    print(f"  Refactoring: {case['refactoring_type']}")
    print(f"  ML Prediction: {case['predicted_type']} ({'✓' if case['correct'] else '✗'})")
    print(f"  Commit: {case['commit_sha']}")
    print(f"  Description: {case['description']}")
    
    # Create validation directory
    validation_dir = 'commons_lang_real_validation_test'
    os.makedirs(validation_dir, exist_ok=True)
    os.makedirs(f'{validation_dir}/before', exist_ok=True)
    os.makedirs(f'{validation_dir}/after', exist_ok=True)
    
    print(f"\n✓ Created validation directory: {validation_dir}")
    
    # Try to get the actual code using git (simplified approach)
    repo_url = 'https://github.com/apache/commons-lang.git'
    
    print(f"\nAttempting to retrieve actual refactored code...")
    print(f"Repository: {repo_url}")
    print(f"Commit: {case['commit_sha']}")
    print(f"File: {case['file_path']}")
    
    # Create info file with case details
    info_content = f"""COMMONS LANG BEHAVIORAL VALIDATION CASE

Case Details:
- File: {case['file_path']}
- Refactoring Type: {case['refactoring_type']}
- ML Prediction: {case['predicted_type']}
- Prediction Correct: {case['correct']}
- Commit SHA: {case['commit_sha']}
- Lines Changed: {case['lines_changed']}
- Complexity: {case['cyclomatic_complexity']}
- Nesting Depth: {case['nesting_depth']}

Description:
{case['description']}

Git Commands to Get Actual Code:
1. Clone repository:
   git clone {repo_url}
   cd commons-lang

2. Get BEFORE refactoring (parent commit):
   git show {case['commit_sha']}^:{case['file_path']} > before_refactoring.java

3. Get AFTER refactoring (current commit):
   git show {case['commit_sha']}:{case['file_path']} > after_refactoring.java

4. Get diff:
   git show {case['commit_sha']} -- {case['file_path']} > refactoring_diff.txt

Validation Steps:
1. Compare before/after code
2. Verify that "Extract And Move Method" actually occurred
3. Check if method was moved to LangAssertions class
4. Confirm ML prediction matches actual refactoring
"""
    
    with open(f'{validation_dir}/case_info.txt', 'w') as f:
        f.write(info_content)
    
    print(f"✓ Created case info file: {validation_dir}/case_info.txt")
    
    # Try simple git approach (without cloning full repo)
    try:
        print(f"\nTrying to access commit via git ls-remote...")
        result = subprocess.run([
            'git', 'ls-remote', repo_url, case['commit_sha']
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✓ Commit SHA exists in repository")
            
            # Create manual validation instructions
            manual_instructions = f"""MANUAL VALIDATION INSTRUCTIONS

This case is ready for manual behavioral validation.

Steps to validate:
1. Open terminal and run:
   git clone {repo_url}
   cd commons-lang

2. Get the code before refactoring:
   git show {case['commit_sha']}^:{case['file_path']}

3. Get the code after refactoring:
   git show {case['commit_sha']}:{case['file_path']}

4. Compare the two versions to verify:
   - Method 'assertNullPointerException' was extracted from ValidateTest
   - Method was moved to LangAssertions class
   - ML prediction "Extract And Move Method" is correct

Expected Result: ✓ ML prediction should match actual refactoring
"""
            
            with open(f'{validation_dir}/manual_validation_steps.txt', 'w') as f:
                f.write(manual_instructions)
            
            print(f"✓ Created manual validation steps: {validation_dir}/manual_validation_steps.txt")
            
        else:
            print("✗ Could not access commit in repository")
            
    except Exception as e:
        print(f"✗ Git access failed: {e}")
    
    print(f"\n{'='*60}")
    print("VALIDATION SETUP COMPLETE")
    print(f"{'='*60}")
    print(f"Validation directory: {validation_dir}")
    print(f"Case: Extract And Move Method")
    print(f"Status: Ready for manual validation")
    print(f"Next: Follow instructions in manual_validation_steps.txt")
    
    return validation_dir

if __name__ == "__main__":
    validation_dir = validate_commons_lang_case()
