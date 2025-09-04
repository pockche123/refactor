#!/usr/bin/env python3
"""
Compilation Validation for Mixed Domain Results
Tests if correctly predicted refactorings produce compilable code
"""

import os
import subprocess
import pandas as pd
import tempfile
import shutil
from pathlib import Path

class CompilationValidator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.temp_dir = None
        
    def setup_temp_workspace(self):
        """Create temporary workspace for testing"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="refactoring_validation_"))
        print(f"🔧 Created temp workspace: {self.temp_dir}")
        
    def cleanup_temp_workspace(self):
        """Clean up temporary workspace"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up temp workspace")
    
    def copy_file_with_dependencies(self, file_path, project_base):
        """Copy file and try to resolve basic dependencies"""
        source_file = project_base / file_path
        if not source_file.exists():
            return None
            
        # Create directory structure in temp
        relative_path = Path(file_path)
        temp_file = self.temp_dir / relative_path
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(source_file, temp_file)
        return temp_file
    
    def simple_java_compile(self, java_file):
        """Attempt basic Java compilation"""
        try:
            result = subprocess.run([
                'javac', 
                '-cp', '.',  # Basic classpath
                str(java_file)
            ], 
            capture_output=True, 
            text=True, 
            timeout=30,
            cwd=java_file.parent
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Compilation timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def apply_simple_refactoring(self, file_path, refactoring_type):
        """Apply basic refactoring transformations for compilation testing"""
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Simple transformations for compilation testing
        if refactoring_type == "Rename Variable":
            # Find first variable declaration and rename it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'int ' in line and '=' in line:
                    lines[i] = line.replace('int ', 'int renamed_')
                    break
            content = '\n'.join(lines)
            
        elif refactoring_type == "Change Method Access Modifier":
            # Change first private method to public
            content = content.replace('private void ', 'public void ', 1)
            content = content.replace('private int ', 'public int ', 1)
            
        elif refactoring_type == "Rename Method":
            # Rename first method
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'public void test' in line:
                    lines[i] = line.replace('test', 'renamedTest', 1)
                    break
            content = '\n'.join(lines)
        
        # Write modified content
        with open(file_path, 'w') as f:
            f.write(content)
            
        return content != original_content  # Return if any change was made
    
    def validate_refactoring(self, file_path, refactoring_type, project_base):
        """Validate a single refactoring through compilation"""
        
        # Copy file to temp workspace
        temp_file = self.copy_file_with_dependencies(file_path, project_base)
        if not temp_file:
            return {'status': 'FILE_NOT_FOUND', 'file_path': file_path}
        
        # Test original compilation
        original_result = self.simple_java_compile(temp_file)
        
        # Apply refactoring
        refactoring_applied = self.apply_simple_refactoring(temp_file, refactoring_type)
        
        if not refactoring_applied:
            return {
                'status': 'NO_REFACTORING_APPLIED',
                'file_path': file_path,
                'refactoring_type': refactoring_type
            }
        
        # Test post-refactoring compilation
        refactored_result = self.simple_java_compile(temp_file)
        
        return {
            'status': 'VALIDATED',
            'file_path': file_path,
            'refactoring_type': refactoring_type,
            'original_compiles': original_result['success'],
            'refactored_compiles': refactored_result['success'],
            'compilation_valid': refactored_result['success'],
            'original_errors': original_result.get('stderr', ''),
            'refactored_errors': refactored_result.get('stderr', '')
        }

def validate_mixed_domain_results(domain_name, results_file, project_base, sample_size=50):
    """Validate compilation for mixed domain results"""
    
    print(f"🚀 Starting compilation validation for {domain_name}")
    print(f"📁 Results file: {results_file}")
    print(f"📁 Project base: {project_base}")
    
    # Load results
    df = pd.read_csv(results_file)
    
    # Filter for correct predictions only
    correct_predictions = df[df['correct'] == True]
    print(f"✅ Found {len(correct_predictions)} correct predictions")
    
    # Sample for testing
    if len(correct_predictions) > sample_size:
        sample_df = correct_predictions.sample(n=sample_size, random_state=42)
        print(f"📊 Sampling {sample_size} predictions for validation")
    else:
        sample_df = correct_predictions
        print(f"📊 Validating all {len(sample_df)} correct predictions")
    
    # Initialize validator
    validator = CompilationValidator(project_base)
    validator.setup_temp_workspace()
    
    results = []
    
    try:
        for idx, row in sample_df.iterrows():
            print(f"🔍 Validating {idx+1}/{len(sample_df)}: {row['refactoring_type']} in {row['file_path']}")
            
            result = validator.validate_refactoring(
                row['file_path'], 
                row['refactoring_type'],
                Path(project_base)
            )
            
            results.append(result)
            
            # Print progress
            if result['status'] == 'VALIDATED':
                status = "✅" if result['compilation_valid'] else "❌"
                print(f"   {status} Compilation: {result['compilation_valid']}")
    
    finally:
        validator.cleanup_temp_workspace()
    
    # Save results
    results_df = pd.DataFrame(results)
    output_file = f"results/{domain_name}_compilation_validation.csv"
    results_df.to_csv(output_file, index=False)
    
    # Summary
    validated = results_df[results_df['status'] == 'VALIDATED']
    if len(validated) > 0:
        success_rate = (validated['compilation_valid'].sum() / len(validated)) * 100
        print(f"\n📊 Compilation Validation Summary for {domain_name}:")
        print(f"   Total validated: {len(validated)}")
        print(f"   Compilation success rate: {success_rate:.1f}%")
        print(f"   Results saved to: {output_file}")
    
    return results_df

if __name__ == "__main__":
    # Validate Apache Commons/Gson (highest accuracy domain)
    validate_mixed_domain_results(
        domain_name="commons_gson",
        results_file="results/commons_gson_mixed_domain_results.csv",
        project_base="/path/to/apache-commons-collections",  # Update this path
        sample_size=100
    )
