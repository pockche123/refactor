#!/usr/bin/env python3
"""
Spring Framework Refactoring Extraction
Extract refactorings from Spring Framework using RefactoringMiner
Following same methodology as Commons Lang (between-commits approach)
"""

import subprocess
import json
import os
from pathlib import Path

SPRING_PATH = "/Users/parjalrai/Workspace/spring-framework"
OUTPUT_FILE = "data/spring_refactorings.json"

def get_commits_from_period(repo_path, since_date="2023-01-01", until_date="2024-12-31", max_commits=100):
    """Get commits from a specific time period"""
    try:
        result = subprocess.run([
            'git', 'log', '--format=%H', '--no-merges', 
            f'--since={since_date}', f'--until={until_date}', f'-{max_commits}'
        ], 
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=60
        )
        
        if result.returncode == 0:
            commits = result.stdout.strip().split('\n')
            return [commit for commit in commits if commit]
        else:
            print(f"Error getting commits: {result.stderr}")
            return []
            
    except Exception as e:
        print(f"Exception getting commits: {e}")
        return []

def extract_refactorings_between_commits(start_commit, end_commit):
    """Extract refactorings between two commits using RefactoringMiner -bc option"""
    
    print(f"🔍 Processing range {start_commit[:8]}..{end_commit[:8]}...")
    
    try:
        # Create temporary JSON file
        temp_json = "/tmp/spring_refactorings_temp.json"
        
        # Run RefactoringMiner between commits with JSON output
        result = subprocess.run([
            'java', '-jar', '/Users/parjalrai/Workspace/RefactoringMiner/build/libs/RM-fat.jar',
            '-bc', SPRING_PATH, start_commit, end_commit, '-json', temp_json
        ],
        capture_output=True,
        text=True,
        timeout=600  # 10 minute timeout for large ranges
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
    print("🚀 SPRING FRAMEWORK REFACTORING EXTRACTION")
    print("=" * 50)
    
    # Ensure output directory exists
    Path("data").mkdir(exist_ok=True)
    
    # Get commits from 2023-2024
    print("📊 Getting commits from Spring Framework (2023-2024)...")
    commits = get_commits_from_period(SPRING_PATH, "2023-01-01", "2024-12-31", 200)  # Start smaller
    
    if len(commits) < 2:
        print("❌ Need at least 2 commits for range extraction!")
        return
    
    print(f"   Found {len(commits)} commits")
    
    # Extract refactorings using between-commits approach (same as Commons Lang)
    print("🔍 Extracting refactorings using between-commits approach...")
    
    # Use the first and last commit to get a range
    start_commit = commits[-1]  # Oldest commit
    end_commit = commits[0]     # Newest commit
    
    refactoring_data = extract_refactorings_between_commits(start_commit, end_commit)
    
    if refactoring_data:
        # Save the raw JSON (same format as Commons Lang)
        print(f"\n💾 Saving refactoring data...")
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(refactoring_data, f, indent=2)
        
        print(f"   ✅ {OUTPUT_FILE}")
        
        # Count refactorings
        total_refactorings = 0
        refactoring_types = {}
        
        if 'commits' in refactoring_data:
            for commit_data in refactoring_data['commits']:
                for refactoring in commit_data.get('refactorings', []):
                    total_refactorings += 1
                    ref_type = refactoring.get('type', 'Unknown')
                    refactoring_types[ref_type] = refactoring_types.get(ref_type, 0) + 1
        
        print(f"\n📈 EXTRACTION SUMMARY:")
        print(f"   Total commits analyzed: {len(refactoring_data.get('commits', []))}")
        print(f"   Total refactorings: {total_refactorings}")
        
        if refactoring_types:
            print(f"   Unique types: {len(refactoring_types)}")
            print(f"   Top 5 types:")
            
            sorted_types = sorted(refactoring_types.items(), key=lambda x: x[1], reverse=True)
            for ref_type, count in sorted_types[:5]:
                percentage = (count / total_refactorings) * 100
                print(f"     {ref_type}: {count} ({percentage:.1f}%)")
        else:
            print("   No refactorings found in this range")
    
    else:
        print("❌ No refactoring data extracted")

if __name__ == "__main__":
    main()
