# Enhanced Cross-Domain Generalization Results

## Overview

Testing the trained model on different software domains with **real complexity features** extracted from source code analysis.

## Performance Summary Table

| Project                     | Dataset Size | Accuracy | Complexity Range | Nesting Range | Dominant Refactoring Type             |
| --------------------------- | ------------ | -------- | ---------------- | ------------- | ------------------------------------- |
| **Training** (Commons/Gson) | 1,089        | 81.8%    | Real features    | Real features | Change Method Access Modifier (77.9%) |
| **IntelliJ** (IDE)          | 125          | 8.0%     | 1-12             | 1-5           | Add Parameter Annotation (39.2%)      |
| **Mockito** (Testing)       | 97           | 5.2%     | 1-52             | 1-5           | Rename Method (17.5%)                 |
| **Elasticsearch** (Search)  | 7,266        | 2.1%     | 1-509            | 1-22          | Rename Variable (22.3%)               |

## Complete Performance Comparison Table

| Metric                | Original (Commons/Gson) | IntelliJ | Mockito | Elasticsearch |
| --------------------- | ----------------------- | -------- | ------- | ------------- |
| **Accuracy**          | 81.8%                   | 8.0%     | 5.2%    | 2.1%          |
| **Accuracy Drop**     | -                       | -73.8%   | -76.6%  | -79.7%        |
| **Precision (macro)** | 70.2%                   | 0.0%     | 0.0%    | 0.0%          |
| **Precision Drop**    | -                       | -70.2%   | -70.2%  | -70.2%        |
| **Recall (macro)**    | 81.8%                   | 4.0%     | 4.0%    | 1.0%          |
| **Recall Drop**       | -                       | -77.8%   | -77.8%  | -80.8%        |
| **F1-Score (macro)**  | 75.5%                   | 1.0%     | 0.0%    | 0.0%          |
| **F1-Score Drop**     | -                       | -74.5%   | -75.5%  | -75.5%        |
| **Dataset Size**      | 1,089                   | 125      | 97      | 7,266         |
| **Complexity Range**  | Real                    | 1-12     | 1-52    | 1-509         |
| **Nesting Range**     | Real                    | 1-5      | 1-5     | 1-22          |

## Performance Drop Summary

| Domain            | Accuracy Drop | Precision Drop | Recall Drop | F1-Score Drop |
| ----------------- | ------------- | -------------- | ----------- | ------------- |
| **IntelliJ**      | -73.8%        | -70.2%         | -77.8%      | -74.5%        |
| **Mockito**       | -76.6%        | -70.2%         | -77.8%      | -75.5%        |
| **Elasticsearch** | -79.7%        | -70.2%         | -80.8%      | -75.5%        |
| **Average Drop**  | -76.7%        | -70.2%         | -78.8%      | -75.2%        |

## Detailed Results

### IntelliJ Community Edition (IDE)

- **Dataset**: 125 refactoring instances
- **Accuracy**: 8.0%
- **Complexity Range**: 1-12 (real cyclomatic complexity)
- **Nesting Range**: 1-5 (real nesting depth)
- **Model Behavior**: Predicts "Change Method Access Modifier" for 100% of instances

**Complete Classification Report:**

```
                                 precision    recall  f1-score   support
       Add Attribute Annotation       0.00      0.00      0.00         9
           Add Class Annotation       0.00      0.00      0.00         4
          Add Method Annotation       0.00      0.00      0.00         8
       Add Parameter Annotation       0.00      0.00      0.00        49
          Change Attribute Type       0.00      0.00      0.00         1
  Change Method Access Modifier       0.08      1.00      0.15        10
   Change Thrown Exception Type       0.00      0.00      0.00         1
           Change Variable Type       0.00      0.00      0.00        10
                 Extract Method       0.00      0.00      0.00         7
               Extract Variable       0.00      0.00      0.00         3
                Inline Variable       0.00      0.00      0.00         1
        Modify Class Annotation       0.00      0.00      0.00         1
       Modify Method Annotation       0.00      0.00      0.00         1
                     Move Class       0.00      0.00      0.00         1
                      Move Code       0.00      0.00      0.00         1
      Remove Attribute Modifier       0.00      0.00      0.00         1
      Remove Parameter Modifier       0.00      0.00      0.00         2
               Rename Attribute       0.00      0.00      0.00         1
                  Rename Method       0.00      0.00      0.00         3
               Rename Parameter       0.00      0.00      0.00         2
                Rename Variable       0.00      0.00      0.00         6
   Replace Anonymous With Class       0.00      0.00      0.00         1
Replace Attribute With Variable       0.00      0.00      0.00         1
Replace Variable With Attribute       0.00      0.00      0.00         1

                       accuracy                           0.08       125
                      macro avg       0.00      0.04      0.01       125
                   weighted avg       0.01      0.08      0.01       125
```

### Mockito (Testing Framework)

- **Dataset**: 97 refactoring instances
- **Accuracy**: 5.2%
- **Complexity Range**: 1-52 (real cyclomatic complexity)
- **Nesting Range**: 1-5 (real nesting depth)
- **Model Behavior**: Predicts "Change Method Access Modifier" for 100% of instances

**Complete Classification Report:**

```
                                  precision    recall  f1-score   support
              Add Class Modifier       0.00      0.00      0.00         2
           Add Method Annotation       0.00      0.00      0.00         4
                   Add Parameter       0.00      0.00      0.00         1
Change Attribute Access Modifier       0.00      0.00      0.00         1
           Change Attribute Type       0.00      0.00      0.00         3
    Change Class Access Modifier       0.00      0.00      0.00         4
   Change Method Access Modifier       0.05      1.00      0.10         5
           Change Parameter Type       0.00      0.00      0.00         9
              Change Return Type       0.00      0.00      0.00         7
            Change Variable Type       0.00      0.00      0.00         1
                  Extract Method       0.00      0.00      0.00         2
                Extract Variable       0.00      0.00      0.00         2
          Move And Inline Method       0.00      0.00      0.00         1
                      Move Class       0.00      0.00      0.00         3
              Move Source Folder       0.00      0.00      0.00         1
        Remove Method Annotation       0.00      0.00      0.00         1
          Remove Method Modifier       0.00      0.00      0.00         1
                Remove Parameter       0.00      0.00      0.00        15
    Remove Thrown Exception Type       0.00      0.00      0.00         1
        Remove Variable Modifier       0.00      0.00      0.00         1
                Rename Attribute       0.00      0.00      0.00         1
                   Rename Method       0.00      0.00      0.00        17
                Rename Parameter       0.00      0.00      0.00        10
                 Rename Variable       0.00      0.00      0.00         3
 Replace Variable With Attribute       0.00      0.00      0.00         1

                        accuracy                           0.05        97
                       macro avg       0.00      0.04      0.00        97
                    weighted avg       0.00      0.05      0.01        97
```

### Elasticsearch (Search Engine)

- **Dataset**: 7,266 refactoring instances
- **Accuracy**: 2.1%
- **Complexity Range**: 1-509 (real cyclomatic complexity)
- **Nesting Range**: 1-22 (real nesting depth)
- **Model Behavior**: Predicts "Change Method Access Modifier" for 100% of instances

**Top 15 Most Common Refactoring Types:**

```
                                  precision    recall  f1-score   support
                Rename Variable       0.00      0.00      0.00      1624
               Rename Parameter       0.00      0.00      0.00      1018
                Extract Variable       0.00      0.00      0.00       734
                   Add Parameter       0.00      0.00      0.00       513
            Change Variable Type       0.00      0.00      0.00       350
           Change Parameter Type       0.00      0.00      0.00       320
                  Rename Method       0.00      0.00      0.00       226
                Remove Parameter       0.00      0.00      0.00       210
              Change Return Type       0.00      0.00      0.00       178
   Change Method Access Modifier       0.02      1.00      0.04       150
                     Move Method       0.00      0.00      0.00       119
           Change Attribute Type       0.00      0.00      0.00       108
                Rename Attribute       0.00      0.00      0.00        87
Change Attribute Access Modifier       0.00      0.00      0.00        68
                  Move Attribute       0.00      0.00      0.00        66
```

## Key Findings

### 1. Real Complexity Features Don't Improve Generalization

- Despite extracting real cyclomatic complexity (1-509 range) and nesting depth (1-22 range)
- Performance remains identical to dummy feature results
- Confirms that feature quality is not the primary limitation

### 2. Systematic Cross-Domain Failure

- All domains show 73-80% performance drops from training accuracy (81.8%)
- Model predicts only the training domain's dominant class for 100% of instances
- Zero precision/recall for minority classes across all domains

### 3. Domain-Specific Refactoring Patterns

- **Libraries** (training): Access modifier changes (77.9%)
- **IDEs**: Annotation additions (39.2%)
- **Testing frameworks**: Method renaming (17.5%)
- **Search engines**: Variable renaming (22.3%)

### 4. Scale Independence

- Failure pattern consistent across dataset sizes (97 to 7,266 instances)
- Large datasets don't improve generalization
- Confirms systematic rather than sample-size issues

## Technical Insights

- **Class Imbalance Root Cause**: Training data dominated by single refactoring type (77.9%)
- **Feature Engineering Insufficient**: Real complexity metrics don't overcome training bias
- **Cross-Validation Limitations**: Within-domain CV cannot predict cross-domain performance
- **Domain Adaptation Needed**: Requires balanced training data or domain-specific approaches

## Implications for Future Work

1. **Balanced Training Data**: Equal representation of refactoring types
2. **Class Weighting**: Adjust model to handle imbalanced classes
3. **Domain Adaptation**: Transfer learning or ensemble approaches
4. **Feature Engineering**: Domain-specific feature extraction strategies
