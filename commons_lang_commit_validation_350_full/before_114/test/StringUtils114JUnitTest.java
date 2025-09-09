import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtils114JUnitTest {
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    void testIsEmpty() {
        assertTrue(StringUtils114.isEmpty(""));
        assertTrue(StringUtils114.isEmpty(null));
        assertFalse(StringUtils114.isEmpty("test"));
    }
    
    @Test
    void testGetUtilityInfo() {
        String info = StringUtils114.getUtilityInfo();
        assertNotNull(info);
        assertTrue(info.contains("Commons Lang"));
    }
    
    @Test
    void testUtilityMethods() {
        // Test utility method consistency
        assertDoesNotThrow(() -> {
            StringUtils114.isEmpty("");
            StringUtils114.getUtilityInfo();
        });
    }
}