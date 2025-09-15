import json
import csv
import os

def extract_350_real_data(json_file, output_csv, domain_name):
    """Extract exactly 350 real refactoring records from RefactoringMiner JSON"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    records = []
    
    for commit in data['commits']:
        commit_sha = commit['sha1']
        
        for refactoring in commit['refactorings']:
            # Extract detailed info
            refactoring_type = refactoring['type']
            description = refactoring['description']
            
            # Get locations
            left_locations = refactoring.get('leftSideLocations', [])
            right_locations = refactoring.get('rightSideLocations', [])
            
            # Get file path from first available location
            file_path = ""
            if left_locations:
                file_path = left_locations[0].get('filePath', '')
            elif right_locations:
                file_path = right_locations[0].get('filePath', '')
            
            # Calculate metrics based on actual location data
            total_locations = len(left_locations) + len(right_locations)
            lines_changed = 0
            
            # Sum up line ranges from locations
            for loc in left_locations + right_locations:
                start_line = loc.get('startLine', 0)
                end_line = loc.get('endLine', 0)
                if start_line and end_line:
                    lines_changed += abs(end_line - start_line) + 1
            
            # Heuristic complexity metrics
            cyclomatic_complexity = min(max(lines_changed // 3, 1), 10)
            nesting_depth = min(max(total_locations // 2, 1), 5)
            
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
                'has_left_locations': len(left_locations) > 0,
                'has_right_locations': len(right_locations) > 0
            }
            
            records.append(record)
            
            # Stop at exactly 350
            if len(records) >= 350:
                break
        
        if len(records) >= 350:
            break
    
    # Write exactly 350 records (or all if less than 350)
    final_records = records[:350]
    
    if final_records:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=final_records[0].keys())
            writer.writeheader()
            writer.writerows(final_records)
    
    return len(final_records)

def main():
    data_dir = 'data'
    
    # Process each domain - extract exactly 350 from each
    domains = {
        'commons_lang': 'commons_lang_refactorings.json',
        'intellij': 'intellij_refactorings.json', 
        'spring': 'spring_refactorings.json',
        'kafka': 'kafka_refactorings.json',
        'mockito': 'mockito_refactorings.json'
    }
    
    print("Extracting exactly 350 real records per project...")
    
    for domain, json_file in domains.items():
        json_path = os.path.join(data_dir, json_file)
        csv_path = os.path.join(data_dir, f'{domain}_350_real.csv')
        
        if os.path.exists(json_path):
            count = extract_350_real_data(json_path, csv_path, domain)
            print(f"✅ {domain}: {count} records → {csv_path}")
        else:
            print(f"❌ {domain}: {json_path} not found")

if __name__ == "__main__":
    main()
