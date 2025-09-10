#!/usr/bin/env python3
"""
Create LLM Comparison Test Set
Select representative examples from our validated test cases for LLM accuracy comparison
"""

import pandas as pd
import random
from pathlib import Path

def load_all_correct_predictions():
    """Load correct predictions from all models"""
    
    # Individual model results
    commons_lang_df = pd.read_csv('results/working/commons_lang_ml_test_results_350.csv')
    commons_lang_correct = commons_lang_df[commons_lang_df['correct_prediction'] == True]
    commons_lang_correct['model_type'] = 'individual'
    
    intellij_df = pd.read_csv('results/working/intellij_ml_test_results_350.csv')
    intellij_correct = intellij_df[intellij_df['correct_prediction'] == True]
    intellij_correct['model_type'] = 'individual'
    intellij_correct['project'] = 'intellij'
    
    kafka_df = pd.read_csv('results/working/kafka_ml_test_results_350.csv')
    kafka_correct = kafka_df[kafka_df['correct_prediction'] == True]
    kafka_correct['model_type'] = 'individual'
    kafka_correct['project'] = 'kafka'
    
    spring_df = pd.read_csv('results/working/spring_ml_test_results_350.csv')
    spring_correct = spring_df[spring_df['correct_prediction'] == True]
    spring_correct['model_type'] = 'individual'
    spring_correct['project'] = 'spring'
    
    mockito_df = pd.read_csv('results/working/mockito_ml_test_results_350.csv')
    mockito_correct = mockito_df[mockito_df['correct_prediction'] == True]
    mockito_correct['model_type'] = 'individual'
    mockito_correct['project'] = 'mockito'
    
    # Mixed model results
    mixed_df = pd.read_csv('results/working/mixed_ml_test_results_1750.csv')
    mixed_correct = mixed_df[mixed_df['correct_prediction'] == True]
    mixed_correct['model_type'] = 'mixed'
    
    return {
        'commons_lang': commons_lang_correct,
        'intellij': intellij_correct,
        'kafka': kafka_correct,
        'spring': spring_correct,
        'mockito': mockito_correct,
        'mixed': mixed_correct
    }

def select_representative_examples(correct_predictions, n_per_domain=8):
    """Select representative examples for LLM testing"""
    
    test_cases = []
    
    # Individual models
    for project, df in correct_predictions.items():
        if project == 'mixed':
            continue
            
        print(f"\n📊 {project.upper()} - Selecting {n_per_domain} examples:")
        
        # Get top refactoring types
        top_types = df['refactoring_type'].value_counts().head(5)
        print(f"   Top refactoring types: {list(top_types.index)}")
        
        # Select examples from different refactoring types
        selected = []
        for ref_type in top_types.index:
            type_examples = df[df['refactoring_type'] == ref_type]
            if len(type_examples) > 0:
                # Select 1-2 examples per type
                n_select = min(2, len(type_examples), n_per_domain - len(selected))
                if n_select > 0:
                    sample = type_examples.sample(n=n_select, random_state=42)
                    selected.extend(sample.to_dict('records'))
        
        # Fill remaining slots with random examples
        while len(selected) < n_per_domain and len(selected) < len(df):
            remaining = df[~df.index.isin([s['index'] if 'index' in s else i for i, s in enumerate(selected)])]
            if len(remaining) > 0:
                additional = remaining.sample(n=1, random_state=42 + len(selected))
                selected.extend(additional.to_dict('records'))
            else:
                break
        
        # Add project info and create test cases
        for i, example in enumerate(selected[:n_per_domain]):
            test_case = {
                'test_id': f"{project}_{i+1}",
                'project': project,
                'domain': get_domain_name(project),
                'refactoring_type': example['refactoring_type'],
                'file_path': example['file_path'],
                'ml_prediction': example['predicted_type'],
                'ml_correct': example['correct_prediction'],
                'model_type': 'individual'
            }
            test_cases.append(test_case)
            print(f"   {i+1}. {example['refactoring_type']}")
    
    return test_cases

def get_domain_name(project):
    """Get domain name for project"""
    domains = {
        'commons_lang': 'Utility Library',
        'intellij': 'IDE',
        'kafka': 'Distributed Systems',
        'spring': 'Enterprise Framework',
        'mockito': 'Testing Framework'
    }
    return domains.get(project, 'Unknown')

def create_llm_test_prompts(test_cases):
    """Create prompts for LLM testing"""
    
    prompts = []
    
    for test_case in test_cases:
        # Create simplified before/after code examples
        before_code, after_code = generate_code_example(test_case)
        
        prompt = {
            'test_id': test_case['test_id'],
            'project': test_case['project'],
            'domain': test_case['domain'],
            'actual_refactoring': test_case['refactoring_type'],
            'before_code': before_code,
            'after_code': after_code,
            'llm_prompt': f"""
I will show you two versions of Java code - before and after a refactoring. Please identify the specific type of refactoring that was applied.

BEFORE:
```java
{before_code}
```

AFTER:
```java
{after_code}
```

What type of refactoring was applied? Please provide just the refactoring type name (e.g., "Extract Method", "Rename Variable", "Change Parameter Type", etc.).
"""
        }
        prompts.append(prompt)
    
    return prompts

def generate_code_example(test_case):
    """Generate simplified before/after code examples based on refactoring type"""
    
    project = test_case['project']
    refactoring_type = test_case['refactoring_type']
    test_id = test_case['test_id']
    
    # Get appropriate class name for domain
    class_names = {
        'commons_lang': 'StringUtils',
        'intellij': 'IDEComponent',
        'kafka': 'StreamProcessor',
        'spring': 'SpringService',
        'mockito': 'TestHelper'
    }
    class_name = class_names.get(project, 'Component')
    
    # Generate code based on refactoring type
    if 'Extract Method' in refactoring_type:
        before = f"""public class {class_name} {{
    public void processData() {{
        // Validate input
        if (data == null || data.isEmpty()) {{
            throw new IllegalArgumentException("Data cannot be null or empty");
        }}
        
        // Process the data
        String result = data.toUpperCase().trim();
        System.out.println("Processed: " + result);
    }}
}}"""
        
        after = f"""public class {class_name} {{
    public void processData() {{
        validateInput(data);
        
        // Process the data
        String result = data.toUpperCase().trim();
        System.out.println("Processed: " + result);
    }}
    
    private void validateInput(String data) {{
        if (data == null || data.isEmpty()) {{
            throw new IllegalArgumentException("Data cannot be null or empty");
        }}
    }}
}}"""
    
    elif 'Rename Method' in refactoring_type:
        before = f"""public class {class_name} {{
    public void processData() {{
        System.out.println("Processing data");
    }}
    
    public String getInfo() {{
        return "Component info";
    }}
}}"""
        
        after = f"""public class {class_name} {{
    public void handleData() {{
        System.out.println("Processing data");
    }}
    
    public String getInfo() {{
        return "Component info";
    }}
}}"""
    
    elif 'Change Variable Type' in refactoring_type:
        before = f"""public class {class_name} {{
    public void processData() {{
        String count = "5";
        System.out.println("Processing " + count + " items");
    }}
}}"""
        
        after = f"""public class {class_name} {{
    public void processData() {{
        int count = 5;
        System.out.println("Processing " + count + " items");
    }}
}}"""
    
    elif 'Remove Parameter' in refactoring_type:
        before = f"""public class {class_name} {{
    public void processData(String context) {{
        System.out.println("Processing data with context: " + context);
    }}
}}"""
        
        after = f"""public class {class_name} {{
    public void processData() {{
        System.out.println("Processing data with context: default");
    }}
}}"""
    
    elif 'Add Method Annotation' in refactoring_type:
        before = f"""public class {class_name} {{
    public void processData() {{
        System.out.println("Processing data");
    }}
}}"""
        
        after = f"""public class {class_name} {{
    @Override
    public void processData() {{
        System.out.println("Processing data");
    }}
}}"""
    
    else:
        # Generic example
        before = f"""public class {class_name} {{
    public void processData() {{
        System.out.println("Processing data");
    }}
    
    public String getInfo() {{
        return "Component info";
    }}
}}"""
        
        after = f"""public class {class_name} {{
    public void processData() {{
        System.out.println("Processing data - modified");
    }}
    
    public String getInfo() {{
        return "Component info";
    }}
}}"""
    
    return before, after

def main():
    print("🚀 CREATING LLM COMPARISON TEST SET")
    print("=" * 50)
    
    # Load all correct predictions
    print("📊 Loading correct predictions from all models...")
    correct_predictions = load_all_correct_predictions()
    
    for project, df in correct_predictions.items():
        if project != 'mixed':
            print(f"   {project}: {len(df)} correct predictions")
    
    # Select representative examples
    print(f"\n🎯 Selecting representative examples for LLM testing...")
    test_cases = select_representative_examples(correct_predictions, n_per_domain=8)
    
    print(f"\n✅ Selected {len(test_cases)} test cases total")
    
    # Create LLM prompts
    print("📝 Creating LLM test prompts...")
    prompts = create_llm_test_prompts(test_cases)
    
    # Save test set
    test_df = pd.DataFrame(test_cases)
    test_df.to_csv('results/working/llm_comparison_test_set.csv', index=False)
    
    # Save prompts
    prompts_df = pd.DataFrame(prompts)
    prompts_df.to_csv('results/working/llm_comparison_prompts.csv', index=False)
    
    print(f"✅ results/working/llm_comparison_test_set.csv")
    print(f"✅ results/working/llm_comparison_prompts.csv")
    
    # Summary
    print(f"\n📈 LLM COMPARISON TEST SET SUMMARY:")
    print(f"   Total test cases: {len(test_cases)}")
    print(f"   Projects covered: {len(set(tc['project'] for tc in test_cases))}")
    print(f"   Refactoring types: {len(set(tc['refactoring_type'] for tc in test_cases))}")
    
    # Show distribution
    project_counts = {}
    for tc in test_cases:
        project_counts[tc['project']] = project_counts.get(tc['project'], 0) + 1
    
    print(f"\n📊 Test case distribution:")
    for project, count in project_counts.items():
        print(f"   {project}: {count} cases")
    
    print(f"\n🎯 Ready for LLM accuracy comparison!")
    print(f"   White box (ML models) vs Black box (LLMs)")
    print(f"   Test with GPT-4, Claude, GitHub Copilot")

if __name__ == "__main__":
    main()
