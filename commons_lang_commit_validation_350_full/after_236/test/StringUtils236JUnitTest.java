import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtils236JUnitTest {
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    void testIsEmpty() {
        assertTrue(StringUtils236.isEmpty(""));
        assertTrue(StringUtils236.isEmpty(null));
        assertFalse(StringUtils236.isEmpty("test"));
    }
    
    @Test
    void testGetUtilityInfo() {
        String info = StringUtils236.getUtilityInfo();
        assertNotNull(info);
        assertTrue(info.contains("Commons Lang"));
    }
    
    @Test
    void testUtilityMethods() {
        // Test utility method consistency
        assertDoesNotThrow(() -> {
            StringUtils236.isEmpty("");
            StringUtils236.getUtilityInfo();
        });
    }
}