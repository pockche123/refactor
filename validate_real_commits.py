import csv
import requests
import time
import os

def check_commit_exists(repo_url, commit_sha):
    """Check if commit exists in GitHub repository"""
    # Extract owner/repo from URL
    if 'github.com' in repo_url:
        parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
        owner, repo = parts[0], parts[1]
    else:
        return False, "Not a GitHub repo"
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            commit_data = response.json()
            return True, commit_data.get('commit', {}).get('message', 'No message')
        elif response.status_code == 404:
            return False, "Commit not found"
        else:
            return False, f"API error: {response.status_code}"
    except Exception as e:
        return False, f"Request failed: {str(e)}"

def validate_dataset(csv_file):
    """Validate commits in a CSV dataset"""
    print(f"\nValidating {csv_file}...")
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return
    
    # Determine repository based on filename
    repo_map = {
        'commons_lang': 'https://github.com/apache/commons-lang',
        'intellij': 'https://github.com/JetBrains/intellij-community', 
        'spring': 'https://github.com/spring-projects/spring-framework',
        'kafka': 'https://github.com/apache/kafka',
        'mockito': 'https://github.com/mockito/mockito'
    }
    
    repo_url = None
    for domain, url in repo_map.items():
        if domain in csv_file:
            repo_url = url
            break
    
    if not repo_url:
        print(f"❌ Unknown repository for {csv_file}")
        return
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        print(f"❌ Empty dataset: {csv_file}")
        return
    
    # Check if it's synthetic data
    first_commit = rows[0].get('commit_sha', '')
    if first_commit.startswith('dummy_commit'):
        print(f"❌ SYNTHETIC DATA: Contains dummy commits like '{first_commit}'")
        return
    
    # Sample validation - check first 5 commits
    sample_size = min(5, len(rows))
    real_commits = 0
    
    print(f"Checking {sample_size} sample commits...")
    
    for i in range(sample_size):
        commit_sha = rows[i].get('commit_sha', '')
        if not commit_sha:
            print(f"  Row {i+1}: ❌ No commit_sha")
            continue
            
        exists, message = check_commit_exists(repo_url, commit_sha)
        if exists:
            real_commits += 1
            print(f"  Row {i+1}: ✅ {commit_sha[:8]} - '{message[:50]}...'")
        else:
            print(f"  Row {i+1}: ❌ {commit_sha[:8]} - {message}")
        
        time.sleep(0.2)  # Rate limiting
    
    print(f"\nResult: {real_commits}/{sample_size} commits verified as real")
    if real_commits == sample_size:
        print(f"✅ REAL DATASET: {len(rows)} total records")
    else:
        print(f"❌ QUESTIONABLE DATASET: Some commits not verified")

def main():
    data_dir = 'data'
    
    # Find all CSV files in data directory
    csv_files = []
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            csv_files.append(os.path.join(data_dir, file))
    
    print(f"Found {len(csv_files)} CSV files to validate:")
    
    for csv_file in sorted(csv_files):
        validate_dataset(csv_file)
    
    print("\n" + "="*50)
    print("VALIDATION COMPLETE")

if __name__ == "__main__":
    main()
