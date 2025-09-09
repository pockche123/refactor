public class StringUtils21Test {
    
    public static void main(String[] args) {
        StringUtils21 utils = new StringUtils21();
        StringHelper21 helper = new StringHelper21();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils21.isEmpty("");
        String capitalized = StringUtils21.capitalize("hello");
        String reversed = StringHelper21.reverse("hello");
        String helperInfo = StringHelper21.getHelperInfo();
        
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