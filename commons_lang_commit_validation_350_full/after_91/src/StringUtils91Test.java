public class StringUtils91Test {
    
    public static void main(String[] args) {
        StringUtils91 utils = new StringUtils91();
        StringHelper91 helper = new StringHelper91();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils91.isEmpty("");
        String capitalized = StringUtils91.capitalize("hello");
        String reversed = StringHelper91.reverse("hello");
        String helperInfo = StringHelper91.getHelperInfo();
        
        // Simple validation
        int testsRun = 4;
        int testsPassed = 0;
        
        if (isEmpty) {
            testsPassed++;
        }
        
        if ("Hello".equals(capitalized)) {
            testsPassed++;
        }
        
        if ("olleh".equals(reversed)) {
            testsPassed++;
        }
        
        if ("String utility helper".equals(helperInfo)) {
            testsPassed++;
        }
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {
            System.out.println("ALL TESTS PASSED!");
        } else {
            System.out.println("SOME TESTS FAILED!");
        }
    }
}