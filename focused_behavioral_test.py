#!/usr/bin/env python3

import pandas as pd
import subprocess
import os

def get_commit_diff(repo_url, commit_sha, file_path):
    """Get the diff for a specific file in a commit using git show"""
    try:
        # Clone repo temporarily and get diff
        temp_dir = f'/tmp/repo_{commit_sha[:8]}'
        if not os.path.exists(temp_dir):
            clone_result = subprocess.run(['git', 'clone', '--depth', '50', repo_url, temp_dir], 
                                        capture_output=True, text=True, timeout=60)
            if clone_result.returncode != 0:
                return {'success': False, 'error': f'Clone failed: {clone_result.stderr}'}
        
        # Get the diff
        os.chdir(temp_dir)
        cmd = ['git', 'show', '--format=', commit_sha, '--', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return {
                'success': True,
                'diff': result.stdout,
                'lines_added': result.stdout.count('\n+'),
                'lines_removed': result.stdout.count('\n-')
            }
        else:
            return {'success': False, 'error': f'Git show failed: {result.stderr}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def analyze_refactoring_diff(diff_text, predicted_type, actual_type):
    """Analyze diff to validate refactoring type"""
    
    # Simple pattern matching for common refactoring types
    validation_patterns = {
        'Add Parameter Annotation': lambda d: any(ann in d for ann in ['+@NotNull', '+@Nullable', '+@Override']),
        'Extract And Move Method': lambda d: '+public ' in d or '+private ' in d or '+protected ' in d,
        'Rename Method': lambda d: '-public ' in d and '+public ' in d,
        'Rename Variable': lambda d: d.count('-') > 0 and d.count('+') > 0 and len(d.split('\n')) < 50,
        'Add Method Annotation': lambda d: any(ann in d for ann in ['+@Override', '+@Test', '+@Deprecated']),
        'Change Variable Type': lambda d: any(f'-{t}' in d for t in ['String', 'int', 'boolean']) and any(f'+{t}' in d for t in ['String', 'int', 'boolean'])
    }
    
    prediction_correct = predicted_type == actual_type
    
    # Check if the actual refactoring type has expected patterns in diff
    behavioral_evidence = False
    if actual_type in validation_patterns:
        try:
            behavioral_evidence = validation_patterns[actual_type](diff_text)
        except:
            behavioral_evidence = None
    
    return {
        'prediction_correct': prediction_correct,
        'behavioral_evidence': behavioral_evidence,
        'diff_size': len(diff_text),
        'lines_changed_in_diff': diff_text.count('\n+') + diff_text.count('\n-')
    }

def run_focused_behavioral_test():
    """Run behavioral validation on a focused sample"""
    
    # Test cases: domain, model, max_samples
    test_cases = [
        ('commons_lang', 'randomforest', 2),  # Best performer
        ('intellij', 'logisticregression', 2),  # Moderate performer  
    ]
    
    repositories = {
        'commons_lang': 'https://github.com/apache/commons-lang.git',
        'intellij': 'https://github.com/JetBrains/intellij-community.git',
    }
    
    all_results = []
    
    for domain, model, max_samples in test_cases:
        print(f"\n{'='*60}")
        print(f"BEHAVIORAL VALIDATION: {domain.upper()} - {model.upper()}")
        print(f"{'='*60}")
        
        # Load correct predictions
        results_file = f'results/ml_testing/{domain}_{model}_results.csv'
        try:
            df = pd.read_csv(results_file)
            correct_df = df[df['correct'] == True].head(max_samples)
            
            print(f"Testing {len(correct_df)} correct predictions...")
            
            for idx, row in correct_df.iterrows():
                print(f"\nTest {idx+1}: {row['predicted_type']}")
                print(f"  File: {row['file_path']}")
                print(f"  Commit: {row['commit_sha'][:12]}...")
                
                # Get diff
                diff_result = get_commit_diff(
                    repositories[domain], 
                    row['commit_sha'], 
                    row['file_path']
                )
                
                if diff_result['success']:
                    # Analyze the diff
                    analysis = analyze_refactoring_diff(
                        diff_result['diff'],
                        row['predicted_type'],
                        row['refactoring_type']
                    )
                    
                    # Store results
                    result = {
                        'domain': domain,
                        'model': model,
                        'commit_sha': row['commit_sha'],
                        'file_path': row['file_path'],
                        'predicted_type': row['predicted_type'],
                        'actual_type': row['refactoring_type'],
                        'ml_correct': True,
                        'diff_retrieved': True,
                        'behavioral_evidence': analysis['behavioral_evidence'],
                        'diff_size': analysis['diff_size'],
                        'lines_in_diff': analysis['lines_changed_in_diff'],
                        'reported_lines': row['lines_changed']
                    }
                    
                    all_results.append(result)
                    
                    # Print analysis
                    evidence_status = "✓" if analysis['behavioral_evidence'] else "?" if analysis['behavioral_evidence'] is None else "✗"
                    print(f"  Behavioral Evidence: {evidence_status}")
                    print(f"  Diff Size: {analysis['diff_size']} chars")
                    print(f"  Lines Changed: {analysis['lines_changed_in_diff']} (reported: {row['lines_changed']})")
                    
                else:
                    print(f"  ✗ Failed to get diff: {diff_result['error']}")
                    
                    result = {
                        'domain': domain,
                        'model': model,
                        'commit_sha': row['commit_sha'],
                        'file_path': row['file_path'],
                        'predicted_type': row['predicted_type'],
                        'actual_type': row['refactoring_type'],
                        'ml_correct': True,
                        'diff_retrieved': False,
                        'error': diff_result['error']
                    }
                    
                    all_results.append(result)
        
        except Exception as e:
            print(f"Error processing {domain}: {e}")
    
    # Save all results
    if all_results:
        results_df = pd.DataFrame(all_results)
        output_file = 'results/behavioral_validation/focused_behavioral_test.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n✓ Saved behavioral test results: {output_file}")
        
        # Summary
        print(f"\n{'='*60}")
        print("BEHAVIORAL VALIDATION SUMMARY")
        print(f"{'='*60}")
        
        total_tests = len(results_df)
        diff_retrieved = results_df['diff_retrieved'].sum()
        behavioral_evidence = results_df['behavioral_evidence'].sum() if 'behavioral_evidence' in results_df else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Diffs Retrieved: {diff_retrieved}/{total_tests} ({diff_retrieved/total_tests*100:.1f}%)")
        if diff_retrieved > 0:
            print(f"Behavioral Evidence Found: {behavioral_evidence}/{diff_retrieved} ({behavioral_evidence/diff_retrieved*100:.1f}% of retrieved)")

if __name__ == "__main__":
    run_focused_behavioral_test()
