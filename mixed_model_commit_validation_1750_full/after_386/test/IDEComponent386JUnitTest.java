import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class IDEComponent386JUnitTest {
    
    private IDEComponent386 component;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        component = new IDEComponent386();
    }
    
    @Test
    void testMethodFunctionality() {
        assertDoesNotThrow(() -> {
            component.processData();
        });
    }
    
    @Test
    void testGetDomainInfo() {
        String info = component.getDomainInfo();
        assertNotNull(info);
        assertTrue(info.contains("intellij"));
    }
    
    @Test
    void testObjectCreation() {
        assertNotNull(component);
    }
}