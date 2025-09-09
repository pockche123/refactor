public class SpringService1061Test {
    
    public static void main(String[] args) {
        SpringService1061 component = new SpringService1061();
        
        // Test functionality
        component.processData();
        String domainInfo = component.getDomainInfo();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (domainInfo != null && domainInfo.contains("spring")) {
            testsPassed++;
        }
        
        try {
            component.processData();
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