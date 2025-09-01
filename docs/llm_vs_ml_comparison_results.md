# LLM vs ML Refactoring Comparison - Thesis Documentation

## Executive Summary

This document presents the results of a systematic comparison between Large Language Model (LLM) refactoring suggestions and traditional Machine Learning (ML) model predictions using behavioral validation on the Mockito codebase. The study reveals that while LLMs can achieve higher safety rates when successfully applied (80% vs 57%), implementation reliability remains a significant challenge.

## Methodology

### Experimental Design

- **ML Baseline**: Mixed-domain Random Forest classifier achieving 30.8% accuracy on Mockito test set
- **LLM Approach**: Fresh ChatGPT-4 suggestions on identical code snippets
- **Evaluation Metric**: Functional safety measured by maintaining 940 Mockito unit tests
- **Sample Size**: 8 correct ML predictions used as test cases

### Behavioral Validation Process

1. **Baseline Establishment**: Run complete Mockito test suite (940 tests)
2. **Refactoring Application**: Apply ML prediction or LLM suggestion using proper Java refactoring tools
3. **Safety Measurement**: Re-run test suite and compare results
4. **Restoration**: Restore original code for next test

### Code Snippets Evaluated

Eight Java code snippets from Mockito project covering:

- Test method naming and annotations
- Variable extraction and naming
- Method signature modifications
- Interface annotations
- Complex reflection operations

## Results

### Overall Safety Comparison

| Approach          | Suggestions | Applied | Safe | Safety Rate | Implementation Rate |
| ----------------- | ----------- | ------- | ---- | ----------- | ------------------- |
| **ML Model**      | 8           | 7       | 4    | **57.1%**   | 87.5%               |
| **Fresh ChatGPT** | 8           | 5       | 4    | **80.0%**   | 62.5%               |

### Key Findings

#### 1. LLM Superior Safety When Applied

- **ChatGPT achieved 80.0% safety rate** vs ML's 57.1%
- **22.9 percentage point advantage** for successfully applied LLM suggestions
- **Higher quality reasoning** led to more conservative, safer transformations

#### 2. Implementation Reliability Challenge

- **37.5% of LLM suggestions failed to apply** due to implementation issues
- **ML suggestions more reliably implementable** (87.5% vs 62.5%)
- **Pattern matching fragility** in automated transformation tools

#### 3. Approach Agreement Analysis

- **50% agreement rate** between ML and LLM on refactoring types
- **Different strategies** for same code improvement opportunities
- **Complementary rather than competing** approaches suggested

### Detailed Results by Code Location

#### Safe LLM Suggestions (4/5 applied)

1. **HashCodeAndEqualsSafeSetTest.java**

   - **Suggestion**: Rename method `isNotEqualToAnOtherTypeOfSetWithSameContent` → `isNotEqualToDifferentSetTypeWithSameContent`
   - **Reasoning**: Fix typo-like "AnOther", improve readability
   - **Result**: ✅ SAFE - Tests maintained functionality
   - **ML Disagreement**: ML suggested "Add Method Annotation"

2. **ReturnsEmptyValuesTest.java**

   - **Suggestion**: Rename method `should_return_empty_collections_or_null_for_non_collections` → `shouldReturnEmptyCollectionsOrNullForNonCollections`
   - **Reasoning**: Follow Java camelCase conventions
   - **Result**: ✅ SAFE - Tests maintained functionality
   - **ML Agreement**: Both suggested "Rename Method"

3. **ModuleHandler.java (Case 3)**

   - **Suggestion**: Rename method `classLoadingStrategy` → `resolveClassLoadingStrategy`
   - **Reasoning**: Better communicate method's purpose
   - **Result**: ✅ SAFE - Updated 11 references across 3 files
   - **ML Agreement**: Both suggested "Rename Method"

4. **InlineDelegateByteBuddyMockMaker.java**
   - **Suggestion**: Rename variable `count` → `initializationCount`
   - **Reasoning**: More descriptive variable name
   - **Result**: ✅ SAFE - Tests maintained functionality
   - **ML Disagreement**: ML suggested "Change Attribute Type"

#### Unsafe LLM Suggestion (1/5 applied)

1. **ModuleHandler.java (Case 2)**
   - **Suggestion**: Extract Method for reflection operations
   - **Reasoning**: Separate reflection logic from error handling
   - **Result**: ❌ UNSAFE - Broke test functionality
   - **ML Agreement**: Both suggested "Extract Method"
   - **Issue**: Complex dependency extraction broke variable scope

#### Implementation Failures (3/8 total)

1. **MockitoTest.java**

   - **Suggestion**: Extract Variable `mock(List.class, withSettings().stubOnly())`
   - **Failure**: Pattern matching couldn't locate target expression
   - **ML Disagreement**: ML suggested "Rename Method"

2. **MockAccess.java**

   - **Suggestion**: Add `@Nullable` annotation to `getHandler()`
   - **Failure**: File not found (path resolution issue)
   - **ML Disagreement**: ML suggested "Move Class"

3. **ModuleHandler.java (Case 1)**
   - **Suggestion**: Change return type `boolean` → `Boolean`
   - **Failure**: Pattern matching couldn't locate method signature
   - **ML Agreement**: Both suggested "Change Return Type"

## Analysis and Implications

### LLM Advantages

1. **Higher Quality Reasoning**: Natural language explanations provide better context for refactoring decisions
2. **Conservative Approach**: ChatGPT suggestions focused on safe, conventional improvements
3. **Semantic Understanding**: Better grasp of code conventions and naming patterns
4. **Contextual Awareness**: Considered broader code quality principles

### LLM Limitations

1. **Implementation Fragility**: 37.5% of suggestions couldn't be automatically applied
2. **Tool Dependency**: Requires sophisticated transformation infrastructure
3. **Consistency Issues**: Different LLM sessions produce different suggestions
4. **Pattern Matching Challenges**: Complex refactorings difficult to implement reliably

### ML Model Advantages

1. **Implementation Reliability**: 87.5% of predictions successfully applied
2. **Consistent Predictions**: Deterministic output for same input features
3. **Training-Based Safety**: Learned from historical successful refactorings
4. **Feature-Based Approach**: Structural patterns more reliably implementable

### ML Model Limitations

1. **Lower Safety Rate**: 57.1% vs 80% for successfully applied LLM suggestions
2. **Limited Semantic Understanding**: Feature-based approach misses contextual nuances
3. **Conservative Bias**: May miss beneficial refactoring opportunities
4. **Domain Specificity**: Performance varies significantly across different codebases

## Research Contributions

### 1. Novel Empirical Comparison

- **First systematic behavioral validation** of LLM vs ML refactoring approaches
- **Real-world safety measurement** using production test suites
- **Implementation reliability assessment** beyond accuracy metrics

### 2. Practical Deployment Insights

- **Quality vs Reliability Trade-off**: LLMs offer higher quality but lower reliability
- **Hybrid Approach Potential**: Combining ML reliability with LLM quality
- **Tool Infrastructure Requirements**: Sophisticated transformation tools essential for LLM deployment

### 3. Methodological Innovation

- **Behavioral validation framework** for refactoring tool evaluation
- **Multi-dimensional assessment**: Safety, reliability, and agreement analysis
- **Reproducible experimental design** for future comparative studies

## Implications for Tool Development

### 1. Hybrid Architecture Recommendation

```
ML Model (Reliable) → LLM Refinement (Quality) → Behavioral Validation (Safety)
```

### 2. Implementation Strategy

- **Use ML for initial candidate identification** (high reliability)
- **Apply LLM for suggestion refinement** (high quality)
- **Mandatory behavioral validation** for all suggestions (safety assurance)

### 3. Tool Requirements

- **Robust pattern matching** for diverse refactoring types
- **Comprehensive test integration** for safety validation
- **Fallback mechanisms** for implementation failures

## Limitations and Future Work

### Study Limitations

1. **Small sample size** (8 test cases) limits statistical significance
2. **Single LLM evaluation** (ChatGPT-4) may not generalize to other models
3. **Implementation constraints** limited refactoring type coverage
4. **Single domain testing** (Mockito) may not represent broader applicability

### Future Research Directions

1. **Larger-scale evaluation** across multiple projects and domains
2. **Multiple LLM comparison** (GPT-4, Claude, Gemini, etc.)
3. **Hybrid approach development** combining ML reliability with LLM quality
4. **Advanced transformation tools** to improve implementation reliability
5. **Long-term maintenance impact** assessment of applied refactorings

## Conclusion

This study demonstrates that while LLMs can achieve superior refactoring safety rates (80% vs 57%), implementation reliability remains a critical challenge for practical deployment. The findings suggest that **hybrid approaches combining ML reliability with LLM quality** may offer the best path forward for automated refactoring tools.

The **22.9 percentage point safety advantage** of LLMs, when successfully applied, validates the potential of natural language reasoning for code transformation tasks. However, the **37.5% implementation failure rate** highlights the need for more sophisticated transformation infrastructure before LLM-based refactoring tools can achieve production readiness.

**Key Takeaway**: The future of automated refactoring lies not in choosing between ML and LLM approaches, but in intelligently combining their complementary strengths while addressing their respective limitations through robust behavioral validation frameworks.
