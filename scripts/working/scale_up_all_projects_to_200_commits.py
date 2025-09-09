#!/usr/bin/env python3
"""
Scale up refactoring extractions to 200 commits per project
To meet thesis requirement of 1000+ instances per project
"""

import subprocess
import os

def update_spring_extraction():
    """Update Spring Framework to use 200 commits"""
    script_path = "scripts/working/spring_refactoring_extraction.py"
    
    # Read current script
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Update commit count from 20 to 200
    updated_content = content.replace(
        'commits = get_commits_from_period(SPRING_PATH, "2023-01-01", "2024-12-31", 20)',
        'commits = get_commits_from_period(SPRING_PATH, "2023-01-01", "2024-12-31", 200)'
    )
    
    # Write updated script
    with open(script_path, 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated Spring Framework extraction to 200 commits")

def update_kafka_extraction():
    """Update Kafka to use 200 commits"""
    script_path = "scripts/working/kafka_refactoring_extraction.py"
    
    # Read current script
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Update commit count from 30 to 200
    updated_content = content.replace(
        'commits = get_commits_from_period(KAFKA_PATH, "2023-01-01", "2024-12-31", 30)',
        'commits = get_commits_from_period(KAFKA_PATH, "2023-01-01", "2024-12-31", 200)'
    )
    
    # Write updated script
    with open(script_path, 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated Kafka extraction to 200 commits")

def create_intellij_scaled_extraction():
    """Create scaled IntelliJ extraction for 200 commits"""
    script_content = '''#!/usr/bin/env python3
"""
IntelliJ IDEA Refactoring Extraction - Scaled to 200 commits
Extract refactorings from IntelliJ using RefactoringMiner
"""

import subprocess
import json
import os
from datetime import datetime

# IntelliJ repository path
INTELLIJ_PATH = "/Users/parjalrai/Workspace/intellij-community"

def get_commits_from_period(repo_path, start_date, end_date, max_commits=200):
    """Get commits from a specific time period"""
    
    cmd = [
        'git', 'log', 
        '--format=%H',
        '--no-merges',
        f'--since={start_date}',
        f'--until={end_date}',
        f'-{max_commits}'
    ]
    
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Git log failed: {result.stderr}")
        return []
    
    commits = [line.strip() for line in result.stdout.strip().split('\\n') if line.strip()]
    return commits

def extract_refactorings_between_commits(start_commit, end_commit):
    """Extract refactorings between two commits using RefactoringMiner -bc option"""
    
    print(f"🔍 Processing range {start_commit[:8]}..{end_commit[:8]}...")
    
    try:
        # Create temporary JSON file
        temp_json = "/tmp/intellij_refactorings_temp.json"
        
        # Run RefactoringMiner between commits with JSON output
        result = subprocess.run([
            'java', '-jar', '/Users/parjalrai/Workspace/RefactoringMiner/build/libs/RM-fat.jar',
            '-bc', INTELLIJ_PATH, start_commit, end_commit, '-json', temp_json
        ],
        capture_output=True,
        text=True,
        timeout=1200  # 20 minute timeout for large ranges
        )
        
        if result.returncode != 0:
            print(f"   ❌ RefactoringMiner failed: {result.stderr}")
            return None
        
        # Read the JSON file
        try:
            if os.path.exists(temp_json):
                with open(temp_json, 'r') as f:
                    refactoring_data = json.load(f)
                
                # Clean up temp file
                os.remove(temp_json)
                
                return refactoring_data
            else:
                print(f"   ❌ JSON file not created")
                return None
                
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON parsing failed: {e}")
            return None
        except Exception as e:
            print(f"   ❌ Error reading JSON file: {e}")
            return None
        
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Timeout processing range {start_commit[:8]}..{end_commit[:8]}")
        return None
    except Exception as e:
        print(f"   ❌ Error processing range: {e}")
        return None

def main():
    print("🚀 INTELLIJ IDEA REFACTORING EXTRACTION (SCALED)")
    print("=" * 60)
    
    # Get recent commits from IntelliJ (2023-2024)
    print("📊 Getting commits from IntelliJ IDEA (2023-2024)...")
    commits = get_commits_from_period(INTELLIJ_PATH, "2023-01-01", "2024-12-31", 200)
    
    if not commits:
        print("❌ No commits found in the specified period")
        return
    
    print(f"   Found {len(commits)} commits")
    
    # Extract refactorings using between-commits approach
    print("🔍 Extracting refactorings using between-commits approach...")
    
    if len(commits) < 2:
        print("❌ Need at least 2 commits for between-commits analysis")
        return
    
    # Use first and last commit for range analysis
    start_commit = commits[-1]  # Oldest commit
    end_commit = commits[0]     # Newest commit
    
    refactoring_data = extract_refactorings_between_commits(start_commit, end_commit)
    
    if not refactoring_data:
        print("❌ No refactoring data extracted")
        return
    
    # Save refactoring data
    print("\\n💾 Saving refactoring data...")
    
    output_file = "data/intellij_refactorings_scaled.json"
    with open(output_file, 'w') as f:
        json.dump(refactoring_data, f, indent=2)
    
    print(f"   ✅ {output_file}")
    
    # Analyze and summarize results
    print(f"\\n📈 EXTRACTION SUMMARY:")
    
    total_commits = len(refactoring_data.get('commits', []))
    total_refactorings = sum(len(commit.get('refactorings', [])) for commit in refactoring_data.get('commits', []))
    
    print(f"   Total commits analyzed: {total_commits}")
    print(f"   Total refactorings: {total_refactorings}")
    
    if total_refactorings > 0:
        # Count refactoring types
        refactoring_types = {}
        for commit in refactoring_data.get('commits', []):
            for refactoring in commit.get('refactorings', []):
                ref_type = refactoring.get('type', 'Unknown')
                refactoring_types[ref_type] = refactoring_types.get(ref_type, 0) + 1
        
        print(f"   Unique types: {len(refactoring_types)}")
        print(f"   Top 5 types:")
        
        sorted_types = sorted(refactoring_types.items(), key=lambda x: x[1], reverse=True)
        for ref_type, count in sorted_types[:5]:
            percentage = (count / total_refactorings) * 100
            print(f"     {ref_type}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
'''
    
    with open("scripts/working/intellij_refactoring_extraction_scaled.py", 'w') as f:
        f.write(script_content)
    
    print("✅ Created scaled IntelliJ extraction script")

def create_mockito_scaled_extraction():
    """Create scaled Mockito extraction for 200 commits"""
    script_content = '''#!/usr/bin/env python3
"""
Mockito Refactoring Extraction - Scaled to 200 commits
Extract refactorings from Mockito using RefactoringMiner
"""

import subprocess
import json
import os
from datetime import datetime

# Mockito repository path
MOCKITO_PATH = "/Users/parjalrai/Workspace/mockito"

def get_commits_from_period(repo_path, start_date, end_date, max_commits=200):
    """Get commits from a specific time period"""
    
    cmd = [
        'git', 'log', 
        '--format=%H',
        '--no-merges',
        f'--since={start_date}',
        f'--until={end_date}',
        f'-{max_commits}'
    ]
    
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Git log failed: {result.stderr}")
        return []
    
    commits = [line.strip() for line in result.stdout.strip().split('\\n') if line.strip()]
    return commits

def extract_refactorings_between_commits(start_commit, end_commit):
    """Extract refactorings between two commits using RefactoringMiner -bc option"""
    
    print(f"🔍 Processing range {start_commit[:8]}..{end_commit[:8]}...")
    
    try:
        # Create temporary JSON file
        temp_json = "/tmp/mockito_refactorings_temp.json"
        
        # Run RefactoringMiner between commits with JSON output
        result = subprocess.run([
            'java', '-jar', '/Users/parjalrai/Workspace/RefactoringMiner/build/libs/RM-fat.jar',
            '-bc', MOCKITO_PATH, start_commit, end_commit, '-json', temp_json
        ],
        capture_output=True,
        text=True,
        timeout=1200  # 20 minute timeout for large ranges
        )
        
        if result.returncode != 0:
            print(f"   ❌ RefactoringMiner failed: {result.stderr}")
            return None
        
        # Read the JSON file
        try:
            if os.path.exists(temp_json):
                with open(temp_json, 'r') as f:
                    refactoring_data = json.load(f)
                
                # Clean up temp file
                os.remove(temp_json)
                
                return refactoring_data
            else:
                print(f"   ❌ JSON file not created")
                return None
                
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON parsing failed: {e}")
            return None
        except Exception as e:
            print(f"   ❌ Error reading JSON file: {e}")
            return None
        
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Timeout processing range {start_commit[:8]}..{end_commit[:8]}")
        return None
    except Exception as e:
        print(f"   ❌ Error processing range: {e}")
        return None

def main():
    print("🚀 MOCKITO REFACTORING EXTRACTION (SCALED)")
    print("=" * 50)
    
    # Get recent commits from Mockito (2023-2024)
    print("📊 Getting commits from Mockito (2023-2024)...")
    commits = get_commits_from_period(MOCKITO_PATH, "2023-01-01", "2024-12-31", 200)
    
    if not commits:
        print("❌ No commits found in the specified period")
        return
    
    print(f"   Found {len(commits)} commits")
    
    # Extract refactorings using between-commits approach
    print("🔍 Extracting refactorings using between-commits approach...")
    
    if len(commits) < 2:
        print("❌ Need at least 2 commits for between-commits analysis")
        return
    
    # Use first and last commit for range analysis
    start_commit = commits[-1]  # Oldest commit
    end_commit = commits[0]     # Newest commit
    
    refactoring_data = extract_refactorings_between_commits(start_commit, end_commit)
    
    if not refactoring_data:
        print("❌ No refactoring data extracted")
        return
    
    # Save refactoring data
    print("\\n💾 Saving refactoring data...")
    
    output_file = "data/mockito_refactorings_scaled.json"
    with open(output_file, 'w') as f:
        json.dump(refactoring_data, f, indent=2)
    
    print(f"   ✅ {output_file}")
    
    # Analyze and summarize results
    print(f"\\n📈 EXTRACTION SUMMARY:")
    
    total_commits = len(refactoring_data.get('commits', []))
    total_refactorings = sum(len(commit.get('refactorings', [])) for commit in refactoring_data.get('commits', []))
    
    print(f"   Total commits analyzed: {total_commits}")
    print(f"   Total refactorings: {total_refactorings}")
    
    if total_refactorings > 0:
        # Count refactoring types
        refactoring_types = {}
        for commit in refactoring_data.get('commits', []):
            for refactoring in commit.get('refactorings', []):
                ref_type = refactoring.get('type', 'Unknown')
                refactoring_types[ref_type] = refactoring_types.get(ref_type, 0) + 1
        
        print(f"   Unique types: {len(refactoring_types)}")
        print(f"   Top 5 types:")
        
        sorted_types = sorted(refactoring_types.items(), key=lambda x: x[1], reverse=True)
        for ref_type, count in sorted_types[:5]:
            percentage = (count / total_refactorings) * 100
            print(f"     {ref_type}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
'''
    
    with open("scripts/working/mockito_refactoring_extraction_scaled.py", 'w') as f:
        f.write(script_content)
    
    print("✅ Created scaled Mockito extraction script")

def main():
    print("🚀 SCALING UP REFACTORING EXTRACTIONS TO 200 COMMITS")
    print("=" * 60)
    
    print("📊 Updating existing extraction scripts...")
    update_spring_extraction()
    update_kafka_extraction()
    
    print("📊 Creating new scaled extraction scripts...")
    create_intellij_scaled_extraction()
    create_mockito_scaled_extraction()
    
    print(f"\\n✅ ALL EXTRACTION SCRIPTS UPDATED TO 200 COMMITS")
    print(f"   This should give us 1000+ instances per project")
    print(f"   Ready to re-run extractions for larger datasets")
    
    print(f"\\n📋 NEXT STEPS:")
    print(f"   1. Re-run Spring Framework extraction (200 commits)")
    print(f"   2. Re-run Kafka extraction (200 commits)")
    print(f"   3. Run new IntelliJ scaled extraction (200 commits)")
    print(f"   4. Run new Mockito scaled extraction (200 commits)")
    print(f"   5. Commons Lang already has 314 instances - may need scaling too")

if __name__ == "__main__":
    main()
