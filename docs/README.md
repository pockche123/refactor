# ML-Guided Refactoring with Behavioral Validation

## Project Overview
Machine learning approach for predicting and validating code refactorings with rigorous behavioral preservation testing.

## Key Results
- **50% success rate** on ML predictions applied to unseen code
- **Identified validation bias** in initial 100% success (70% trivial refactorings)
- **End-to-end pipeline**: ML prediction → Application → Behavioral validation

## Project Structure
```
├── data/                   # Core datasets
│   ├── dataset.csv        # Original refactoring data
│   └── enhanced_dataset.csv # Enhanced feature set
├── models/                 # Trained ML models
├── results/               # Validation results
│   ├── behavioral_validation_improved_results.csv
│   ├── finegrained_ml_validation_results.csv
│   └── unseen_project_predictions.csv
├── docs/                  # Documentation
│   ├── FINAL_ML_VALIDATION_SUMMARY.md
│   └── thesis_methodology_validation_rigor.md
└── scripts/               # Core scripts
    ├── finegrained_ml_validation.py
    └── test_unseen_projects.py
```

## Key Findings
1. **Validation Rigor**: Initial 100% success due to trivial refactoring bias
2. **ML Performance**: 50% success on unseen enterprise codebases (Kafka, HttpComponents)
3. **Methodology**: Stratified validation approach for realistic assessment

## Usage
```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run ML predictions on unseen code
python scripts/test_unseen_projects.py

# Validate ML predictions
python scripts/finegrained_ml_validation.py
```

## Academic Contribution
- Novel ML-guided refactoring pipeline with behavioral validation
- Identified and addressed dataset composition bias in refactoring research
- Realistic performance assessment (50% vs false 100% confidence)
