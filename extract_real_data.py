import json
import csv
import os

def extract_refactoring_data(json_file, output_csv, max_records=1200):
    """Extract refactoring data from RefactoringMiner JSON to CSV format"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    records = []
    
    for commit in data['commits']:
        commit_sha = commit['sha1']
        
        for refactoring in commit['refactorings']:
            # Extract basic info
            refactoring_type = refactoring['type']
            description = refactoring['description']
            
            # Count locations
            left_locations = len(refactoring.get('leftSideLocations', []))
            right_locations = len(refactoring.get('rightSideLocations', []))
            
            # Get file path from first location if available
            file_path = ""
            if refactoring.get('leftSideLocations'):
                file_path = refactoring['leftSideLocations'][0].get('filePath', '')
            elif refactoring.get('rightSideLocations'):
                file_path = refactoring['rightSideLocations'][0].get('filePath', '')
            
            # Calculate complexity metrics (simplified)
            lines_changed = left_locations + right_locations
            cyclomatic_complexity = min(lines_changed // 2, 10)  # Simple heuristic
            nesting_depth = min(lines_changed // 3, 5)  # Simple heuristic
            
            record = {
                'file_path': file_path,
                'refactoring_type': refactoring_type,
                'lines_changed': lines_changed,
                'cyclomatic_complexity': cyclomatic_complexity,
                'nesting_depth': nesting_depth,
                'commit_sha': commit_sha,
                'commit_idx': len(records),
                'refactoring_idx': len(records),
                'description': description,
                'has_left_locations': left_locations > 0,
                'has_right_locations': right_locations > 0
            }
            
            records.append(record)
            
            if len(records) >= max_records:
                break
        
        if len(records) >= max_records:
            break
    
    # Write to CSV
    if records:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
    
    return len(records)

def main():
    data_dir = 'data'
    
    # Process each domain
    domains = {
        'commons_lang': 'commons_lang_refactorings.json',
        'intellij': 'intellij_refactorings.json', 
        'spring': 'spring_refactorings.json',
        'kafka': 'kafka_refactorings.json',
        'mockito': 'mockito_refactorings.json'
    }
    
    for domain, json_file in domains.items():
        json_path = os.path.join(data_dir, json_file)
        csv_path = os.path.join(data_dir, f'{domain}_real_dataset.csv')
        
        if os.path.exists(json_path):
            count = extract_refactoring_data(json_path, csv_path)
            print(f"{domain}: Extracted {count} records to {csv_path}")
        else:
            print(f"Warning: {json_path} not found")

if __name__ == "__main__":
    main()
