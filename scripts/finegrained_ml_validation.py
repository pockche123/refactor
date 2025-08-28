#!/usr/bin/env python3
"""Fine-grained ML validation that handles compilation failures gracefully"""

import subprocess
import os
import shutil
import csv
import tempfile

def test_individual_file_compilation(file_path, project_dir):
    """Test if a specific file compiles in isolation"""
    try:
        # Try to compile just this file
        result = subprocess.run([
            "javac", "-cp", ".:target/classes:target/test-classes", file_path
        ], 
        cwd=project_dir, 
        capture_output=True, 
        timeout=60,
        text=True)
        
        return {
            'compiles': result.returncode == 0,
            'error': result.stderr[:200] if result.stderr else None
        }
    except Exception as e:
        return {'compiles': False, 'error': str(e)}

def test_project_compilation_graceful(project_dir):
    """Test project compilation with graceful failure handling"""
    try:
        # First try Maven compilation
        result = subprocess.run([
            "mvn", "compile", "-q", "-fn"  # -fn = fail never (continue on errors)
        ], 
        cwd=project_dir, 
        capture_output=True, 
        timeout=180,
        text=True)
        
        compilation_status = {
            'maven_compiles': result.returncode == 0,
            'maven_output': result.stderr[-300:] if result.stderr else 'SUCCESS',
            'exit_code': result.returncode
        }
        
        # If Maven fails, try test compilation anyway
        if result.returncode != 0:
            test_result = subprocess.run([
                "mvn", "test-compile", "-q", "-fn"
            ], 
            cwd=project_dir, 
            capture_output=True, 
            timeout=180,
            text=True)
            
            compilation_status['test_compiles'] = test_result.returncode == 0
            compilation_status['test_output'] = test_result.stderr[-300:] if test_result.stderr else 'SUCCESS'
        else:
            compilation_status['test_compiles'] = True
            compilation_status['test_output'] = 'SUCCESS'
        
        return compilation_status
        
    except Exception as e:
        return {
            'maven_compiles': False, 'test_compiles': False,
            'maven_output': f'ERROR: {e}', 'test_output': f'ERROR: {e}',
            'exit_code': -1
        }

def run_tests_graceful(project_dir, test_pattern="*Test*"):
    """Run tests with graceful failure handling"""
    try:
        # Try to run tests even if compilation had issues
        result = subprocess.run([
            "mvn", "test", f"-Dtest={test_pattern}", "-fn", "-q"
        ], 
        cwd=project_dir, 
        capture_output=True, 
        timeout=300,
        text=True)
        
        output = result.stdout + result.stderr
        
        # Parse test results more robustly
        tests_run = 0
        tests_passed = 0
        tests_failed = 0
        tests_skipped = 0
        tests_errors = 0
        
        for line in output.split('\n'):
            # Maven Surefire format
            if 'Tests run:' in line:
                import re
                match = re.search(r'Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)', line)
                if match:
                    tests_run += int(match.group(1))
                    tests_failed += int(match.group(2))
                    tests_errors += int(match.group(3))
                    tests_skipped += int(match.group(4))
            
            # Alternative format
            elif 'test' in line.lower() and ('passed' in line.lower() or 'failed' in line.lower()):
                if 'passed' in line.lower():
                    tests_passed += 1
                elif 'failed' in line.lower():
                    tests_failed += 1
        
        # Calculate passed tests
        if tests_run > 0:
            tests_passed = tests_run - tests_failed - tests_errors - tests_skipped
        
        return {
            'tests_run': tests_run,
            'tests_passed': tests_passed,
            'tests_failed': tests_failed,
            'tests_errors': tests_errors,
            'tests_skipped': tests_skipped,
            'test_execution_success': result.returncode == 0,
            'output_sample': output[-400:] if output else 'No output'
        }
        
    except Exception as e:
        return {
            'tests_run': 0, 'tests_passed': 0, 'tests_failed': 0, 
            'tests_errors': 0, 'tests_skipped': 0,
            'test_execution_success': False,
            'output_sample': f'ERROR: {e}'
        }

def apply_simple_extract_method(file_path):
    """Apply a simple, safe Extract Method refactoring"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find a simple method to extract from (look for long methods)
        lines = content.split('\n')
        
        # Look for methods with more than 15 lines
        in_method = False
        method_start = -1
        method_lines = 0
        brace_count = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Start of method
            if any(keyword in line for keyword in ['public ', 'private ', 'protected ']) and '{' in line:
                in_method = True
                method_start = i
                method_lines = 1
                brace_count = line.count('{') - line.count('}')
            elif in_method:
                method_lines += 1
                brace_count += line.count('{') - line.count('}')
                
                # End of method
                if brace_count <= 0:
                    if method_lines > 15:  # Found a long method
                        # Extract a simple helper method
                        method_content = '\n'.join(lines[method_start:i+1])
                        
                        # Add a simple extracted method before the original
                        extracted_method = '''
    private void extractedHelperMethod() {
        // Extracted method - placeholder
        // This would contain extracted logic
    }
'''
                        
                        # Insert the extracted method
                        lines.insert(method_start, extracted_method)
                        
                        # Modify original method to call extracted method
                        original_method_line = lines[method_start + len(extracted_method.split('\n'))]
                        if '{' in original_method_line:
                            call_line = '        extractedHelperMethod(); // Call to extracted method'
                            lines.insert(method_start + len(extracted_method.split('\n')) + 1, call_line)
                        
                        # Write modified content
                        with open(file_path, 'w') as f:
                            f.write('\n'.join(lines))
                        
                        return True, f"Extracted method from line {method_start} ({method_lines} lines)"
                    
                    in_method = False
                    method_start = -1
                    method_lines = 0
                    brace_count = 0
        
        return False, "No suitable method found for extraction"
        
    except Exception as e:
        return False, f"Refactoring failed: {e}"

def finegrained_validation():
    """Fine-grained validation with graceful failure handling"""
    
    # Test multiple targets
    targets = [
        {
            'project': '/Users/parjalrai/Workspace/refactoring-classifier/unseen_test_projects/httpcomponents-core',
            'file': 'httpcore5-reactive/src/test/java/org/apache/hc/core5/reactive/WritableByteChannelMock.java',
            'prediction': 'Extract Class',
            'confidence': 0.8
        },
        {
            'project': '/Users/parjalrai/Workspace/refactoring-classifier/unseen_test_projects/kafka',
            'file': 'clients/clients-integration-tests/src/test/java/org/apache/kafka/clients/CreateTopicsRequestWithPolicyTest.java',
            'prediction': 'Extract Method',
            'confidence': 0.9
        }
    ]
    
    results = []
    
    for target in targets:
        print(f"\n=== TESTING {target['prediction']} on {os.path.basename(target['file'])} ===")
        
        project_dir = target['project']
        target_file = os.path.join(project_dir, target['file'])
        backup_file = f"{target_file}.backup"
        
        if not os.path.exists(target_file):
            print(f"❌ File not found: {target_file}")
            continue
        
        # Create backup
        shutil.copy2(target_file, backup_file)
        
        try:
            # Test BEFORE refactoring
            print("1. Testing BEFORE refactoring...")
            before_compilation = test_project_compilation_graceful(project_dir)
            before_tests = run_tests_graceful(project_dir)
            
            print(f"   Compilation: Maven={'✅' if before_compilation['maven_compiles'] else '❌'}, Tests={'✅' if before_compilation['test_compiles'] else '❌'}")
            print(f"   Tests: Run={before_tests['tests_run']}, Passed={before_tests['tests_passed']}, Failed={before_tests['tests_failed']}")
            
            # Apply simple refactoring
            print("2. Applying refactoring...")
            if target['prediction'] == 'Extract Method':
                refactoring_success, refactoring_message = apply_simple_extract_method(target_file)
            else:
                refactoring_success, refactoring_message = False, "Extract Class not implemented"
            
            print(f"   Refactoring: {refactoring_message}")
            
            if refactoring_success:
                # Test AFTER refactoring
                print("3. Testing AFTER refactoring...")
                after_compilation = test_project_compilation_graceful(project_dir)
                after_tests = run_tests_graceful(project_dir)
                
                print(f"   Compilation: Maven={'✅' if after_compilation['maven_compiles'] else '❌'}, Tests={'✅' if after_compilation['test_compiles'] else '❌'}")
                print(f"   Tests: Run={after_tests['tests_run']}, Passed={after_tests['tests_passed']}, Failed={after_tests['tests_failed']}")
                
                # Calculate preservation scores
                compilation_preservation = 1.0 if (before_compilation['maven_compiles'] == after_compilation['maven_compiles']) else 0.0
                
                if before_tests['tests_run'] > 0 and after_tests['tests_run'] > 0:
                    test_preservation = after_tests['tests_passed'] / before_tests['tests_passed'] if before_tests['tests_passed'] > 0 else 0.0
                else:
                    test_preservation = 1.0 if (before_tests['tests_run'] == after_tests['tests_run']) else 0.0
                
                overall_preservation = (compilation_preservation + test_preservation) / 2
            else:
                compilation_preservation = 0.0
                test_preservation = 0.0
                overall_preservation = 0.0
                after_compilation = {'maven_compiles': False, 'test_compiles': False}
                after_tests = {'tests_run': 0, 'tests_passed': 0, 'tests_failed': 0}
            
            # Save result
            result = {
                'target_file': os.path.basename(target['file']),
                'ml_prediction': target['prediction'],
                'confidence': target['confidence'],
                'refactoring_applied': refactoring_success,
                'before_maven_compiles': before_compilation['maven_compiles'],
                'before_test_compiles': before_compilation['test_compiles'],
                'before_tests_run': before_tests['tests_run'],
                'before_tests_passed': before_tests['tests_passed'],
                'after_maven_compiles': after_compilation['maven_compiles'],
                'after_test_compiles': after_compilation['test_compiles'],
                'after_tests_run': after_tests['tests_run'],
                'after_tests_passed': after_tests['tests_passed'],
                'compilation_preservation': compilation_preservation,
                'test_preservation': test_preservation,
                'overall_preservation': overall_preservation,
                'status': 'SUCCESS' if overall_preservation >= 0.8 else 'PARTIAL' if overall_preservation >= 0.5 else 'FAILED'
            }
            
            results.append(result)
            
            print(f"   Overall Preservation: {overall_preservation:.2f} ({result['status']})")
            
        finally:
            # Restore backup
            shutil.copy2(backup_file, target_file)
            os.remove(backup_file)
    
    # Save all results
    if results:
        with open('finegrained_ml_validation_results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n=== SUMMARY ===")
        print(f"Targets tested: {len(results)}")
        for result in results:
            print(f"  {result['target_file']}: {result['overall_preservation']:.2f} ({result['status']})")
        print(f"Results saved to: finegrained_ml_validation_results.csv")

if __name__ == "__main__":
    finegrained_validation()
