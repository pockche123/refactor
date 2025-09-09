import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class IntellijComponent272JUnitTest {
    
    private IntellijComponent272 component;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        component = new IntellijComponent272();
    }
    
    @Test
    void testMethodFunctionality() {
        assertDoesNotThrow(() -> {
            component.processFile();
        });
    }
    
    @Test
    void testGetComponentInfo() {
        String info = component.getComponentInfo();
        assertNotNull(info);
        assertTrue(info.contains("IntelliJ"));
    }
    
    @Test
    void testObjectCreation() {
        assertNotNull(component);
    }
}