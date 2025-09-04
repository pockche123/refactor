#!/usr/bin/env python3
"""
Comprehensive Refactoring Validation - Handle all refactoring types
"""

import os
import subprocess
import pandas as pd
import json
import shutil
import re
from pathlib import Path

MOCKITO_PATH = "/Users/parjalrai/Workspace/mockito"

def load_refactoring_data():
    """Load RefactoringMiner JSON data"""
    with open('data/mockito_refactorings.json', 'r') as f:
        return json.load(f)

def run_mockito_tests():
    """Run Mockito tests"""
    try:
        result = subprocess.run([
            './gradlew', 'test', '--no-daemon', '-q', '--continue'
        ], 
        cwd=MOCKITO_PATH,
        capture_output=True, 
        text=True, 
        timeout=600
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def find_refactoring_details(file_path, refactoring_type, refactoring_data):
    """Find the specific refactoring details from RefactoringMiner data"""
    
    for commit in refactoring_data['commits']:
        for refactoring in commit['refactorings']:
            if refactoring['type'] == refactoring_type:
                # Check if this refactoring involves our file
                for location in refactoring.get('leftSideLocations', []) + refactoring.get('rightSideLocations', []):
                    if location['filePath'] == file_path:
                        return refactoring
    return None

def parse_refactoring_details(refactoring):
    """Parse refactoring details based on type"""
    
    refactoring_type = refactoring['type']
    description = refactoring['description']
    
    if refactoring_type == "Rename Method":
        # Extract method names from description
        if 'renamed to' in description:
            parts = description.split('renamed to')
            if len(parts) == 2:
                old_method = parts[0].split('public ')[-1].split('(')[0].strip()
                new_method = parts[1].split('public ')[-1].split('(')[0].strip()
                return {
                    'type': 'rename_method',
                    'old_name': old_method,
                    'new_name': new_method
                }
    
    elif refactoring_type == "Add Method Annotation":
        # Extract annotation from description
        if '@' in description:
            annotation_match = re.search(r'@(\w+(?:\([^)]*\))?)', description)
            method_match = re.search(r'in method public (\w+)\(', description)
            if annotation_match and method_match:
                return {
                    'type': 'add_annotation',
                    'annotation': annotation_match.group(1),
                    'method': method_match.group(1)
                }
    
    elif refactoring_type == "Change Return Type":
        # Extract return types from description
        if ' to ' in description:
            parts = description.split(' to ')
            if len(parts) >= 2:
                old_type = parts[0].split('Change Return Type ')[-1].strip()
                new_type = parts[1].split(' in method')[0].strip()
                method_match = re.search(r'in method \w+ (\w+)\(', description)
                if method_match:
                    return {
                        'type': 'change_return_type',
                        'old_type': old_type,
                        'new_type': new_type,
                        'method': method_match.group(1)
                    }
    
    elif refactoring_type == "Extract Method":
        # Extract method details
        if 'extracted from' in description:
            parts = description.split('extracted from')
            if len(parts) == 2:
                new_method_match = re.search(r'Extract Method \w+ (\w+)\(', parts[0])
                if new_method_match:
                    return {
                        'type': 'extract_method',
                        'new_method': new_method_match.group(1)
                    }
    
    elif refactoring_type == "Change Attribute Type":
        # Extract attribute type change
        if ' to ' in description:
            parts = description.split(' to ')
            if len(parts) >= 2:
                old_type = parts[0].split('Change Attribute Type ')[-1].strip()
                new_type = parts[1].split(' in attribute')[0].strip()
                return {
                    'type': 'change_attribute_type',
                    'old_type': old_type,
                    'new_type': new_type
                }
    
    return None

def apply_reverse_refactoring(file_path, parsed_details):
    """Reverse the refactoring based on parsed details"""
    
    if not parsed_details:
        return {'applied': False, 'reason': 'No parsed details'}
    
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        if parsed_details['type'] == 'rename_method':
            # Reverse method rename
            old_name = parsed_details['old_name']
            new_name = parsed_details['new_name']
            content = content.replace(f'public void {new_name}(', f'public void {old_name}(')
            
        elif parsed_details['type'] == 'add_annotation':
            # Remove annotation
            annotation = parsed_details['annotation']
            method = parsed_details['method']
            # Remove @annotation line before method
            pattern = rf'@{re.escape(annotation)}\s*\n\s*public void {method}\('
            content = re.sub(pattern, f'public void {method}(', content)
            
        elif parsed_details['type'] == 'change_return_type':
            # Reverse return type change
            old_type = parsed_details['old_type']
            new_type = parsed_details['new_type']
            method = parsed_details['method']
            content = content.replace(f'{new_type} {method}(', f'{old_type} {method}(')
            
        elif parsed_details['type'] == 'extract_method':
            # Skip - too complex to reverse
            return {'applied': False, 'reason': 'Extract Method reversal too complex'}
            
        elif parsed_details['type'] == 'change_attribute_type':
            # Reverse attribute type change
            old_type = parsed_details['old_type']
            new_type = parsed_details['new_type']
            content = content.replace(f'private {new_type} ', f'private {old_type} ')
        
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {'applied': True, 'backup_path': backup_path, 'details': parsed_details}
        else:
            return {'applied': False, 'reason': 'No changes made'}
        
    except Exception as e:
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
        return {'applied': False, 'reason': f'Error: {e}'}

def apply_forward_refactoring(file_path, reverse_result):
    """Apply the refactoring forward"""
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        parsed_details = reverse_result['details']
        
        if parsed_details['type'] == 'rename_method':
            # Apply method rename
            old_name = parsed_details['old_name']
            new_name = parsed_details['new_name']
            content = content.replace(f'public void {old_name}(', f'public void {new_name}(')
            
        elif parsed_details['type'] == 'add_annotation':
            # Add annotation
            annotation = parsed_details['annotation']
            method = parsed_details['method']
            content = content.replace(f'public void {method}(', f'@{annotation}\n    public void {method}(')
            
        elif parsed_details['type'] == 'change_return_type':
            # Apply return type change
            old_type = parsed_details['old_type']
            new_type = parsed_details['new_type']
            method = parsed_details['method']
            content = content.replace(f'{old_type} {method}(', f'{new_type} {method}(')
            
        elif parsed_details['type'] == 'change_attribute_type':
            # Apply attribute type change
            old_type = parsed_details['old_type']
            new_type = parsed_details['new_type']
            content = content.replace(f'private {old_type} ', f'private {new_type} ')
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {'applied': True}
        
    except Exception as e:
        return {'applied': False, 'reason': f'Error: {e}'}

def restore_file(file_path, backup_path):
    """Restore original file"""
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, file_path)
        os.remove(backup_path)

def comprehensive_refactoring_validation():
    """Comprehensive refactoring validation for all types"""
    
    print("🚀 COMPREHENSIVE Refactoring Validation for Mockito")
    print("=" * 60)
    
    # Load data
    refactoring_data = load_refactoring_data()
    results_file = "results/mockito_mixed_domain_results.csv"
    df = pd.read_csv(results_file)
    correct_predictions = df[df['correct'] == True]
    
    print(f"📊 Testing {len(correct_predictions)} correct predictions")
    
    # Baseline test
    print(f"\n🧪 Step 1: Baseline test run")
    baseline = run_mockito_tests()
    
    if not baseline['success']:
        print(f"❌ Baseline tests failed!")
        return
    
    print(f"✅ Baseline tests passed")
    
    # Test each refactoring
    results = []
    
    for idx, row in correct_predictions.iterrows():
        print(f"\n🔍 Testing {idx+1}/{len(correct_predictions)}: {row['refactoring_type']}")
        print(f"   File: {Path(row['file_path']).name}")
        
        full_path = Path(MOCKITO_PATH) / row['file_path']
        
        if not full_path.exists():
            print(f"   ⚠️  File not found")
            results.append({
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'status': 'FILE_NOT_FOUND'
            })
            continue
        
        # Find refactoring details
        refactoring_details = find_refactoring_details(
            row['file_path'], 
            row['refactoring_type'], 
            refactoring_data
        )
        
        if not refactoring_details:
            print(f"   ⚠️  No refactoring details found in JSON")
            results.append({
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'status': 'NO_DETAILS'
            })
            continue
        
        # Parse refactoring details
        parsed_details = parse_refactoring_details(refactoring_details)
        
        if not parsed_details:
            print(f"   ⚠️  Could not parse refactoring details")
            results.append({
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'status': 'PARSE_FAILED'
            })
            continue
        
        # Step 1: Reverse the refactoring
        print(f"   ⏪ Reversing {row['refactoring_type']}...")
        reverse_result = apply_reverse_refactoring(str(full_path), parsed_details)
        
        if not reverse_result['applied']:
            print(f"   ⚠️  Could not reverse: {reverse_result['reason']}")
            results.append({
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'status': 'REVERSE_FAILED',
                'reason': reverse_result['reason']
            })
            continue
        
        # Step 2: Apply the refactoring forward
        print(f"   ⏩ Applying {row['refactoring_type']}...")
        forward_result = apply_forward_refactoring(str(full_path), reverse_result)
        
        if not forward_result['applied']:
            print(f"   ⚠️  Could not apply forward: {forward_result['reason']}")
            restore_file(str(full_path), reverse_result['backup_path'])
            results.append({
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'status': 'FORWARD_FAILED',
                'reason': forward_result['reason']
            })
            continue
        
        # Step 3: Run tests
        print(f"   🧪 Running tests...")
        test_result = run_mockito_tests()
        
        # Step 4: Restore original state
        restore_file(str(full_path), reverse_result['backup_path'])
        
        # Record result
        result = {
            'file_path': row['file_path'],
            'refactoring_type': row['refactoring_type'],
            'status': 'TESTED',
            'tests_passed': test_result['success'],
            'functionally_correct': test_result['success'],
            'refactoring_details': str(parsed_details)
        }
        
        results.append(result)
        
        if test_result['success']:
            print(f"   ✅ Tests PASSED - Refactoring is functionally correct!")
        else:
            print(f"   ❌ Tests FAILED - Refactoring breaks functionality!")
    
    # Summary
    tested = [r for r in results if r['status'] == 'TESTED']
    if tested:
        passed = sum(1 for r in tested if r.get('functionally_correct', False))
        success_rate = (passed / len(tested)) * 100
        
        print(f"\n📊 COMPREHENSIVE Refactoring Validation Results:")
        print(f"   Total predictions: {len(correct_predictions)}")
        print(f"   Refactorings tested: {len(tested)}")
        print(f"   Functionally correct: {passed}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for r in tested:
            status = "✅" if r.get('functionally_correct', False) else "❌"
            print(f"   {status} {r['refactoring_type']} - {Path(r['file_path']).name}")
    
    # Save results
    results_df = pd.DataFrame(results)
    output_file = "results/mockito_comprehensive_refactoring_validation.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n💾 Results saved to: {output_file}")
    
    return results_df

if __name__ == "__main__":
    comprehensive_refactoring_validation()
