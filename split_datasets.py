import csv
import os
from sklearn.model_selection import train_test_split
import pandas as pd

def split_dataset(csv_file, test_size=0.3, random_state=42):
    """Split dataset into 70% train, 30% test"""
    
    # Read the dataset
    df = pd.read_csv(csv_file)
    
    # Split 70-30
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=random_state,
        stratify=df['refactoring_type'] if len(df['refactoring_type'].unique()) > 1 else None
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
    
    print("Splitting datasets 70% train / 30% test...")
    print("=" * 50)
    
    for dataset in sorted(datasets):
        domain = os.path.basename(dataset).replace('_350_real.csv', '')
        
        try:
            train_count, test_count, train_file, test_file = split_dataset(dataset)
            
            print(f"✅ {domain}:")
            print(f"   Total: {train_count + test_count} records")
            print(f"   Train: {train_count} records → {os.path.basename(train_file)}")
            print(f"   Test:  {test_count} records → {os.path.basename(test_file)}")
            print()
            
        except Exception as e:
            print(f"❌ {domain}: Error - {e}")
    
    print("=" * 50)
    print("Split complete! Use test sets for behavioral validation.")

if __name__ == "__main__":
    main()
