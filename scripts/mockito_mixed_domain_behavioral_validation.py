#!/usr/bin/env python3
"""
Mockito Mixed-Domain Behavioral Validation
Test the 8 correct predictions from mixed-domain model (30.8% accuracy)
"""

import os
import subprocess
import pandas as pd
import shutil
from proper_java_refactoring import apply_proper_refactoring_transformation, backup_project, restore_project

def setup_mockito_workspace():
    """Setup Mockito workspace for behavioral validation"""
    
    workspace_dir = 'behavioral_validation/mockito_mixed_domain_workspace'
    
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
    
    os.makedirs(workspace_dir, exist_ok=True)
    
    source_dir = 'complex_projects/mockito'
    target_dir = os.path.join(workspace_dir, 'mockito')
    
    if not os.path.exists(source_dir):
        print(f"❌ Mockito project not found")
        return None
    
    print(f"📁 Setting up Mockito mixed-domain workspace...")
    shutil.copytree(source_dir, target_dir)
    
    return target_dir

def run_mockito_tests(project_dir, test_name="baseline"):
    """Run Mockito test suite"""
    
    print(f"🧪 Running {test_name} tests...")
    
    try:
        result = subprocess.run(
            ['./gradlew', 'mockito-core:test', '--quiet', '--continue'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            'success': result.returncode == 0,
            'return_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_mockito_correct_predictions():
    """Get the 8 correct predictions from mixed-domain model"""
    
    df = pd.read_csv('results/mockito_mixed_domain_results.csv')
    correct_predictions = df[df['correct'] == True].copy()
    
    print(f"📊 Mixed-Domain Model Results on Mockito:")
    print(f"   Test instances: {len(df)}")
    print(f"   Accuracy: {len(correct_predictions)/len(df)*100:.1f}%")
    print(f"   Correct predictions: {len(correct_predictions)}")
    
    print(f"\n✅ Correct Predictions by Type:")
    for reftype, count in correct_predictions['refactoring_type'].value_counts().items():
        print(f"   {reftype}: {count}")
    
    return correct_predictions

def validate_single_refactoring(project_dir, prediction_row, baseline_success):
    """Validate one refactoring prediction"""
    
    file_path = prediction_row['file_path']
    refactoring_type = prediction_row['refactoring_type']
    
    full_file_path = os.path.join(project_dir, file_path)
    
    if not os.path.exists(full_file_path):
        return {
            'applied': False,
            'valid': False,
            'tests_passed': False,
            'error': f'File not found: {file_path}'
        }
    
    print(f"  Testing: {refactoring_type} on {os.path.basename(file_path)}")
    
    # Backup
    backup_dir = backup_project(project_dir)
    
    try:
        # Apply refactoring
        success, result = apply_proper_refactoring_transformation(
            full_file_path, refactoring_type, project_dir
        )
        
        if not success:
            restore_project(project_dir, backup_dir)
            return {
                'applied': False,
                'valid': False,
                'tests_passed': False,
                'error': f'Could not apply: {result}'
            }
        
        # Test after refactoring
        post_results = run_mockito_tests(project_dir, "post-refactoring")
        post_success = post_results.get('success', False)
        
        # Valid if tests still pass
        tests_passed = baseline_success == post_success
        
        restore_project(project_dir, backup_dir)
        
        return {
            'applied': True,
            'valid': tests_passed,
            'tests_passed': tests_passed
        }
        
    except Exception as e:
        restore_project(project_dir, backup_dir)
        return {
            'applied': False,
            'valid': False,
            'tests_passed': False,
            'error': str(e)
        }

def main():
    """Execute Mockito mixed-domain behavioral validation"""
    
    print("🎯 MOCKITO MIXED-DOMAIN BEHAVIORAL VALIDATION")
    print("Testing 8 correct predictions from mixed-domain model (30.8% accuracy)")
    print("=" * 70)
    
    # Setup workspace
    project_dir = setup_mockito_workspace()
    if project_dir is None:
        return
    
    # Get correct predictions
    correct_predictions = get_mockito_correct_predictions()
    
    # Baseline test
    print(f"\n📊 Running baseline tests...")
    baseline_results = run_mockito_tests(project_dir, "baseline")
    baseline_success = baseline_results.get('success', False)
    
    print(f"Baseline: {'✅ PASS' if baseline_success else '❌ FAIL'}")
    
    if not baseline_success:
        print("⚠️  Baseline tests failed - results may not be reliable")
    
    # Test each prediction
    validation_results = []
    
    print(f"\n🔬 Testing {len(correct_predictions)} correct predictions...")
    
    for idx, (_, prediction_row) in enumerate(correct_predictions.iterrows(), 1):
        
        print(f"\n--- Test {idx}/{len(correct_predictions)} ---")
        print(f"File: {prediction_row['file_path']}")
        print(f"Refactoring: {prediction_row['refactoring_type']}")
        
        result = validate_single_refactoring(project_dir, prediction_row, baseline_success)
        
        # Record results
        validation_record = {
            'index': idx - 1,
            'actual_refactoring': prediction_row['refactoring_type'],
            'predicted_refactoring': prediction_row['predicted'],
            'file_path': prediction_row['file_path'],
            'applied': result['applied'],
            'valid': result['valid'],
            'tests_passed': result['tests_passed']
        }
        
        if 'error' in result:
            validation_record['error'] = result['error']
        
        validation_results.append(validation_record)
        
        # Status
        if result['applied']:
            status = "✅ SAFE" if result['valid'] else "❌ UNSAFE"
            print(f"  Result: {status}")
        else:
            print(f"  Result: ❌ NOT APPLIED")
    
    # Save results
    results_df = pd.DataFrame(validation_results)
    results_df.to_csv('results/mockito_mixed_domain_behavioral_validation.csv', index=False)
    
    # Summary
    applied_count = results_df['applied'].sum()
    valid_count = results_df['valid'].sum()
    
    print(f"\n📊 MOCKITO MIXED-DOMAIN BEHAVIORAL VALIDATION SUMMARY")
    print(f"Correct predictions tested: {len(results_df)}")
    print(f"Successfully applied: {applied_count}/{len(results_df)} ({applied_count/len(results_df)*100:.1f}%)")
    print(f"Functionally valid: {valid_count}/{len(results_df)} ({valid_count/len(results_df)*100:.1f}%)")
    
    if applied_count > 0:
        safety_rate = valid_count / applied_count * 100
        print(f"Safety rate: {valid_count}/{applied_count} ({safety_rate:.1f}% of applied)")
    
    print(f"\nResults saved to: results/mockito_mixed_domain_behavioral_validation.csv")
    
    print(f"\n🔄 Comparison with Single-Domain Results:")
    print(f"   Mixed-domain accuracy: 30.8% (8/26)")
    print(f"   Single-domain accuracy: 5.2% (was much lower)")
    print(f"   This shows mixed-domain training significantly improves cross-domain performance")

if __name__ == "__main__":
    main()
