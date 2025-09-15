import csv
import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(csv_file, test_size=0.3, random_state=42):
    """Split dataset into 70% train, 30% test with simple random split"""
    
    # Read the dataset
    df = pd.read_csv(csv_file)
    
    # Simple random split (no stratification)
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=random_state
    )
    
    # Generate output filenames
    base_name = csv_file.replace('.csv', '')
    train_file = f"{base_name}_train.csv"
    test_file = f"{base_name}_test.csv"
    
    # Save splits
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)
    
    return len(train_df), len(test_df), train_file, test_file

def main():
    data_dir = 'data'
    
    # Find all 350_real datasets
    datasets = []
    for file in os.listdir(data_dir):
        if file.endswith('_350_real.csv'):
            datasets.append(os.path.join(data_dir, file))
    
    print("Splitting datasets 70% train / 30% test (random split)...")
    print("=" * 60)
    
    total_train = 0
    total_test = 0
    
    for dataset in sorted(datasets):
        domain = os.path.basename(dataset).replace('_350_real.csv', '')
        
        try:
            train_count, test_count, train_file, test_file = split_dataset(dataset)
            
            total_train += train_count
            total_test += test_count
            
            print(f"✅ {domain}:")
            print(f"   Total: {train_count + test_count} → Train: {train_count} | Test: {test_count}")
            print(f"   Files: {os.path.basename(train_file)} | {os.path.basename(test_file)}")
            print()
            
        except Exception as e:
            print(f"❌ {domain}: Error - {e}")
    
    print("=" * 60)
    print(f"SUMMARY: {total_train} train records | {total_test} test records")
    print("✅ Ready for ML training and LLM behavioral validation!")

if __name__ == "__main__":
    main()
