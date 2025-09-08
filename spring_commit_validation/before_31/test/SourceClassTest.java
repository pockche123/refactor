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
    void testProcessData() {
        // Test public method functionality
        String result = sourceClass.processData();
        assertEquals("helper result", result);
    }
    
    @Test
    void testProcessDataNotNull() {
        // Test method doesn't return null
        String result = sourceClass.processData();
        assertNotNull(result);
    }
    
    @Test
    void testGetStatus() {
        // Test status method
        String status = sourceClass.getStatus();
        assertEquals("working", status);
    }
    
    @Test
    void testObjectCreation() {
        // Test object can be created
        assertNotNull(sourceClass);
    }
}