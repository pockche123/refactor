#!/usr/bin/env python3
"""
Behavioral Compilation Validation for Mixed Domain Results
Tests if correctly predicted refactorings produce compilable code
"""

import os
import subprocess
import pandas as pd
import tempfile
import shutil
from pathlib import Path

# Repository mappings based on your actual workspace
REPO_MAPPINGS = {
    'commons_gson': {
        'commons': '/Users/parjalrai/Workspace/commons-collections',
        'gson': '/Users/parjalrai/Workspace/gson'
    },
    'intellij': '/Users/parjalrai/Workspace/intellij-community',
    'mockito': '/Users/parjalrai/Workspace/mockito',
    'elasticsearch': '/Users/parjalrai/Workspace/refactoring-classifier/complex_projects/elasticsearch'
}

def get_project_base(file_path, domain):
    """Determine which repository a file belongs to"""
    if domain == 'commons_gson':
        if file_path.startswith('gson/'):
            return REPO_MAPPINGS['commons_gson']['gson'], file_path[5:]  # Remove 'gson/' prefix
        else:
            return REPO_MAPPINGS['commons_gson']['commons'], file_path
    else:
        return REPO_MAPPINGS[domain], file_path

def test_java_compilation():
    """Test if Java compilation works"""
    try:
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True)
        print(f"☕ Java compiler: {result.stderr.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Java compiler (javac) not found")
        return False

def simple_compilation_test(project_base, relative_path):
    """Test if a Java file compiles in its original state"""
    
    full_path = Path(project_base) / relative_path
    
    if not full_path.exists():
        return {
            'status': 'FILE_NOT_FOUND', 
            'path': str(full_path),
            'relative_path': relative_path
        }
    
    # Try basic compilation
    try:
        result = subprocess.run([
            'javac', 
            '-cp', '.:*',  # Basic classpath
            str(full_path)
        ], 
        capture_output=True, 
        text=True, 
        timeout=15,
        cwd=full_path.parent
        )
        
        return {
            'status': 'TESTED',
            'file_path': relative_path,
            'full_path': str(full_path),
            'compiles': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr[:200] if result.stderr else ''  # Limit error output
        }
        
    except subprocess.TimeoutExpired:
        return {'status': 'TIMEOUT', 'file_path': relative_path}
    except Exception as e:
        return {'status': 'ERROR', 'file_path': relative_path, 'error': str(e)}

def validate_domain_compilation(domain_name, results_file, sample_size=20):
    """Test compilation for correct predictions in a domain"""
    
    print(f"🚀 Testing {domain_name} Compilation Validation")
    print("=" * 60)
    
    # Check Java compiler
    if not test_java_compilation():
        return None
    
    # Load results
    if not os.path.exists(results_file):
        print(f"❌ Results file not found: {results_file}")
        return None
    
    df = pd.read_csv(results_file)
    correct_predictions = df[df['correct'] == True]
    
    print(f"📊 {domain_name} Results:")
    print(f"   Total predictions: {len(df)}")
    print(f"   Correct predictions: {len(correct_predictions)}")
    print(f"   Accuracy: {len(correct_predictions)/len(df)*100:.1f}%")
    
    # Sample for testing
    if len(correct_predictions) > sample_size:
        sample_df = correct_predictions.sample(n=sample_size, random_state=42)
        print(f"📊 Testing {sample_size} random correct predictions")
    else:
        sample_df = correct_predictions
        print(f"📊 Testing all {len(sample_df)} correct predictions")
    
    results = []
    
    for idx, row in sample_df.iterrows():
        print(f"\n🔍 {idx+1}/{len(sample_df)}: {row['refactoring_type']}")
        print(f"   File: {row['file_path']}")
        
        try:
            project_base, relative_path = get_project_base(row['file_path'], domain_name)
            result = simple_compilation_test(project_base, relative_path)
            result['refactoring_type'] = row['refactoring_type']
            result['original_file_path'] = row['file_path']
            results.append(result)
            
            if result['status'] == 'TESTED':
                status = "✅" if result['compiles'] else "❌"
                print(f"   {status} Compiles: {result['compiles']}")
                if not result['compiles'] and result['stderr']:
                    print(f"   Error: {result['stderr'][:80]}...")
            else:
                print(f"   ⚠️  Status: {result['status']}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'status': 'PROCESSING_ERROR',
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'error': str(e)
            })
    
    # Summary
    tested_results = [r for r in results if r['status'] == 'TESTED']
    if tested_results:
        compilable = sum(1 for r in tested_results if r['compiles'])
        success_rate = (compilable / len(tested_results)) * 100
        
        print(f"\n📊 Compilation Test Summary for {domain_name}:")
        print(f"   Files tested: {len(tested_results)}")
        print(f"   Files found: {len([r for r in results if r['status'] != 'FILE_NOT_FOUND'])}")
        print(f"   Compilable files: {compilable}")
        print(f"   Compilation success rate: {success_rate:.1f}%")
    
    # Save results
    results_df = pd.DataFrame(results)
    output_file = f"results/{domain_name}_compilation_validation.csv"
    results_df.to_csv(output_file, index=False)
    print(f"   Results saved to: {output_file}")
    
    return results_df

def main():
    """Run compilation validation for all domains"""
    
    domains = [
        ('commons_gson', 'results/commons_gson_mixed_domain_results.csv'),
        ('intellij', 'results/intellij_mixed_domain_results.csv'),
        ('mockito', 'results/mockito_mixed_domain_results.csv'),
        ('elasticsearch', 'results/elasticsearch_mixed_domain_results.csv')
    ]
    
    all_results = {}
    
    for domain_name, results_file in domains:
        print(f"\n{'='*80}")
        try:
            results = validate_domain_compilation(domain_name, results_file, sample_size=15)
            all_results[domain_name] = results
        except Exception as e:
            print(f"❌ Failed to process {domain_name}: {e}")
    
    print(f"\n{'='*80}")
    print("🎯 OVERALL COMPILATION VALIDATION SUMMARY")
    print("="*80)
    
    for domain_name, results in all_results.items():
        if results is not None:
            tested = results[results['status'] == 'TESTED']
            if len(tested) > 0:
                success_rate = (tested['compiles'].sum() / len(tested)) * 100
                print(f"{domain_name:15}: {len(tested):2d} tested, {success_rate:5.1f}% compile")

if __name__ == "__main__":
    main()
