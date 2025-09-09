public class StringUtils335Test {
    
    public static void main(String[] args) {
        StringUtils335 utils = new StringUtils335();
        StringHelper335 helper = new StringHelper335();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils335.isEmpty("");
        String capitalized = StringUtils335.capitalize("hello");
        String reversed = StringHelper335.reverse("hello");
        String helperInfo = StringHelper335.getHelperInfo();
        
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