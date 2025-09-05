#!/usr/bin/env python3
"""
Behavioral validation for correct predictions
"""

import csv
import json
import subprocess
import shutil
import os
from pathlib import Path

MOCKITO_PATH = "/Users/parjalrai/Workspace/mockito"

def load_correct_predictions():
    """Load correct predictions from test results"""
    correct_predictions = []
    with open('results/mockito_test_results.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['correct'] == 'True':
                correct_predictions.append(row)
    return correct_predictions

def load_behavioral_metadata():
    """Load behavioral metadata"""
    metadata = {}
    with open('data/mockito_behavioral_dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['file_path'], row['refactoring_type'])
            metadata[key] = row
    return metadata

def load_refactoring_json():
    """Load original RefactoringMiner JSON"""
    with open('data/mockito_refactorings.json', 'r') as f:
        return json.load(f)

def get_refactoring_details(prediction, metadata, json_data):
    """Get detailed refactoring info for behavioral validation"""
    
    key = (prediction['file_path'], prediction['refactoring_type'])
    if key not in metadata:
        return None
    
    meta = metadata[key]
    commit_idx = int(meta['commit_idx'])
    ref_idx = int(meta['refactoring_idx'])
    
    try:
        commit = json_data['commits'][commit_idx]
        refactoring = commit['refactorings'][ref_idx]
        return refactoring
    except (IndexError, KeyError):
        return None

def run_mockito_tests():
    """Run Mockito tests"""
    try:
        result = subprocess.run([
            './gradlew', 'test', '--no-daemon', '-q', '--continue'
        ], 
        cwd=MOCKITO_PATH,
        capture_output=True, 
        text=True, 
        timeout=300
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def apply_rename_method_refactoring(file_path, refactoring_details):
    """Apply rename method refactoring"""
    
    description = refactoring_details['description']
    
    # Extract method names from description
    if 'renamed to' not in description:
        return {'applied': False, 'reason': 'Cannot parse rename'}
    
    parts = description.split('renamed to')
    if len(parts) != 2:
        return {'applied': False, 'reason': 'Cannot parse rename parts'}
    
    # Extract old and new method names
    try:
        old_method = parts[0].split('public ')[-1].split('(')[0].strip()
        new_method = parts[1].split('public ')[-1].split('(')[0].strip()
    except:
        return {'applied': False, 'reason': 'Cannot extract method names'}
    
    # Backup file
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    
    try:
        # Read file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Reverse the refactoring (go back to old name)
        if f'public void {new_method}(' in content:
            content = content.replace(f'public void {new_method}(', f'public void {old_method}(')
            
            # Write reversed content
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {
                'applied': True,
                'backup_path': backup_path,
                'old_method': old_method,
                'new_method': new_method,
                'reversed': True
            }
        else:
            return {'applied': False, 'reason': f'Method {new_method} not found in file'}
            
    except Exception as e:
        # Restore backup on error
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
        return {'applied': False, 'reason': f'Error: {e}'}

def apply_forward_refactoring(file_path, reverse_result):
    """Apply the refactoring forward"""
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        old_method = reverse_result['old_method']
        new_method = reverse_result['new_method']
        
        # Apply forward refactoring
        if f'public void {old_method}(' in content:
            content = content.replace(f'public void {old_method}(', f'public void {new_method}(')
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {'applied': True}
        else:
            return {'applied': False, 'reason': f'Method {old_method} not found'}
            
    except Exception as e:
        return {'applied': False, 'reason': f'Error: {e}'}

def restore_file(file_path, backup_path):
    """Restore original file"""
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, file_path)
        os.remove(backup_path)

def behavioral_validation():
    """Run behavioral validation on correct predictions"""
    
    print("🚀 BEHAVIORAL VALIDATION")
    print("=" * 40)
    
    # Load data
    correct_predictions = load_correct_predictions()
    metadata = load_behavioral_metadata()
    json_data = load_refactoring_json()
    
    print(f"📊 Correct predictions to validate: {len(correct_predictions)}")
    
    # Baseline test
    print(f"\n🧪 Step 1: Baseline test run")
    baseline = run_mockito_tests()
    
    if not baseline['success']:
        print(f"❌ Baseline tests failed!")
        return
    
    print(f"✅ Baseline tests passed")
    
    # Validate each correct prediction
    results = []
    
    for i, prediction in enumerate(correct_predictions):
        print(f"\n🔍 Testing {i+1}/{len(correct_predictions)}: {prediction['refactoring_type']}")
        print(f"   File: {Path(prediction['file_path']).name}")
        
        # Get refactoring details
        refactoring_details = get_refactoring_details(prediction, metadata, json_data)
        
        if not refactoring_details:
            print(f"   ⚠️  No refactoring details found")
            results.append({
                'file_path': prediction['file_path'],
                'refactoring_type': prediction['refactoring_type'],
                'status': 'NO_DETAILS'
            })
            continue
        
        full_path = Path(MOCKITO_PATH) / prediction['file_path']
        
        if not full_path.exists():
            print(f"   ⚠️  File not found")
            results.append({
                'file_path': prediction['file_path'],
                'refactoring_type': prediction['refactoring_type'],
                'status': 'FILE_NOT_FOUND'
            })
            continue
        
        # Apply refactoring (only handle Rename Method for now)
        if prediction['refactoring_type'] == 'Rename Method':
            
            # Step 1: Reverse refactoring
            print(f"   ⏪ Reversing refactoring...")
            reverse_result = apply_rename_method_refactoring(str(full_path), refactoring_details)
            
            if not reverse_result['applied']:
                print(f"   ⚠️  Could not reverse: {reverse_result['reason']}")
                results.append({
                    'file_path': prediction['file_path'],
                    'refactoring_type': prediction['refactoring_type'],
                    'status': 'REVERSE_FAILED',
                    'reason': reverse_result['reason']
                })
                continue
            
            # Step 2: Apply forward refactoring
            print(f"   ⏩ Applying refactoring...")
            forward_result = apply_forward_refactoring(str(full_path), reverse_result)
            
            if not forward_result['applied']:
                print(f"   ⚠️  Could not apply forward: {forward_result['reason']}")
                restore_file(str(full_path), reverse_result['backup_path'])
                results.append({
                    'file_path': prediction['file_path'],
                    'refactoring_type': prediction['refactoring_type'],
                    'status': 'FORWARD_FAILED',
                    'reason': forward_result['reason']
                })
                continue
            
            # Step 3: Run tests
            print(f"   🧪 Running tests...")
            test_result = run_mockito_tests()
            
            # Step 4: Restore original
            restore_file(str(full_path), reverse_result['backup_path'])
            
            # Record result
            result = {
                'file_path': prediction['file_path'],
                'refactoring_type': prediction['refactoring_type'],
                'status': 'TESTED',
                'tests_passed': test_result['success'],
                'functionally_correct': test_result['success'],
                'old_method': reverse_result['old_method'],
                'new_method': reverse_result['new_method']
            }
            
            results.append(result)
            
            if test_result['success']:
                print(f"   ✅ Tests PASSED - Refactoring is functionally correct!")
            else:
                print(f"   ❌ Tests FAILED - Refactoring breaks functionality!")
        
        else:
            print(f"   ⚠️  Refactoring type not implemented yet")
            results.append({
                'file_path': prediction['file_path'],
                'refactoring_type': prediction['refactoring_type'],
                'status': 'NOT_IMPLEMENTED'
            })
    
    # Summary
    tested = [r for r in results if r['status'] == 'TESTED']
    if tested:
        passed = sum(1 for r in tested if r.get('functionally_correct', False))
        success_rate = (passed / len(tested)) * 100
        
        print(f"\n📊 BEHAVIORAL VALIDATION RESULTS:")
        print(f"   Correct predictions: {len(correct_predictions)}")
        print(f"   Refactorings tested: {len(tested)}")
        print(f"   Functionally correct: {passed}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for r in tested:
            status = "✅" if r.get('functionally_correct', False) else "❌"
            print(f"   {status} {r['refactoring_type']} - {Path(r['file_path']).name}")
            if r.get('old_method') and r.get('new_method'):
                print(f"      {r['old_method']} → {r['new_method']}")
    
    # Save results
    with open('results/behavioral_validation_results.csv', 'w', newline='') as f:
        if results:
            fieldnames = list(results[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\n💾 Results saved to: results/behavioral_validation_results.csv")
    
    return results

if __name__ == "__main__":
    behavioral_validation()
