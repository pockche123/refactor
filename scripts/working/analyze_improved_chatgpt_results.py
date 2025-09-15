#!/usr/bin/env python3
"""
Analyze Improved ChatGPT Results
Compare domain-aware ChatGPT vs original ChatGPT vs ML model
"""

import pandas as pd
from pathlib import Path
from collections import Counter

def analyze_improved_results():
    """Analyze improved ChatGPT performance"""
    
    results_dir = Path("results/working")
    
    # Load comparison template
    comparison_file = results_dir / "intellij_simple_ml_vs_llm_comparison.csv"
    df = pd.read_csv(comparison_file)
    
    # New ChatGPT predictions (domain-aware)
    improved_chatgpt_predictions = [
        "Add Method Annotation", "Add Method Annotation", "Add Parameter Annotation", "Add Parameter Annotation", "Add Method Annotation",
        "Add Method Annotation", "Extract Variable", "Add Parameter Annotation", "Add Method Annotation", "Add Parameter Annotation",
        "Add Method Annotation", "Add Method Annotation", "Extract Method", "Extract Method", "Rename Method",
        "Add Parameter Annotation", "Add Parameter Annotation", "Add Method Annotation", "Add Parameter Annotation", "Rename Method",
        "Rename Method", "Extract Variable", "Extract Variable", "Add Method Annotation", "Add Parameter Annotation",
        "Add Parameter Annotation", "Add Method Annotation", "Extract Variable", "Rename Method", "Add Parameter Annotation",
        "Add Method Annotation", "Rename Method", "Extract Variable", "Add Parameter Annotation", "Extract Variable",
        "Extract Method", "Rename Method", "Add Method Annotation", "Add Parameter Annotation", "Add Parameter Annotation",
        "Add Parameter Annotation", "Extract Variable", "Add Method Annotation", "Add Method Annotation", "Add Parameter Annotation",
        "Add Method Annotation", "Extract Method", "Add Parameter Annotation", "Extract Method", "Add Method Annotation",
        "Extract Variable", "Add Parameter Annotation", "Add Method Annotation", "Add Method Annotation", "Add Parameter Annotation",
        "Add Parameter Annotation", "Add Parameter Annotation", "Add Parameter Annotation", "Add Parameter Annotation", "Rename Method",
        "Add Parameter Annotation", "Extract Variable", "Add Method Annotation", "Add Method Annotation", "Rename Method",
        "Add Parameter Annotation", "Add Method Annotation", "Add Parameter Annotation", "Add Parameter Annotation", "Add Parameter Annotation",
        "Extract Variable", "Add Parameter Annotation", "Add Parameter Annotation", "Add Parameter Annotation", "Add Method Annotation",
        "Add Parameter Annotation", "Add Parameter Annotation", "Add Method Annotation", "Add Method Annotation", "Add Parameter Annotation",
        "Add Parameter Annotation", "Add Parameter Annotation", "Add Method Annotation", "Add Parameter Annotation", "Extract Method",
        "Add Method Annotation", "Add Parameter Annotation", "Rename Method", "Add Method Annotation", "Add Method Annotation",
        "Extract Variable", "Add Method Annotation", "Add Parameter Annotation", "Rename Method", "Add Method Annotation",
        "Extract Variable", "Add Method Annotation", "Add Parameter Annotation", "Extract Variable", "Add Parameter Annotation",
        "Add Parameter Annotation", "Add Parameter Annotation", "Extract Variable", "Add Parameter Annotation", "Add Method Annotation"
    ]
    
    # Update dataframe with improved predictions
    df['improved_llm_prediction'] = improved_chatgpt_predictions[:len(df)]
    df['improved_llm_correct'] = df['improved_llm_prediction'] == df['actual_refactoring']
    
    # Calculate accuracies
    ml_accuracy = df['ml_correct'].mean() * 100
    original_llm_accuracy = df['llm_correct'].mean() * 100
    improved_llm_accuracy = df['improved_llm_correct'].mean() * 100
    
    ml_correct = df['ml_correct'].sum()
    original_llm_correct = df['llm_correct'].sum()
    improved_llm_correct = df['improved_llm_correct'].sum()
    total_cases = len(df)
    
    print("=== INTELLIJ: ML vs ORIGINAL vs IMPROVED CHATGPT ===")
    print(f"Total test cases: {total_cases}")
    print(f"\nFINAL ACCURACY COMPARISON:")
    print(f"Your ML Model:        {ml_accuracy:.1f}% ({ml_correct}/{total_cases})")
    print(f"Original ChatGPT:     {original_llm_accuracy:.1f}% ({original_llm_correct}/{total_cases})")
    print(f"Improved ChatGPT:     {improved_llm_accuracy:.1f}% ({improved_llm_correct}/{total_cases})")
    
    print(f"\nIMPROVEMENT:")
    improvement = improved_llm_accuracy - original_llm_accuracy
    print(f"ChatGPT improvement: +{improvement:.1f} percentage points")
    
    if improved_llm_accuracy > ml_accuracy:
        print(f"🏆 IMPROVED LLM WINS by {improved_llm_accuracy - ml_accuracy:.1f} percentage points!")
    elif ml_accuracy > improved_llm_accuracy:
        print(f"🏆 ML STILL WINS by {ml_accuracy - improved_llm_accuracy:.1f} percentage points!")
    else:
        print(f"🤝 TIE at {ml_accuracy:.1f}% accuracy!")
    
    # Analyze improved ChatGPT's prediction patterns
    print(f"\n=== IMPROVED CHATGPT PREDICTION ANALYSIS ===")
    improved_counts = Counter(improved_chatgpt_predictions)
    actual_counts = Counter(df['actual_refactoring'])
    
    print(f"Improved ChatGPT predicted:")
    for pred, count in improved_counts.most_common():
        print(f"  {pred}: {count} times ({count/total_cases*100:.1f}%)")
    
    print(f"\nActual refactoring types:")
    for actual, count in actual_counts.most_common()[:5]:  # Top 5
        print(f"  {actual}: {count} times ({count/total_cases*100:.1f}%)")
    
    # Check if improved ChatGPT learned the dominant pattern
    improved_dominant = improved_counts.most_common(1)[0][0]
    actual_dominant = actual_counts.most_common(1)[0][0]
    
    print(f"\n=== PATTERN RECOGNITION ===")
    print(f"Improved ChatGPT dominant: {improved_dominant} ({improved_counts[improved_dominant]} times)")
    print(f"Actual dominant type: {actual_dominant} ({actual_counts[actual_dominant]} times)")
    
    if improved_dominant == actual_dominant:
        print("✅ Improved ChatGPT correctly identified the dominant pattern!")
    else:
        print("❌ Still missed the dominant pattern")
    
    # Performance by refactoring type for top types
    print(f"\n=== ACCURACY BY REFACTORING TYPE (Top Types) ===")
    for ref_type in ['Add Parameter Annotation', 'Change Method Access Modifier', 'Add Attribute Annotation']:
        subset = df[df['actual_refactoring'] == ref_type]
        if len(subset) > 0:
            ml_acc = subset['ml_correct'].mean() * 100
            orig_llm_acc = subset['llm_correct'].mean() * 100
            impr_llm_acc = subset['improved_llm_correct'].mean() * 100
            
            print(f"{ref_type} ({len(subset)} cases):")
            print(f"  ML: {ml_acc:.1f}%, Original LLM: {orig_llm_acc:.1f}%, Improved LLM: {impr_llm_acc:.1f}%")
    
    # Agreement analysis
    both_ml_improved = (df['ml_correct'] & df['improved_llm_correct']).sum()
    ml_only = (df['ml_correct'] & ~df['improved_llm_correct']).sum()
    improved_only = (~df['ml_correct'] & df['improved_llm_correct']).sum()
    both_wrong = (~df['ml_correct'] & ~df['improved_llm_correct']).sum()
    
    print(f"\n=== ML vs IMPROVED LLM AGREEMENT ===")
    print(f"Both correct: {both_ml_improved}/{total_cases} ({both_ml_improved/total_cases*100:.1f}%)")
    print(f"ML only correct: {ml_only}/{total_cases} ({ml_only/total_cases*100:.1f}%)")
    print(f"Improved LLM only: {improved_only}/{total_cases} ({improved_only/total_cases*100:.1f}%)")
    print(f"Both wrong: {both_wrong}/{total_cases} ({both_wrong/total_cases*100:.1f}%)")
    
    # Save updated results
    updated_file = results_dir / "intellij_ml_vs_improved_llm_final_results.csv"
    df.to_csv(updated_file, index=False)
    print(f"\n📊 Updated results saved to: {updated_file}")
    
    return {
        'ml_accuracy': ml_accuracy,
        'original_llm_accuracy': original_llm_accuracy,
        'improved_llm_accuracy': improved_llm_accuracy,
        'improvement': improvement
    }

if __name__ == "__main__":
    results = analyze_improved_results()
