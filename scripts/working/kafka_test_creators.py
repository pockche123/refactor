#!/usr/bin/env python3
"""
Kafka test creation functions for different refactoring types
"""

def create_variable_type_test(before_src, after_src, before_test, after_test, index):
    """Create test for variable type change refactoring"""
    
    # Before: Original variable type
    before_class = f"""public class KafkaProcessor {{
    
    public void processMessage{index}() {{
        String messageId = "msg-" + System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # After: Changed variable type
    after_class = f"""public class KafkaProcessor {{
    
    public void processMessage{index}() {{
        Long messageId = System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # Write source files
    with open(before_src / "KafkaProcessor.java", 'w') as f:
        f.write(before_class)
    
    with open(after_src / "KafkaProcessor.java", 'w') as f:
        f.write(after_class)
    
    # Create simple tests
    create_simple_test(before_src, after_src, "KafkaProcessor", f"processMessage{index}")
    
    # Create JUnit tests
    create_junit_test(before_test, after_test, "KafkaProcessor", f"processMessage{index}", "variable_type")

def create_return_type_test(before_src, after_src, before_test, after_test, index):
    """Create test for return type change refactoring"""
    
    # Before: Original return type
    before_class = f"""public class KafkaProcessor {{
    
    public String getMessageId{index}() {{
        return "msg-" + System.currentTimeMillis();
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # After: Changed return type
    after_class = f"""public class KafkaProcessor {{
    
    public Long getMessageId{index}() {{
        return System.currentTimeMillis();
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # Write source files
    with open(before_src / "KafkaProcessor.java", 'w') as f:
        f.write(before_class)
    
    with open(after_src / "KafkaProcessor.java", 'w') as f:
        f.write(after_class)
    
    # Create simple tests
    create_simple_test(before_src, after_src, "KafkaProcessor", f"getMessageId{index}")
    
    # Create JUnit tests
    create_junit_test(before_test, after_test, "KafkaProcessor", f"getMessageId{index}", "return_type")

def create_rename_method_test(before_src, after_src, before_test, after_test, index):
    """Create test for rename method refactoring"""
    
    # Before: Original method name
    before_class = f"""public class KafkaProcessor {{
    
    public void processData{index}() {{
        System.out.println("Processing Kafka message");
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # After: Renamed method
    after_class = f"""public class KafkaProcessor {{
    
    public void processKafkaMessage{index}() {{
        System.out.println("Processing Kafka message");
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # Write source files
    with open(before_src / "KafkaProcessor.java", 'w') as f:
        f.write(before_class)
    
    with open(after_src / "KafkaProcessor.java", 'w') as f:
        f.write(after_class)
    
    # Create simple tests (different method names)
    create_simple_test_rename(before_src, after_src, "KafkaProcessor", f"processData{index}", f"processKafkaMessage{index}")
    
    # Create JUnit tests
    create_junit_test_rename(before_test, after_test, "KafkaProcessor", f"processData{index}", f"processKafkaMessage{index}")

def create_move_method_test(before_src, after_src, before_test, after_test, index):
    """Create test for move method refactoring"""
    
    # Before: Method in source class
    before_class = f"""public class KafkaProcessor {{
    
    public void processMessage{index}() {{
        System.out.println("Processing message");
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    before_helper = """public class MessageHelper {
    
    public String getHelperStatus() {
        return "helper ready";
    }
}"""
    
    # After: Method moved to helper class
    after_class = f"""public class KafkaProcessor {{
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    after_helper = f"""public class MessageHelper {{
    
    public void processMessage{index}() {{
        System.out.println("Processing message");
    }}
    
    public String getHelperStatus() {{
        return "helper ready";
    }}
}}"""
    
    # Write source files
    with open(before_src / "KafkaProcessor.java", 'w') as f:
        f.write(before_class)
    with open(before_src / "MessageHelper.java", 'w') as f:
        f.write(before_helper)
    
    with open(after_src / "KafkaProcessor.java", 'w') as f:
        f.write(after_class)
    with open(after_src / "MessageHelper.java", 'w') as f:
        f.write(after_helper)
    
    # Create simple tests
    create_simple_test_move(before_src, after_src, f"processMessage{index}")
    
    # Create JUnit tests
    create_junit_test_move(before_test, after_test, f"processMessage{index}")

def create_generic_test(before_src, after_src, before_test, after_test, refactoring_type, index):
    """Create generic test for other refactoring types"""
    
    # Generic before/after classes
    before_class = f"""public class KafkaProcessor {{
    
    public String processData{index}() {{
        return "original kafka processing";
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    after_class = f"""public class KafkaProcessor {{
    
    public String processData{index}() {{
        return "refactored kafka processing";
    }}
    
    public String getStatus() {{
        return "processing";
    }}
}}"""
    
    # Write source files
    with open(before_src / "KafkaProcessor.java", 'w') as f:
        f.write(before_class)
    
    with open(after_src / "KafkaProcessor.java", 'w') as f:
        f.write(after_class)
    
    # Create simple tests
    create_simple_test(before_src, after_src, "KafkaProcessor", f"processData{index}")
    
    # Create JUnit tests
    create_junit_test(before_test, after_test, "KafkaProcessor", f"processData{index}", "generic")

def create_simple_test(before_src, after_src, class_name, method_name):
    """Create simple main() method tests"""
    
    test_class = f"""public class {class_name}Test {{
    
    public static void main(String[] args) {{
        {class_name} processor = new {class_name}();
        
        // Test method functionality
        processor.{method_name}();
        
        // Test status
        String status = processor.getStatus();
        
        // Simple test validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {{
            testsPassed++;
        }}
        
        // Method should execute without error
        try {{
            processor.{method_name}();
            testsPassed++;
        }} catch (Exception e) {{
            // Test failed
        }}
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {{
            System.out.println("ALL TESTS PASSED!");
        }} else {{
            System.out.println("SOME TESTS FAILED!");
        }}
    }}
}}"""
    
    with open(before_src / f"{class_name}Test.java", 'w') as f:
        f.write(test_class)
    
    with open(after_src / f"{class_name}Test.java", 'w') as f:
        f.write(test_class)

def create_simple_test_rename(before_src, after_src, class_name, old_method, new_method):
    """Create simple tests for renamed methods"""
    
    before_test = f"""public class {class_name}Test {{
    
    public static void main(String[] args) {{
        {class_name} processor = new {class_name}();
        
        // Test method functionality
        processor.{old_method}();
        
        // Test status
        String status = processor.getStatus();
        
        // Simple test validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {{
            testsPassed++;
        }}
        
        try {{
            processor.{old_method}();
            testsPassed++;
        }} catch (Exception e) {{
            // Test failed
        }}
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {{
            System.out.println("ALL TESTS PASSED!");
        }} else {{
            System.out.println("SOME TESTS FAILED!");
        }}
    }}
}}"""
    
    after_test = f"""public class {class_name}Test {{
    
    public static void main(String[] args) {{
        {class_name} processor = new {class_name}();
        
        // Test method functionality
        processor.{new_method}();
        
        // Test status
        String status = processor.getStatus();
        
        // Simple test validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {{
            testsPassed++;
        }}
        
        try {{
            processor.{new_method}();
            testsPassed++;
        }} catch (Exception e) {{
            // Test failed
        }}
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {{
            System.out.println("ALL TESTS PASSED!");
        }} else {{
            System.out.println("SOME TESTS FAILED!");
        }}
    }}
}}"""
    
    with open(before_src / f"{class_name}Test.java", 'w') as f:
        f.write(before_test)
    
    with open(after_src / f"{class_name}Test.java", 'w') as f:
        f.write(after_test)

def create_simple_test_move(before_src, after_src, method_name):
    """Create simple tests for moved methods"""
    
    before_test = f"""public class KafkaProcessorTest {{
    
    public static void main(String[] args) {{
        KafkaProcessor processor = new KafkaProcessor();
        MessageHelper helper = new MessageHelper();
        
        // Test method functionality
        processor.{method_name}();
        
        // Test status
        String status = processor.getStatus();
        String helperStatus = helper.getHelperStatus();
        
        // Simple test validation
        int testsRun = 3;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {{
            testsPassed++;
        }}
        
        if ("helper ready".equals(helperStatus)) {{
            testsPassed++;
        }}
        
        try {{
            processor.{method_name}();
            testsPassed++;
        }} catch (Exception e) {{
            // Test failed
        }}
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {{
            System.out.println("ALL TESTS PASSED!");
        }} else {{
            System.out.println("SOME TESTS FAILED!");
        }}
    }}
}}"""
    
    after_test = f"""public class KafkaProcessorTest {{
    
    public static void main(String[] args) {{
        KafkaProcessor processor = new KafkaProcessor();
        MessageHelper helper = new MessageHelper();
        
        // Test method functionality (now in helper)
        helper.{method_name}();
        
        // Test status
        String status = processor.getStatus();
        String helperStatus = helper.getHelperStatus();
        
        // Simple test validation
        int testsRun = 3;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {{
            testsPassed++;
        }}
        
        if ("helper ready".equals(helperStatus)) {{
            testsPassed++;
        }}
        
        try {{
            helper.{method_name}();
            testsPassed++;
        }} catch (Exception e) {{
            // Test failed
        }}
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {{
            System.out.println("ALL TESTS PASSED!");
        }} else {{
            System.out.println("SOME TESTS FAILED!");
        }}
    }}
}}"""
    
    with open(before_src / "KafkaProcessorTest.java", 'w') as f:
        f.write(before_test)
    
    with open(after_src / "KafkaProcessorTest.java", 'w') as f:
        f.write(after_test)

def create_junit_test(before_test, after_test, class_name, method_name, test_type):
    """Create JUnit tests"""
    
    junit_test = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class {class_name}JUnitTest {{
    
    private {class_name} processor;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        processor = new {class_name}();
    }}
    
    @Test
    void testMethodFunctionality() {{
        // Test method execution
        assertDoesNotThrow(() -> {{
            processor.{method_name}();
        }});
    }}
    
    @Test
    void testGetStatus() {{
        // Test status method
        String status = processor.getStatus();
        assertEquals("processing", status);
    }}
    
    @Test
    void testObjectCreation() {{
        // Test object can be created
        assertNotNull(processor);
    }}
    
    @Test
    void testMethodConsistency() {{
        // Test method executes consistently
        assertDoesNotThrow(() -> {{
            processor.{method_name}();
            processor.{method_name}();
        }});
    }}
}}"""
    
    with open(before_test / f"{class_name}JUnitTest.java", 'w') as f:
        f.write(junit_test)
    
    with open(after_test / f"{class_name}JUnitTest.java", 'w') as f:
        f.write(junit_test)

def create_junit_test_rename(before_test, after_test, class_name, old_method, new_method):
    """Create JUnit tests for renamed methods"""
    
    before_junit = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class {class_name}JUnitTest {{
    
    private {class_name} processor;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        processor = new {class_name}();
    }}
    
    @Test
    void testMethodFunctionality() {{
        assertDoesNotThrow(() -> {{
            processor.{old_method}();
        }});
    }}
    
    @Test
    void testGetStatus() {{
        String status = processor.getStatus();
        assertEquals("processing", status);
    }}
    
    @Test
    void testObjectCreation() {{
        assertNotNull(processor);
    }}
}}"""
    
    after_junit = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class {class_name}JUnitTest {{
    
    private {class_name} processor;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        processor = new {class_name}();
    }}
    
    @Test
    void testMethodFunctionality() {{
        assertDoesNotThrow(() -> {{
            processor.{new_method}();
        }});
    }}
    
    @Test
    void testGetStatus() {{
        String status = processor.getStatus();
        assertEquals("processing", status);
    }}
    
    @Test
    void testObjectCreation() {{
        assertNotNull(processor);
    }}
}}"""
    
    with open(before_test / f"{class_name}JUnitTest.java", 'w') as f:
        f.write(before_junit)
    
    with open(after_test / f"{class_name}JUnitTest.java", 'w') as f:
        f.write(after_junit)

def create_junit_test_move(before_test, after_test, method_name):
    """Create JUnit tests for moved methods"""
    
    before_junit = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class KafkaProcessorJUnitTest {{
    
    private KafkaProcessor processor;
    private MessageHelper helper;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        processor = new KafkaProcessor();
        helper = new MessageHelper();
    }}
    
    @Test
    void testMethodFunctionality() {{
        assertDoesNotThrow(() -> {{
            processor.{method_name}();
        }});
    }}
    
    @Test
    void testGetStatus() {{
        String status = processor.getStatus();
        assertEquals("processing", status);
    }}
    
    @Test
    void testHelperStatus() {{
        String status = helper.getHelperStatus();
        assertEquals("helper ready", status);
    }}
}}"""
    
    after_junit = f"""import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class KafkaProcessorJUnitTest {{
    
    private KafkaProcessor processor;
    private MessageHelper helper;
    
    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        processor = new KafkaProcessor();
        helper = new MessageHelper();
    }}
    
    @Test
    void testMethodFunctionality() {{
        assertDoesNotThrow(() -> {{
            helper.{method_name}();
        }});
    }}
    
    @Test
    void testGetStatus() {{
        String status = processor.getStatus();
        assertEquals("processing", status);
    }}
    
    @Test
    void testHelperStatus() {{
        String status = helper.getHelperStatus();
        assertEquals("helper ready", status);
    }}
}}"""
    
    with open(before_test / "KafkaProcessorJUnitTest.java", 'w') as f:
        f.write(before_junit)
    
    with open(after_test / "KafkaProcessorJUnitTest.java", 'w') as f:
        f.write(after_junit)
