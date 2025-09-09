public class StringUtils72Test {
    
    public static void main(String[] args) {
        StringUtils72 utils = new StringUtils72();
        StringHelper72 helper = new StringHelper72();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils72.isEmpty("");
        String capitalized = StringUtils72.capitalize("hello");
        String reversed = StringHelper72.reverse("hello");
        String helperInfo = StringHelper72.getHelperInfo();
        
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