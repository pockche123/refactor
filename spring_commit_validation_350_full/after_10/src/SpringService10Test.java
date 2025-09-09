public class SpringService10Test {
    
    public static void main(String[] args) {
        SpringService10 service = new SpringService10();
        SpringHelper10 helper = new SpringHelper10();
        
        // Test functionality (method now in helper)
        helper.processData();
        String status = service.getStatus();
        String helperStatus = helper.getHelperStatus();
        
        // Simple validation
        int testsRun = 3;
        int testsPassed = 0;
        
        if ("active".equals(status)) {
            testsPassed++;
        }
        
        if ("helper ready".equals(helperStatus)) {
            testsPassed++;
        }
        
        try {
            helper.processData();
            testsPassed++;
        } catch (Exception e) {
            // Test failed
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