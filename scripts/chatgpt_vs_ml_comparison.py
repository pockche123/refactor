#!/usr/bin/env python3
"""
ChatGPT vs ML Comparison for Refactoring Suggestions
Using fresh ChatGPT suggestions vs our mixed-domain ML model
"""

import os
import pandas as pd
import joblib
import subprocess
import shutil
import re
from sklearn.model_selection import train_test_split
from proper_java_refactoring import backup_project, restore_project

def get_chatgpt_suggestions():
    """Fresh ChatGPT suggestions from new conversation"""
    
    return {
        'mockito-core/src/test/java/org/mockito/internal/util/collections/HashCodeAndEqualsSafeSetTest.java': {
            'refactoring_type': 'Rename Method',
            'details': 'rename method isNotEqualToAnOtherTypeOfSetWithSameContent to isNotEqualToDifferentSetTypeWithSameContent',
            'reasoning': 'The new name is more concise and avoids the typo-like "AnOther", improving readability and clarity.',
            'old_method': 'isNotEqualToAnOtherTypeOfSetWithSameContent',
            'new_method': 'isNotEqualToDifferentSetTypeWithSameContent'
        },
        
        'mockito-core/src/test/java/org/mockito/MockitoTest.java': {
            'refactoring_type': 'Extract Variable',
            'details': 'extract mock(List.class, withSettings().stubOnly()) into a named variable like stubOnlyListMock',
            'reasoning': 'Improves readability by giving a meaningful name to the mock, clarifying its role in the test.',
            'target_expression': 'mock(List.class, withSettings().stubOnly())',
            'variable_name': 'stubOnlyListMock'
        },
        
        'mockito-core/src/test/java/org/mockito/internal/stubbing/defaultanswers/ReturnsEmptyValuesTest.java': {
            'refactoring_type': 'Rename Method',
            'details': 'rename method should_return_empty_collections_or_null_for_non_collections to shouldReturnEmptyCollectionsOrNullForNonCollections',
            'reasoning': 'Removes underscores to follow Java method naming conventions (camelCase), improving consistency.',
            'old_method': 'should_return_empty_collections_or_null_for_non_collections',
            'new_method': 'shouldReturnEmptyCollectionsOrNullForNonCollections'
        },
        
        'mockito-core/src/main/java/org/mockito/internal/creation/bytebuddy/MockAccess.java': {
            'refactoring_type': 'Add Method Annotation',
            'details': 'add @Nullable annotation to getHandler() return type',
            'reasoning': 'Clarifies that getHandler() may return null, improving API usability and preventing misuse.',
            'method_name': 'getHandler',
            'annotation': '@Nullable'
        },
        
        'mockito-core/src/main/java/org/mockito/internal/creation/bytebuddy/ModuleHandler.java': {
            'refactoring_type': 'Change Return Type',
            'details': 'change return type of isExported from boolean to Boolean',
            'reasoning': 'Returning a boxed Boolean allows distinguishing between false and "not applicable" (e.g., in case of reflection failure), making error handling more expressive.',
            'method_name': 'isExported',
            'old_type': 'boolean',
            'new_type': 'Boolean'
        },
        
        'mockito-core/src/main/java/org/mockito/internal/creation/bytebuddy/ModuleHandler.java_extract': {
            'refactoring_type': 'Extract Method',
            'details': 'extract lines 90–96 (reflection setup and invocation) into a private method addModuleReadAccess(Object target, Object mockLoader)',
            'reasoning': 'Improves readability by separating reflection logic from error handling, reducing method complexity.',
            'extracted_method': 'addModuleReadAccess'
        },
        
        'mockito-core/src/main/java/org/mockito/internal/creation/bytebuddy/ModuleHandler.java_rename': {
            'refactoring_type': 'Rename Method',
            'details': 'rename method classLoadingStrategy to resolveClassLoadingStrategy',
            'reasoning': 'The new name better communicates the method\'s purpose (deciding strategy based on input), improving clarity.',
            'old_method': 'classLoadingStrategy',
            'new_method': 'resolveClassLoadingStrategy'
        },
        
        'mockito-core/src/main/java/org/mockito/internal/creation/bytebuddy/InlineDelegateByteBuddyMockMaker.java': {
            'refactoring_type': 'Rename Variable',
            'details': 'rename variable count to initializationCount',
            'reasoning': 'Improves clarity by making the variable\'s purpose explicit, reducing ambiguity about what is being counted.',
            'old_variable': 'count',
            'new_variable': 'initializationCount'
        }
    }

def apply_chatgpt_suggestion(project_dir, file_path, suggestion):
    """Apply ChatGPT suggestion using our refactoring tools"""
    
    # Handle the special ModuleHandler cases
    if file_path.endswith('_extract'):
        file_path = file_path.replace('_extract', '')
    elif file_path.endswith('_rename'):
        file_path = file_path.replace('_rename', '')
    
    full_file_path = os.path.join(project_dir, file_path)
    
    if not os.path.exists(full_file_path):
        return False, f"File not found: {file_path}"
    
    refactoring_type = suggestion['refactoring_type']
    
    try:
        with open(full_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if refactoring_type == 'Rename Method':
            # Use our proper refactoring for method renaming
            from proper_java_refactoring import apply_proper_rename_method
            old_method = suggestion.get('old_method', 'defaultMethod')
            new_method = suggestion.get('new_method', 'defaultMethodRenamed')
            
            return apply_proper_rename_method(full_file_path, project_dir, old_method, new_method)
        
        elif refactoring_type == 'Extract Variable':
            # Simple extract variable implementation
            target_expr = suggestion.get('target_expression', 'defaultExpression')
            var_name = suggestion.get('variable_name', 'extractedVar')
            
            # Find the target expression and extract it
            if target_expr in content:
                # Simple extraction - add variable declaration before first usage
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if target_expr in line and var_name not in line:
                        # Add variable declaration
                        indent = len(line) - len(line.lstrip())
                        var_declaration = ' ' * indent + f"Object {var_name} = {target_expr};"
                        
                        # Replace the expression with variable name
                        updated_line = line.replace(target_expr, var_name)
                        
                        # Insert declaration and update line
                        lines.insert(i, var_declaration)
                        lines[i + 1] = updated_line
                        break
                
                updated_content = '\n'.join(lines)
                
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                return True, {
                    'type': 'Extract Variable (ChatGPT)',
                    'expression': target_expr,
                    'variable_name': var_name,
                    'location': file_path
                }
        
        elif refactoring_type == 'Add Method Annotation':
            # Add annotation to method
            method_name = suggestion.get('method_name', 'getHandler')
            annotation = suggestion.get('annotation', '@Nullable')
            
            # Find method and add annotation
            method_pattern = rf'(\s*)(.*?)\s+{re.escape(method_name)}\s*\('
            
            def add_annotation(match):
                indent = match.group(1)
                return_type = match.group(2)
                return f"{indent}{annotation}\n{indent}{return_type} {method_name}("
            
            updated_content = re.sub(method_pattern, add_annotation, content)
            
            if updated_content != content:
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                return True, {
                    'type': 'Add Method Annotation (ChatGPT)',
                    'method_name': method_name,
                    'annotation': annotation,
                    'location': file_path
                }
        
        elif refactoring_type == 'Change Return Type':
            # Change method return type
            method_name = suggestion.get('method_name', 'isExported')
            old_type = suggestion.get('old_type', 'boolean')
            new_type = suggestion.get('new_type', 'Boolean')
            
            # Update method signature
            method_pattern = rf'(public\s+){re.escape(old_type)}(\s+{re.escape(method_name)}\s*\()'
            replacement = rf'\g<1>{new_type}\g<2>'
            
            updated_content = re.sub(method_pattern, replacement, content)
            
            if updated_content != content:
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                return True, {
                    'type': 'Change Return Type (ChatGPT)',
                    'method_name': method_name,
                    'old_type': old_type,
                    'new_type': new_type,
                    'location': file_path
                }
        
        elif refactoring_type == 'Extract Method':
            # Use our existing extract method implementation
            from proper_java_refactoring import apply_proper_refactoring_transformation
            return apply_proper_refactoring_transformation(full_file_path, refactoring_type, project_dir)
        
        elif refactoring_type == 'Rename Variable':
            # Use our existing rename variable implementation
            from proper_java_refactoring import apply_proper_rename_variable
            old_var = suggestion.get('old_variable', 'count')
            new_var = suggestion.get('new_variable', 'initializationCount')
            
            return apply_proper_rename_variable(full_file_path, project_dir, old_var, new_var)
        
        else:
            return False, f"Unsupported refactoring type: {refactoring_type}"
    
    except Exception as e:
        return False, f"Error applying ChatGPT suggestion: {e}"
    
    return False, "No changes made"

def get_correct_predictions():
    """Get the same 8 correct predictions we tested before"""
    
    mockito_df = pd.read_csv('data/mockito_enhanced_dataset.csv')
    
    class_counts = mockito_df['refactoring_type'].value_counts()
    valid_classes = class_counts[class_counts >= 2].index
    df_filtered = mockito_df[mockito_df['refactoring_type'].isin(valid_classes)]
    
    train_df, test_df = train_test_split(
        df_filtered, 
        test_size=0.3, 
        random_state=42, 
        stratify=df_filtered['refactoring_type']
    )
    
    model = joblib.load('models/complete_mixed_domain_classifier.pkl')
    
    feature_cols = ['class_encoded', 'method_encoded', 'lines_changed', 'cyclomatic_complexity', 'nesting_depth']
    X_test = test_df[feature_cols].fillna(0)
    predictions = model.predict(X_test)
    
    test_df = test_df.copy()
    test_df['predicted_refactoring'] = predictions
    
    correct_predictions = test_df[test_df['refactoring_type'] == test_df['predicted_refactoring']]
    
    return correct_predictions

def setup_comparison_workspace():
    """Setup workspace for ChatGPT vs ML comparison"""
    
    workspace_dir = 'behavioral_validation/chatgpt_vs_ml_workspace'
    
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
    
    os.makedirs(workspace_dir, exist_ok=True)
    
    source_dir = 'complex_projects/mockito'
    target_dir = os.path.join(workspace_dir, 'mockito')
    
    if not os.path.exists(source_dir):
        print(f"❌ Mockito project not found")
        return None
    
    print(f"📁 Setting up ChatGPT vs ML comparison workspace...")
    shutil.copytree(source_dir, target_dir)
    
    return target_dir

def run_test_suite(project_dir, test_name="baseline"):
    """Run Mockito test suite"""
    
    print(f"🧪 Running {test_name} tests...")
    
    try:
        result = subprocess.run(
            ['./gradlew', 'mockito-core:test', '--quiet', '--continue'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            'success': result.returncode == 0,
            'return_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    """Execute ChatGPT vs ML comparison"""
    
    print("🎯 CHATGPT vs ML REFACTORING COMPARISON")
    print("Comparing Fresh ChatGPT suggestions with Mixed-Domain ML model")
    print("=" * 70)
    
    # Get correct predictions and ChatGPT suggestions
    correct_predictions = get_correct_predictions()
    chatgpt_suggestions = get_chatgpt_suggestions()
    
    print(f"📊 Testing on {len(correct_predictions)} correct ML predictions")
    print(f"🤖 Using {len(chatgpt_suggestions)} fresh ChatGPT suggestions")
    
    # Setup workspace
    project_dir = setup_comparison_workspace()
    if project_dir is None:
        return
    
    # Run baseline tests
    print(f"\n📊 Establishing baseline...")
    baseline_results = run_test_suite(project_dir, "baseline")
    
    if not baseline_results.get('success'):
        print(f"❌ Baseline tests failed - cannot proceed")
        return
    
    print(f"✅ Baseline established")
    
    # Map predictions to ChatGPT suggestions
    comparison_results = []
    modulehandler_count = 0
    
    print(f"\n🔬 Comparing Fresh ChatGPT vs ML on each code location...")
    
    for idx, (_, prediction_row) in enumerate(correct_predictions.iterrows()):
        
        print(f"\n--- Comparison {idx + 1}/{len(correct_predictions)} ---")
        
        file_path = prediction_row['file_path']
        ml_prediction = prediction_row['refactoring_type']
        
        # Handle multiple ModuleHandler cases
        chatgpt_key = file_path
        if 'ModuleHandler.java' in file_path:
            modulehandler_count += 1
            if modulehandler_count == 1:
                chatgpt_key = file_path  # Change Return Type case
            elif modulehandler_count == 2:
                chatgpt_key = file_path + '_extract'  # Extract Method case
            elif modulehandler_count == 3:
                chatgpt_key = file_path + '_rename'  # Rename Method case
        
        if chatgpt_key not in chatgpt_suggestions:
            print(f"⏭️  Skipping - no ChatGPT suggestion for {file_path}")
            continue
        
        chatgpt_suggestion = chatgpt_suggestions[chatgpt_key]
        
        print(f"File: {file_path}")
        print(f"ML Prediction: {ml_prediction}")
        print(f"ChatGPT Suggestion: {chatgpt_suggestion['refactoring_type']}")
        print(f"ChatGPT Details: {chatgpt_suggestion['details']}")
        
        # Test ChatGPT approach
        print(f"🧪 Testing Fresh ChatGPT suggestion...")
        
        backup_dir = backup_project(project_dir)
        
        try:
            # Apply ChatGPT suggestion
            chatgpt_success, chatgpt_result = apply_chatgpt_suggestion(project_dir, chatgpt_key, chatgpt_suggestion)
            
            if chatgpt_success:
                print(f"✅ Applied ChatGPT suggestion")
                
                # Test functionality
                post_chatgpt_results = run_test_suite(project_dir, "post-chatgpt")
                
                baseline_success = baseline_results.get('success', False)
                post_chatgpt_success = post_chatgpt_results.get('success', False)
                
                chatgpt_maintained_correctness = (baseline_success == post_chatgpt_success)
                
                status = "✅ SAFE" if chatgpt_maintained_correctness else "❌ UNSAFE"
                print(f"   Fresh ChatGPT Result: {status}")
                
                comparison_record = {
                    'file_path': file_path,
                    'ml_prediction': ml_prediction,
                    'chatgpt_suggestion': chatgpt_suggestion['refactoring_type'],
                    'chatgpt_details': chatgpt_suggestion['details'],
                    'chatgpt_reasoning': chatgpt_suggestion['reasoning'],
                    'chatgpt_applied': True,
                    'chatgpt_safe': chatgpt_maintained_correctness,
                    'approaches_agree': ml_prediction == chatgpt_suggestion['refactoring_type'],
                    'baseline_passed': baseline_success,
                    'post_chatgpt_passed': post_chatgpt_success
                }
                
            else:
                print(f"❌ Could not apply ChatGPT suggestion: {chatgpt_result}")
                comparison_record = {
                    'file_path': file_path,
                    'ml_prediction': ml_prediction,
                    'chatgpt_suggestion': chatgpt_suggestion['refactoring_type'],
                    'chatgpt_details': chatgpt_suggestion['details'],
                    'chatgpt_reasoning': chatgpt_suggestion['reasoning'],
                    'chatgpt_applied': False,
                    'chatgpt_safe': False,
                    'approaches_agree': ml_prediction == chatgpt_suggestion['refactoring_type'],
                    'error': chatgpt_result
                }
        
        except Exception as e:
            print(f"❌ Error testing ChatGPT suggestion: {e}")
            comparison_record = {
                'file_path': file_path,
                'ml_prediction': ml_prediction,
                'chatgpt_suggestion': chatgpt_suggestion['refactoring_type'],
                'chatgpt_applied': False,
                'chatgpt_safe': False,
                'approaches_agree': False,
                'error': str(e)
            }
        
        finally:
            restore_project(project_dir, backup_dir)
        
        comparison_results.append(comparison_record)
    
    # Analysis
    print(f"\n📊 FRESH CHATGPT vs ML COMPARISON RESULTS")
    print("=" * 70)
    
    total_comparisons = len(comparison_results)
    chatgpt_applied_count = sum(1 for r in comparison_results if r.get('chatgpt_applied', False))
    chatgpt_safe_count = sum(1 for r in comparison_results if r.get('chatgpt_safe', False))
    agreement_count = sum(1 for r in comparison_results if r.get('approaches_agree', False))
    
    print(f"Total comparisons: {total_comparisons}")
    print(f"Fresh ChatGPT suggestions applied: {chatgpt_applied_count}")
    print(f"Fresh ChatGPT suggestions safe: {chatgpt_safe_count}")
    print(f"ML-ChatGPT agreement: {agreement_count}")
    
    if chatgpt_applied_count > 0:
        chatgpt_safety_rate = (chatgpt_safe_count / chatgpt_applied_count) * 100
        ml_safety_rate = 57.1  # From our previous analysis
        
        print(f"\n🎯 SAFETY COMPARISON:")
        print(f"Fresh ChatGPT safety rate: {chatgpt_safety_rate:.1f}%")
        print(f"ML safety rate: {ml_safety_rate:.1f}%")
        
        if chatgpt_safety_rate > ml_safety_rate:
            print(f"🎉 Fresh ChatGPT outperforms ML by {chatgpt_safety_rate - ml_safety_rate:.1f} percentage points!")
        elif chatgpt_safety_rate < ml_safety_rate:
            print(f"📊 ML outperforms Fresh ChatGPT by {ml_safety_rate - chatgpt_safety_rate:.1f} percentage points")
        else:
            print(f"🤝 Fresh ChatGPT and ML have similar safety rates")
    
    if total_comparisons > 0:
        agreement_rate = (agreement_count / total_comparisons) * 100
        print(f"Agreement rate: {agreement_rate:.1f}%")
    
    # Detailed results
    print(f"\nDetailed Comparison:")
    for result in comparison_results:
        agree_symbol = "✅" if result.get('approaches_agree', False) else "❌"
        safe_symbol = "✅" if result.get('chatgpt_safe', False) else "❌"
        
        print(f"  {agree_symbol} {safe_symbol} {os.path.basename(result['file_path'])}")
        print(f"      ML: {result['ml_prediction']}")
        print(f"      ChatGPT: {result['chatgpt_suggestion']} - {result['chatgpt_details']}")
    
    # Save results
    results_df = pd.DataFrame(comparison_results)
    results_file = 'results/fresh_chatgpt_vs_ml_comparison.csv'
    os.makedirs('results', exist_ok=True)
    results_df.to_csv(results_file, index=False)
    print(f"\n💾 Results saved to {results_file}")
    
    print(f"\n🎯 KEY RESEARCH FINDINGS:")
    print(f"1. Fresh ChatGPT Safety Rate: {chatgpt_safety_rate:.1f}% vs ML Safety Rate: 57.1%")
    print(f"2. Approach Agreement: {agreement_rate:.1f}% of suggestions match")
    print(f"3. ChatGPT Reasoning: Natural language explanations vs ML feature-based")
    print(f"4. Fresh Comparison: {'ChatGPT' if chatgpt_safety_rate > 57.1 else 'ML'} shows better behavioral safety")

if __name__ == "__main__":
    main()
