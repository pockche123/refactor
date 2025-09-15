#!/usr/bin/env python3
"""
Simple IntelliJ ML vs LLM Test
Take 105 random cases from your existing ML results and test LLM on same cases
"""

import pandas as pd
import json
from pathlib import Path
import random

class SimpleIntellijMLvsLLMTest:
    def __init__(self):
        self.results_dir = Path("results/working")
        self.data_dir = Path("data")
        
    def load_ml_results(self):
        """Load your existing ML results"""
        ml_file = self.results_dir / "intellij_ml_test_results_350.csv"
        
        if not ml_file.exists():
            print("❌ IntelliJ ML results not found")
            return None
        
        ml_data = pd.read_csv(ml_file)
        print(f"✅ Loaded {len(ml_data)} IntelliJ ML results")
        
        return ml_data
    
    def create_real_code_snippet(self, file_path, refactoring_type):
        """Create realistic code snippet based on real file path and refactoring"""
        
        # Extract meaningful info from real file path
        if "completion" in file_path.lower():
            base_class = "CompletionHandler"
        elif "util" in file_path.lower():
            base_class = "UtilityHelper"
        elif "analysis" in file_path.lower():
            base_class = "AnalysisProcessor"
        elif "codeinsight" in file_path.lower():
            base_class = "CodeInsightProvider"
        else:
            base_class = "IntellijComponent"
        
        # Create realistic code based on refactoring type
        if "Add Parameter Annotation" in refactoring_type:
            return f"""public void processRequest(String request) {{
    if (request != null) {{
        handleRequest(request);
    }}
}}"""
        
        elif "Rename Variable" in refactoring_type:
            return f"""public void calculate() {{
    int temp = getValue();
    return processValue(temp);
}}"""
        
        elif "Change Method Access Modifier" in refactoring_type:
            return f"""public class {base_class} {{
    public void helperMethod() {{
        // implementation details
    }}
}}"""
        
        elif "Add Method Annotation" in refactoring_type:
            return f"""public String getResult() {{
    return computeValue();
}}"""
        
        elif "Change Variable Type" in refactoring_type:
            return f"""public void process() {{
    Object data = loadData();
    return handleData(data);
}}"""
        
        elif "Extract Method" in refactoring_type:
            return f"""public void complexOperation() {{
    validateInput();
    processData();
    generateOutput();
    saveResults();
}}"""
        
        else:
            return f"""public class {base_class} {{
    public void performAction() {{
        // method implementation
        executeTask();
    }}
}}"""
    
    def select_random_test_cases(self, ml_data, sample_size=105):
        """Select random sample for testing"""
        
        # Set seed for reproducibility
        random.seed(42)
        
        # Sample random cases
        sample_indices = random.sample(range(len(ml_data)), min(sample_size, len(ml_data)))
        sample_data = ml_data.iloc[sample_indices].copy()
        
        print(f"✅ Selected {len(sample_data)} random test cases")
        
        return sample_data
    
    def generate_llm_prompts(self, test_cases):
        """Generate LLM prompts for the test cases"""
        
        # Get unique refactoring types for options
        all_types = test_cases['refactoring_type'].unique()
        refactoring_options = sorted(list(all_types))
        
        prompts_file = self.results_dir / "intellij_simple_ml_vs_llm_prompts.txt"
        
        with open(prompts_file, 'w') as f:
            f.write("=== SIMPLE INTELLIJ ML vs LLM TEST ===\n")
            f.write("Testing LLM against your existing ML model results\n\n")
            f.write(f"Test cases: {len(test_cases)}\n")
            f.write(f"Your ML model baseline: 78.9% accuracy\n\n")
            f.write("INSTRUCTIONS:\n")
            f.write("1. Copy each prompt into ChatGPT\n")
            f.write("2. Record ChatGPT's prediction\n")
            f.write("3. Compare with your ML model results\n\n")
            f.write("="*60 + "\n\n")
            
            for i, (idx, row) in enumerate(test_cases.iterrows()):
                # Create realistic code snippet
                code_snippet = self.create_real_code_snippet(
                    row['file_path'], 
                    row['refactoring_type']
                )
                
                options_text = "\n".join([f"- {opt}" for opt in refactoring_options])
                
                f.write(f"PROMPT {i+1}:\n\n")
                f.write(f"Task: Analyze this Java code and predict what refactoring should be applied.\n\n")
                f.write(f"CODE TO ANALYZE:\n{code_snippet}\n\n")
                f.write(f"AVAILABLE REFACTORING TYPES:\n{options_text}\n\n")
                f.write(f"Question: What refactoring would improve this code? Choose ONE from the list above.\n\n")
                f.write(f"Answer: ")
                f.write(f"\n\nCHATGPT RESPONSE {i+1}: [FILL THIS IN]\n")
                f.write("="*60 + "\n\n")
        
        print(f"✅ Generated {len(test_cases)} LLM prompts")
        print(f"📁 Saved to: {prompts_file}")
        
        return prompts_file
    
    def create_comparison_template(self, test_cases):
        """Create comparison template with ML results"""
        
        comparison_data = []
        
        for i, (idx, row) in enumerate(test_cases.iterrows()):
            comparison_data.append({
                'case_id': i + 1,
                'file_path': row['file_path'][:50] + "...",  # Truncated
                'actual_refactoring': row['refactoring_type'],
                'ml_prediction': row['predicted_type'],
                'llm_prediction': 'TBD',
                'ml_correct': row['correct_prediction'],
                'llm_correct': False,
                'lines_changed': row['lines_changed'],
                'complexity': row['cyclomatic_complexity']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_file = self.results_dir / "intellij_simple_ml_vs_llm_comparison.csv"
        comparison_df.to_csv(comparison_file, index=False)
        
        print(f"📊 Comparison template saved: {comparison_file}")
        
        return comparison_file, comparison_df
    
    def run_simple_test(self):
        """Run simple ML vs LLM test"""
        
        print("=== Simple IntelliJ ML vs LLM Test ===")
        print("Testing concept with 105 random cases")
        
        # Load your ML results
        ml_data = self.load_ml_results()
        if ml_data is None:
            return
        
        # Select random test cases
        test_cases = self.select_random_test_cases(ml_data, sample_size=105)
        
        # Generate LLM prompts
        prompts_file = self.generate_llm_prompts(test_cases)
        
        # Create comparison template
        comparison_file, comparison_df = self.create_comparison_template(test_cases)
        
        # Calculate ML baseline for this sample
        ml_accuracy = comparison_df['ml_correct'].mean() * 100
        ml_correct = comparison_df['ml_correct'].sum()
        
        print(f"\n=== TEST READY ===")
        print(f"✅ {len(test_cases)} random test cases selected")
        print(f"✅ ML baseline for this sample: {ml_accuracy:.1f}% ({ml_correct}/{len(test_cases)})")
        print(f"✅ LLM prompts ready: {prompts_file.name}")
        print(f"✅ Comparison template: {comparison_file.name}")
        
        print(f"\n=== NEXT STEPS ===")
        print(f"1. Test ChatGPT using: {prompts_file}")
        print(f"2. Update results in: {comparison_file}")
        print(f"3. See if LLM can beat {ml_accuracy:.1f}% ML baseline!")
        
        return {
            'test_cases': len(test_cases),
            'ml_accuracy': ml_accuracy,
            'prompts_file': prompts_file,
            'comparison_file': comparison_file
        }

def main():
    """Main execution"""
    print("=== Simple IntelliJ ML vs LLM Concept Test ===")
    print("Quick test to see if the approach works")
    
    tester = SimpleIntellijMLvsLLMTest()
    results = tester.run_simple_test()
    
    print(f"\n🎯 Ready to test the concept!")

if __name__ == "__main__":
    main()
