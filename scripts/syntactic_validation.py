#!/usr/bin/env python3
"""
Syntactic Validation for Mixed Domain Results
Tests if correctly predicted refactorings correspond to syntactically valid Java files
"""

import os
import pandas as pd
import ast
import re
from pathlib import Path

# Repository mappings
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
            return REPO_MAPPINGS['commons_gson']['gson'], file_path[5:]
        else:
            return REPO_MAPPINGS['commons_gson']['commons'], file_path
    else:
        return REPO_MAPPINGS[domain], file_path

def validate_java_syntax(file_path):
    """Basic Java syntax validation"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Basic syntax checks
        checks = {
            'has_content': len(content.strip()) > 0,
            'balanced_braces': content.count('{') == content.count('}'),
            'balanced_parens': content.count('(') == content.count(')'),
            'has_class_or_interface': bool(re.search(r'\b(class|interface|enum)\s+\w+', content)),
            'no_obvious_syntax_errors': not bool(re.search(r'[{}]\s*[{}]|;;|,,', content)),
            'proper_imports': not bool(re.search(r'import\s+[^;]*[^;]$', content, re.MULTILINE))
        }
        
        # Count issues
        syntax_score = sum(checks.values()) / len(checks)
        
        return {
            'status': 'VALIDATED',
            'syntax_valid': syntax_score >= 0.8,  # 80% of checks pass
            'syntax_score': syntax_score,
            'checks': checks,
            'file_size': len(content),
            'line_count': len(content.split('\n'))
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e),
            'syntax_valid': False
        }

def analyze_refactoring_context(file_path, refactoring_type):
    """Analyze if the file context makes sense for the refactoring type"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        context_checks = {}
        
        if refactoring_type in ['Change Method Access Modifier', 'Change Class Access Modifier']:
            context_checks['has_access_modifiers'] = bool(re.search(r'\b(public|private|protected)\s+(class|void|int|String)', content))
        
        elif refactoring_type in ['Rename Method', 'Rename Variable', 'Rename Parameter']:
            context_checks['has_identifiers'] = bool(re.search(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*[=(]', content))
        
        elif refactoring_type in ['Add Parameter Annotation', 'Add Method Annotation']:
            context_checks['has_annotations_or_methods'] = bool(re.search(r'@\w+|public\s+\w+\s+\w+\s*\(', content))
        
        elif refactoring_type in ['Extract Method', 'Extract Variable']:
            context_checks['has_method_bodies'] = bool(re.search(r'\{[^}]*\}', content))
        
        context_score = sum(context_checks.values()) / max(len(context_checks), 1)
        
        return {
            'context_appropriate': context_score > 0.5,
            'context_score': context_score,
            'context_checks': context_checks
        }
        
    except Exception as e:
        return {
            'context_appropriate': False,
            'error': str(e)
        }

def validate_domain_syntax(domain_name, results_file, sample_size=30):
    """Validate syntax for correct predictions in a domain"""
    
    print(f"🔍 Syntactic Validation for {domain_name}")
    print("=" * 50)
    
    if not os.path.exists(results_file):
        print(f"❌ Results file not found: {results_file}")
        return None
    
    df = pd.read_csv(results_file)
    correct_predictions = df[df['correct'] == True]
    
    print(f"📊 {domain_name} Dataset:")
    print(f"   Total predictions: {len(df)}")
    print(f"   Correct predictions: {len(correct_predictions)}")
    print(f"   Accuracy: {len(correct_predictions)/len(df)*100:.1f}%")
    
    # Sample for testing
    if len(correct_predictions) > sample_size:
        sample_df = correct_predictions.sample(n=sample_size, random_state=42)
        print(f"   Testing {sample_size} random correct predictions")
    else:
        sample_df = correct_predictions
        print(f"   Testing all {len(sample_df)} correct predictions")
    
    results = []
    
    for idx, row in sample_df.iterrows():
        try:
            project_base, relative_path = get_project_base(row['file_path'], domain_name)
            full_path = Path(project_base) / relative_path
            
            if not full_path.exists():
                result = {
                    'status': 'FILE_NOT_FOUND',
                    'file_path': row['file_path'],
                    'refactoring_type': row['refactoring_type']
                }
            else:
                # Validate syntax
                syntax_result = validate_java_syntax(full_path)
                context_result = analyze_refactoring_context(full_path, row['refactoring_type'])
                
                result = {
                    'file_path': row['file_path'],
                    'refactoring_type': row['refactoring_type'],
                    'full_path': str(full_path),
                    **syntax_result,
                    **context_result
                }
            
            results.append(result)
            
        except Exception as e:
            results.append({
                'status': 'PROCESSING_ERROR',
                'file_path': row['file_path'],
                'refactoring_type': row['refactoring_type'],
                'error': str(e)
            })
    
    # Analysis
    validated = [r for r in results if r.get('status') == 'VALIDATED']
    found_files = [r for r in results if r.get('status') != 'FILE_NOT_FOUND']
    
    if validated:
        syntax_valid = sum(1 for r in validated if r.get('syntax_valid', False))
        context_appropriate = sum(1 for r in validated if r.get('context_appropriate', False))
        
        print(f"\n📊 Validation Results:")
        print(f"   Files found: {len(found_files)}/{len(results)}")
        print(f"   Files validated: {len(validated)}")
        print(f"   Syntactically valid: {syntax_valid}/{len(validated)} ({syntax_valid/len(validated)*100:.1f}%)")
        print(f"   Context appropriate: {context_appropriate}/{len(validated)} ({context_appropriate/len(validated)*100:.1f}%)")
        
        # Average scores
        avg_syntax_score = sum(r.get('syntax_score', 0) for r in validated) / len(validated)
        avg_context_score = sum(r.get('context_score', 0) for r in validated) / len(validated)
        print(f"   Average syntax score: {avg_syntax_score:.2f}")
        print(f"   Average context score: {avg_context_score:.2f}")
    
    # Save results
    results_df = pd.DataFrame(results)
    output_file = f"results/{domain_name}_syntactic_validation.csv"
    results_df.to_csv(output_file, index=False)
    print(f"   Results saved to: {output_file}")
    
    return results_df

def main():
    """Run syntactic validation for all domains"""
    
    domains = [
        ('commons_gson', 'results/commons_gson_mixed_domain_results.csv'),
        ('intellij', 'results/intellij_mixed_domain_results.csv'),
        ('mockito', 'results/mockito_mixed_domain_results.csv'),
        ('elasticsearch', 'results/elasticsearch_mixed_domain_results.csv')
    ]
    
    all_results = {}
    
    for domain_name, results_file in domains:
        print(f"\n{'='*70}")
        try:
            results = validate_domain_syntax(domain_name, results_file, sample_size=25)
            all_results[domain_name] = results
        except Exception as e:
            print(f"❌ Failed to process {domain_name}: {e}")
    
    # Overall summary
    print(f"\n{'='*70}")
    print("🎯 OVERALL SYNTACTIC VALIDATION SUMMARY")
    print("="*70)
    
    for domain_name, results in all_results.items():
        if results is not None:
            validated = results[results['status'] == 'VALIDATED']
            if len(validated) > 0:
                syntax_valid = validated['syntax_valid'].sum()
                context_appropriate = validated['context_appropriate'].sum()
                print(f"{domain_name:15}: {len(validated):2d} files, {syntax_valid:2d} syntax valid ({syntax_valid/len(validated)*100:4.1f}%), {context_appropriate:2d} context appropriate ({context_appropriate/len(validated)*100:4.1f}%)")

if __name__ == "__main__":
    main()
