#!/usr/bin/env python3
"""
Simple Compilation Test for Mixed Domain Results
Start with IntelliJ project since we have the source code
"""

import os
import subprocess
import pandas as pd
import tempfile
import shutil
from pathlib import Path

def test_java_compilation():
    """Test if Java compilation works"""
    try:
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True)
        print(f"☕ Java compiler: {result.stderr.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Java compiler (javac) not found")
        return False

def simple_file_compilation_test(project_base, file_path):
    """Test if a single Java file can compile"""
    
    full_path = Path(project_base) / file_path
    
    if not full_path.exists():
        return {'status': 'FILE_NOT_FOUND', 'path': str(full_path)}
    
    # Try basic compilation
    try:
        result = subprocess.run([
            'javac', 
            '-cp', '.:*',  # Basic classpath
            str(full_path)
        ], 
        capture_output=True, 
        text=True, 
        timeout=10,
        cwd=full_path.parent
        )
        
        return {
            'status': 'TESTED',
            'file_path': file_path,
            'compiles': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr[:500] if result.stderr else ''  # Limit error output
        }
        
    except subprocess.TimeoutExpired:
        return {'status': 'TIMEOUT', 'file_path': file_path}
    except Exception as e:
        return {'status': 'ERROR', 'file_path': file_path, 'error': str(e)}

def test_intellij_compilation():
    """Test compilation for IntelliJ correct predictions"""
    
    print("🚀 Testing IntelliJ Compilation Validation")
    print("=" * 50)
    
    # Check Java compiler
    if not test_java_compilation():
        return
    
    # Load IntelliJ results
    results_file = "results/intellij_mixed_domain_results.csv"
    project_base = "complex_projects/intellij-community"
    
    if not os.path.exists(results_file):
        print(f"❌ Results file not found: {results_file}")
        return
        
    if not os.path.exists(project_base):
        print(f"❌ Project not found: {project_base}")
        return
    
    # Load and filter results
    df = pd.read_csv(results_file)
    correct_predictions = df[df['correct'] == True]
    
    print(f"📊 IntelliJ Results:")
    print(f"   Total predictions: {len(df)}")
    print(f"   Correct predictions: {len(correct_predictions)}")
    print(f"   Accuracy: {len(correct_predictions)/len(df)*100:.1f}%")
    
    # Test compilation for first 10 correct predictions
    sample_size = min(10, len(correct_predictions))
    sample_df = correct_predictions.head(sample_size)
    
    print(f"\n🔍 Testing compilation for {sample_size} correct predictions:")
    
    results = []
    
    for idx, row in sample_df.iterrows():
        print(f"\n{idx+1}. Testing: {row['refactoring_type']}")
        print(f"   File: {row['file_path']}")
        
        result = simple_file_compilation_test(project_base, row['file_path'])
        result['refactoring_type'] = row['refactoring_type']
        results.append(result)
        
        if result['status'] == 'TESTED':
            status = "✅" if result['compiles'] else "❌"
            print(f"   {status} Compiles: {result['compiles']}")
            if not result['compiles'] and result['stderr']:
                print(f"   Error: {result['stderr'][:100]}...")
        else:
            print(f"   ⚠️  Status: {result['status']}")
    
    # Summary
    tested_results = [r for r in results if r['status'] == 'TESTED']
    if tested_results:
        compilable = sum(1 for r in tested_results if r['compiles'])
        success_rate = (compilable / len(tested_results)) * 100
        
        print(f"\n📊 Compilation Test Summary:")
        print(f"   Files tested: {len(tested_results)}")
        print(f"   Compilable files: {compilable}")
        print(f"   Success rate: {success_rate:.1f}%")
    
    # Save results
    results_df = pd.DataFrame(results)
    output_file = "results/intellij_compilation_test.csv"
    results_df.to_csv(output_file, index=False)
    print(f"   Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    test_intellij_compilation()
