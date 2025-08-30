#!/usr/bin/env python3
"""
Analyze test suites in our projects to identify candidates for behavioral validation
"""

import os
import subprocess
import glob
from pathlib import Path

def analyze_project_tests(project_path, project_name):
    """Analyze test coverage and structure for a project"""
    
    if not os.path.exists(project_path):
        print(f"❌ {project_name}: Project not found at {project_path}")
        return None
    
    print(f"\n🔍 Analyzing {project_name.upper()}")
    print(f"Path: {project_path}")
    
    # Check if it's a valid project directory
    if not os.path.isdir(project_path):
        print(f"❌ Not a directory")
        return None
    
    # Look for build files
    build_files = []
    for build_file in ['pom.xml', 'build.gradle', 'build.gradle.kts']:
        if os.path.exists(os.path.join(project_path, build_file)):
            build_files.append(build_file)
    
    if not build_files:
        print(f"❌ No build files found (Maven/Gradle)")
        return None
    
    print(f"✅ Build system: {', '.join(build_files)}")
    
    # Find test directories
    test_dirs = []
    common_test_paths = [
        'src/test/java',
        'src/test',
        'test',
        'tests',
        '**/src/test/java',
        '**/test'
    ]
    
    for pattern in common_test_paths:
        matches = glob.glob(os.path.join(project_path, pattern), recursive=True)
        test_dirs.extend([m for m in matches if os.path.isdir(m)])
    
    # Remove duplicates and sort
    test_dirs = sorted(list(set(test_dirs)))
    
    if not test_dirs:
        print(f"❌ No test directories found")
        return None
    
    print(f"✅ Test directories found: {len(test_dirs)}")
    for test_dir in test_dirs[:3]:  # Show first 3
        print(f"   📁 {test_dir}")
    if len(test_dirs) > 3:
        print(f"   ... and {len(test_dirs) - 3} more")
    
    # Count test files
    total_test_files = 0
    for test_dir in test_dirs:
        java_tests = glob.glob(os.path.join(test_dir, '**/*.java'), recursive=True)
        total_test_files += len(java_tests)
    
    print(f"✅ Total test files: {total_test_files}")
    
    # Try to run tests (quick check)
    test_command = None
    if 'pom.xml' in build_files:
        test_command = 'mvn test -q'
    elif any('gradle' in f for f in build_files):
        test_command = './gradlew test --quiet'
    
    if test_command:
        print(f"🧪 Testing build system with: {test_command}")
        try:
            # Change to project directory and run test command
            result = subprocess.run(
                test_command.split(),
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )
            
            if result.returncode == 0:
                print(f"✅ Tests can be executed successfully")
                return {
                    'name': project_name,
                    'path': project_path,
                    'build_files': build_files,
                    'test_dirs': test_dirs,
                    'test_files': total_test_files,
                    'test_command': test_command,
                    'tests_runnable': True
                }
            else:
                print(f"⚠️  Tests exist but may have issues:")
                print(f"   Return code: {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")
                return {
                    'name': project_name,
                    'path': project_path,
                    'build_files': build_files,
                    'test_dirs': test_dirs,
                    'test_files': total_test_files,
                    'test_command': test_command,
                    'tests_runnable': False,
                    'error': result.stderr[:200]
                }
        
        except subprocess.TimeoutExpired:
            print(f"⚠️  Test execution timed out (>60s)")
            return {
                'name': project_name,
                'path': project_path,
                'build_files': build_files,
                'test_dirs': test_dirs,
                'test_files': total_test_files,
                'test_command': test_command,
                'tests_runnable': False,
                'error': 'Timeout'
            }
        except Exception as e:
            print(f"⚠️  Error running tests: {e}")
            return {
                'name': project_name,
                'path': project_path,
                'build_files': build_files,
                'test_dirs': test_dirs,
                'test_files': total_test_files,
                'test_command': test_command,
                'tests_runnable': False,
                'error': str(e)
            }
    
    return {
        'name': project_name,
        'path': project_path,
        'build_files': build_files,
        'test_dirs': test_dirs,
        'test_files': total_test_files,
        'test_command': None,
        'tests_runnable': False
    }

def main():
    """Analyze all available projects for behavioral validation suitability"""
    
    print("🎯 BEHAVIORAL VALIDATION - PROJECT ANALYSIS")
    print("=" * 60)
    
    # Projects to analyze
    projects = [
        ('complex_projects/mockito', 'Mockito'),
        ('complex_projects/intellij-community', 'IntelliJ Community'),
        ('complex_projects/elasticsearch', 'Elasticsearch'),
        ('complex_projects/spring-framework', 'Spring Framework'),
        ('complex_projects/junit5', 'JUnit 5')
    ]
    
    suitable_projects = []
    
    for project_path, project_name in projects:
        result = analyze_project_tests(project_path, project_name)
        if result and result.get('test_files', 0) > 0:
            suitable_projects.append(result)
    
    # Summary
    print(f"\n📊 SUMMARY")
    print("=" * 60)
    
    if not suitable_projects:
        print("❌ No suitable projects found for behavioral validation")
        return
    
    print(f"✅ Found {len(suitable_projects)} projects with test suites:")
    
    for project in suitable_projects:
        status = "✅ Ready" if project.get('tests_runnable') else "⚠️  Needs setup"
        print(f"\n📦 {project['name']}")
        print(f"   Test files: {project['test_files']}")
        print(f"   Build system: {', '.join(project['build_files'])}")
        print(f"   Status: {status}")
        if not project.get('tests_runnable') and project.get('error'):
            print(f"   Issue: {project['error']}")
    
    # Recommendations
    print(f"\n🎯 RECOMMENDATIONS FOR BEHAVIORAL VALIDATION:")
    
    ready_projects = [p for p in suitable_projects if p.get('tests_runnable')]
    if ready_projects:
        print(f"\n✅ Ready to use immediately:")
        for project in ready_projects:
            print(f"   • {project['name']} ({project['test_files']} test files)")
    
    setup_projects = [p for p in suitable_projects if not p.get('tests_runnable')]
    if setup_projects:
        print(f"\n⚠️  Need setup/investigation:")
        for project in setup_projects:
            print(f"   • {project['name']} ({project['test_files']} test files)")

if __name__ == "__main__":
    main()
