#!/usr/bin/env python3
"""
Runner script for compilation validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compilation_validation import validate_mixed_domain_results

def main():
    print("🔧 Compilation Validation for Mixed Domain Results")
    print("=" * 60)
    
    # Check if Java compiler is available
    import subprocess
    try:
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True)
        print(f"☕ Java compiler found: {result.stderr.strip()}")
    except FileNotFoundError:
        print("❌ Java compiler (javac) not found. Please install JDK.")
        return
    
    # You'll need to update these paths to your actual project locations
    domains = [
        {
            'name': 'commons_gson',
            'results_file': 'results/commons_gson_mixed_domain_results.csv',
            'project_base': '/path/to/apache-commons-collections',  # UPDATE THIS
            'sample_size': 50
        },
        # Add other domains later
        # {
        #     'name': 'intellij',
        #     'results_file': 'results/intellij_mixed_domain_results.csv',
        #     'project_base': '/path/to/intellij-community',
        #     'sample_size': 20
        # }
    ]
    
    for domain in domains:
        print(f"\n🚀 Processing {domain['name']}...")
        
        # Check if files exist
        if not os.path.exists(domain['results_file']):
            print(f"❌ Results file not found: {domain['results_file']}")
            continue
            
        if not os.path.exists(domain['project_base']):
            print(f"❌ Project base not found: {domain['project_base']}")
            print(f"   Please update the project_base path in this script")
            continue
        
        try:
            results_df = validate_mixed_domain_results(
                domain_name=domain['name'],
                results_file=domain['results_file'],
                project_base=domain['project_base'],
                sample_size=domain['sample_size']
            )
            print(f"✅ Completed validation for {domain['name']}")
            
        except Exception as e:
            print(f"❌ Error validating {domain['name']}: {e}")

if __name__ == "__main__":
    main()
