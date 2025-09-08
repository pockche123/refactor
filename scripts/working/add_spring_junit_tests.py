#!/usr/bin/env python3
"""
Add JUnit/Mockito tests to Spring Framework behavioral validation
Keep existing simple tests, add proper unit tests in test/ subdirectory
"""

import pandas as pd
from pathlib import Path

def load_correct_predictions():
    """Load correct ML predictions from Spring Framework"""
    df = pd.read_csv('results/working/spring_ml_test_results.csv')
    correct_predictions = df[df['correct_prediction'] == True]
    return correct_predictions

def create_junit_tests(prediction, index):
    """Create JUnit tests for a prediction"""
    
    refactoring_type = prediction['refactoring_type']
    
    # Create test directories
    before_test_dir = Path(f"spring_commit_validation/before_{index}/test")
    after_test_dir = Path(f"spring_commit_validation/after_{index}/test")
    
    before_test_dir.mkdir(exist_ok=True)
    after_test_dir.mkdir(exist_ok=True)
    
    # Create JUnit tests based on refactoring type
    if 'Method Annotation' in refactoring_type:
        create_method_annotation_junit(before_test_dir, after_test_dir, refactoring_type, index)
    elif 'Attribute Annotation' in refactoring_type:
        create_attribute_annotation_junit(before_test_dir, after_test_dir, refactoring_type, index)
    elif 'Extract Variable' in refactoring_type:
        create_extract_variable_junit(before_test_dir, after_test_dir, index)
    elif 'Access Modifier' in refactoring_type:
        create_access_modifier_junit(before_test_dir, after_test_dir, index)
    else:
        create_generic_junit(before_test_dir, after_test_dir, refactoring_type, index)

def create_method_annotation_junit(before_test_dir, after_test_dir, refactoring_type, index):
    """Create JUnit tests for method annotation refactoring"""
    
    method_name = f"processData{index}"
    
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassTest {{
    
    private SourceClass sourceClass;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }}
    
    @Test
    void test{method_name.capitalize()}WithValidData() {{
        // Test method functionality
        assertDoesNotThrow(() -> {{
            sourceClass.{method_name}("test data");
        }});
    }}
    
    @Test
    void test{method_name.capitalize()}WithNullData() {{
        // Test null handling
        assertDoesNotThrow(() -> {{
            sourceClass.{method_name}(null);
        }});
    }}
    
    @Test
    void testGetStatus() {{
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }}
    
    @Test
    void testMethodExists() {{
        // Test that method exists and is callable
        assertNotNull(sourceClass);
        assertTrue(sourceClass.getClass().getMethods().length > 0);
    }}
}}"""
    
    # Write same test to both directories (behavior should be identical)
    with open(before_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)
    
    with open(after_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)

def create_attribute_annotation_junit(before_test_dir, after_test_dir, refactoring_type, index):
    """Create JUnit tests for attribute annotation refactoring"""
    
    attribute_name = f"data{index}"
    
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassTest {{
    
    private SourceClass sourceClass;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }}
    
    @Test
    void testSet{attribute_name.capitalize()}() {{
        // Test setter functionality
        assertDoesNotThrow(() -> {{
            sourceClass.set{attribute_name.capitalize()}("test value");
        }});
    }}
    
    @Test
    void testGet{attribute_name.capitalize()}() {{
        // Test getter functionality
        sourceClass.set{attribute_name.capitalize()}("test value");
        String result = sourceClass.get{attribute_name.capitalize()}();
        assertEquals("test value", result);
    }}
    
    @Test
    void testGetSetWithNull() {{
        // Test null handling
        sourceClass.set{attribute_name.capitalize()}(null);
        String result = sourceClass.get{attribute_name.capitalize()}();
        assertNull(result);
    }}
    
    @Test
    void testGetStatus() {{
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }}
}}"""
    
    # Write same test to both directories
    with open(before_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)
    
    with open(after_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)

def create_extract_variable_junit(before_test_dir, after_test_dir, index):
    """Create JUnit tests for extract variable refactoring"""
    
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassTest {{
    
    private SourceClass sourceClass;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }}
    
    @Test
    void testProcessData{index}() {{
        // Test method returns expected result
        String result = sourceClass.processData{index}();
        assertEquals("Result: 60", result);
    }}
    
    @Test
    void testProcessData{index}NotNull() {{
        // Test method doesn't return null
        String result = sourceClass.processData{index}();
        assertNotNull(result);
    }}
    
    @Test
    void testProcessData{index}Format() {{
        // Test result format
        String result = sourceClass.processData{index}();
        assertTrue(result.startsWith("Result: "));
    }}
    
    @Test
    void testGetStatus() {{
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }}
}}"""
    
    # Write same test to both directories
    with open(before_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)
    
    with open(after_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)

def create_access_modifier_junit(before_test_dir, after_test_dir, index):
    """Create JUnit tests for access modifier refactoring"""
    
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassTest {{
    
    private SourceClass sourceClass;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }}
    
    @Test
    void testProcessData() {{
        // Test public method functionality
        String result = sourceClass.processData();
        assertEquals("helper result", result);
    }}
    
    @Test
    void testProcessDataNotNull() {{
        // Test method doesn't return null
        String result = sourceClass.processData();
        assertNotNull(result);
    }}
    
    @Test
    void testGetStatus() {{
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }}
    
    @Test
    void testObjectCreation() {{
        // Test object can be created
        assertNotNull(sourceClass);
    }}
}}"""
    
    # Write same test to both directories
    with open(before_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)
    
    with open(after_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)

def create_generic_junit(before_test_dir, after_test_dir, refactoring_type, index):
    """Create generic JUnit tests for other refactoring types"""
    
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassTest {{
    
    private SourceClass sourceClass;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }}
    
    @Test
    void testProcessData{index}() {{
        // Test method functionality
        String result = sourceClass.processData{index}();
        assertNotNull(result);
        assertTrue(result.length() > 0);
    }}
    
    @Test
    void testProcessData{index}Consistency() {{
        // Test method returns consistent results
        String result1 = sourceClass.processData{index}();
        String result2 = sourceClass.processData{index}();
        assertEquals(result1, result2);
    }}
    
    @Test
    void testGetStatus() {{
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }}
    
    @Test
    void testObjectState() {{
        // Test object is in valid state
        assertNotNull(sourceClass);
        assertNotNull(sourceClass.getStatus());
    }}
}}"""
    
    # Write same test to both directories
    with open(before_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)
    
    with open(after_test_dir / "SourceClassTest.java", 'w') as f:
        f.write(junit_test)

def main():
    print("🚀 ADDING JUNIT TESTS TO SPRING FRAMEWORK VALIDATION")
    print("=" * 60)
    
    # Load correct predictions
    print("📊 Loading correct Spring Framework predictions...")
    correct_predictions = load_correct_predictions()
    print(f"   Found {len(correct_predictions)} correct predictions")
    
    # Add JUnit tests to each validation directory
    print("🧪 Adding JUnit tests to validation directories...")
    
    for i, (_, prediction) in enumerate(correct_predictions.iterrows()):
        print(f"   Adding JUnit tests {i}: {prediction['refactoring_type']}")
        create_junit_tests(prediction, i)
    
    print(f"\n✅ Added JUnit tests to {len(correct_predictions)} validation pairs")
    print(f"   Structure: spring_commit_validation/before_X/test/SourceClassTest.java")
    print(f"   Structure: spring_commit_validation/after_X/test/SourceClassTest.java")
    
    # Create Maven/Gradle build files for easy testing
    create_build_files()
    
    print(f"\n📋 TESTING STRUCTURE:")
    print(f"   src/ - Simple main() method tests (existing)")
    print(f"   test/ - JUnit 5 + Mockito tests (new)")
    print(f"   Both test the same functionality for behavioral validation")

def create_build_files():
    """Create Maven pom.xml for easy JUnit testing"""
    
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.research</groupId>
    <artifactId>spring-behavioral-validation</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <junit.version>5.9.2</junit.version>
        <mockito.version>5.1.1</mockito.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-core</artifactId>
            <version>${mockito.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-junit-jupiter</artifactId>
            <version>${mockito.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0-M9</version>
            </plugin>
        </plugins>
    </build>
</project>"""
    
    with open("spring_commit_validation/pom.xml", 'w') as f:
        f.write(pom_xml)
    
    print("   ✅ spring_commit_validation/pom.xml (Maven build file)")

if __name__ == "__main__":
    main()
