import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtils162JUnitTest {
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    void testIsEmpty() {
        assertTrue(StringUtils162.isEmpty(""));
        assertTrue(StringUtils162.isEmpty(null));
        assertFalse(StringUtils162.isEmpty("test"));
    }
    
    @Test
    void testGetUtilityInfo() {
        String info = StringUtils162.getUtilityInfo();
        assertNotNull(info);
        assertTrue(info.contains("Commons Lang"));
    }
    
    @Test
    void testUtilityMethods() {
        // Test utility method consistency
        assertDoesNotThrow(() -> {
            StringUtils162.isEmpty("");
            StringUtils162.getUtilityInfo();
        });
    }
}