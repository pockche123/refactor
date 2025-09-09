import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class IDEComponent446JUnitTest {
    
    private IDEComponent446 component;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        component = new IDEComponent446();
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