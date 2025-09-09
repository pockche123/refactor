import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class IDEComponent387JUnitTest {
    
    private IDEComponent387 component;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        component = new IDEComponent387();
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