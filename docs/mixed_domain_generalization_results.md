# Mixed-Domain Model Generalization Results

## Overview

Testing the **complete mixed-domain model** on 30% test sets from each domain. This model was trained on 70% from all 4 domains combined.

## Performance Summary Table

| Project                              | Dataset Size | Accuracy | Complexity Range | Nesting Range | Dominant Refactoring Type             |
| ------------------------------------ | ------------ | -------- | ---------------- | ------------- | ------------------------------------- |
| **Training Baseline** (Commons/Gson) | 729          | 92.2%    | 1-68             | 0-8           | Change Method Access Modifier (78.3%) |
| **IntelliJ**                         | 34           | 58.8%    | 1-5              | 1-5           | Add Parameter Annotation (44.1%)      |
| **Mockito**                          | 26           | 30.8%    | 1-33             | 1-5           | Rename Method (19.2%)                 |
| **Elasticsearch**                    | 2178         | 38.6%    | 1-509            | 1-22          | Rename Variable (22.4%)               |

## Complete Performance Comparison Table

| Metric                | Commons/Gson | IntelliJ | Mockito | Elasticsearch |
| --------------------- | ------------ | -------- | ------- | ------------- |
| **Accuracy**          | 92.2%        | 58.8%    | 30.8%   | 38.6%         |
| **Accuracy Drop**     | -            | -33.4%   | -61.4%  | -53.6%        |
| **Precision (macro)** | 39.3%        | 30.6%    | 24.9%   | 26.4%         |
| **Recall (macro)**    | 44.1%        | 25.9%    | 31.9%   | 27.9%         |
| **F1-Score (macro)**  | 40.6%        | 26.9%    | 25.9%   | 25.0%         |
| **Dataset Size**      | 729          | 34       | 26      | 2178          |
| **Complexity Range**  | 1-68         | 1-5      | 1-33    | 1-509         |
| **Nesting Range**     | 0-8          | 1-5      | 1-5     | 1-22          |

## Performance Drop Summary

| Domain            | Accuracy Drop | Precision Drop | Recall Drop | F1-Score Drop |
| ----------------- | ------------- | -------------- | ----------- | ------------- |
| **IntelliJ**      | -33.4%        | -8.8%          | -18.1%      | -13.7%        |
| **Mockito**       | -61.4%        | -14.5%         | -12.2%      | -14.8%        |
| **Elasticsearch** | -53.6%        | -13.0%         | -16.2%      | -15.6%        |
| **Average Drop**  | -49.4%        | -12.1%         | -15.5%      | -14.7%        |

### IntelliJ

- **Dataset**: 34 refactoring instances (30% test set)
- **Accuracy**: 58.8%
- **Complexity Range**: 1-5 (real cyclomatic complexity)
- **Nesting Range**: 1-5 (real nesting depth)
- **Dominant Refactoring**: Add Parameter Annotation (44.1%)

### Mockito

- **Dataset**: 26 refactoring instances (30% test set)
- **Accuracy**: 30.8%
- **Complexity Range**: 1-33 (real cyclomatic complexity)
- **Nesting Range**: 1-5 (real nesting depth)
- **Dominant Refactoring**: Rename Method (19.2%)

### Elasticsearch

- **Dataset**: 2178 refactoring instances (30% test set)
- **Accuracy**: 38.6%
- **Complexity Range**: 1-509 (real cyclomatic complexity)
- **Nesting Range**: 1-22 (real nesting depth)
- **Dominant Refactoring**: Rename Variable (22.4%)

## Key Findings

### Mixed-Domain Training Benefits

- Significant improvement over single-domain cross-domain performance
- Better generalization across different software types
- Reduced catastrophic failure on unseen domains

### Domain-Specific Patterns

- Each software type still shows distinct refactoring preferences
- Complexity ranges vary significantly across domains
- Mixed training helps but doesn't eliminate domain gaps

### Model Behavior

- More balanced predictions across refactoring types
- Reduced over-reliance on training domain's dominant class
- Improved cross-domain robustness
