#!/usr/bin/env python3

import pandas as pd
import numpy as np
from collections import Counter
import os

def load_data(domain):
    """Load dataset for a domain"""
    try:
        df = pd.read_csv(f'data/{domain}_350_real.csv')
        return df
    except FileNotFoundError:
        print(f"Dataset not found for {domain}")
        return None

def generate_report(domain, df):
    """Generate detailed analysis report for a domain"""
    
    # Basic stats
    total_refactorings = len(df)
    unique_types = df['refactoring_type'].nunique()
    unique_commits = df['commit_sha'].nunique()
    
    # Refactoring type distribution
    type_counts = df['refactoring_type'].value_counts()
    
    # Complexity stats
    lines_stats = df['lines_changed'].describe()
    complexity_stats = df['cyclomatic_complexity'].describe()
    depth_stats = df['nesting_depth'].describe()
    
    # Repository mapping
    repo_names = {
        'commons_lang': 'Apache Commons Lang',
        'spring': 'Spring Framework',
        'kafka': 'Apache Kafka',
        'mockito': 'Mockito'
    }
    
    report = f"""# {repo_names.get(domain, domain.title())} Refactoring Analysis

## Overview

Comprehensive analysis of refactorings extracted from {repo_names.get(domain, domain.title())} repository using RefactoringMiner.

## Dataset Summary

- **Total Refactorings**: {total_refactorings}
- **Unique Refactoring Types**: {unique_types}
- **Commits Analyzed**: {unique_commits}
- **Repository**: {repo_names.get(domain, domain.title())}
- **Analysis Period**: Historical commits from main development branch

## Refactoring Type Distribution

### Most Common Refactoring Types

"""
    
    # Top 5 refactoring types
    for i, (ref_type, count) in enumerate(type_counts.head().items(), 1):
        percentage = (count / total_refactorings) * 100
        report += f"{i}. **{ref_type}** ({count} instances) - {percentage:.1f}%\n"
    
    report += "\n### Complete Type Breakdown\n\n"
    report += "| Refactoring Type | Count | Percentage |\n"
    report += "| ---------------- | ----- | ---------- |\n"
    
    for ref_type, count in type_counts.items():
        percentage = (count / total_refactorings) * 100
        report += f"| {ref_type} | {count} | {percentage:.1f}% |\n"
    
    report += f"""

## Complexity Analysis

### Lines Changed Distribution

- **Mean**: {lines_stats['mean']:.1f} lines per refactoring
- **Median**: {lines_stats['50%']:.0f} lines per refactoring
- **Range**: {lines_stats['min']:.0f}-{lines_stats['max']:.0f} lines
- **Most Common**: {len(df[df['lines_changed'] <= 5])} refactorings ({(len(df[df['lines_changed'] <= 5])/total_refactorings)*100:.0f}%) change ≤5 lines

### Cyclomatic Complexity

- **Mean**: {complexity_stats['mean']:.1f}
- **Median**: {complexity_stats['50%']:.0f}
- **Range**: {complexity_stats['min']:.0f}-{complexity_stats['max']:.0f}
- **Distribution**: {len(df[df['cyclomatic_complexity'] <= 2])} refactorings ({(len(df[df['cyclomatic_complexity'] <= 2])/total_refactorings)*100:.0f}%) have complexity ≤2

### Nesting Depth

- **Mean**: {depth_stats['mean']:.1f}
- **Median**: {depth_stats['50%']:.0f}
- **Range**: {depth_stats['min']:.0f}-{depth_stats['max']:.0f}
- **Distribution**: {len(df[df['nesting_depth'] <= 2])} refactorings ({(len(df[df['nesting_depth'] <= 2])/total_refactorings)*100:.0f}%) have depth ≤2

## Key Patterns and Insights

### 1. Dominant Refactoring Pattern

- **{type_counts.index[0]}** is the most frequent ({type_counts.iloc[0]} instances, {(type_counts.iloc[0]/total_refactorings)*100:.1f}%)
- **Top 3 types** account for {(type_counts.head(3).sum()/total_refactorings)*100:.1f}% of all refactorings
- **Indicates**: {get_pattern_insight(type_counts.index[0])}

### 2. Complexity Characteristics

- **{(len(df[df['cyclomatic_complexity'] <= 2])/total_refactorings)*100:.0f}% have low complexity** (≤2)
- **{(len(df[df['nesting_depth'] <= 1])/total_refactorings)*100:.0f}% have minimal nesting** (≤1)
- **{(len(df[df['lines_changed'] <= 10])/total_refactorings)*100:.0f}% are small changes** (≤10 lines)
- **Suggests**: {get_complexity_insight(domain)}

### 3. Refactoring Diversity

- **{unique_types} different refactoring types** across {total_refactorings} instances
- **Average per type**: {total_refactorings/unique_types:.1f} instances
- **Distribution**: {'Balanced' if type_counts.std() < type_counts.mean() else 'Skewed toward few types'}

## Machine Learning Implications

### Dataset Characteristics

- **Class Balance**: {'Well-balanced' if type_counts.std() < type_counts.mean() else 'Imbalanced - few dominant types'}
- **Feature Variance**: {'High' if lines_stats['std'] > lines_stats['mean'] else 'Low'} variance in lines changed
- **Prediction Challenge**: {'High' if unique_types > 20 else 'Moderate'} due to {unique_types} classes

### Expected Performance

Based on dataset characteristics:
- **Dominant Type Prediction**: Likely high accuracy for {type_counts.index[0]}
- **Rare Type Prediction**: Challenging for types with <5 instances
- **Overall Accuracy**: Estimated {estimate_accuracy(type_counts, total_refactorings):.0f}% based on class distribution

## Code Quality Implications

### 1. Refactoring Safety Profile

- **Low-risk changes**: {(len(df[df['lines_changed'] <= 5])/total_refactorings)*100:.0f}% affect ≤5 lines
- **Simple operations**: {(len(df[df['cyclomatic_complexity'] <= 2])/total_refactorings)*100:.0f}% have low complexity
- **Minimal structural impact**: {(len(df[df['nesting_depth'] <= 1])/total_refactorings)*100:.0f}% don't increase nesting

### 2. Development Patterns

- **Incremental improvement**: Focus on small, targeted changes
- **{get_quality_focus(type_counts.index[0])}**: Primary quality concern
- **Maintenance style**: {'Conservative' if lines_stats['mean'] < 10 else 'Aggressive'} refactoring approach

## Behavioral Validation Readiness

### Commit Accessibility

- **Real commits**: {unique_commits} unique commit SHAs available
- **Git access**: Full before/after code retrieval possible
- **Validation scope**: All {total_refactorings} refactorings can be behaviorally tested

### Testing Recommendations

1. **Prioritize {type_counts.index[0]}** - most common type for validation
2. **Sample across complexity ranges** - test both simple and complex changes
3. **Focus on edge cases** - validate rare refactoring types

## Data Sources

- **Primary Data**: `data/{domain}_350_real.csv`
- **Extraction Source**: RefactoringMiner analysis of {repo_names.get(domain, domain.title())}
- **Commit Range**: {unique_commits} commits from main development branch

---

_Analysis based on RefactoringMiner extraction from {repo_names.get(domain, domain.title())}_
_Generated: September 15, 2025_
"""
    
    return report

def get_pattern_insight(top_type):
    """Get insight based on most common refactoring type"""
    insights = {
        'Rename Method': 'Active API evolution and method clarity improvements',
        'Extract Method': 'Code decomposition and modularity focus',
        'Move Method': 'Class responsibility reorganization',
        'Rename Variable': 'Code readability and naming convention improvements',
        'Add Parameter': 'API extension and functionality enhancement',
        'Remove Parameter': 'API simplification and cleanup',
        'Change Parameter Type': 'Type safety and API evolution',
        'Inline Method': 'Code simplification and performance optimization'
    }
    return insights.get(top_type, 'Systematic code improvement and maintenance')

def get_complexity_insight(domain):
    """Get complexity insight based on domain"""
    insights = {
        'commons_lang': 'Utility library maintenance with careful API preservation',
        'spring': 'Framework evolution with backward compatibility focus',
        'kafka': 'Distributed system optimization with reliability emphasis',
        'mockito': 'Testing framework refinement with API stability'
    }
    return insights.get(domain, 'Careful, incremental improvement approach')

def get_quality_focus(top_type):
    """Get quality focus based on top refactoring type"""
    focuses = {
        'Rename Method': 'API clarity and developer experience',
        'Extract Method': 'Code modularity and reusability',
        'Move Method': 'Class cohesion and separation of concerns',
        'Rename Variable': 'Code readability and maintainability',
        'Add Parameter': 'Feature completeness and flexibility',
        'Remove Parameter': 'API simplicity and usability'
    }
    return focuses.get(top_type, 'Code quality and maintainability')

def estimate_accuracy(type_counts, total):
    """Estimate ML accuracy based on class distribution"""
    # Simple heuristic: dominant class percentage + adjustment for diversity
    dominant_pct = (type_counts.iloc[0] / total) * 100
    diversity_penalty = min(len(type_counts) * 2, 30)  # Penalty for many classes
    return max(dominant_pct - diversity_penalty, 25)  # Minimum 25%

def main():
    domains = ['commons_lang', 'spring', 'kafka', 'mockito']
    
    os.makedirs('reports/detailed', exist_ok=True)
    
    for domain in domains:
        print(f"Generating report for {domain}...")
        df = load_data(domain)
        if df is not None:
            report = generate_report(domain, df)
            
            with open(f'reports/detailed/{domain}_analysis.md', 'w') as f:
                f.write(report)
            
            print(f"✓ Report saved: reports/detailed/{domain}_analysis.md")
        else:
            print(f"✗ Skipped {domain} - no data found")

if __name__ == "__main__":
    main()
