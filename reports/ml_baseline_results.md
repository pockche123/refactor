# Machine Learning Baseline Results

## Executive Summary

Comprehensive evaluation of machine learning models for refactoring type prediction across five major Java repositories using real RefactoringMiner data. This establishes the ML baseline for comparison with Large Language Model approaches.

**Key Findings:**
- **Commons Lang achieves 91.4% accuracy** with RandomForest due to dominant "Extract And Move Method" pattern
- **High refactoring diversity significantly impacts performance** - domains with 40+ types show <50% accuracy
- **RandomForest consistently outperforms** LogisticRegression and SVM across most domains
- **Real commit-based validation** enables behavioral testing of all predictions

## Methodology

### Dataset Characteristics

| Domain | Total Refactorings | Unique Types | Commits | Top Refactoring Type | Dominance |
|--------|-------------------|--------------|---------|---------------------|-----------|
| Commons Lang | 350 | 26 | 29 | Extract And Move Method | 76.3% |
| Spring | 350 | 42 | 32 | Modify Method Annotation | 15.7% |
| Kafka | 350 | 41 | 33 | Add Parameter | 11.4% |
| Intellij | 125 | 24 | 24 | Add Parameter Annotation | 39.2% |
| Mockito | 98 | 25 | 9 | Rename Method | 17.3% |

### Model Configuration

- **RandomForest**: n_estimators=100, random_state=42
- **LogisticRegression**: max_iter=1000, random_state=42  
- **SVM**: probability=True, random_state=42
- **Features**: lines_changed, cyclomatic_complexity, nesting_depth
- **Split**: 70% train, 30% test
- **Evaluation**: Accuracy, Precision, Recall, F1-score

## Results by Domain

### Performance Summary

| Domain | RandomForest | LogisticRegression | SVM | Best Model |
|--------|--------------|-------------------|-----|------------|
| Commons Lang | 91.4% | 89.5% | 73.3% | RandomForest (91.4%) |
| Spring | 48.6% | 38.1% | 24.8% | RandomForest (48.6%) |
| Kafka | 43.8% | 27.6% | 21.0% | RandomForest (43.8%) |
| Intellij | 52.6% | 63.2% | 42.1% | LogisticRegression (63.2%) |
| Mockito | 40.0% | 40.0% | 20.0% | RandomForest (40.0%) |

### Detailed Domain Analysis

#### 1. Commons Lang - Exceptional Performance (91.4%)

**Why it works:**
- **Dominant pattern**: "Extract And Move Method" represents 76.3% of refactorings
- **Low diversity**: Only 26 refactoring types with clear class imbalance
- **Consistent complexity**: Mean complexity 6.3, predictable patterns

**Model performance:**
- **RandomForest**: 91.4% accuracy - excellent at capturing dominant pattern
- **LogisticRegression**: 89.5% accuracy - linear patterns work well
- **SVM**: 73.3% accuracy - struggles with class imbalance

**Key insight**: When one refactoring type dominates (>75%), ML models achieve excellent accuracy.

#### 2. IntelliJ - Moderate Success (63.2%)

**Characteristics:**
- **Annotation focus**: "Add Parameter Annotation" is most common (39.5% of test cases)
- **Moderate diversity**: 24 refactoring types
- **Smaller dataset**: 125 total refactorings

**Model performance:**
- **LogisticRegression**: 63.2% accuracy - best for this domain
- **RandomForest**: 52.6% accuracy - overfitting on small dataset
- **SVM**: 42.1% accuracy - insufficient data for complex boundaries

**Key insight**: LogisticRegression can outperform RandomForest on smaller, focused datasets.

#### 3. Spring Framework - High Diversity Challenge (48.6%)

**Challenges:**
- **Extreme diversity**: 42 different refactoring types
- **Balanced distribution**: Top type only 15.7% of cases
- **Complex patterns**: Annotation management, API evolution

**Model performance:**
- **RandomForest**: 48.6% accuracy - handles diversity better than others
- **LogisticRegression**: 38.1% accuracy - struggles with non-linear patterns
- **SVM**: 24.8% accuracy - poor performance on high-dimensional sparse data

**Key insight**: High refactoring diversity (40+ types) makes prediction extremely challenging.

#### 4. Apache Kafka - Similar Diversity Issues (43.8%)

**Characteristics:**
- **API evolution focus**: "Add Parameter" leads at 11.4%
- **High diversity**: 41 refactoring types
- **Distributed system patterns**: Complex refactoring needs

**Model performance:**
- **RandomForest**: 43.8% accuracy - best at handling complexity
- **LogisticRegression**: 27.6% accuracy - linear assumptions fail
- **SVM**: 21.0% accuracy - worst performance across all domains

**Key insight**: Distributed systems show complex refactoring patterns that challenge traditional ML.

#### 5. Mockito - Small Dataset Limitations (40.0%)

**Constraints:**
- **Limited data**: Only 98 refactorings total
- **Method focus**: "Rename Method" leads at 17.3%
- **Testing framework patterns**: API clarity improvements

**Model performance:**
- **RandomForest & LogisticRegression**: Both 40.0% accuracy - tied performance
- **SVM**: 20.0% accuracy - insufficient training data

**Key insight**: Small datasets limit ML model effectiveness regardless of pattern clarity.

## Cross-Domain Insights

### 1. Model Performance Patterns

**RandomForest Advantages:**
- Handles class imbalance well (Commons Lang success)
- Robust to overfitting on diverse datasets (Spring, Kafka)
- Feature importance provides interpretability

**LogisticRegression Strengths:**
- Performs well on focused, smaller datasets (IntelliJ)
- Fast training and prediction
- Good baseline for linear patterns

**SVM Limitations:**
- Consistently worst performer across all domains
- Struggles with high-dimensional, sparse categorical data
- Poor scalability to diverse refactoring types

### 2. Dataset Characteristics Impact

**Class Imbalance Effect:**
- **Positive**: When dominant type >70% (Commons Lang), accuracy >90%
- **Negative**: Rare types (<5 instances) rarely predicted correctly

**Diversity Impact:**
- **Low diversity** (<30 types): Accuracy >60% achievable
- **High diversity** (>40 types): Accuracy typically <50%

**Dataset Size:**
- **Large datasets** (350 samples): More stable performance
- **Small datasets** (<100 samples): High variance, limited learning

### 3. Feature Engineering Insights

**Current Features:**
- **lines_changed**: Most predictive feature across domains
- **cyclomatic_complexity**: Secondary importance
- **nesting_depth**: Least predictive but still useful

**Limitations:**
- Structural metrics insufficient for semantic refactoring patterns
- Missing context about code semantics and developer intent
- No temporal or project-specific features

## Behavioral Validation Readiness

### Validation Scope

**Total Test Cases**: 383 across all domains
- Commons Lang: 105 test cases
- Spring: 105 test cases  
- Kafka: 105 test cases
- IntelliJ: 38 test cases
- Mockito: 30 test cases

**Commit Accessibility:**
- **All predictions have real commit SHAs** for git-based validation
- **Before/after code retrieval** possible for every test case
- **Compilation and execution testing** feasible

### Validation Priorities

1. **High-confidence predictions** (Commons Lang RandomForest)
2. **Dominant refactoring types** across all domains
3. **Edge cases** where models disagree
4. **Cross-domain patterns** for generalization testing

## Comparison with Synthetic Data

**Previous Synthetic Results** (from conversation history):
- IntelliJ: 33.3% accuracy (8/24 correct)
- All correct predictions were "Add Parameter Annotation"

**Real Data Results**:
- IntelliJ: 63.2% accuracy (24/38 correct) with LogisticRegression
- Diverse correct predictions across multiple refactoring types

**Improvement**: **90% increase in accuracy** using real RefactoringMiner data vs synthetic data.

## Recommendations

### For ML vs LLM Comparison

1. **Use identical test sets** - 383 real test cases with commit SHAs
2. **Focus on high-performing domains** - Commons Lang for fair comparison
3. **Analyze failure modes** - where ML struggles, can LLMs succeed?
4. **Behavioral validation** - test actual code changes for both approaches

### For Model Improvement

1. **Enhanced features** - semantic analysis, AST patterns, commit messages
2. **Domain-specific models** - train separate models per repository type
3. **Ensemble approaches** - combine predictions across models
4. **Temporal features** - refactoring sequences and developer patterns

### For Research Directions

1. **Investigate semantic features** beyond structural metrics
2. **Study cross-domain transfer learning** 
3. **Analyze temporal refactoring patterns**
4. **Explore few-shot learning** for rare refactoring types

## Data Availability

**ML Results**: `results/ml_testing/` - 15 CSV files with detailed predictions
**Training Data**: `data/*_350_real_train.csv` - 5 training datasets  
**Test Data**: `data/*_350_real_test.csv` - 5 test datasets
**Source Code**: Real commits accessible via git for behavioral validation

## Conclusion

This ML baseline establishes that **traditional machine learning can achieve excellent performance (>90%) when refactoring patterns are dominated by a single type**, but **struggles significantly with diverse refactoring portfolios** common in modern software development.

The **91.4% accuracy on Commons Lang** demonstrates the upper bound of ML performance under ideal conditions, while **<50% accuracy on Spring and Kafka** reveals the limitations when facing real-world refactoring diversity.

These results provide a **robust baseline for LLM comparison** using identical real test cases with authentic commit references, enabling fair evaluation of whether large language models can overcome the diversity challenges that limit traditional ML approaches.

---

_Generated: September 15, 2025_
_Based on RefactoringMiner data from 5 major Java repositories_
_Total test cases: 383 real refactorings with commit validation capability_
