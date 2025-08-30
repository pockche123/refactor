# Refactoring Classifier Project - Complete Context

## Project Overview

Masters thesis project developing a machine learning classifier to predict refactoring types in Java code. The project demonstrates cross-domain generalization challenges in software engineering ML applications.

## Current Status: Cross-Domain Generalization Analysis Complete

### What We've Accomplished

#### 1. Initial Model Development

- **Training Data**: Commons Collections + Gson libraries (1,089 instances)
- **Model**: Enhanced Random Forest classifier
- **Features**: class_encoded, method_encoded, lines_changed, cyclomatic_complexity, nesting_depth
- **Training Performance**: 81.8% accuracy, 70.2% precision, 75.5% F1-score
- **Class Distribution Problem**: 77.9% dominated by "Change Method Access Modifier"

#### 2. Cross-Domain Testing Infrastructure

- **RefactoringMiner Integration**: Automated refactoring mining from complex projects
- **Feature Extraction Pipeline**: Real complexity analysis from source code (not dummy values)
- **Test Domains**: IntelliJ (IDE), Mockito (Testing), Elasticsearch (Search Engine)

#### 3. Cross-Domain Results (With Real Complexity Features)

| Domain        | Dataset Size | Accuracy | Performance Drop | Complexity Range |
| ------------- | ------------ | -------- | ---------------- | ---------------- |
| IntelliJ      | 125          | 8.0%     | -73.8%           | 1-12             |
| Mockito       | 97           | 5.2%     | -76.6%           | 1-52             |
| Elasticsearch | 7,266        | 2.1%     | -79.7%           | 1-509            |

#### 4. Key Scientific Findings

- **Systematic Failure**: Model predicts only training domain's dominant class (100% "Change Method Access Modifier")
- **Feature Quality Irrelevant**: Real vs dummy complexity features show identical performance
- **Root Cause**: Severe class imbalance in training data, not feature engineering
- **Domain Specificity**: Each software type has distinct refactoring patterns
- **Scale Independence**: Failure consistent across dataset sizes (97 to 7,266 instances)

### Current File Structure

```
├── scripts/
│   ├── extract_complexity_features.py    # Extracts real complexity from source code
│   ├── test_enhanced_generalization.py   # Tests model with real features
│   └── [other scripts...]
├── docs/
│   ├── enhanced_generalization_results.md # Complete results with real complexity
│   ├── final_ml_validation_summary.md     # [OUTDATED - contains dummy results]
│   └── PROJECT_ROADMAP.md
├── data/
│   ├── *_enhanced_dataset.csv            # Datasets with real complexity features
│   └── [original datasets...]
├── models/
│   └── enhanced_refactoring_classifier.pkl # Trained model
└── complex_projects/                      # Source code for feature extraction
```

## Next Phase: Solution Implementation

### Proposed 70-30 Mixed Training Approach

**Objective**: Demonstrate that balanced, cross-domain training improves generalization

#### Implementation Plan:

1. **Combine All Datasets**: Merge Commons/Gson + IntelliJ + Mockito + Elasticsearch
2. **70-30 Split**: 70% mixed training data, 30% held-out testing per domain
3. **Balanced Training**: Address class imbalance through sampling or weighting
4. **Cross-Domain Evaluation**: Test on held-out portions of each domain
5. **Expected Outcome**: 40-60% accuracy (realistic improvement vs current 2-8%)

#### Technical Requirements:

- Merge enhanced datasets with real complexity features
- Implement stratified sampling to maintain class balance
- Retrain model on mixed, balanced data
- Evaluate on domain-specific held-out sets

### Thesis Narrative Arc

1. **Problem**: Cross-domain generalization failure (73-80% performance drops)
2. **Analysis**: Class imbalance and domain specificity identified as root causes
3. **Solution**: Mixed-domain training with balanced class representation
4. **Evaluation**: Improved cross-domain performance demonstrates solution effectiveness

## Key Insights for Future Sessions

### What Works

- Real complexity feature extraction from source code
- RefactoringMiner integration for automated data collection
- Systematic cross-domain testing methodology
- Comprehensive performance analysis and documentation

### What Doesn't Work

- Single-domain training with severe class imbalance
- Dummy/hardcoded feature values (now eliminated)
- Within-domain cross-validation for predicting cross-domain performance

### Critical Success Factors

- **Class Balance**: Essential for generalization
- **Domain Diversity**: Training must include multiple software types
- **Real Features**: Actual complexity metrics from source code analysis
- **Systematic Evaluation**: Test across multiple domains and scales

## Files to Clean Up

- `final_ml_validation_summary.md` - Contains outdated dummy feature results
- Old generalization test scripts - Already removed (used dummy complexity)

## Ready for Next Phase

The project has solid foundations for implementing the mixed-training solution. All infrastructure is in place, and the problem is well-characterized. The 70-30 approach should provide the realistic improvements needed to complete the thesis narrative.

## Masters-Level Contributions

1. **Methodological Innovation**: Cross-domain testing reveals limitations missed by standard CV
2. **Practical Insights**: Demonstrates importance of balanced, diverse training in SE ML
3. **Realistic Results**: Shows ML limitations rather than unrealistic "perfect" performance
4. **Systematic Analysis**: Comprehensive evaluation across domains, scales, and feature types
