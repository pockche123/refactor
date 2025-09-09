public class StringUtils331Test {
    
    public static void main(String[] args) {
        StringUtils331 utils = new StringUtils331();
        StringHelper331 helper = new StringHelper331();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils331.isEmpty("");
        String capitalized = StringUtils331.capitalize("hello");
        String reversed = StringHelper331.reverse("hello");
        String helperInfo = StringHelper331.getHelperInfo();
        
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