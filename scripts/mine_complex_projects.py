#!/usr/bin/env python3
"""
Mine refactorings from projects known for complex refactoring patterns
"""

import subprocess
import os
import sys

def clone_and_mine(repo_url, project_name):
    """Clone project and run RefactoringMiner"""
    workspace = "/Users/parjalrai/Workspace"
    project_path = f"{workspace}/{project_name}"
    
    # Clone if not exists
    if not os.path.exists(project_path):
        print(f"Cloning {project_name}...")
        # Use shallow clone for large repos
        subprocess.run(["git", "clone", "--depth", "100", repo_url, project_path])
    
    # Mine refactorings
    refactoring_miner = "/Users/parjalrai/Workspace/RefactoringMiner"
    output_file = f"data/{project_name}_refactorings.json"
    
    cmd = [
        "java", "-jar", f"{refactoring_miner}/build/libs/RefactoringMiner-3.0.11.jar",
        "-a", project_path, "-json", output_file
    ]
    
    print(f"Mining {project_name}...")
    subprocess.run(cmd)
    print(f"Saved to {output_file}")

def main():
    # Projects known for complex refactorings
    projects = {
        "intellij-community": "https://github.com/JetBrains/intellij-community.git",
        "spring-boot": "https://github.com/spring-projects/spring-boot.git", 
        "hibernate-orm": "https://github.com/hibernate/hibernate-orm.git",
        "mockito": "https://github.com/mockito/mockito.git",
        "elasticsearch": "https://github.com/elastic/elasticsearch.git"
    }
    
    # Allow command line selection or default to intellij
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = "intellij-community"
    
    if project_name in projects:
        clone_and_mine(projects[project_name], project_name)
    else:
        print(f"Available projects: {list(projects.keys())}")

if __name__ == "__main__":
    main()
