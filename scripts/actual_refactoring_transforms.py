#!/usr/bin/env python3
"""
Actual Refactoring Transformations - Real code modifications for behavioral validation
"""

import os
import re
import ast
import javalang
from pathlib import Path
import random
import string

def parse_java_file(file_path):
    """Parse Java file and return AST"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with javalang
        tree = javalang.parse.parse(content)
        return tree, content
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None, None

def apply_rename_method(file_path, original_content):
    """Actually rename a method in Java file"""
    
    # Find method declarations using regex (simple approach)
    method_pattern = r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*\{'
    
    matches = list(re.finditer(method_pattern, original_content))
    
    if not matches:
        return None, "No methods found to rename"
    
    # Pick a random method to rename
    match = random.choice(matches)
    old_method_name = match.group(3)
    
    # Generate new method name
    new_method_name = f"{old_method_name}Renamed"
    
    # Replace method declaration
    new_content = original_content.replace(
        match.group(0),
        match.group(0).replace(old_method_name, new_method_name)
    )
    
    # Replace method calls (simple pattern matching)
    call_pattern = rf'\b{old_method_name}\s*\('
    new_content = re.sub(call_pattern, f'{new_method_name}(', new_content)
    
    transformation = {
        'type': 'Rename Method',
        'old_name': old_method_name,
        'new_name': new_method_name,
        'location': f"Line {original_content[:match.start()].count(chr(10)) + 1}"
    }
    
    return new_content, transformation

def apply_rename_variable(file_path, original_content):
    """Actually rename a variable in Java file"""
    
    # Find variable declarations
    var_pattern = r'(\w+)\s+(\w+)\s*='
    
    matches = list(re.finditer(var_pattern, original_content))
    
    if not matches:
        return None, "No variables found to rename"
    
    # Pick a random variable
    match = random.choice(matches)
    var_type = match.group(1)
    old_var_name = match.group(2)
    
    # Skip if it's likely a type name (starts with capital)
    if old_var_name[0].isupper():
        return None, "Skipped type name"
    
    new_var_name = f"{old_var_name}Renamed"
    
    # Replace all occurrences of the variable name
    # Use word boundaries to avoid partial matches
    new_content = re.sub(rf'\b{old_var_name}\b', new_var_name, original_content)
    
    transformation = {
        'type': 'Rename Variable',
        'old_name': old_var_name,
        'new_name': new_var_name,
        'location': f"Line {original_content[:match.start()].count(chr(10)) + 1}"
    }
    
    return new_content, transformation

def apply_extract_variable(file_path, original_content):
    """Extract a variable from an expression"""
    
    # Find method calls that could be extracted
    call_pattern = r'(\w+\.\w+\([^)]*\))'
    
    matches = list(re.finditer(call_pattern, original_content))
    
    if not matches:
        return None, "No expressions found to extract"
    
    match = random.choice(matches)
    expression = match.group(1)
    
    # Generate variable name
    extracted_var_name = f"extracted{random.randint(1000, 9999)}"
    
    # Find the line containing this expression
    lines = original_content.split('\n')
    line_num = original_content[:match.start()].count('\n')
    
    if line_num >= len(lines):
        return None, "Invalid line number"
    
    original_line = lines[line_num]
    
    # Extract variable declaration
    # Assume it's a String for simplicity (in real implementation, would need type inference)
    extracted_declaration = f"        String {extracted_var_name} = {expression};"
    
    # Replace the expression with the variable
    new_line = original_line.replace(expression, extracted_var_name)
    
    # Insert the declaration before the current line
    lines.insert(line_num, extracted_declaration)
    lines[line_num + 1] = new_line
    
    new_content = '\n'.join(lines)
    
    transformation = {
        'type': 'Extract Variable',
        'variable_name': extracted_var_name,
        'expression': expression,
        'location': f"Line {line_num + 1}"
    }
    
    return new_content, transformation

def apply_refactoring_transformation(file_path, refactoring_type):
    """Apply actual refactoring transformation to Java file"""
    
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    # Read original content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Apply transformation based on type
    new_content = None
    transformation_info = None
    
    if refactoring_type == 'Rename Method':
        new_content, transformation_info = apply_rename_method(file_path, original_content)
    elif refactoring_type == 'Rename Variable':
        new_content, transformation_info = apply_rename_variable(file_path, original_content)
    elif refactoring_type == 'Extract Variable':
        new_content, transformation_info = apply_extract_variable(file_path, original_content)
    # Import additional transformations
    elif refactoring_type in ['Add Method Annotation', 'Change Return Type', 'Extract Method', 'Change Attribute Type', 'Move Class']:
        from additional_transformations import apply_additional_refactoring_transformation
        return apply_additional_refactoring_transformation(file_path, refactoring_type)
    else:
        return False, f"Unsupported refactoring type: {refactoring_type}"
    
    if new_content is None:
        return False, f"Could not apply {refactoring_type}: {transformation_info}"
    
    # Write transformed content back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, {
            'refactoring_type': refactoring_type,
            'file_path': file_path,
            'transformation': transformation_info,
            'original_size': len(original_content),
            'new_size': len(new_content)
        }
    
    except Exception as e:
        return False, f"Error writing transformed file: {e}"

def backup_file(file_path):
    """Create backup of original file"""
    backup_path = f"{file_path}.backup"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as original:
            content = original.read()
        
        with open(backup_path, 'w', encoding='utf-8') as backup:
            backup.write(content)
        
        return backup_path
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def restore_file(file_path, backup_path):
    """Restore file from backup"""
    try:
        with open(backup_path, 'r', encoding='utf-8') as backup:
            content = backup.read()
        
        with open(file_path, 'w', encoding='utf-8') as original:
            original.write(content)
        
        # Remove backup
        os.remove(backup_path)
        return True
    except Exception as e:
        print(f"❌ Error restoring file: {e}")
        return False
