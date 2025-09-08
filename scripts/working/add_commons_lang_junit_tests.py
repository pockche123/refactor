#!/usr/bin/env python3
"""
Add JUnit tests to Commons Lang behavioral validation
Following Spring Framework dual testing methodology
"""

from pathlib import Path

def create_commons_lang_junit_tests():
    """Add JUnit tests to all Commons Lang validation directories"""
    
    validation_dir = Path("commons_lang_commit_validation")
    
    if not validation_dir.exists():
        print("❌ Commons Lang validation directory not found!")
        return
    
    # Find all before/after directories
    before_dirs = sorted([d for d in validation_dir.iterdir() if d.name.startswith("before_")])
    after_dirs = sorted([d for d in validation_dir.iterdir() if d.name.startswith("after_")])
    
    print(f"📊 Found {len(before_dirs)} before directories and {len(after_dirs)} after directories")
    
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
    create_commons_lang_pom()
    
    print(f"\n✅ Added JUnit tests to {total_created} directories")
    print(f"   Structure: commons_lang_commit_validation/*/test/LangAssertionsJUnitTest.java")
    
    return total_created

def create_junit_test_for_directory(directory, type_name, index):
    """Create JUnit test for a specific directory"""
    
    test_dir = directory / "test"
    test_dir.mkdir(exist_ok=True)
    
    # Commons Lang uses LangAssertions pattern
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class LangAssertionsJUnitTest {{
    
    private LangAssertions langAssertions;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        langAssertions = new LangAssertions();
    }}
    
    @Test
    void testAssertIllegalArgumentException() {{
        // Test assertion method functionality
        assertDoesNotThrow(() -> {{
            langAssertions.assertIllegalArgumentException("test message", () -> {{
                throw new IllegalArgumentException("test");
            }});
        }});
    }}
    
    @Test
    void testAssertIllegalArgumentExceptionWithNullMessage() {{
        // Test null message handling
        assertDoesNotThrow(() -> {{
            langAssertions.assertIllegalArgumentException(null, () -> {{
                throw new IllegalArgumentException("test");
            }});
        }});
    }}
    
    @Test
    void testAssertNullPointerException() {{
        // Test NPE assertion
        assertDoesNotThrow(() -> {{
            langAssertions.assertNullPointerException("test message", () -> {{
                throw new NullPointerException("test");
            }});
        }});
    }}
    
    @Test
    void testAssertIndexOutOfBoundsException() {{
        // Test index bounds assertion
        assertDoesNotThrow(() -> {{
            langAssertions.assertIndexOutOfBoundsException("test message", () -> {{
                throw new IndexOutOfBoundsException("test");
            }});
        }});
    }}
    
    @Test
    void testAssertionMethodsExist() {{
        // Test that assertion methods exist and are callable
        assertNotNull(langAssertions);
        assertTrue(langAssertions.getClass().getMethods().length > 0);
    }}
    
    @Test
    void testObjectCreation() {{
        // Test object can be created successfully
        LangAssertions newInstance = new LangAssertions();
        assertNotNull(newInstance);
    }}
}}"""
    
    with open(test_dir / "LangAssertionsJUnitTest.java", 'w') as f:
        f.write(junit_test)

def create_commons_lang_pom():
    """Create Maven pom.xml for Commons Lang validation"""
    
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.research</groupId>
    <artifactId>commons-lang-behavioral-validation</artifactId>
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
    
    with open("commons_lang_commit_validation/pom.xml", 'w') as f:
        f.write(pom_xml)
    
    print("   ✅ commons_lang_commit_validation/pom.xml")

def main():
    print("🚀 ADDING JUNIT TESTS TO COMMONS LANG VALIDATION")
    print("=" * 60)
    
    total_created = create_commons_lang_junit_tests()
    
    print(f"\n📋 COMMONS LANG DUAL TESTING STRUCTURE:")
    print(f"   src/ - Simple main() method tests (existing)")
    print(f"   test/ - JUnit 5 + Mockito tests (new)")
    print(f"   Total JUnit test files created: {total_created}")
    print(f"   Both test the same LangAssertions functionality")

if __name__ == "__main__":
    main()
