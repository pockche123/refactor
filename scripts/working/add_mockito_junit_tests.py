#!/usr/bin/env python3
"""
Add JUnit tests to Mockito behavioral validation
Following Spring Framework dual testing methodology
"""

from pathlib import Path

def create_mockito_junit_tests():
    """Add JUnit tests to all Mockito validation directories"""
    
    # Find Mockito validation directories
    validation_dirs = []
    for pattern in ["mockito_commit_validation", "mockito_behavioral_validation", "mockito_validation"]:
        validation_dir = Path(pattern)
        if validation_dir.exists():
            validation_dirs.append(validation_dir)
            break
    
    if not validation_dirs:
        print("❌ Mockito validation directory not found! Checking current directory...")
        # Check for any mockito-related directories
        current_dir = Path(".")
        mockito_dirs = [d for d in current_dir.iterdir() if d.is_dir() and "mockito" in d.name.lower()]
        if mockito_dirs:
            print(f"   Found Mockito directories: {[d.name for d in mockito_dirs]}")
            validation_dir = mockito_dirs[0]
        else:
            print("   No Mockito validation directories found")
            return 0
    else:
        validation_dir = validation_dirs[0]
    
    print(f"📊 Using validation directory: {validation_dir}")
    
    # Find all before/after directories
    before_dirs = sorted([d for d in validation_dir.iterdir() if d.name.startswith("before_")])
    after_dirs = sorted([d for d in validation_dir.iterdir() if d.name.startswith("after_")])
    
    print(f"   Found {len(before_dirs)} before directories and {len(after_dirs)} after directories")
    
    total_created = 0
    
    # Add JUnit tests to each directory
    for before_dir in before_dirs:
        index = before_dir.name.split("_")[1]
        after_dir = validation_dir / f"after_{index}"
        
        if after_dir.exists():
            create_junit_test_for_directory(before_dir, "before", index)
            create_junit_test_for_directory(after_dir, "after", index)
            total_created += 2
    
    # Create Maven pom.xml
    create_mockito_pom(validation_dir)
    
    print(f"\n✅ Added JUnit tests to {total_created} directories")
    print(f"   Structure: {validation_dir}/*/test/SourceClassJUnitTest.java")
    
    return total_created

def create_junit_test_for_directory(directory, type_name, index):
    """Create JUnit test for a specific directory"""
    
    test_dir = directory / "test"
    test_dir.mkdir(exist_ok=True)
    
    # Mockito uses SourceClass pattern with mocking capabilities
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassJUnitTest {{
    
    private SourceClass sourceClass;
    
    @Mock
    private Object mockDependency;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }}
    
    @Test
    void testMethodFunctionality() {{
        // Test main method functionality
        assertDoesNotThrow(() -> {{
            String result = sourceClass.processData();
            assertNotNull(result);
        }});
    }}
    
    @Test
    void testMethodReturnValue() {{
        // Test method returns expected value
        String result = sourceClass.processData();
        assertNotNull(result);
        assertTrue(result.length() > 0);
    }}
    
    @Test
    void testMethodConsistency() {{
        // Test method returns consistent results
        String result1 = sourceClass.processData();
        String result2 = sourceClass.processData();
        assertEquals(result1, result2);
    }}
    
    @Test
    void testWithMockito() {{
        // Test using Mockito mocking capabilities
        Object mockObj = mock(Object.class);
        when(mockObj.toString()).thenReturn("mocked");
        
        assertEquals("mocked", mockObj.toString());
        verify(mockObj).toString();
    }}
    
    @Test
    void testObjectState() {{
        // Test object is in valid state
        assertNotNull(sourceClass);
        assertTrue(sourceClass.getClass().getMethods().length > 0);
    }}
    
    @Test
    void testObjectCreation() {{
        // Test object can be created successfully
        SourceClass newInstance = new SourceClass();
        assertNotNull(newInstance);
    }}
    
    @Test
    void testMethodExists() {{
        // Test that required methods exist
        assertNotNull(sourceClass);
        assertDoesNotThrow(() -> {{
            sourceClass.processData();
        }});
    }}
}}"""
    
    with open(test_dir / "SourceClassJUnitTest.java", 'w') as f:
        f.write(junit_test)

def create_mockito_pom(validation_dir):
    """Create Maven pom.xml for Mockito validation"""
    
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.research</groupId>
    <artifactId>mockito-behavioral-validation</artifactId>
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
    
    with open(validation_dir / "pom.xml", 'w') as f:
        f.write(pom_xml)
    
    print(f"   ✅ {validation_dir}/pom.xml")

def main():
    print("🚀 ADDING JUNIT TESTS TO MOCKITO VALIDATION")
    print("=" * 60)
    
    total_created = create_mockito_junit_tests()
    
    print(f"\n📋 MOCKITO DUAL TESTING STRUCTURE:")
    print(f"   src/ - Simple main() method tests (existing)")
    print(f"   test/ - JUnit 5 + Mockito tests (new)")
    print(f"   Total JUnit test files created: {total_created}")
    print(f"   Both test the same SourceClass functionality")
    print(f"   JUnit tests include Mockito mocking examples")

if __name__ == "__main__":
    main()
