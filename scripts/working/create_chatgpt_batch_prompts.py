#!/usr/bin/env python3
"""
Create ChatGPT Batch Prompts for LLM Testing
Format multiple test cases into single prompts for manual testing
"""

import pandas as pd
import json

def create_batch_prompt(test_cases, batch_number):
    """Create a batch prompt with multiple test cases"""
    
    header = f"""You are analyzing refactoring patterns in software development. I will give you {len(test_cases)} test cases to analyze.

For each test case:
1. Carefully analyze the BEFORE and AFTER code
2. Identify the specific refactoring type applied
3. Respond with: "Test X: REFACTORING_TYPE: [exact name]"

REFACTORING TYPES TO CONSIDER:
- Extract Method, Extract Variable, Extract Class
- Inline Method, Inline Variable  
- Rename Method, Rename Variable, Rename Parameter, Rename Attribute
- Move Method, Move Class, Move Attribute
- Change Method Access Modifier, Change Parameter Type, Change Return Type, Change Variable Type
- Add Parameter, Remove Parameter, Change Parameter Type
- Add Method Annotation, Remove Method Annotation, Modify Method Annotation
- Add Parameter Annotation, Remove Parameter Annotation
- Add Class Annotation, Remove Class Annotation
- Parameterize Variable, Replace Generic With Diamond
- Split Conditional, Merge Method
- And many others...

Here are the {len(test_cases)} test cases:

"""
    
    cases_text = ""
    for i, case in enumerate(test_cases, 1):
        # Extract before/after code from the prompt
        prompt_lines = case['llm_prompt'].split('\n')
        
        # Find BEFORE and AFTER code sections
        before_start = -1
        after_start = -1
        
        for j, line in enumerate(prompt_lines):
            if 'BEFORE CODE:' in line:
                before_start = j + 1
            elif 'AFTER CODE:' in line:
                after_start = j + 1
                break
        
        # Extract the code sections
        before_code = ""
        after_code = ""
        
        if before_start > 0 and after_start > 0:
            # Get BEFORE code
            for j in range(before_start, after_start - 1):
                if j < len(prompt_lines):
                    before_code += prompt_lines[j] + "\n"
            
            # Get AFTER code  
            for j in range(after_start, len(prompt_lines)):
                if j < len(prompt_lines) and 'What specific refactoring' not in prompt_lines[j]:
                    after_code += prompt_lines[j] + "\n"
        
        cases_text += f"""
=== TEST CASE {i} ===
Project: {case['project'].upper()}
File: {case['test_id']}

BEFORE:
{before_code.strip()}

AFTER:
{after_code.strip()}

"""
    
    footer = f"""
Please analyze all {len(test_cases)} test cases above and provide your answers in this format:
Test 1: REFACTORING_TYPE: [name]
Test 2: REFACTORING_TYPE: [name]
...
Test {len(test_cases)}: REFACTORING_TYPE: [name]
"""
    
    return header + cases_text + footer

def main():
    print("🚀 CREATING CHATGPT BATCH PROMPTS")
    print("=" * 50)
    
    # Load test cases
    df = pd.read_csv('results/working/llm_ml_comparison_test_cases.csv')
    print(f"📊 Loaded {len(df)} test cases")
    
    # Create batches of 10 cases each
    batch_size = 10
    batches = []
    
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size]
        batch_cases = batch_df.to_dict('records')
        
        batch_number = (i // batch_size) + 1
        batch_prompt = create_batch_prompt(batch_cases, batch_number)
        
        batches.append({
            'batch_number': batch_number,
            'test_cases': len(batch_cases),
            'projects': list(batch_df['project'].unique()),
            'prompt': batch_prompt,
            'expected_answers': [
                f"Test {j+1}: {case['actual_refactoring_type']}" 
                for j, case in enumerate(batch_cases)
            ]
        })
        
        print(f"   Batch {batch_number}: {len(batch_cases)} cases ({', '.join(batch_df['project'].unique())})")
    
    # Save batches
    with open('results/working/chatgpt_batch_prompts.json', 'w') as f:
        json.dump(batches, f, indent=2)
    
    # Create individual batch files for easy copy-paste
    batch_dir = Path('results/working/chatgpt_batches')
    batch_dir.mkdir(exist_ok=True)
    
    for batch in batches:
        batch_file = batch_dir / f"batch_{batch['batch_number']:02d}.txt"
        with open(batch_file, 'w') as f:
            f.write(batch['prompt'])
        
        # Also create expected answers file
        answers_file = batch_dir / f"batch_{batch['batch_number']:02d}_expected.txt"
        with open(answers_file, 'w') as f:
            f.write(f"Expected answers for Batch {batch['batch_number']}:\n\n")
            for answer in batch['expected_answers']:
                f.write(answer + "\n")
    
    print(f"\n✅ Created {len(batches)} batch prompts")
    print(f"✅ results/working/chatgpt_batch_prompts.json")
    print(f"✅ results/working/chatgpt_batches/ (individual files)")
    
    # Show first batch as example
    print(f"\n📋 BATCH 1 PREVIEW (first 500 chars):")
    print(batches[0]['prompt'][:500] + "...")
    
    print(f"\n🎯 USAGE INSTRUCTIONS:")
    print(f"   1. Copy content from batch_01.txt")
    print(f"   2. Paste into ChatGPT")
    print(f"   3. Compare results with batch_01_expected.txt")
    print(f"   4. Repeat for all {len(batches)} batches")
    print(f"   5. Calculate accuracy: correct/total per batch")

if __name__ == "__main__":
    from pathlib import Path
    main()
