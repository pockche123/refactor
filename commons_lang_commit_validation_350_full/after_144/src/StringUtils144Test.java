public class StringUtils144Test {
    
    public static void main(String[] args) {
        StringUtils144 utils = new StringUtils144();
        StringHelper144 helper = new StringHelper144();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils144.isEmpty("");
        String capitalized = StringUtils144.capitalize("hello");
        String reversed = StringHelper144.reverse("hello");
        String helperInfo = StringHelper144.getHelperInfo();
        
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