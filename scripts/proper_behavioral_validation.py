#!/usr/bin/env python3
"""
Proper Behavioral Validation - Real Java refactoring with reference tracking
"""

import os
import subprocess
import pandas as pd
import shutil
import joblib
from sklearn.model_selection import train_test_split
from proper_java_refactoring import apply_proper_refactoring_transformation, backup_project, restore_project

def get_correct_test_predictions():
    """Get only the correct predictions from the 26 Mockito test instances"""
    
    # Load Mockito dataset and recreate 70-30 split
    mockito_df = pd.read_csv('data/mockito_enhanced_dataset.csv')
    
    class_counts = mockito_df['refactoring_type'].value_counts()
    valid_classes = class_counts[class_counts >= 2].index
    df_filtered = mockito_df[mockito_df['refactoring_type'].isin(valid_classes)]
    
    train_df, test_df = train_test_split(
        df_filtered, 
        test_size=0.3, 
        random_state=42, 
        stratify=df_filtered['refactoring_type']
    )
    
    # Load model and make predictions
    model = joblib.load('models/complete_mixed_domain_classifier.pkl')
    
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X_test = test_df[feature_cols].fillna(0)
    predictions = model.predict(X_test)
    
    test_df = test_df.copy()
    test_df['predicted_refactoring'] = predictions
    
    # Filter for CORRECT predictions only
    correct_predictions = test_df[test_df['refactoring_type'] == test_df['predicted_refactoring']]
    
    print(f"📊 Mockito Test Set Analysis:")
    print(f"   Test instances: {len(test_df)}")
    print(f"   Accuracy: {len(correct_predictions)/len(test_df)*100:.1f}%")
    print(f"   Correct predictions: {len(correct_predictions)}")
    
    print(f"\n✅ Correct Predictions by Type:")
    for reftype, count in correct_predictions['refactoring_type'].value_counts().items():
        print(f"   {reftype}: {count}")
    
    # Filter for implementable types with proper refactoring - now all 8!
    implementable_types = ['Rename Method', 'Rename Variable', 'Add Method Annotation', 'Change Return Type',
                          'Move Class', 'Extract Method', 'Change Attribute Type']
    implementable_correct = correct_predictions[correct_predictions['refactoring_type'].isin(implementable_types)]
    
    print(f"\n🔧 Implementable with Proper Refactoring: {len(implementable_correct)}")
    if len(implementable_correct) > 0:
        for reftype, count in implementable_correct['refactoring_type'].value_counts().items():
            print(f"   {reftype}: {count}")
    
    return implementable_correct

def setup_proper_workspace():
    """Setup workspace for proper refactoring"""
    
    workspace_dir = 'behavioral_validation/proper_refactoring_workspace'
    
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
    
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Copy Mockito project
    source_dir = 'complex_projects/mockito'
    target_dir = os.path.join(workspace_dir, 'mockito')
    
    if not os.path.exists(source_dir):
        print(f"❌ Mockito project not found")
        return None
    
    print(f"📁 Setting up proper refactoring workspace...")
    shutil.copytree(source_dir, target_dir)
    
    return target_dir

def run_test_suite(project_dir, test_name="baseline"):
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
        
        success = result.returncode == 0
        
        return {
            'success': success,
            'return_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print(f"⚠️  {test_name} tests timed out")
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        print(f"❌ Error running {test_name} tests: {e}")
        return {'success': False, 'error': str(e)}

def validate_proper_refactoring(project_dir, refactoring_info, baseline_results):
    """Apply proper refactoring and validate functionality"""
    
    refactoring_type = refactoring_info['refactoring_type']
    file_path = refactoring_info['file_path']
    full_file_path = os.path.join(project_dir, file_path)
    
    print(f"\n🎯 Applying PROPER {refactoring_type} to {file_path}")
    
    # Create backup of entire project (not just one file)
    backup_dir = backup_project(project_dir)
    
    try:
        # Apply proper refactoring with project-wide reference tracking
        success, result = apply_proper_refactoring_transformation(full_file_path, refactoring_type, project_dir)
        
        if not success:
            restore_project(project_dir, backup_dir)
            print(f"❌ Proper refactoring failed: {result}")
            return {'success': False, 'transformation_applied': False, 'error': result}
        
        print(f"✅ Applied proper refactoring: {result}")
        
        # Test functionality after proper refactoring
        print(f"🧪 Testing functionality after PROPER refactoring...")
        post_refactoring_results = run_test_suite(project_dir, "post-proper-refactoring")
        
        # Compare results
        baseline_success = baseline_results.get('success', False)
        post_success = post_refactoring_results.get('success', False)
        
        maintained_correctness = (baseline_success == post_success)
        
        validation_result = {
            'success': True,
            'transformation_applied': True,
            'transformation_details': result,
            'baseline_passed': baseline_success,
            'post_refactoring_passed': post_success,
            'maintained_correctness': maintained_correctness,
            'refactoring_method': 'proper_java_refactoring'
        }
        
        if maintained_correctness:
            print(f"✅ Proper refactoring maintained functionality")
        else:
            print(f"❌ Even proper refactoring broke functionality")
            print(f"   Baseline: {'PASS' if baseline_success else 'FAIL'}")
            print(f"   After proper refactoring: {'PASS' if post_success else 'FAIL'}")
        
        # Restore project for next test
        restore_project(project_dir, backup_dir)
        
        return validation_result
        
    except Exception as e:
        # Restore on any error
        restore_project(project_dir, backup_dir)
        return {'success': False, 'transformation_applied': False, 'error': str(e)}

def main():
    """Execute proper behavioral validation"""
    
    print("🎯 PROPER BEHAVIORAL VALIDATION")
    print("Using real Java refactoring with reference tracking")
    print("=" * 70)
    
    # Get correct predictions
    correct_predictions = get_correct_test_predictions()
    
    if len(correct_predictions) == 0:
        print("❌ No implementable correct predictions found")
        return
    
    # Setup workspace
    project_dir = setup_proper_workspace()
    if project_dir is None:
        return
    
    # Run baseline tests
    print(f"\n📊 Establishing baseline...")
    baseline_results = run_test_suite(project_dir, "baseline")
    
    if not baseline_results.get('success'):
        print(f"❌ Baseline tests failed - cannot proceed")
        return
    
    print(f"✅ Baseline established")
    
    # Test all correct predictions with proper refactoring
    print(f"\n🔧 Testing {len(correct_predictions)} CORRECT predictions with PROPER refactoring...")
    
    validation_results = []
    
    for idx, refactoring in correct_predictions.iterrows():
        print(f"\n--- Proper Refactoring {len(validation_results) + 1}/{len(correct_predictions)} ---")
        
        # Apply proper refactoring
        result = validate_proper_refactoring(project_dir, refactoring, baseline_results)
        
        # Record results for successfully applied transformations
        if result.get('transformation_applied', False):
            result_record = {
                'index': idx,
                'refactoring_type': refactoring['refactoring_type'],
                'file_path': refactoring['file_path'],
                'transformation_applied': True,
                'maintained_correctness': result.get('maintained_correctness', False),
                'baseline_passed': result.get('baseline_passed', False),
                'post_refactoring_passed': result.get('post_refactoring_passed', False),
                'transformation_details': result.get('transformation_details', {}),
                'method': 'proper_java_refactoring'
            }
            
            validation_results.append(result_record)
            
            status = "✅ SAFE" if result.get('maintained_correctness') else "❌ UNSAFE"
            print(f"   Result: {status}")
        else:
            print(f"   Result: ⏭️  SKIPPED (transformation failed)")
    
    # Analysis
    print(f"\n📊 PROPER REFACTORING BEHAVIORAL VALIDATION")
    print("=" * 70)
    
    total_tested = len(validation_results)
    safe_count = sum(1 for r in validation_results if r['maintained_correctness'])
    
    print(f"Correct predictions tested with proper refactoring: {total_tested}")
    print(f"Functionally safe: {safe_count}")
    print(f"Functionally unsafe: {total_tested - safe_count}")
    
    if total_tested > 0:
        safety_rate = (safe_count / total_tested) * 100
        print(f"Safety rate with PROPER refactoring: {safety_rate:.1f}%")
    
    # Detailed breakdown
    print(f"\nDetailed Results:")
    for result in validation_results:
        status = "✅ SAFE" if result['maintained_correctness'] else "❌ UNSAFE"
        transformation = result['transformation_details']
        if 'old_name' in transformation and 'new_name' in transformation:
            details = f"{transformation['old_name']} → {transformation['new_name']}"
        else:
            details = transformation.get('type', 'Unknown')
        print(f"  {status} {result['refactoring_type']}: {details}")
    
    # Save results
    results_df = pd.DataFrame(validation_results)
    results_file = 'results/proper_refactoring_validation.csv'
    os.makedirs('results', exist_ok=True)
    results_df.to_csv(results_file, index=False)
    print(f"\n💾 Results saved to {results_file}")
    
    print(f"\n🎯 KEY THESIS FINDING:")
    if total_tested > 0:
        print(f"With PROPER Java refactoring (handling references):")
        print(f"• {safety_rate:.1f}% of correct ML predictions are functionally safe")
        print(f"• {100-safety_rate:.1f}% still break functionality despite proper tooling")
        print(f"This shows the impact of sophisticated refactoring tools vs naive transformations.")
    else:
        print("No correct predictions could be tested with proper refactoring.")

if __name__ == "__main__":
    main()
