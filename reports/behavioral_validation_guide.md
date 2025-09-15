# Behavioral Validation Guide

## What is Behavioral Validation?

Behavioral validation tests whether ML predictions match **actual code changes** in real commits, not just labels.

## How It Works

### 1. We Have Real Commit SHAs
Every prediction has a real commit SHA from RefactoringMiner analysis:
- Commons Lang: 16 unique commits with 105 test cases
- Spring: 27 unique commits with 105 test cases  
- Kafka: 24 unique commits with 105 test cases
- IntelliJ: 15 unique commits with 38 test cases
- Mockito: 6 unique commits with 30 test cases

### 2. Get Actual Refactored Code

For any prediction, you can get the actual code:

```bash
# Example: Commons Lang refactoring
git clone https://github.com/apache/commons-lang.git
cd commons-lang

# Get code BEFORE refactoring
git show 6b93cbe15693055e50a7f8550bd2baa93fa7f870^:src/test/java/org/apache/commons/lang3/ValidateTest.java

# Get code AFTER refactoring  
git show 6b93cbe15693055e50a7f8550bd2baa93fa7f870:src/test/java/org/apache/commons/lang3/ValidateTest.java

# Get the diff showing exact changes
git show 6b93cbe15693055e50a7f8550bd2baa93fa7f870 -- src/test/java/org/apache/commons/lang3/ValidateTest.java
```

### 3. Validate Predictions

Compare ML prediction against actual code changes:
- **Prediction**: "Extract And Move Method"
- **Actual Code**: Shows method extraction and movement
- **Validation**: ✓ Prediction matches actual refactoring

## Example Validation Cases

### Commons Lang - Extract And Move Method
- **Commit**: 6b93cbe15693055e50a7f8550bd2baa93fa7f870
- **File**: src/test/java/org/apache/commons/lang3/ValidateTest.java
- **ML Prediction**: Extract And Move Method ✓
- **Actual Change**: Method extracted from one class and moved to another

### IntelliJ - Add Parameter Annotation  
- **Commit**: 6e96835a5997dfc842a223fe473363aeb2be4f4d
- **File**: platform/lang-impl/src/com/intellij/codeInsight/completion/CompletionProgressIndicator.java
- **ML Prediction**: Add Parameter Annotation ✓
- **Actual Change**: @NotNull annotation added to method parameter

## Validation Results

**157 predictions ready for behavioral validation** across all domains:
- Commons Lang: 96/96 correct predictions ready
- Spring: 51/51 correct predictions ready  
- IntelliJ: 10/24 correct predictions ready

## Why This Matters

1. **Real Validation**: Tests against actual code, not synthetic data
2. **ML vs LLM**: Same test cases for fair comparison
3. **Research Quality**: Establishes behavioral testing methodology
4. **Practical Impact**: Validates predictions work on real refactorings

---

*All commit SHAs are from real RefactoringMiner analysis of actual Java repositories*
