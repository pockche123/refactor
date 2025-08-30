# Refactoring Classifier - Project Roadmap & Status

## Current Status (2025-08-29)

### ✅ COMPLETED
1. **Data Collection**: 2,443 refactoring instances from Commons Lang/Collections/Gson
2. **Model Training**: 81.8% accuracy on training data (Enhanced Random Forest)
3. **Cross-Domain Testing**: 
   - IntelliJ Community: 8.0% accuracy (125 instances, 24 types)
   - Spring Boot: 0.7% accuracy (858 instances, 34 types)
4. **Comprehensive Evaluation**: Detailed metrics, classification reports, domain analysis

### 🔄 IN PROGRESS
- Cross-domain generalization study (2/4 projects complete)

### ❌ TODO
1. **Additional Projects**: Mine Mockito, Elasticsearch for complete cross-domain study
2. **Behavioral Validation**: Full test suite runs with statistical analysis
3. **Final Analysis**: Comprehensive thesis write-up

## Project Structure

```
refactoring-classifier/
├── data/
│   ├── enhanced_dataset.csv           # Training data (2,443 instances)
│   ├── intellij_dataset.csv           # IntelliJ test data (125 instances)
│   ├── spring-boot_dataset.csv        # Spring Boot test data (858 instances)
│   ├── intellij-community_refactorings.json
│   └── spring-boot_refactorings.json
├── models/
│   └── enhanced_refactoring_classifier.pkl  # Trained model (81.8% accuracy)
├── results/
│   ├── original_model_evaluation.csv
│   ├── intellij_generalization_results.csv
│   └── springboot_generalization_results.csv
├── scripts/
│   ├── evaluate_original_model.py
│   ├── test_generalization.py
│   ├── test_springboot_generalization.py
│   ├── extract_intellij_features.py
│   ├── mine_complex_projects.py
│   └── behavioral_validation_improved.py
└── docs/
    └── final_ml_validation_summary.md
```

## Current Results Summary

### Cross-Domain Performance
| Domain | Dataset Size | Accuracy | Top Actual Refactoring | Performance Drop |
|--------|-------------|----------|------------------------|------------------|
| **Training** (Commons/Gson) | 489 | 81.8% | Change Method Access Modifier (79%) | - |
| **IntelliJ** (IDE) | 125 | 8.0% | Add Parameter Annotation (39%) | -73.8% |
| **Spring Boot** (Framework) | 858 | 0.7% | Move Class (29%) | -81.1% |

### Key Findings
- **Systematic Overfitting**: Model predicts training domain's dominant class (Change Method Access Modifier) for 100% of new instances
- **Domain Specificity**: Each domain has completely different refactoring patterns
- **Progressive Degradation**: Performance gets worse as domains become more different

## NEXT SESSION ACTIONS

### Immediate Tasks (Priority 1)
1. **Mine Additional Projects**:
   ```bash
   cd /Users/parjalrai/Workspace/refactoring-classifier
   python scripts/mine_complex_projects.py mockito
   python scripts/mine_complex_projects.py elasticsearch
   ```

2. **Extract Features & Test**:
   ```bash
   python scripts/extract_features_generic.py mockito
   python scripts/extract_features_generic.py elasticsearch
   # Create test scripts for each project
   ```

3. **Update Final Summary**: Add Spring Boot results to `docs/final_ml_validation_summary.md`

### Secondary Tasks (Priority 2)
4. **Behavioral Validation Setup**:
   - Choose project with good test coverage (likely Spring Boot)
   - Implement test runner for before/after refactoring
   - Statistical analysis of test results

5. **Complete Cross-Domain Study**:
   - 4 domains total: Commons/Gson (training), IntelliJ, Spring Boot, Mockito/Elasticsearch
   - Comprehensive comparison table
   - Domain-specific refactoring pattern analysis

## Technical Context

### Model Details
- **Algorithm**: Enhanced Random Forest Classifier
- **Features**: class_encoded, method_encoded, lines_changed, cyclomatic_complexity, nesting_depth
- **Training**: Apache Commons Lang/Collections, Google Gson
- **Class Imbalance**: 78% of training data is "Change Method Access Modifier"

### Generalization Issues
- **Root Cause**: Severe class imbalance in training data
- **Symptom**: Model always predicts dominant training class
- **Evidence**: 100% prediction rate for "Change Method Access Modifier" on new domains

### Available Tools
- **RefactoringMiner**: `/Users/parjalrai/Workspace/RefactoringMiner` (use gradle run)
- **Projects**: IntelliJ, Spring Boot cloned; Mockito, Elasticsearch need cloning
- **Scripts**: All extraction and evaluation scripts ready

## Expected Outcomes

### Cross-Domain Study (4 projects)
- **Hypothesis**: Continued performance degradation across domains
- **Expected Results**: 0-15% accuracy on new domains
- **Thesis Value**: Demonstrates need for domain-specific models

### Behavioral Validation
- **Method**: Run existing test suites before/after applying predicted refactorings
- **Metrics**: Test pass rate, statistical significance tests
- **Expected**: High failure rate due to poor predictions

## Thesis Contributions
1. **Systematic Cross-Domain Evaluation**: First study testing refactoring prediction across multiple software domains
2. **Quantified Generalization Failure**: Precise measurement of performance degradation
3. **Domain-Specific Patterns**: Evidence that refactoring patterns are domain-dependent
4. **Practical Implications**: Need for balanced training data and domain adaptation

## Commands for Next Session

```bash
# Navigate to project
cd /Users/parjalrai/Workspace/refactoring-classifier

# Mine remaining projects
python scripts/mine_complex_projects.py mockito
python scripts/mine_complex_projects.py elasticsearch

# Extract features
python scripts/extract_features_generic.py mockito
python scripts/extract_features_generic.py elasticsearch

# Test generalization (create scripts as needed)
python scripts/test_mockito_generalization.py
python scripts/test_elasticsearch_generalization.py

# Update final summary with all results
# Implement behavioral validation if time permits
```

---
**Last Updated**: 2025-08-29  
**Status**: Cross-domain study 50% complete (2/4 projects)  
**Next Priority**: Complete remaining project mining and testing
