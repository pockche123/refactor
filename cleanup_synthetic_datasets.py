import os
import csv

def is_synthetic_dataset(csv_file):
    """Check if dataset is synthetic/invalid"""
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            first_row = next(reader, None)
            
            if not first_row:
                return True, "Empty file"
            
            commit_sha = first_row.get('commit_sha', '')
            
            # Check for synthetic patterns
            if commit_sha.startswith('dummy_commit'):
                return True, f"Dummy commit: {commit_sha}"
            elif not commit_sha:
                return True, "No commit_sha column"
            else:
                return False, "Has real commit_sha"
                
    except Exception as e:
        return True, f"Error reading file: {e}"

def main():
    data_dir = 'data'
    synthetic_files = []
    real_files = []
    
    print("Analyzing datasets...")
    
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(data_dir, file)
            is_synthetic, reason = is_synthetic_dataset(file_path)
            
            if is_synthetic:
                synthetic_files.append((file, reason))
            else:
                real_files.append(file)
    
    print(f"\n✅ REAL DATASETS ({len(real_files)}):")
    for file in sorted(real_files):
        print(f"  {file}")
    
    print(f"\n❌ SYNTHETIC/INVALID DATASETS ({len(synthetic_files)}):")
    for file, reason in sorted(synthetic_files):
        print(f"  {file} - {reason}")
    
    if synthetic_files:
        print(f"\nDelete {len(synthetic_files)} synthetic datasets? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            for file, _ in synthetic_files:
                file_path = os.path.join(data_dir, file)
                os.remove(file_path)
                print(f"Deleted: {file}")
            print(f"\n✅ Cleaned up {len(synthetic_files)} synthetic datasets")
        else:
            print("No files deleted")

if __name__ == "__main__":
    main()
