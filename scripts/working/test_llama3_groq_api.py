#!/usr/bin/env python3
"""
Test Llama 3 via Groq API on our 525 refactoring test cases
Direct comparison: ML Models vs Llama 3 LLM
"""

import pandas as pd
import requests
import json
import time
from pathlib import Path
import os

def setup_groq_client():
    """Setup Groq API client"""
    
    # You'll need to get a free API key from https://console.groq.com/
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ Please set GROQ_API_KEY environment variable")
        print("   1. Go to https://console.groq.com/")
        print("   2. Sign up for free account")
        print("   3. Get API key")
        print("   4. Set: export GROQ_API_KEY='your-key-here'")
        return None
    
    return {
        'api_key': api_key,
        'base_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.1-8b-instant'  # Updated to current Llama 3.1 model
    }

def create_llama_prompt(test_case):
    """Create optimized prompt for Llama 3"""
    
    # Extract before/after code from the original prompt
    original_prompt = test_case['llm_prompt']
    
    # Find the code sections
    lines = original_prompt.split('\n')
    before_code = ""
    after_code = ""
    
    in_before = False
    in_after = False
    
    for line in lines:
        if 'BEFORE CODE:' in line:
            in_before = True
            in_after = False
            continue
        elif 'AFTER CODE:' in line:
            in_before = False
            in_after = True
            continue
        elif 'What specific refactoring' in line:
            break
        
        if in_before and line.strip():
            before_code += line + "\n"
        elif in_after and line.strip():
            after_code += line + "\n"
    
    # Create concise prompt for Llama 3
    prompt = f"""Analyze these two Java code versions and identify the refactoring type.

PROJECT: {test_case['project'].upper()}

BEFORE:
{before_code.strip()}

AFTER:
{after_code.strip()}

REFACTORING TYPES:
Extract Method, Rename Method, Change Variable Type, Add Method Annotation, Remove Method Annotation, Change Parameter Type, Remove Parameter, Add Parameter Annotation, Parameterize Variable, Change Return Type, Move Method, Extract Variable, Inline Method, Change Method Access Modifier, and others.

TASK: What specific refactoring was applied? Respond with only: "REFACTORING_TYPE: [exact name]"
"""
    
    return prompt

def call_groq_api(client, prompt, max_retries=3):
    """Call Groq API with retry logic"""
    
    headers = {
        'Authorization': f'Bearer {client["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': client['model'],
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'max_tokens': 100,
        'temperature': 0.1  # Low temperature for consistent results
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(client['base_url'], headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            elif response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt
                print(f"   Rate limit hit, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"   API error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"   Request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    return None

def extract_refactoring_type(llm_response):
    """Extract refactoring type from LLM response"""
    
    if not llm_response:
        return "NO_RESPONSE"
    
    # Look for "REFACTORING_TYPE: " pattern
    if "REFACTORING_TYPE:" in llm_response:
        parts = llm_response.split("REFACTORING_TYPE:")
        if len(parts) > 1:
            return parts[1].strip()
    
    # Fallback: return the whole response
    return llm_response.strip()

def test_sample_cases(client, test_cases, n_sample=10):
    """Test a small sample first"""
    
    print(f"🧪 Testing {n_sample} sample cases with Llama 3...")
    
    sample_cases = test_cases.head(n_sample)
    results = []
    
    for i, (_, test_case) in enumerate(sample_cases.iterrows()):
        print(f"   Testing case {i+1}/{n_sample}: {test_case['project']} - {test_case['actual_refactoring_type']}")
        
        # Create prompt
        prompt = create_llama_prompt(test_case)
        
        # Call API
        llm_response = call_groq_api(client, prompt)
        predicted_type = extract_refactoring_type(llm_response)
        
        # Check accuracy
        is_correct = predicted_type.lower() == test_case['actual_refactoring_type'].lower()
        
        result = {
            'test_id': test_case['test_id'],
            'project': test_case['project'],
            'actual_type': test_case['actual_refactoring_type'],
            'predicted_type': predicted_type,
            'llm_response': llm_response,
            'correct': is_correct
        }
        
        results.append(result)
        
        print(f"      Expected: {test_case['actual_refactoring_type']}")
        print(f"      Predicted: {predicted_type}")
        print(f"      Correct: {'✅' if is_correct else '❌'}")
        
        # Small delay to respect rate limits
        time.sleep(0.1)
    
    return results

def test_all_cases(client, test_cases):
    """Test all 525 cases"""
    
    print(f"🚀 Testing ALL {len(test_cases)} cases with Llama 3...")
    
    results = []
    correct_count = 0
    
    for i, (_, test_case) in enumerate(test_cases.iterrows()):
        if i % 50 == 0:
            print(f"   Progress: {i}/{len(test_cases)} ({i/len(test_cases)*100:.1f}%)")
        
        # Create prompt
        prompt = create_llama_prompt(test_case)
        
        # Call API
        llm_response = call_groq_api(client, prompt)
        predicted_type = extract_refactoring_type(llm_response)
        
        # Check accuracy
        is_correct = predicted_type.lower() == test_case['actual_refactoring_type'].lower()
        if is_correct:
            correct_count += 1
        
        result = {
            'test_id': test_case['test_id'],
            'project': test_case['project'],
            'actual_type': test_case['actual_refactoring_type'],
            'predicted_type': predicted_type,
            'llm_response': llm_response,
            'correct': is_correct
        }
        
        results.append(result)
        
        # Small delay to respect rate limits
        time.sleep(0.05)
    
    accuracy = correct_count / len(test_cases) * 100
    print(f"\n✅ Completed! Overall accuracy: {accuracy:.1f}% ({correct_count}/{len(test_cases)})")
    
    return results

def analyze_results(results):
    """Analyze Llama 3 results"""
    
    results_df = pd.DataFrame(results)
    
    print(f"\n📊 LLAMA 3 RESULTS ANALYSIS:")
    
    # Overall accuracy
    overall_accuracy = results_df['correct'].mean() * 100
    print(f"   Overall Accuracy: {overall_accuracy:.1f}%")
    
    # Per-project accuracy
    print(f"\n📊 Per-Project Accuracy:")
    project_accuracy = results_df.groupby('project')['correct'].agg(['count', 'sum', 'mean'])
    for project, stats in project_accuracy.iterrows():
        accuracy = stats['mean'] * 100
        print(f"   {project.upper()}: {accuracy:.1f}% ({stats['sum']}/{stats['count']})")
    
    # Per-refactoring-type accuracy
    print(f"\n📊 Top 10 Refactoring Types by Frequency:")
    type_accuracy = results_df.groupby('actual_type')['correct'].agg(['count', 'sum', 'mean']).sort_values('count', ascending=False)
    for ref_type, stats in type_accuracy.head(10).iterrows():
        accuracy = stats['mean'] * 100
        print(f"   {ref_type}: {accuracy:.1f}% ({stats['sum']}/{stats['count']})")
    
    return results_df

def main():
    print("🚀 LLAMA 3 vs ML MODELS COMPARISON")
    print("=" * 50)
    
    # Setup Groq client
    print("🔧 Setting up Groq API client...")
    client = setup_groq_client()
    if not client:
        return
    
    print(f"✅ Using model: {client['model']}")
    
    # Load test cases
    print("📊 Loading test cases...")
    test_cases = pd.read_csv('results/working/llm_ml_comparison_test_cases.csv')
    print(f"   Loaded {len(test_cases)} test cases")
    
    # Ask user preference
    print(f"\nChoose testing approach:")
    print(f"   1. Sample test (10 cases) - Quick validation")
    print(f"   2. Full test (525 cases) - Complete comparison")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Test sample
        results = test_sample_cases(client, test_cases, n_sample=10)
    else:
        # Test all cases
        results = test_all_cases(client, test_cases)
    
    # Analyze results
    results_df = analyze_results(results)
    
    # Save results
    output_file = 'results/working/llama3_groq_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Results saved: {output_file}")
    
    # Compare with ML models
    print(f"\n🔬 COMPARISON WITH ML MODELS:")
    print(f"   Llama 3 Accuracy: {results_df['correct'].mean()*100:.1f}%")
    print(f"   ML Model Accuracies:")
    print(f"     Commons Lang: 96.3%")
    print(f"     IntelliJ: 78.9%")
    print(f"     Kafka: 73.7%")
    print(f"     Spring: 69.4%")
    print(f"     Mockito: 56.9%")
    print(f"     Mixed Model: 74.6%")

if __name__ == "__main__":
    main()
