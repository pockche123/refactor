#!/usr/bin/env python3

import pandas as pd
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

def create_validation_structure(domain, case_id, commit_sha, file_path):
    """Create before/after directory structure for a validation case"""
    
    base_dir = f"{domain}_real_commit_validation"
    before_dir = f"{base_dir}/before_{case_id}"
    after_dir = f"{base_dir}/after_{case_id}"
    
    # Create directories
    os.makedirs(before_dir, exist_ok=True)
    os.makedirs(after_dir, exist_ok=True)
    
    return before_dir, after_dir

def get_code_from_commit(repo_url, commit_sha, file_path, is_before=True):
    """Get code from commit with error handling"""
    
    try:
        # Create temporary directory for repo
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = os.path.join(temp_dir, 'repo')
            
            # Clone with limited depth for speed
            print(f"  Cloning repository...")
            clone_result = subprocess.run([
                'git', 'clone', '--depth', '10', repo_url, repo_dir
            ], capture_output=True, text=True, timeout=120)
            
            if clone_result.returncode != 0:
                return {
                    'success': False, 
                    'error': f'Clone failed: {clone_result.stderr}',
                    'error_type': 'clone_failed'
                }
            
            os.chdir(repo_dir)
            
            # Get the appropriate commit (before = parent, after = current)
            target_commit = f"{commit_sha}^" if is_before else commit_sha
            
            # Try to get the file
            get_result = subprocess.run([
                'git', 'show', f'{target_commit}:{file_path}'
            ], capture_output=True, text=True, timeout=30)
            
            if get_result.returncode != 0:
                return {
                    'success': False,
                    'error': f'File not found in commit: {get_result.stderr}',
                    'error_type': 'file_not_found'
                }
            
            return {
                'success': True,
                'code': get_result.stdout,
                'commit': target_commit,
                'file_path': file_path
            }
            
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Git operation timed out',
            'error_type': 'timeout'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'error_type': 'unknown'
        }

def create_fallback_structure(before_dir, after_dir, error_info):
    """Create fallback structure when git access fails"""
    
    # Create error info file
    error_file = os.path.join(os.path.dirname(before_dir), 'validation_error.txt')
    with open(error_file, 'w') as f:
        f.write(f"Validation Error: {error_info['error']}\n")
        f.write(f"Error Type: {error_info['error_type']}\n")
        f.write("This case requires manual validation.\n")
    
    # Create placeholder files
    placeholder_content = f"""
// VALIDATION ERROR: Could not retrieve actual code
// Error: {error_info['error']}
// This file is a placeholder - manual validation required
public class PlaceholderClass {{
    // Original validation failed due to: {error_info['error_type']}
}}
"""
    
    with open(os.path.join(before_dir, 'PlaceholderBefore.java'), 'w') as f:
        f.write(placeholder_content)
    
    with open(os.path.join(after_dir, 'PlaceholderAfter.java'), 'w') as f:
        f.write(placeholder_content)

def validate_single_case(domain, case_id, row, repo_url):
    """Validate a single ML prediction case"""
    
    print(f"\n=== Validating Case {case_id}: {row['refactoring_type']} ===")
    print(f"File: {row['file_path']}")
    print(f"Commit: {row['commit_sha'][:12]}...")
    print(f"ML Prediction: {row['predicted_type']} ({'✓' if row['correct'] else '✗'})")
    
    # Create directory structure
    before_dir, after_dir = create_validation_structure(
        domain, case_id, row['commit_sha'], row['file_path']
    )
    
    validation_result = {
        'case_id': case_id,
        'domain': domain,
        'commit_sha': row['commit_sha'],
        'file_path': row['file_path'],
        'refactoring_type': row['refactoring_type'],
        'predicted_type': row['predicted_type'],
        'ml_correct': row['correct'],
        'before_retrieved': False,
        'after_retrieved': False,
        'validation_status': 'pending'
    }
    
    # Try to get BEFORE code
    print("  Getting BEFORE code...")
    before_result = get_code_from_commit(repo_url, row['commit_sha'], row['file_path'], is_before=True)
    
    if before_result['success']:
        # Save before code
        file_name = os.path.basename(row['file_path'])
        before_file_path = os.path.join(before_dir, file_name)
        
        with open(before_file_path, 'w') as f:
            f.write(before_result['code'])
        
        validation_result['before_retrieved'] = True
        print("  ✓ BEFORE code retrieved")
    else:
        print(f"  ✗ BEFORE code failed: {before_result['error_type']}")
        validation_result['before_error'] = before_result['error']
    
    # Try to get AFTER code
    print("  Getting AFTER code...")
    after_result = get_code_from_commit(repo_url, row['commit_sha'], row['file_path'], is_before=False)
    
    if after_result['success']:
        # Save after code
        file_name = os.path.basename(row['file_path'])
        after_file_path = os.path.join(after_dir, file_name)
        
        with open(after_file_path, 'w') as f:
            f.write(after_result['code'])
        
        validation_result['after_retrieved'] = True
        print("  ✓ AFTER code retrieved")
    else:
        print(f"  ✗ AFTER code failed: {after_result['error_type']}")
        validation_result['after_error'] = after_result['error']
    
    # Determine validation status
    if validation_result['before_retrieved'] and validation_result['after_retrieved']:
        validation_result['validation_status'] = 'ready'
        print("  ✓ Case ready for behavioral validation")
    elif validation_result['before_retrieved'] or validation_result['after_retrieved']:
        validation_result['validation_status'] = 'partial'
        print("  ⚠ Partial validation possible")
    else:
        validation_result['validation_status'] = 'failed'
        print("  ✗ Validation failed - creating fallback structure")
        
        # Create fallback structure
        error_info = before_result if not before_result['success'] else after_result
        create_fallback_structure(before_dir, after_dir, error_info)
    
    return validation_result

def run_commons_lang_validation(max_cases=5):
    """Run behavioral validation for Commons Lang cases"""
    
    print("COMMONS LANG REAL COMMIT BEHAVIORAL VALIDATION")
    print("=" * 60)
    
    # Load ML results
    df = pd.read_csv('results/ml_testing/commons_lang_randomforest_results.csv')
    correct_predictions = df[df['correct'] == True].head(max_cases)
    
    repo_url = 'https://github.com/apache/commons-lang.git'
    validation_results = []
    
    for idx, (_, row) in enumerate(correct_predictions.iterrows(), 1):
        try:
            result = validate_single_case('commons_lang', idx, row, repo_url)
            validation_results.append(result)
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            validation_results.append({
                'case_id': idx,
                'domain': 'commons_lang',
                'validation_status': 'error',
                'error': str(e)
            })
    
    # Save validation results
    results_df = pd.DataFrame(validation_results)
    results_df.to_csv('commons_lang_real_commit_validation/validation_results.csv', index=False)
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    ready_count = len(results_df[results_df['validation_status'] == 'ready'])
    partial_count = len(results_df[results_df['validation_status'] == 'partial'])
    failed_count = len(results_df[results_df['validation_status'] == 'failed'])
    
    print(f"Total Cases: {len(results_df)}")
    print(f"Ready for Validation: {ready_count}")
    print(f"Partial Validation: {partial_count}")
    print(f"Failed: {failed_count}")
    
    if ready_count > 0:
        print(f"\n✓ {ready_count} cases ready for behavioral testing")
        print("Directory structure created with before/after code")
    
    return results_df

if __name__ == "__main__":
    # Start with Commons Lang - 3 cases to test the approach
    results = run_commons_lang_validation(max_cases=3)
