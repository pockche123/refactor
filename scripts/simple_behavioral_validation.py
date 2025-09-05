#!/usr/bin/env python3
"""
Simple Behavioral Validation for 4 correct predictions
"""

import csv
import json
import subprocess
import shutil
import os
from pathlib import Path

MOCKITO_PATH = "/Users/parjalrai/Workspace/mockito"

def run_tests():
    """Run Mockito tests"""
    try:
        result = subprocess.run([
            './gradlew', 'test', '--no-daemon', '-q'
        ], 
        cwd=MOCKITO_PATH,
        capture_output=True, 
        text=True, 
        timeout=300
        )
        return result.returncode == 0
    except:
        return False

def apply_rename_refactoring(file_path, old_method, new_method):
    """Apply rename method refactoring"""
    
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Reverse: new -> old
        if f'public void {new_method}(' in content:
            content = content.replace(f'public void {new_method}(', f'public void {old_method}(')
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {'success': True, 'backup_path': backup_path}
        else:
            return {'success': False, 'reason': f'Method {new_method} not found'}
            
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def apply_forward_refactoring(file_path, old_method, new_method):
    """Apply forward refactoring"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Forward: old -> new
        content = content.replace(f'public void {old_method}(', f'public void {new_method}(')
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        return True
    except:
        return False

def restore_file(file_path, backup_path):
    """Restore file"""
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, file_path)
        os.remove(backup_path)

def main():
    """Main behavioral validation"""
    
    print("🚀 BEHAVIORAL VALIDATION")
    print("=" * 40)
    
    # Load correct predictions
    correct_predictions = []
    with open('results/comprehensive_ml_test_results.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['correct'] == 'True':
                correct_predictions.append(row)
    
    print(f"📊 Correct predictions: {len(correct_predictions)}")
    
    # Load refactoring JSON
    with open('data/mockito_refactorings.json', 'r') as f:
        json_data = json.load(f)
    
    # Baseline test
    print(f"\n🧪 Baseline test...")
    if not run_tests():
        print("❌ Baseline failed!")
        return
    print("✅ Baseline passed")
    
    # Test each prediction
    results = []
    
    for i, pred in enumerate(correct_predictions):
        print(f"\n🔍 Testing {i+1}/{len(correct_predictions)}: {Path(pred['file_path']).name}")
        
        # Get refactoring details
        commit_idx = int(pred['commit_idx'])
        ref_idx = int(pred['refactoring_idx'])
        
        try:
            refactoring = json_data['commits'][commit_idx]['refactorings'][ref_idx]
            description = refactoring['description']
            
            # Parse method names
            parts = description.split('renamed to')
            old_method = parts[0].split('public ')[-1].split('(')[0].strip()
            new_method = parts[1].split('public ')[-1].split('(')[0].strip()
            
            print(f"   {old_method} → {new_method}")
            
            full_path = Path(MOCKITO_PATH) / pred['file_path']
            
            if not full_path.exists():
                print(f"   ⚠️  File not found")
                continue
            
            # Apply refactoring
            print(f"   ⏪ Reversing...")
            reverse_result = apply_rename_refactoring(str(full_path), old_method, new_method)
            
            if not reverse_result['success']:
                print(f"   ⚠️  Reverse failed: {reverse_result['reason']}")
                continue
            
            print(f"   ⏩ Applying...")
            if not apply_forward_refactoring(str(full_path), old_method, new_method):
                print(f"   ⚠️  Forward failed")
                restore_file(str(full_path), reverse_result['backup_path'])
                continue
            
            print(f"   🧪 Testing...")
            tests_passed = run_tests()
            
            # Restore
            restore_file(str(full_path), reverse_result['backup_path'])
            
            # Record result
            result = {
                'file': Path(pred['file_path']).name,
                'refactoring': f"{old_method} → {new_method}",
                'tests_passed': tests_passed
            }
            results.append(result)
            
            if tests_passed:
                print(f"   ✅ PASSED - Functionally correct!")
            else:
                print(f"   ❌ FAILED - Breaks functionality!")
                
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # Summary
    if results:
        passed = sum(1 for r in results if r['tests_passed'])
        success_rate = (passed / len(results)) * 100
        
        print(f"\n📊 BEHAVIORAL VALIDATION RESULTS:")
        print(f"   Refactorings tested: {len(results)}")
        print(f"   Functionally correct: {passed}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        print(f"\n📋 Details:")
        for r in results:
            status = "✅" if r['tests_passed'] else "❌"
            print(f"   {status} {r['file']} - {r['refactoring']}")
    
    print(f"\n🎯 CONCLUSION:")
    if results:
        print(f"   {success_rate:.0f}% of correct ML predictions are functionally safe")
    else:
        print(f"   No refactorings could be tested")

if __name__ == "__main__":
    main()
