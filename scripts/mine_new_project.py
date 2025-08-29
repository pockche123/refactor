#!/usr/bin/env python3
"""
Mine refactorings from a new project for generalization testing
"""

import subprocess
import json
import os
from pathlib import Path

def clone_project(repo_url, project_name):
    """Clone new project for testing"""
    workspace = "/Users/parjalrai/Workspace"
    project_path = f"{workspace}/{project_name}"
    
    if not os.path.exists(project_path):
        print(f"Cloning {repo_url}...")
        subprocess.run(["git", "clone", repo_url, project_path])
    return project_path

def mine_refactorings(project_path, output_file):
    """Run RefactoringMiner on new project"""
    refactoring_miner = "/Users/parjalrai/Workspace/RefactoringMiner"
    
    cmd = [
        "java", "-jar", f"{refactoring_miner}/build/libs/RefactoringMiner-3.0.9.jar",
        "-a", project_path, "-json", output_file
    ]
    
    print(f"Mining refactorings from {project_path}...")
    subprocess.run(cmd)
    print(f"Results saved to {output_file}")

def main():
    # Test projects (pick one)
    projects = {
        "spring-framework": "https://github.com/spring-projects/spring-framework.git",
        "kafka": "https://github.com/apache/kafka.git", 
        "elasticsearch": "https://github.com/elastic/elasticsearch.git"
    }
    
    # Start with Spring Framework (smaller than others)
    project_name = "spring-framework"
    repo_url = projects[project_name]
    
    # Clone and mine
    project_path = clone_project(repo_url, project_name)
    output_file = f"data/{project_name}_refactorings.json"
    mine_refactorings(project_path, output_file)

if __name__ == "__main__":
    main()
