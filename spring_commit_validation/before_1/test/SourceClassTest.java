import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class SourceClassTest {
    
    private SourceClass sourceClass;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        sourceClass = new SourceClass();
    }
    
    @Test
    void testProcessData1() {
        // Test method returns expected result
        String result = sourceClass.processData1();
        assertEquals("Result: 60", result);
    }
    
    @Test
    void testProcessData1NotNull() {
        // Test method doesn't return null
        String result = sourceClass.processData1();
        assertNotNull(result);
    }
    
    @Test
    void testProcessData1Format() {
        // Test result format
        String result = sourceClass.processData1();
        assertTrue(result.startsWith("Result: "));
    }
    
    @Test
    void testGetStatus() {
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }
}