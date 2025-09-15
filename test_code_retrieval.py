import csv
import requests
import json

def get_commit_code(repo_url, commit_sha, file_path):
    """Get before/after code for a specific file in a commit"""
    # Extract owner/repo from URL
    parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
    owner, repo = parts[0], parts[1]
    
    # Get commit details
    commit_api = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    
    try:
        response = requests.get(commit_api, timeout=10)
        if response.status_code != 200:
            return False, f"Commit API error: {response.status_code}"
        
        commit_data = response.json()
        
        # Find the file in the commit
        files = commit_data.get('files', [])
        target_file = None
        
        for file in files:
            if file['filename'] == file_path:
                target_file = file
                break
        
        if not target_file:
            return False, f"File {file_path} not found in commit"
        
        # Get before/after content
        before_content = target_file.get('patch', '')
        status = target_file.get('status', '')
        additions = target_file.get('additions', 0)
        deletions = target_file.get('deletions', 0)
        
        result = {
            'status': status,
            'additions': additions,
            'deletions': deletions,
            'patch_preview': before_content[:200] + '...' if len(before_content) > 200 else before_content
        }
        
        return True, result
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_datasets():
    """Test code retrieval for one record from each dataset"""
    
    datasets = {
        'commons_lang': 'https://github.com/apache/commons-lang',
        'intellij': 'https://github.com/JetBrains/intellij-community',
        'spring': 'https://github.com/spring-projects/spring-framework',
        'kafka': 'https://github.com/apache/kafka',
        'mockito': 'https://github.com/mockito/mockito'
    }
    
    for domain, repo_url in datasets.items():
        csv_file = f'data/{domain}_350_real.csv'
        
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                first_row = next(reader)
                
                commit_sha = first_row['commit_sha']
                file_path = first_row['file_path']
                refactoring_type = first_row['refactoring_type']
                
                print(f"\n🔍 Testing {domain}:")
                print(f"  Commit: {commit_sha}")
                print(f"  File: {file_path}")
                print(f"  Refactoring: {refactoring_type}")
                
                success, result = get_commit_code(repo_url, commit_sha, file_path)
                
                if success:
                    print(f"  ✅ SUCCESS: {result['status']} (+{result['additions']} -{result['deletions']})")
                    print(f"  📝 Patch preview: {result['patch_preview']}")
                else:
                    print(f"  ❌ FAILED: {result}")
                    
        except FileNotFoundError:
            print(f"\n❌ {domain}: Dataset file not found")
        except Exception as e:
            print(f"\n❌ {domain}: Error reading dataset - {e}")

if __name__ == "__main__":
    test_datasets()
