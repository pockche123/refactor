import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtils76JUnitTest {
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    void testIsEmpty() {
        assertTrue(StringUtils76.isEmpty(""));
        assertTrue(StringUtils76.isEmpty(null));
        assertFalse(StringUtils76.isEmpty("test"));
    }
    
    @Test
    void testGetUtilityInfo() {
        String info = StringUtils76.getUtilityInfo();
        assertNotNull(info);
        assertTrue(info.contains("Commons Lang"));
    }
    
    @Test
    void testUtilityMethods() {
        // Test utility method consistency
        assertDoesNotThrow(() -> {
            StringUtils76.isEmpty("");
            StringUtils76.getUtilityInfo();
        });
    }
}