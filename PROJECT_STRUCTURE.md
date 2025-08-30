# Refactoring Classifier - Clean Project Structure

## Core Scripts (Essential)

### Data Processing & Feature Extraction
- `scripts/extract_complexity_features.py` - Extract complexity metrics from Java code
- `scripts/extract_intellij_features.py` - Extract features from IntelliJ dataset
- `scripts/mine_complex_projects.py` - Mine refactorings from complex projects using RefactoringMiner

### Model Training & Evaluation
- `scripts/complete_mixed_training.py` - Complete mixed-domain model training pipeline
- `scripts/mixed_domain_training.py` - Mixed-domain training implementation

### Behavioral Validation
- `scripts/proper_behavioral_validation.py` - Proper behavioral validation with real Java refactoring
- `scripts/proper_java_refactoring.py` - Proper Java refactoring transformations with reference tracking
- `scripts/actual_refactoring_transforms.py` - Basic refactoring transformation implementations

### LLM Comparison
- `scripts/chatgpt_vs_ml_comparison.py` - Final ChatGPT vs ML comparison with behavioral validation

### Analysis
- `scripts/analyze_test_suites.py` - Analyze test suite coverage and characteristics

## Data Structure

### Datasets
- `data/commons_enhanced_dataset.csv` - Apache Commons + Gson training data
- `data/intellij_enhanced_dataset.csv` - IntelliJ Community dataset
- `data/mockito_enhanced_dataset.csv` - Mockito dataset
- `data/elasticsearch_enhanced_dataset.csv` - Elasticsearch dataset

### Models
- `models/complete_mixed_domain_classifier.pkl` - Final trained mixed-domain model

### Results
- `results/fresh_chatgpt_vs_ml_comparison.csv` - Final LLM vs ML comparison results

## Documentation

### Core Documentation
- `docs/ml_limitations_analysis.md` - Detailed analysis of ML limitations with code examples
- `docs/llm_vs_ml_comparison_results.md` - Complete LLM vs ML comparison documentation
- `PROJECT_ROADMAP.md` - Project roadmap and future directions
- `final_ml_validation_summary.md` - Final ML validation summary

### Project Structure
- `PROJECT_STRUCTURE.md` - This file

## Complex Projects (RefactoringMiner Data)
- `complex_projects/mockito/` - Mockito project for behavioral validation
- `complex_projects/intellij/` - IntelliJ Community project
- `complex_projects/elasticsearch/` - Elasticsearch project
- `complex_projects/spring-boot/` - Spring Boot project

## Key Research Findings

### 1. Cross-Domain Generalization (30.8% vs 5.2%)
- Mixed-domain training significantly improves generalization
- Single-domain models fail catastrophically on new domains

### 2. Behavioral Validation (57.1% safety rate)
- ML accuracy ≠ functional safety
- Proper refactoring tools improve safety from 33% to 57%
- Real code transformation testing essential

### 3. LLM vs ML Comparison (80% vs 57.1% safety)
- LLMs achieve higher safety when successfully applied
- Implementation reliability remains challenge (62.5% vs 87.5%)
- Hybrid approaches recommended

## Usage

### Train Mixed-Domain Model
```bash
python scripts/complete_mixed_training.py
```

### Run Behavioral Validation
```bash
python scripts/proper_behavioral_validation.py
```

### Compare with LLM
```bash
python scripts/chatgpt_vs_ml_comparison.py
```

## Dependencies
- scikit-learn, pandas, numpy (ML)
- RefactoringMiner (refactoring detection)
- Mockito project (behavioral validation)
- Java development environment (refactoring application)
