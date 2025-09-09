public class StringUtils193Test {
    
    public static void main(String[] args) {
        StringUtils193 utils = new StringUtils193();
        StringHelper193 helper = new StringHelper193();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils193.isEmpty("");
        String capitalized = StringUtils193.capitalize("hello");
        String reversed = StringHelper193.reverse("hello");
        String helperInfo = StringHelper193.getHelperInfo();
        
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