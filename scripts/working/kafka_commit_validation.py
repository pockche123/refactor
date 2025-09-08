#!/usr/bin/env python3
"""
Apache Kafka Behavioral Validation
Create before/after test directories for ML-predicted refactorings
Following dual testing methodology (simple + JUnit)
"""

import pandas as pd
from pathlib import Path
import shutil
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from kafka_test_creators import *

def load_correct_predictions():
    """Load correct ML predictions from Kafka"""
    df = pd.read_csv('results/working/kafka_ml_test_results.csv')
    correct_predictions = df[df['correct_prediction'] == True]
    return correct_predictions

def create_test_directories(prediction, index):
    """Create before/after test directories for a prediction"""
    
    # Create directories
    before_dir = Path(f"kafka_commit_validation/before_{index}")
    after_dir = Path(f"kafka_commit_validation/after_{index}")
    
    before_dir.mkdir(parents=True, exist_ok=True)
    after_dir.mkdir(parents=True, exist_ok=True)
    
    # Create src and test subdirectories
    before_src = before_dir / "src"
    after_src = after_dir / "src"
    before_test = before_dir / "test"
    after_test = after_dir / "test"
    
    before_src.mkdir(exist_ok=True)
    after_src.mkdir(exist_ok=True)
    before_test.mkdir(exist_ok=True)
    after_test.mkdir(exist_ok=True)
    
    # Extract refactoring details
    refactoring_type = prediction['refactoring_type']
    
    # Create Java files based on refactoring type
    if 'Variable Type' in refactoring_type:
        create_variable_type_test(before_src, after_src, before_test, after_test, index)
    elif 'Return Type' in refactoring_type:
        create_return_type_test(before_src, after_src, before_test, after_test, index)
    elif 'Rename Method' in refactoring_type:
        create_rename_method_test(before_src, after_src, before_test, after_test, index)
    elif 'Move Method' in refactoring_type:
        create_move_method_test(before_src, after_src, before_test, after_test, index)
    else:
        create_generic_test(before_src, after_src, before_test, after_test, refactoring_type, index)

def create_maven_pom():
    """Create Maven pom.xml for Kafka validation"""
    
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.research</groupId>
    <artifactId>kafka-behavioral-validation</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <junit.version>5.9.2</junit.version>
        <mockito.version>5.1.1</mockito.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-core</artifactId>
            <version>${mockito.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-junit-jupiter</artifactId>
            <version>${mockito.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0-M9</version>
            </plugin>
        </plugins>
    </build>
</project>"""
    
    with open("kafka_commit_validation/pom.xml", 'w') as f:
        f.write(pom_xml)

def main():
    print("🚀 APACHE KAFKA BEHAVIORAL VALIDATION")
    print("=" * 50)
    
    # Load correct predictions
    print("📊 Loading correct Kafka predictions...")
    correct_predictions = load_correct_predictions()
    print(f"   Found {len(correct_predictions)} correct predictions")
    
    # Clean up existing validation directory
    validation_dir = Path("kafka_commit_validation")
    if validation_dir.exists():
        shutil.rmtree(validation_dir)
    
    # Create test directories for each correct prediction
    print("🏗️  Creating before/after test directories...")
    
    for i, (_, prediction) in enumerate(correct_predictions.iterrows()):
        print(f"   Creating test {i}: {prediction['refactoring_type']}")
        create_test_directories(prediction, i)
    
    # Create Maven pom.xml
    create_maven_pom()
    
    print(f"\n✅ Created {len(correct_predictions)} before/after test pairs")
    print(f"   Total directories: {len(correct_predictions) * 2}")
    print(f"   Each directory has src/ and test/ subdirectories")
    print(f"   Location: kafka_commit_validation/")
    print(f"   ✅ kafka_commit_validation/pom.xml")
    
    # Summary
    refactoring_types = correct_predictions['refactoring_type'].value_counts()
    print(f"\n📈 VALIDATION SUMMARY:")
    print(f"   Total test cases: {len(correct_predictions)}")
    print(f"   Refactoring types covered:")
    for ref_type, count in refactoring_types.items():
        print(f"     {ref_type}: {count} cases")
    
    print(f"\n📋 KAFKA DUAL TESTING STRUCTURE:")
    print(f"   src/ - Simple main() method tests")
    print(f"   test/ - JUnit 5 + Mockito tests")
    print(f"   Both test distributed systems refactoring functionality")

if __name__ == "__main__":
    main()
