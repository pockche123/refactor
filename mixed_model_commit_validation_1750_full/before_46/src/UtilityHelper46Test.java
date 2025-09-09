public class UtilityHelper46Test {
    
    public static void main(String[] args) {
        UtilityHelper46 component = new UtilityHelper46();
        UtilityUtils46 helper = new UtilityUtils46();
        
        // Test functionality
        component.processData();
        String extracted = component.extractInfo();
        String domainInfo = component.getDomainInfo();
        String utilityInfo = helper.getUtilityInfo();
        
        // Simple validation
        int testsRun = 4;
        int testsPassed = 0;
        
        if (domainInfo != null && domainInfo.contains("commons_lang")) {
            testsPassed++;
        }
        
        if (utilityInfo != null && utilityInfo.contains("commons_lang")) {
            testsPassed++;
        }
        
        if (extracted != null && extracted.contains("Extracted")) {
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