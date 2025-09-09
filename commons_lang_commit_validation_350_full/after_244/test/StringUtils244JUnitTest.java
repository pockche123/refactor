import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtils244JUnitTest {
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    void testIsEmpty() {
        assertTrue(StringUtils244.isEmpty(""));
        assertTrue(StringUtils244.isEmpty(null));
        assertFalse(StringUtils244.isEmpty("test"));
    }
    
    @Test
    void testGetUtilityInfo() {
        String info = StringUtils244.getUtilityInfo();
        assertNotNull(info);
        assertTrue(info.contains("Commons Lang"));
    }
    
    @Test
    void testUtilityMethods() {
        // Test utility method consistency
        assertDoesNotThrow(() -> {
            StringUtils244.isEmpty("");
            StringUtils244.getUtilityInfo();
        });
    }
}