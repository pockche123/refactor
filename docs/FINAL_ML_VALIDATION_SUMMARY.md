# Final ML Model Validation Summary

## Model Performance Comparison

### 1. Original Model Performance (Commons/Gson Libraries)

**Dataset**: 2,443 instances, 29 refactoring types  
**Test Set**: 489 instances (20% split)

**Overall Metrics:**

- **Accuracy**: 81.8%
- **Precision**: 70.2%
- **Recall**: 81.8%
- **F1-Score**: 75.5%
- **Baseline**: 79.1% (most frequent class)
- **Improvement over baseline**: +2.7%

**Detailed Classification Report:**

```
                                  precision    recall  f1-score   support

        Add Attribute Annotation       0.00      0.00      0.00         1
            Add Class Annotation       0.00      0.00      0.00         2
           Add Method Annotation       0.50      0.50      0.50         2
                   Add Parameter       0.00      0.00      0.00         2
          Add Parameter Modifier       0.00      0.00      0.00         3
Change Attribute Access Modifier       0.00      0.00      0.00         8
    Change Class Access Modifier       0.00      0.00      0.00        13
   Change Method Access Modifier       0.85      0.99      0.92       387
           Change Parameter Type       0.00      0.00      0.00         1
              Change Return Type       0.00      0.00      0.00         1
            Change Variable Type       0.00      0.00      0.00         3
                  Extract Method       0.00      0.00      0.00         2
                Extract Variable       0.00      0.00      0.00         2
                 Inline Variable       0.08      0.33      0.13         3
     Modify Attribute Annotation       0.00      0.00      0.00         1
        Modify Method Annotation       0.00      0.00      0.00         2
         Remove Class Annotation       0.00      0.00      0.00         1
           Remove Class Modifier       0.00      0.00      0.00         1
        Remove Method Annotation       1.00      0.50      0.67         2
                Remove Parameter       0.00      0.00      0.00         3
       Remove Parameter Modifier       0.00      0.00      0.00         7
      Remove Variable Annotation       1.00      1.00      1.00         1
        Remove Variable Modifier       0.69      0.79      0.73        14
                    Rename Class       0.00      0.00      0.00         4
                   Rename Method       0.00      0.00      0.00         1
                Rename Parameter       0.00      0.00      0.00         2
                 Rename Variable       0.00      0.00      0.00         1
    Replace Anonymous With Class       0.00      0.00      0.00         1
   Replace Anonymous With Lambda       0.00      0.00      0.00        18

                        accuracy                           0.82       489
                       macro avg       0.14      0.14      0.14       489
                    weighted avg       0.70      0.82      0.75       489
```

### 2. Generalization Test (IntelliJ Community)

**Dataset**: 125 instances, 24 refactoring types  
**Domain**: IDE development (vs library maintenance)

**Overall Metrics:**

- **Accuracy**: 8.0%
- **Precision**: 0.6%
- **Recall**: 8.0%
- **F1-Score**: 1.2%
- **Baseline**: 39.2% (most frequent class)
- **Performance drop**: -73.8 percentage points

**Detailed Classification Report:**

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

## Domain Shift Analysis

### Training Data Distribution (Commons/Gson)

| Refactoring Type              | Count | Percentage |
| ----------------------------- | ----- | ---------- |
| Change Method Access Modifier | 1,903 | 77.9%      |
| Change Class Access Modifier  | 101   | 4.1%       |
| Replace Anonymous With Lambda | 74    | 3.0%       |
| Remove Variable Modifier      | 74    | 3.0%       |
| Remove Parameter Modifier     | 38    | 1.6%       |

### Target Data Distribution (IntelliJ)

| Refactoring Type              | Count | Percentage |
| ----------------------------- | ----- | ---------- |
| Add Parameter Annotation      | 49    | 39.2%      |
| Change Method Access Modifier | 10    | 8.0%       |
| Change Variable Type          | 10    | 8.0%       |
| Add Attribute Annotation      | 9     | 7.2%       |
| Add Method Annotation         | 8     | 6.4%       |

## Key Findings

### Model Behavior Analysis

1. **Original Domain**: Model achieves 85% precision on dominant class but fails on minority classes
2. **Target Domain**: Model predicts "Change Method Access Modifier" for ALL 125 instances (100%)
3. **Class Imbalance Impact**: 78% training data concentration causes severe overfitting
4. **Zero Generalization**: No successful predictions for IntelliJ's dominant refactoring types

### Performance Summary Table

| Metric    | Original (Commons/Gson) | Generalization (IntelliJ) | Drop   |
| --------- | ----------------------- | ------------------------- | ------ |
| Accuracy  | 81.8%                   | 8.0%                      | -73.8% |
| Precision | 70.2%                   | 0.6%                      | -69.6% |
| Recall    | 81.8%                   | 8.0%                      | -73.8% |
| F1-Score  | 75.5%                   | 1.2%                      | -74.3% |

## Conclusions

### Thesis Contributions

1. **Comprehensive ML Evaluation**: Standard metrics (accuracy, precision, recall, F1-score)
2. **Generalization Analysis**: Quantified domain transfer failure
3. **Class Imbalance Impact**: Demonstrated overfitting to dominant classes
4. **Realistic Results**: Honest reporting of model limitations

### Technical Insights

- **Feature Engineering Critical**: Dummy complexity values destroy model performance
- **Domain Specificity**: Library vs IDE refactoring patterns fundamentally different
- **Balanced Training Needed**: Severe class imbalance limits model effectiveness
- **Cross-Validation Insufficient**: Within-domain CV doesn't predict cross-domain performance

---

**Generated**: 2025-08-29  
**Model**: Enhanced Random Forest Classifier  
**Training**: Apache Commons Lang/Collections, Google Gson  
**Validation**: JetBrains IntelliJ Community
