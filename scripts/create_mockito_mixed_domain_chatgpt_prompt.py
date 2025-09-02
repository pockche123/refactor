#!/usr/bin/env python3
"""
Create ChatGPT prompt for Mockito mixed-domain comparison
8 files where mixed-domain ML model was correct (30.8% accuracy)
"""

import pandas as pd
import os

def get_mockito_correct_files():
    """Get the 8 files where mixed-domain model was correct"""
    
    df = pd.read_csv('results/mockito_mixed_domain_results.csv')
    correct_predictions = df[df['correct'] == True].copy()
    
    print(f"Found {len(correct_predictions)} correct predictions:")
    for i, (_, row) in enumerate(correct_predictions.iterrows(), 1):
        print(f"{i}. {row['file_path']} - {row['refactoring_type']}")
    
    return correct_predictions

def extract_source_code(correct_predictions):
    """Extract source code for the correct prediction files"""
    
    mockito_project_dir = 'complex_projects/mockito'
    
    if not os.path.exists(mockito_project_dir):
        print(f"❌ Mockito project not found at {mockito_project_dir}")
        return None
    
    code_snippets = {}
    
    print("\nExtracting source code...")
    
    for idx, (_, row) in enumerate(correct_predictions.iterrows(), 1):
        file_path = row['file_path']
        full_path = os.path.join(mockito_project_dir, file_path)
        
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                code_snippets[file_path] = {
                    'content': content,
                    'ml_prediction': row['refactoring_type'],
                    'file_name': os.path.basename(file_path)
                }
                print(f"✅ {idx}. {file_path}")
                
            except Exception as e:
                print(f"❌ {idx}. Could not read {file_path}: {e}")
        else:
            print(f"❌ {idx}. File not found: {file_path}")
    
    return code_snippets

def create_chatgpt_prompt(code_snippets):
    """Create the formatted prompt for ChatGPT"""
    
    prompt = """I'm comparing machine learning predictions with human expert suggestions for code refactoring in Mockito codebase.

For each Java file below, please suggest ONE specific refactoring that would improve the code quality. Focus on:
- Method/variable naming improvements
- Code structure improvements  
- Extracting methods/variables for clarity
- Adding helpful annotations
- Access modifier improvements

For each suggestion, provide:
1. Refactoring type (e.g., "Rename Method", "Extract Variable", "Add Method Annotation")
2. Specific details of what to change
3. Brief reasoning for why this improves the code

Here are the files with their ML predictions:

"""

    for i, (file_path, info) in enumerate(code_snippets.items(), 1):
        # Truncate very long files for readability
        content = info['content']
        if len(content) > 2000:
            lines = content.split('\n')
            if len(lines) > 80:
                content = '\n'.join(lines[:40]) + '\n\n... [truncated] ...\n\n' + '\n'.join(lines[-40:])
        
        prompt += f"""
=== FILE {i}: {file_path} ===
ML Prediction: {info['ml_prediction']}

```java
{content}
```

"""

    prompt += """
Please provide your refactoring suggestions in this format:

FILE 1: [file_path]
Refactoring: [type]
Details: [specific change]
Reasoning: [why this improves the code]

FILE 2: [file_path]
...
"""

    return prompt

def main():
    """Main function"""
    
    print("=== Mockito Mixed-Domain ChatGPT Prompt Generator ===")
    
    # Get correct predictions
    correct_predictions = get_mockito_correct_files()
    
    # Extract code snippets
    code_snippets = extract_source_code(correct_predictions)
    
    if not code_snippets:
        return
    
    print(f"\nSuccessfully extracted {len(code_snippets)} code snippets")
    
    # Create ChatGPT prompt
    prompt = create_chatgpt_prompt(code_snippets)
    
    # Save prompt to file
    with open('mockito_mixed_domain_chatgpt_prompt.txt', 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"\n✅ ChatGPT prompt saved to: mockito_mixed_domain_chatgpt_prompt.txt")
    print(f"📊 Ready for {len(code_snippets)} file comparisons")
    
    print("\nNext steps:")
    print("1. Copy the prompt from mockito_mixed_domain_chatgpt_prompt.txt")
    print("2. Send to ChatGPT and get suggestions")
    print("3. Compare ChatGPT safety vs ML safety (57.1%)")

if __name__ == "__main__":
    main()
