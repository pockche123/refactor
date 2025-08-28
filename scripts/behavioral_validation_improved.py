import pandas as pd
import subprocess
import os
import tempfile
import csv
import re
from collections import defaultdict

def run_tests(repo_dir):
    """Run Maven tests and return detailed test counts"""
    try:
        result = subprocess.run(
            ["mvn", "test", "-Dmaven.test.failure.ignore=true"], 
            cwd=repo_dir, 
            capture_output=True, 
            timeout=600,
            text=True
        )
        
        output = result.stdout + result.stderr
        
        # Initialize counters
        total_tests_run = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        
        # Parse Maven Surefire output
        # Look for lines like: "Tests run: 123, Failures: 4, Errors: 1, Skipped: 2"
        test_summary_pattern = r'Tests run: (\d+),\s*Failures: (\d+),\s*Errors: (\d+),\s*Skipped: (\d+)'
        
        for line in output.split('\n'):
            match = re.search(test_summary_pattern, line)
            if match:
                total_tests_run += int(match.group(1))
                total_failures += int(match.group(2))
                total_errors += int(match.group(3))
                total_skipped += int(match.group(4))
        
        # Calculate passed tests
        total_passed = total_tests_run - total_failures - total_errors - total_skipped
        
        # If no tests found with regex, try alternative parsing
        if total_tests_run == 0:
            # Look for final summary at end
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if 'Results:' in line or 'Tests run:' in line:
                    # Check next few lines for summary
                    for j in range(i, min(i+5, len(lines))):
                        summary_line = lines[j]
                        if 'Tests run:' in summary_line:
                            # Try simpler parsing
                            numbers = re.findall(r'\d+', summary_line)
                            if len(numbers) >= 4:
                                total_tests_run = int(numbers[0])
                                total_failures = int(numbers[1])
                                total_errors = int(numbers[2])
                                total_skipped = int(numbers[3])
                                total_passed = total_tests_run - total_failures - total_errors - total_skipped
                                break
        
        return {
            'tests_run': total_tests_run,
            'tests_passed': max(0, total_passed),  # Ensure non-negative
            'tests_failed': total_failures,
            'tests_errors': total_errors,
            'tests_skipped': total_skipped,
            'build_success': result.returncode == 0,
            'has_tests': total_tests_run > 0,
            'output_sample': output[-300:] if len(output) > 300 else output
        }
    except subprocess.TimeoutExpired:
        return {'tests_run': 0, 'tests_passed': 0, 'tests_failed': 0, 'has_tests': False, 'error': 'timeout'}
    except Exception as e:
        return {'tests_run': 0, 'tests_passed': 0, 'tests_failed': 0, 'has_tests': False, 'error': str(e)}

def calculate_behavior_preservation(before_results, after_results):
    """Calculate behavior preservation based on test counts"""
    
    before_passed = before_results.get('tests_passed', 0)
    before_total = before_results.get('tests_run', 0)
    before_failed = before_results.get('tests_failed', 0) + before_results.get('tests_errors', 0)
    
    after_passed = after_results.get('tests_passed', 0)
    after_total = after_results.get('tests_run', 0)
    after_failed = after_results.get('tests_failed', 0) + after_results.get('tests_errors', 0)
    
    # No tests = can't validate
    if before_total == 0 or after_total == 0:
        return {
            'preservation_score': None,
            'confidence': 'none',
            'reason': 'No tests available',
            'test_accuracy': None
        }
    
    # Test count changed significantly = low confidence
    if abs(before_total - after_total) > 2:
        return {
            'preservation_score': None,
            'confidence': 'low',
            'reason': f'Test count changed: {before_total} → {after_total}',
            'test_accuracy': None
        }
    
    # Calculate preservation score
    # How many tests that passed before still pass after?
    if before_passed == 0:
        # No passing tests to preserve
        preservation_score = 1.0 if after_passed == 0 else 0.0
        test_accuracy = after_passed / after_total if after_total > 0 else 0.0
    else:
        # Preservation score = min(after_passed, before_passed) / before_passed
        preserved_tests = min(after_passed, before_passed)
        preservation_score = preserved_tests / before_passed
        test_accuracy = after_passed / after_total if after_total > 0 else 0.0
    
    # Determine confidence based on test counts
    if before_total >= 10:
        confidence = 'high'
    elif before_total >= 3:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    # Generate reason
    if preservation_score >= 0.95:
        reason = f'Excellent preservation: {after_passed}/{before_passed} tests still pass'
    elif preservation_score >= 0.8:
        reason = f'Good preservation: {after_passed}/{before_passed} tests still pass'
    elif preservation_score >= 0.5:
        reason = f'Partial preservation: {after_passed}/{before_passed} tests still pass'
    else:
        reason = f'Poor preservation: {after_passed}/{before_passed} tests still pass'
    
    return {
        'preservation_score': preservation_score,
        'confidence': confidence,
        'reason': reason,
        'test_accuracy': test_accuracy
    }

def validate_commit(repo_url, commit_sha, refactoring_types):
    """Validate single commit with test counting"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, "repo")
        
        try:
            # Clone repository
            print(f"  Cloning {repo_url.split('/')[-1]}...")
            clone_result = subprocess.run(
                ["git", "clone", "--depth", "50", repo_url, repo_dir], 
                capture_output=True, timeout=120
            )
            
            if clone_result.returncode != 0:
                return {'status': 'clone_failed', 'error': clone_result.stderr.decode()}
            
            # Test BEFORE refactoring
            print(f"  Testing BEFORE refactoring...")
            subprocess.run(["git", "checkout", f"{commit_sha}^"], cwd=repo_dir, capture_output=True)
            before_results = run_tests(repo_dir)
            
            # Test AFTER refactoring  
            print(f"  Testing AFTER refactoring...")
            subprocess.run(["git", "checkout", commit_sha], cwd=repo_dir, capture_output=True)
            after_results = run_tests(repo_dir)
            
            # Calculate preservation
            preservation = calculate_behavior_preservation(before_results, after_results)
            
            return {
                'status': 'completed',
                'commit_sha': commit_sha,
                'refactoring_types': refactoring_types,
                'before_results': before_results,
                'after_results': after_results,
                'preservation_score': preservation['preservation_score'],
                'test_accuracy': preservation['test_accuracy'],
                'confidence': preservation['confidence'],
                'reason': preservation['reason']
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

def main():
    """Run behavioral validation with test counting"""
    
    # Load commits from enhanced dataset
    df = pd.read_csv('enhanced_dataset.csv')
    
    # Group by commit
    commit_groups = df.groupby('commit_sha').agg({
        'refactoring_type': list,
        'file_path': 'first'
    }).reset_index()
    
    # Map to repository URLs
    repo_mapping = {
        'commons-lang': 'https://github.com/apache/commons-lang.git',
        'commons-collections': 'https://github.com/apache/commons-collections.git',
        'gson': 'https://github.com/google/gson.git'
    }
    
    def get_repo_url(file_path):
        if 'commons/lang' in file_path or 'commons-lang' in file_path:
            return repo_mapping['commons-lang']
        elif 'commons/collections' in file_path or 'commons-collections' in file_path:
            return repo_mapping['commons-collections']
        elif 'gson' in file_path:
            return repo_mapping['gson']
        return None
    
    commit_groups['repo_url'] = commit_groups['file_path'].apply(get_repo_url)
    commit_groups = commit_groups.dropna(subset=['repo_url'])
    
    # Sample commits for validation
    sample_commits = commit_groups.head(10)
    
    print(f"=== BEHAVIORAL VALIDATION WITH TEST COUNTING ===")
    print(f"Validating {len(sample_commits)} commits...")
    print()
    
    results = []
    successful_validations = 0
    total_preservation_score = 0
    high_confidence_results = []
    
    for idx, row in sample_commits.iterrows():
        commit_sha = row['commit_sha']
        repo_url = row['repo_url']
        refactoring_types = row['refactoring_type']
        
        print(f"[{idx+1}/{len(sample_commits)}] Validating {commit_sha[:8]}...")
        print(f"  Refactorings: {', '.join(set(refactoring_types))}")
        
        result = validate_commit(repo_url, commit_sha, refactoring_types)
        results.append(result)
        
        if result['status'] == 'completed':
            successful_validations += 1
            
            preservation_score = result['preservation_score']
            test_accuracy = result['test_accuracy']
            confidence = result['confidence']
            reason = result['reason']
            
            before = result['before_results']
            after = result['after_results']
            
            if preservation_score is not None:
                total_preservation_score += preservation_score
                
                if preservation_score >= 0.9:
                    print(f"  ✅ EXCELLENT: {preservation_score:.1%} preservation ({confidence} confidence)")
                elif preservation_score >= 0.7:
                    print(f"  ✅ GOOD: {preservation_score:.1%} preservation ({confidence} confidence)")
                elif preservation_score >= 0.5:
                    print(f"  ⚠️  PARTIAL: {preservation_score:.1%} preservation ({confidence} confidence)")
                else:
                    print(f"  ❌ POOR: {preservation_score:.1%} preservation ({confidence} confidence)")
                
                print(f"    {reason}")
                print(f"    Before: {before['tests_passed']} passed, {before['tests_failed']} failed, {before['tests_run']} total")
                print(f"    After:  {after['tests_passed']} passed, {after['tests_failed']} failed, {after['tests_run']} total")
                
                if confidence == 'high':
                    high_confidence_results.append(preservation_score)
            else:
                print(f"  ❓ UNKNOWN: {reason} ({confidence} confidence)")
                print(f"    Before: {before['tests_run']} tests, After: {after['tests_run']} tests")
        else:
            print(f"  ⚠️  VALIDATION FAILED: {result.get('error', 'unknown')}")
        
        print()
    
    # Results Summary
    print("=== TEST COUNTING VALIDATION RESULTS ===")
    print(f"Total commits tested: {len(sample_commits)}")
    print(f"Successful validations: {successful_validations}")
    
    valid_scores = [r['preservation_score'] for r in results 
                   if r.get('status') == 'completed' and r.get('preservation_score') is not None]
    
    if valid_scores:
        avg_preservation = sum(valid_scores) / len(valid_scores)
        print(f"Average preservation score: {avg_preservation:.1%}")
        print(f"Validations with tests: {len(valid_scores)}")
        
        excellent = sum(1 for s in valid_scores if s >= 0.9)
        good = sum(1 for s in valid_scores if 0.7 <= s < 0.9)
        partial = sum(1 for s in valid_scores if 0.5 <= s < 0.7)
        poor = sum(1 for s in valid_scores if s < 0.5)
        
        print(f"\nBreakdown:")
        print(f"  Excellent (≥90%): {excellent}")
        print(f"  Good (70-89%): {good}")
        print(f"  Partial (50-69%): {partial}")
        print(f"  Poor (<50%): {poor}")
        
        if high_confidence_results:
            hc_avg = sum(high_confidence_results) / len(high_confidence_results)
            print(f"\nHigh-confidence average: {hc_avg:.1%} ({len(high_confidence_results)} results)")
    
    # Save results
    with open('behavioral_validation_improved_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'commit_sha', 'status', 'preservation_score', 'test_accuracy', 'confidence',
            'reason', 'refactoring_types', 'before_tests_run', 'before_tests_passed', 
            'after_tests_run', 'after_tests_passed', 'error'
        ])
        writer.writeheader()
        
        for result in results:
            before = result.get('before_results', {})
            after = result.get('after_results', {})
            
            writer.writerow({
                'commit_sha': result.get('commit_sha', ''),
                'status': result['status'],
                'preservation_score': result.get('preservation_score'),
                'test_accuracy': result.get('test_accuracy'),
                'confidence': result.get('confidence', ''),
                'reason': result.get('reason', ''),
                'refactoring_types': ', '.join(result.get('refactoring_types', [])),
                'before_tests_run': before.get('tests_run', 0),
                'before_tests_passed': before.get('tests_passed', 0),
                'after_tests_run': after.get('tests_run', 0),
                'after_tests_passed': after.get('tests_passed', 0),
                'error': result.get('error', '')
            })
    
    print(f"\nResults saved to behavioral_validation_improved_results.csv")

if __name__ == "__main__":
    main()
