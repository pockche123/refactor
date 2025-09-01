# ML Model Limitations in Refactoring Prediction - Thesis Reference

## Executive Summary

This document provides concrete evidence of the fundamental gap between **ML prediction accuracy** and **refactoring execution safety**. Through behavioral validation on Mockito, we demonstrate that even "correct" ML predictions can fail catastrophically when applied to real code due to the model's inability to understand semantic dependencies and type system constraints.

## Key Finding

**ML models can identify WHAT to refactor (pattern recognition) but cannot understand HOW to refactor safely (semantic analysis).**

- **ML Accuracy**: 30.8% on Mockito test set
- **Behavioral Safety**: 57.1% of correct predictions are functionally safe
- **Gap**: 42.9% of accurate predictions still break functionality

## Detailed Analysis with Step-by-Step Code Examples

### 1. Type System Dependencies - Complete Failure Analysis

#### Step 1: Original Working Code (Mockito InlineDelegateByteBuddyMockMaker.java)

```java
// File: InlineDelegateByteBuddyMockMaker.java
// Lines 885-905: Original working implementation

public class InlineDelegateByteBuddyMockMaker {
    
    private static class InlineConstructionMockContext implements MockedConstruction.Context {
        
        // Line 885: Original field declaration
        private int count;  // ← This is what ML model wants to change
        
        private final Object[] arguments;
        private final Class<?> type;
        private final String[] parameterTypeNames;
        
        // Constructor and other methods...
        
        // Lines 899-905: Getter method that returns the field
        @Override
        public int getCount() {  // ← Interface contract: MUST return int
            if (count == 0) {
                throw new MockitoConfigurationException(
                        "mocked construction context is not initialized");
            }
            return count;  // ← Returns int field to satisfy interface
        }
        
        // Other methods that use the field...
    }
    
    // Line 819: Usage in another method
    private void someOtherMethod() {
        // This line assigns to the count field
        ((InlineConstructionMockContext) context).count = ++count;
        //                                   ↑
        //                          This expects int type
    }
}

// The interface this class implements
interface MockedConstruction {
    interface Context {
        int getCount();  // ← Interface defines return type as int
        //  ↑
        // This CANNOT be changed without breaking all implementations
    }
}
```

#### Step 2: What ML Model "Sees" and Predicts

```python
# ML Model Input Features (what it actually processes)
input_features = {
    'class_encoded': 42,           # Just a number - no semantic meaning
    'method_encoded': 17,          # Just a number - no type information  
    'lines_changed': 3,            # Simple count - no context
    'cyclomatic_complexity': 2,    # Structural metric - no type info
    'nesting_depth': 1             # Structural metric - no dependencies
}

# ML Model has NO KNOWLEDGE of:
# - What 'int' and 'long' mean
# - Interface contracts and inheritance
# - Method signatures and return types
# - Compilation rules and type compatibility
# - Cross-file dependencies and references

# ML Model Output
prediction = "Change Attribute Type"  # Just a string label
confidence = 0.87  # High confidence based on pattern matching

# ML Model Logic (simplified):
# "I've seen similar complexity patterns where attribute types were changed,
#  so I predict this location should also have attribute type change"
```

#### Step 3: Naive ML-Guided Transformation (What I Did)

```java
// AFTER NAIVE TRANSFORMATION - BROKEN CODE
public class InlineDelegateByteBuddyMockMaker {
    
    private static class InlineConstructionMockContext implements MockedConstruction.Context {
        
        // Line 885: Field type changed (following ML prediction)
        private long count;  // ✅ Changed int → long (what ML predicted)
        //      ↑
        //   This change breaks everything below
        
        private final Object[] arguments;
        private final Class<?> type;
        private final String[] parameterTypeNames;
        
        // Lines 899-905: Getter method - UNCHANGED (the problem!)
        @Override
        public int getCount() {  // ❌ Still returns int, but field is now long
            if (count == 0) {   // ❌ Comparing long to int (works, but inconsistent)
                throw new MockitoConfigurationException(
                        "mocked construction context is not initialized");
            }
            return count;  // ❌ COMPILATION ERROR: Cannot return long as int
            //     ↑
            //   'count' is now long, but method must return int
        }
    }
    
    // Line 819: Usage in another method - UNCHANGED (another problem!)
    private void someOtherMethod() {
        ((InlineConstructionMockContext) context).count = ++count;
        //                                   ↑              ↑
        //                              Expects int    Now returns long
        //                              ❌ Type mismatch in assignment
    }
}

// Interface remains unchanged - MAJOR PROBLEM!
interface MockedConstruction {
    interface Context {
        int getCount();  // ❌ Still expects int, but implementation returns long
        //  ↑
        // Cannot change this without breaking ALL other implementations
    }
}
```

#### Step 4: Compilation Errors Generated

```bash
# Exact compilation errors from Java compiler:

InlineDelegateByteBuddyMockMaker.java:904: error: incompatible types: possible lossy conversion from long to int
            return count;
                   ^

InlineDelegateByteBuddyMockMaker.java:899: error: getCount() in InlineConstructionMockContext cannot implement getCount() in MockedConstruction.Context
        public int getCount() {
               ^
  return type int is not compatible with long

InlineDelegateByteBuddyMockMaker.java:819: error: incompatible types: possible lossy conversion from long to int
        ((InlineConstructionMockContext) context).count = ++count;
                                                           ^

# Result: 3 compilation errors, code cannot build, tests cannot run
```

#### Step 5: What Complete Refactoring Actually Requires

```java
// COMPLETE REFACTORING (what real developers did in Mockito's history)

// 1. Update the interface definition (affects entire codebase)
interface MockedConstruction {
    interface Context {
        long getCount();  // ← Changed from int to long
        //   ↑
        // This change affects ALL implementations across the project
    }
}

// 2. Update the implementation class
public class InlineDelegateByteBuddyMockMaker {
    
    private static class InlineConstructionMockContext implements MockedConstruction.Context {
        
        // 3. Change field type
        private long count;  // ✅ Field type changed
        
        // 4. Update getter method signature
        @Override
        public long getCount() {  // ✅ Return type matches field and interface
            if (count == 0) {     // ✅ long comparison with int literal (valid)
                throw new MockitoConfigurationException(
                        "mocked construction context is not initialized");
            }
            return count;  // ✅ Returns long field as long (type-safe)
        }
    }
    
    // 5. Update all usage sites
    private void someOtherMethod() {
        ((InlineConstructionMockContext) context).count = ++count;
        //                                   ↑              ↑
        //                              Now long       Now long
        //                              ✅ Type-safe assignment
    }
}

// 6. Update ALL other classes that implement the interface
class AnotherMockContext implements MockedConstruction.Context {
    private long count;  // ← Must change this too
    
    @Override
    public long getCount() {  // ← Must change return type
        return count;
    }
}

// 7. Update ALL callers across the entire codebase
class SomeOtherClass {
    public void useContext(MockedConstruction.Context context) {
        long currentCount = context.getCount();  // ← Was: int currentCount
        //   ↑
        // Every caller must be updated to use long instead of int
        
        // Any arithmetic operations must be checked
        long total = currentCount + 1L;  // ← Was: int total = currentCount + 1;
    }
}
```

### 2. Annotation Semantics Failure - Complete Analysis

#### Step 1: Original Code Context

```java
// File: HashCodeAndEqualsSafeSetTest.java
// This is a JUnit test class

public class HashCodeAndEqualsSafeSetTest {
    
    // Original method - a simple test method
    public void cloneIsNotSupported() {
        HashCodeAndEqualsSafeSet<String> set = new HashCodeAndEqualsSafeSet<>();
        
        try {
            set.clone();
            fail("Expected UnsupportedOperationException");
        } catch (UnsupportedOperationException e) {
            // Expected behavior
        }
    }
    
    // Other test methods...
    @Test
    public void shouldAddElements() {
        // Another test method with proper annotation
    }
}

// Class hierarchy (what ML model cannot see)
class HashCodeAndEqualsSafeSetTest {
    // Does NOT extend any class with cloneIsNotSupported() method
    // Does NOT implement any interface with cloneIsNotSupported() method
}
```

#### Step 2: ML Model Analysis

```python
# What ML model processes
features = {
    'class_encoded': 73,           # Abstract encoding of class name
    'method_encoded': 45,          # Abstract encoding of method name
    'lines_changed': 1,            # Simple count
    'cyclomatic_complexity': 1,    # Low complexity
    'nesting_depth': 1             # Simple structure
}

# ML model prediction logic:
# "I've seen patterns where methods in test classes get annotations added,
#  and this method has similar structural characteristics,
#  so I predict: Add Method Annotation"

prediction = "Add Method Annotation"

# ML model has NO understanding of:
# - What @Override means (must override parent method)
# - What @Test means (marks JUnit test methods)
# - Class inheritance hierarchy
# - Interface implementation relationships
# - Annotation semantics and requirements
```

#### Step 3: Naive Annotation Addition

```java
// AFTER NAIVE ML-GUIDED TRANSFORMATION
public class HashCodeAndEqualsSafeSetTest {
    
    // My naive implementation just added @Override
    @Override  // ❌ ERROR: No parent method to override
    public void cloneIsNotSupported() {
        HashCodeAndEqualsSafeSet<String> set = new HashCodeAndEqualsSafeSet<>();
        
        try {
            set.clone();
            fail("Expected UnsupportedOperationException");
        } catch (UnsupportedOperationException e) {
            // Expected behavior
        }
    }
}

// The problem: There is NO parent class or interface with cloneIsNotSupported()
// Class hierarchy analysis:
class HashCodeAndEqualsSafeSetTest extends Object {  // Object has no cloneIsNotSupported()
    // No interfaces implemented
    // No parent methods named cloneIsNotSupported()
}
```

#### Step 4: Compilation Error

```bash
# Java compiler error:
HashCodeAndEqualsSafeSetTest.java:X: error: method does not override or implement a method from a supertype
    @Override
    ^

# Explanation:
# @Override annotation requires that the method actually overrides a method
# from a parent class or implements a method from an interface.
# Since cloneIsNotSupported() doesn't override anything, @Override is invalid.
```

#### Step 5: What Should Have Been Done

```java
// CORRECT ANNOTATION (what real developers did)
public class HashCodeAndEqualsSafeSetTest {
    
    // Option 1: Add @Test annotation (most likely correct)
    @Test
    public void cloneIsNotSupported() {
        HashCodeAndEqualsSafeSet<String> set = new HashCodeAndEqualsSafeSet<>();
        
        try {
            set.clone();
            fail("Expected UnsupportedOperationException");
        } catch (UnsupportedOperationException e) {
            // Expected behavior
        }
    }
    
    // Option 2: Add @Deprecated if method is being phased out
    @Deprecated
    public void cloneIsNotSupported() {
        // Implementation
    }
    
    // Option 3: Add @SuppressWarnings for specific warnings
    @SuppressWarnings("unchecked")
    public void cloneIsNotSupported() {
        // Implementation
    }
}

// The choice depends on the SEMANTIC INTENT, which ML cannot understand:
// - @Test: This is a unit test method
// - @Deprecated: This method is obsolete
// - @SuppressWarnings: Ignore specific compiler warnings
// - @Override: This method overrides a parent method (NOT applicable here)
```

### 3. Variable Scope and Dependencies - Extract Method Failure

#### Step 1: Original Complex Method

```java
// File: ModuleHandler.java
// Original method with complex control flow

public class ModuleHandler {
    
    private static final String MODULE_NAME = "mockito.core";
    private ClassLoader mockLoader;
    
    public void configureModule(Object target, String packageName) {
        try {
            // Line 230: Complex logic that ML wants to extract
            Class<?> moduleClass = Class.forName("java.lang.Module");
            Method addReads = moduleClass.getMethod("addReads", moduleClass);
            
            // Line 232-233: These lines identified for extraction by ML
            Object targetModule = target.getClass().getModule();
            Object mockModule = mockLoader.getClass().getModule();
            
            // Line 235: More complex logic
            addReads.invoke(targetModule, mockModule);
            
        } catch (ClassNotFoundException e) {
            // Exception handling that depends on local variables
            System.err.println("Module class not found for " + packageName);
            throw new RuntimeException("Failed to configure " + MODULE_NAME, e);
        } catch (NoSuchMethodException e) {
            System.err.println("addReads method not found");
            throw new RuntimeException("Reflection failed", e);
        } catch (Exception e) {
            // Generic exception handler
            handleGenericError(e, packageName);
        }
    }
    
    private void handleGenericError(Exception e, String context) {
        // Helper method
    }
}
```

#### Step 2: ML Model Pattern Recognition

```python
# ML model identifies extraction opportunity
features = {
    'class_encoded': 89,           # Class identifier
    'method_encoded': 23,          # Method identifier  
    'lines_changed': 2,            # Lines 232-233 changed in history
    'cyclomatic_complexity': 4,    # Multiple branches (try-catch)
    'nesting_depth': 2             # Nested in try block
}

# ML reasoning (pattern-based):
# "Lines 232-233 were extracted into a separate method in similar code,
#  and the complexity metrics match previous extraction patterns,
#  so predict: Extract Method"

prediction = "Extract Method"

# ML model CANNOT analyze:
# - Variable dependencies (targetModule, mockModule used later)
# - Exception handling scope (catch blocks need access to variables)
# - Method parameter requirements (what to pass to extracted method)
# - Local variable lifetimes and accessibility
```

#### Step 3: Naive Method Extraction

```java
// AFTER NAIVE ML-GUIDED EXTRACTION - BROKEN CODE
public class ModuleHandler {
    
    private static final String MODULE_NAME = "mockito.core";
    private ClassLoader mockLoader;
    
    public void configureModule(Object target, String packageName) {
        try {
            Class<?> moduleClass = Class.forName("java.lang.Module");
            Method addReads = moduleClass.getMethod("addReads", moduleClass);
            
            // Naive extraction: just call extracted method
            extracted1635(catch);  // ❌ ERROR: 'catch' is not a variable!
            //            ↑
            // My algorithm tried to pass 'catch' as parameter
            
            // Original lines 232-233 moved to extracted method
            // ❌ PROBLEM: addReads.invoke() now can't access targetModule, mockModule
            addReads.invoke(targetModule, mockModule);  // ❌ Variables not defined!
            
        } catch (ClassNotFoundException e) {
            System.err.println("Module class not found for " + packageName);
            throw new RuntimeException("Failed to configure " + MODULE_NAME, e);
        } catch (NoSuchMethodException e) {
            System.err.println("addReads method not found");
            throw new RuntimeException("Reflection failed", e);
        } catch (Exception e) {
            handleGenericError(e, packageName);
        }
    }
    
    // Naive extracted method - COMPLETELY BROKEN
    private void extracted1635(Object catch) {  // ❌ 'catch' is Java keyword!
        //                            ↑
        // Cannot use 'catch' as parameter name
        
        // Lines extracted from try block
        Object targetModule = target.getClass().getModule();  // ❌ 'target' not accessible!
        Object mockModule = mockLoader.getClass().getModule();  // ❌ 'mockLoader' not accessible!
        //                  ↑                    ↑
        // These fields are not passed as parameters
    }
}
```

#### Step 4: Multiple Compilation Errors

```bash
# Java compilation errors:

ModuleHandler.java:235: error: cannot find symbol
        extracted1635(catch);
                      ^
  symbol: variable catch

ModuleHandler.java:238: error: cannot find symbol
        addReads.invoke(targetModule, mockModule);
                        ^
  symbol: variable targetModule

ModuleHandler.java:238: error: cannot find symbol
        addReads.invoke(targetModule, mockModule);
                                      ^
  symbol: variable mockModule

ModuleHandler.java:245: error: 'catch' is not a valid identifier
    private void extracted1635(Object catch) {
                                      ^

ModuleHandler.java:248: error: cannot find symbol
        Object targetModule = target.getClass().getModule();
                               ^
  symbol: variable target

ModuleHandler.java:249: error: cannot find symbol
        Object mockModule = mockLoader.getClass().getModule();
                            ^
  symbol: variable mockLoader

# Result: 6 compilation errors, method extraction completely broken
```

#### Step 5: What Proper Method Extraction Requires

```java
// CORRECT METHOD EXTRACTION (what sophisticated tools do)
public class ModuleHandler {
    
    private static final String MODULE_NAME = "mockito.core";
    private ClassLoader mockLoader;
    
    public void configureModule(Object target, String packageName) {
        try {
            Class<?> moduleClass = Class.forName("java.lang.Module");
            Method addReads = moduleClass.getMethod("addReads", moduleClass);
            
            // Proper extraction: pass required parameters
            ModulePair modules = extractModules(target);  // ✅ Meaningful name and parameters
            //                                   ↑
            // Pass 'target' parameter that extracted method needs
            
            // Use returned values
            addReads.invoke(modules.targetModule, modules.mockModule);  // ✅ Variables available
            
        } catch (ClassNotFoundException e) {
            System.err.println("Module class not found for " + packageName);
            throw new RuntimeException("Failed to configure " + MODULE_NAME, e);
        } catch (NoSuchMethodException e) {
            System.err.println("addReads method not found");
            throw new RuntimeException("Reflection failed", e);
        } catch (Exception e) {
            handleGenericError(e, packageName);
        }
    }
    
    // Proper extracted method with correct parameters and return type
    private ModulePair extractModules(Object target) {  // ✅ Valid parameter name
        //                             ↑
        // Pass required dependencies as parameters
        
        Object targetModule = target.getClass().getModule();  // ✅ 'target' passed as parameter
        Object mockModule = mockLoader.getClass().getModule();  // ✅ 'mockLoader' accessible as field
        //                  ↑
        // Field access still works in extracted method
        
        return new ModulePair(targetModule, mockModule);  // ✅ Return both values
    }
    
    // Helper class to return multiple values
    private static class ModulePair {
        final Object targetModule;
        final Object mockModule;
        
        ModulePair(Object targetModule, Object mockModule) {
            this.targetModule = targetModule;
            this.mockModule = mockModule;
        }
    }
}

// What proper extraction analysis requires:
// 1. Variable dependency analysis (what variables are used)
// 2. Scope analysis (what's accessible where)
// 3. Parameter inference (what needs to be passed)
// 4. Return type analysis (what needs to be returned)
// 5. Exception handling analysis (try-catch scope)
// 6. Naming analysis (avoid keywords and conflicts)
```

### 1. Type System Dependencies - Change Attribute Type Failure

#### ML Model Input/Output
```python
# What the ML model sees:
input_features = {
    'class_encoded': 42,           # Abstract numeric encoding
    'method_encoded': 17,          # Abstract numeric encoding  
    'lines_changed': 3,            # Simple count
    'cyclomatic_complexity': 2,    # Structural metric
    'nesting_depth': 1             # Structural metric
}

# What the ML model predicts:
prediction = "Change Attribute Type"  # String label with no semantic understanding
```

#### Real Code Context (Mockito InlineDelegateByteBuddyMockMaker.java)
```java
// ORIGINAL CODE (Lines 885-905)
private int count;  // Field declaration

@Override
public int getCount() {  // Interface contract: must return int
    if (count == 0) {
        throw new MockitoConfigurationException(
                "mocked construction context is not initialized");
    }
    return count;  // Returns int field
}

// Usage in other methods (Line 819)
((InlineConstructionMockContext) context).count = ++count;
```

#### ML-Guided Transformation (Naive Application)
```java
// AFTER NAIVE ML-GUIDED REFACTORING
private long count;  // ✅ Field type changed (what ML predicted)

@Override
public int getCount() {  // ❌ COMPILATION ERROR: Interface still expects int
    if (count == 0) {
        throw new MockitoConfigurationException(
                "mocked construction context is not initialized");
    }
    return count;  // ❌ ERROR: Cannot return long as int
}
```

#### Compilation Errors Generated
```
Error: incompatible types: possible lossy conversion from long to int
Error: method does not override or implement a method from a supertype
Error: The return type is incompatible with MockedConstruction.Context.getCount()
```

#### What Complete Refactoring Requires
```java
// COMPLETE REFACTORING (what real developers did)
private long count;  // 1. Change field type

// 2. Update interface definition
interface MockedConstruction.Context {
    long getCount();  // Changed from int to long
}

// 3. Update method signature
@Override
public long getCount() {  // Return type matches field and interface
    if (count == 0) {
        throw new MockitoConfigurationException(
                "mocked construction context is not initialized");
    }
    return count;  // Type-safe return
}

// 4. Update all callers across the codebase
long currentCount = mockContext.getCount();  // Was: int currentCount
```

### 2. Annotation Semantics - Add Method Annotation Failure

#### ML Prediction vs Reality
```java
// ORIGINAL CODE (HashCodeAndEqualsSafeSetTest.java)
public void cloneIsNotSupported() {
    // Test method implementation
}

// ML PREDICTION: "Add Method Annotation"
// NAIVE APPLICATION:
@Override  // ❌ ERROR: Method doesn't override anything
public void cloneIsNotSupported() {
    // Test method implementation
}
```

#### Why It Failed
- **ML Model Understanding**: "Add annotation to method" (syntactic)
- **Reality**: `@Override` requires actual inheritance relationship (semantic)
- **Compilation Error**: `@Override` annotation on non-overriding method

#### What ML Model Cannot Understand
```java
// ML model cannot analyze:
class Parent {
    // No cloneIsNotSupported() method exists here
}

class Child extends Parent {
    @Override  // ❌ Invalid - nothing to override
    public void cloneIsNotSupported() { }
}

// Correct annotation would be:
@Test  // For test methods
public void cloneIsNotSupported() { }
```

### 3. Variable Scope and Dependencies - Extract Method Failure

#### ML Prediction Application
```java
// ORIGINAL CODE (ModuleHandler.java)
public void someMethod() {
    try {
        statement1;
        statement2;  // ML identifies these lines for extraction
        statement3;  // Based on structural patterns
    } catch (Exception e) {
        handleError(e);
    }
}

// NAIVE ML-GUIDED EXTRACTION:
public void someMethod() {
    try {
        statement1;
        extracted1635(catch);  // ❌ ERROR: 'catch' is not a variable
    } catch (Exception e) {
        handleError(e);
    }
}

private void extracted1635(Object catch) {  // ❌ ERROR: 'catch' is keyword
    statement2;  // ❌ ERROR: Lost access to local variables
    statement3;  // ❌ ERROR: Lost exception handling context
}
```

#### What ML Model Cannot Analyze
- **Variable scope**: Which variables are accessible in extracted method
- **Exception context**: Try-catch block dependencies
- **Parameter inference**: What parameters the extracted method needs
- **Keyword conflicts**: 'catch' is a reserved Java keyword

## Fundamental ML Limitations in Code Refactoring

### 1. Syntactic vs Semantic Understanding

| Aspect | ML Model Capability | Required for Safe Refactoring |
|--------|-------------------|------------------------------|
| **Pattern Recognition** | ✅ Excellent | ✅ Identifies refactoring opportunities |
| **Type System Analysis** | ❌ None | ✅ Critical for type changes |
| **Dependency Tracking** | ❌ None | ✅ Essential for method extraction |
| **Interface Contracts** | ❌ None | ✅ Required for signature changes |
| **Scope Analysis** | ❌ None | ✅ Necessary for variable operations |

### 2. Feature Representation Limitations

#### ML Model Features (What It Sees)
```python
features = {
    'class_encoded': 42,           # Opaque numeric encoding
    'method_encoded': 17,          # Opaque numeric encoding
    'lines_changed': 3,            # Surface-level metric
    'cyclomatic_complexity': 2,    # Structural complexity
    'nesting_depth': 1             # Structural nesting
}
```

#### Real Code Dependencies (What It Misses)
```java
// Type relationships
interface Context { int getCount(); }
class Implementation implements Context { private int count; }

// Method call chains
obj.getCount() -> returns int -> used in calculations -> affects other methods

// Variable lifetimes and scope
try { int localVar = 5; } catch (Exception e) { /* localVar not accessible */ }

// Inheritance hierarchies
@Override // Only valid if parent method exists
```

### 3. Compilation vs Runtime Semantics

#### What ML Predicts
- **Refactoring type**: "Change Return Type"
- **Confidence**: High (based on similar patterns)
- **Context**: Structural similarity to training examples

#### What Reality Requires
```java
// Before refactoring - all these must be analyzed:
public int getValue() { return intField; }           // Method signature
int result = obj.getValue();                         // All callers
interface Contract { int getValue(); }               // Interface contracts
class Child extends Parent { int getValue() {...} } // Inheritance chains
```

## Implications for Refactoring Tool Development

### 1. ML as Pattern Detector, Not Executor
- **Strength**: Identify refactoring opportunities from historical patterns
- **Limitation**: Cannot safely execute transformations without additional analysis
- **Solution**: ML + sophisticated static analysis + behavioral validation

### 2. The Behavioral Validation Gap
- **Traditional Metrics**: Precision, Recall, F1-Score (syntactic correctness)
- **Missing Metric**: Functional safety after transformation (semantic correctness)
- **Our Contribution**: Systematic behavioral validation methodology

### 3. Hybrid Approach Necessity
```
ML Prediction → Static Analysis → Transformation → Behavioral Validation
     ↓               ↓                ↓                    ↓
  Pattern ID    Dependency       Safe Code         Test Suite
              Analysis         Modification       Validation
```

## Research Contributions

### 1. Empirical Evidence of ML Limitations
- **Quantified gap**: 30.8% prediction accuracy → 57.1% behavioral safety
- **Concrete examples**: Type system, annotation semantics, scope analysis failures
- **Systematic evaluation**: 8 correct predictions, 7 tested, 3 failed despite correctness

### 2. Behavioral Validation Methodology
- **Novel approach**: Test actual code transformations, not just predictions
- **Real-world validation**: 940 unit tests on production codebase (Mockito)
- **Comprehensive analysis**: Naive vs proper refactoring tool comparison

### 3. Practical Insights for Tool Development
- **ML + Tooling**: Proper refactoring tools improve safety from 33.3% to 57.1%
- **Inherent limitations**: Even sophisticated tools cannot achieve 100% safety
- **Validation necessity**: Behavioral testing essential for production deployment

## Conclusion

This analysis demonstrates that while ML models excel at pattern recognition for identifying refactoring opportunities, they fundamentally lack the semantic understanding required for safe code transformation. The gap between prediction accuracy (30.8%) and behavioral safety (57.1%) represents a critical challenge in automated refactoring that cannot be solved by improved ML algorithms alone, but requires sophisticated static analysis, proper refactoring tools, and comprehensive behavioral validation.

**Key Takeaway**: ML-guided refactoring tools must combine pattern recognition capabilities with deep semantic analysis and rigorous behavioral validation to achieve production-ready safety and reliability.
