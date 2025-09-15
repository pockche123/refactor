#!/usr/bin/env python3

import pandas as pd
import subprocess
import os
import json

def test_commit_accessibility(commit_sha, repo_url):
    """Test if we can access a commit via GitHub API or git"""
    try:
        # Try to get commit info via git ls-remote
        result = subprocess.run(['git', 'ls-remote', repo_url, commit_sha], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False

def validate_prediction_consistency(df):
    """Validate internal consistency of predictions"""
    results = []
    
    for idx, row in df.iterrows():
        validation = {
            'commit_sha': row['commit_sha'],
            'file_path': row['file_path'],
            'predicted_type': row['predicted_type'],
            'actual_type': row['refactoring_type'],
            'ml_correct': row['correct'],
            'lines_changed': row['lines_changed'],
            'complexity': row['cyclomatic_complexity'],
            'nesting_depth': row['nesting_depth']
        }
        
        # Consistency checks
        validation['has_commit_sha'] = pd.notna(row['commit_sha']) and len(str(row['commit_sha'])) > 10
        validation['has_file_path'] = pd.notna(row['file_path']) and len(str(row['file_path'])) > 0
        validation['reasonable_lines'] = 0 < row['lines_changed'] < 10000
        validation['reasonable_complexity'] = 0 < row['cyclomatic_complexity'] <= 50
        
        # Pattern validation for common refactoring types
        validation['pattern_match'] = validate_refactoring_pattern(row)
        
        results.append(validation)
    
    return pd.DataFrame(results)

def validate_refactoring_pattern(row):
    """Validate if the refactoring type matches expected patterns"""
    ref_type = row['refactoring_type']
    lines = row['lines_changed']
    complexity = row['cyclomatic_complexity']
    
    # Pattern expectations for different refactoring types
    patterns = {
        'Rename Method': lines < 50,  # Usually small changes
        'Rename Variable': lines < 20,  # Very small changes
        'Add Parameter': lines < 100,  # Moderate changes
        'Remove Parameter': lines < 100,  # Moderate changes
        'Extract Method': lines > 5,  # Should involve some code movement
        'Add Parameter Annotation': lines < 10,  # Very small changes
        'Change Parameter Type': lines < 50,  # Small to moderate changes
        'Extract And Move Method': lines > 10,  # Significant changes expected
    }
    
    if ref_type in patterns:
        return patterns[ref_type]
    else:
        return True  # Unknown pattern, assume valid

def analyze_behavioral_readiness(domain, model_name):
    """Analyze how ready predictions are for behavioral validation"""
    
    print(f"\n=== Behavioral Readiness Analysis: {domain.upper()} - {model_name.upper()} ===")
    
    # Load ML results
    results_file = f'results/ml_testing/{domain}_{model_name}_results.csv'
    try:
        df = pd.read_csv(results_file)
    except FileNotFoundError:
        print(f"Results file not found: {results_file}")
        return None
    
    print(f"Total predictions: {len(df)}")
    print(f"Correct predictions: {df['correct'].sum()} ({df['correct'].mean()*100:.1f}%)")
    
    # Validate consistency
    validation_df = validate_prediction_consistency(df)
    
    # Analysis
    has_commit = validation_df['has_commit_sha'].sum()
    has_file = validation_df['has_file_path'].sum()
    reasonable_lines = validation_df['reasonable_lines'].sum()
    reasonable_complexity = validation_df['reasonable_complexity'].sum()
    pattern_match = validation_df['pattern_match'].sum()
    
    print(f"\nData Quality:")
    print(f"  Valid commit SHAs: {has_commit}/{len(df)} ({has_commit/len(df)*100:.1f}%)")
    print(f"  Valid file paths: {has_file}/{len(df)} ({has_file/len(df)*100:.1f}%)")
    print(f"  Reasonable lines changed: {reasonable_lines}/{len(df)} ({reasonable_lines/len(df)*100:.1f}%)")
    print(f"  Reasonable complexity: {reasonable_complexity}/{len(df)} ({reasonable_complexity/len(df)*100:.1f}%)")
    print(f"  Pattern consistency: {pattern_match}/{len(df)} ({pattern_match/len(df)*100:.1f}%)")
    
    # Focus on correct predictions for behavioral validation
    correct_df = validation_df[validation_df['ml_correct'] == True]
    if len(correct_df) > 0:
        print(f"\nCorrect Predictions Analysis ({len(correct_df)} cases):")
        
        # Top refactoring types in correct predictions
        type_counts = correct_df['actual_type'].value_counts().head()
        print("  Most frequent correct predictions:")
        for ref_type, count in type_counts.items():
            print(f"    {ref_type}: {count} cases")
        
        # Behavioral validation readiness
        ready_for_validation = correct_df[
            (correct_df['has_commit_sha']) & 
            (correct_df['has_file_path']) & 
            (correct_df['reasonable_lines']) &
            (correct_df['pattern_match'])
        ]
        
        print(f"\nBehavioral Validation Ready: {len(ready_for_validation)}/{len(correct_df)} correct predictions")
        
        if len(ready_for_validation) > 0:
            print("  Sample cases ready for validation:")
            for idx, row in ready_for_validation.head(3).iterrows():
                print(f"    {row['actual_type']} - {row['commit_sha'][:8]}... - {row['file_path']}")
    
    return validation_df

def test_sample_commits(domain):
    """Test accessibility of sample commits"""
    
    repositories = {
        'commons_lang': 'https://github.com/apache/commons-lang.git',
        'spring': 'https://github.com/spring-projects/spring-framework.git',
        'kafka': 'https://github.com/apache/kafka.git',
        'intellij': 'https://github.com/JetBrains/intellij-community.git',
        'mockito': 'https://github.com/mockito/mockito.git'
    }
    
    if domain not in repositories:
        print(f"Unknown domain: {domain}")
        return
    
    # Load a sample of data
    try:
        df = pd.read_csv(f'data/{domain}_350_real_test.csv')
        sample_commits = df['commit_sha'].unique()[:3]
        
        print(f"\nTesting commit accessibility for {domain}:")
        repo_url = repositories[domain]
        
        for commit in sample_commits:
            accessible = test_commit_accessibility(commit, repo_url)
            status = "✓" if accessible else "✗"
            print(f"  {status} {commit}")
            
    except Exception as e:
        print(f"Error testing commits: {e}")

def main():
    # Test behavioral readiness for best performing models
    test_cases = [
        ('commons_lang', 'randomforest'),  # 91.4% accuracy
        ('intellij', 'logisticregression'),  # 63.2% accuracy
        ('spring', 'randomforest'),  # 48.6% accuracy
    ]
    
    all_results = {}
    
    for domain, model in test_cases:
        validation_df = analyze_behavioral_readiness(domain, model)
        if validation_df is not None:
            # Save detailed validation results
            output_file = f'results/behavioral_validation/{domain}_{model}_readiness.csv'
            validation_df.to_csv(output_file, index=False)
            print(f"✓ Saved readiness analysis: {output_file}")
            
            all_results[f"{domain}_{model}"] = validation_df
        
        # Test sample commit accessibility
        test_sample_commits(domain)
    
    # Overall summary
    print(f"\n{'='*60}")
    print("BEHAVIORAL VALIDATION READINESS SUMMARY")
    print(f"{'='*60}")
    
    for key, df in all_results.items():
        domain, model = key.split('_', 1)
        correct_predictions = df[df['ml_correct'] == True]
        ready_count = len(correct_predictions[
            (correct_predictions['has_commit_sha']) & 
            (correct_predictions['has_file_path']) & 
            (correct_predictions['reasonable_lines']) &
            (correct_predictions['pattern_match'])
        ])
        
        print(f"{domain.upper()} ({model}): {ready_count}/{len(correct_predictions)} correct predictions ready for behavioral validation")

if __name__ == "__main__":
    main()
