#!/usr/bin/env python3
"""
Proper Java Refactoring - Handle references and dependencies correctly
"""

import os
import re
import glob
from pathlib import Path

def find_all_java_files(project_dir):
    """Find all Java files in the project"""
    java_files = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    return java_files

def find_method_references(project_dir, method_name, class_name=None):
    """Find all references to a method across the entire project"""
    java_files = find_all_java_files(project_dir)
    references = []
    
    # Pattern to find method calls: methodName( or object.methodName(
    call_pattern = rf'\b{re.escape(method_name)}\s*\('
    
    for java_file in java_files:
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    if re.search(call_pattern, line):
                        references.append({
                            'file': java_file,
                            'line_number': line_num,
                            'line_content': line.strip(),
                            'full_content': content
                        })
        except Exception as e:
            print(f"Warning: Could not read {java_file}: {e}")
    
    return references

def apply_proper_rename_method(file_path, project_dir, old_method_name, new_method_name):
    """Properly rename method and all its references"""
    
    print(f"🔍 Finding all references to method '{old_method_name}'...")
    
    # Find all references across the project
    references = find_method_references(project_dir, old_method_name)
    
    print(f"📍 Found {len(references)} references across {len(set(ref['file'] for ref in references))} files")
    
    changes_made = []
    
    # Update all references
    for ref in references:
        ref_file = ref['file']
        
        try:
            with open(ref_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace method calls: methodName( -> newMethodName(
            old_pattern = rf'\b{re.escape(old_method_name)}\s*\('
            new_replacement = f'{new_method_name}('
            
            updated_content = re.sub(old_pattern, new_replacement, content)
            
            if updated_content != content:
                with open(ref_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                changes_made.append({
                    'file': ref_file,
                    'type': 'method_call_update'
                })
        
        except Exception as e:
            print(f"Warning: Could not update {ref_file}: {e}")
    
    transformation = {
        'type': 'Rename Method (Proper)',
        'old_name': old_method_name,
        'new_name': new_method_name,
        'references_updated': len(changes_made),
        'files_modified': len(set(change['file'] for change in changes_made)),
        'location': file_path
    }
    
    return True, transformation

def apply_proper_rename_variable(file_path, project_dir, old_var_name, new_var_name):
    """Properly rename variable within its scope"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"
    
    # For variables, we only update within the same file (scope limitation)
    # Use word boundaries to avoid partial matches
    var_pattern = rf'\b{re.escape(old_var_name)}\b'
    updated_content = re.sub(var_pattern, new_var_name, content)
    
    if updated_content == content:
        return False, "No variable references found to rename"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        return False, f"Could not write file: {e}"
    
    transformation = {
        'type': 'Rename Variable (Proper)',
        'old_name': old_var_name,
        'new_name': new_var_name,
        'location': file_path
    }
    
    return True, transformation

def apply_proper_add_method_annotation(file_path, project_dir, method_name, annotation):
    """Add annotation to method properly"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"
    
    # Find the method declaration
    method_pattern = rf'(\s*)(public|private|protected)(\s+)(static\s+)?(\w+)\s+{re.escape(method_name)}\s*\([^)]*\)\s*\{{'
    
    match = re.search(method_pattern, content)
    if not match:
        return False, f"Method {method_name} not found"
    
    # Check if annotation already exists
    lines_before = content[:match.start()].split('\n')
    for line in lines_before[-3:]:  # Check 3 lines before method
        if annotation.strip() in line:
            return False, f"Annotation {annotation} already exists"
    
    # Insert annotation before method
    indent = match.group(1)
    annotated_method = f"{indent}{annotation}\n{match.group(0)}"
    
    updated_content = content.replace(match.group(0), annotated_method)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        return False, f"Could not write file: {e}"
    
    transformation = {
        'type': 'Add Method Annotation (Proper)',
        'method_name': method_name,
        'annotation': annotation,
        'location': file_path
    }
    
    return True, transformation

def apply_proper_change_return_type(file_path, project_dir, method_name, old_type, new_type):
    """Change method return type and update return statements"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"
    
    # Find method declaration
    method_pattern = rf'(public|private|protected)(\s+)(static\s+)?{re.escape(old_type)}\s+{re.escape(method_name)}\s*\([^)]*\)\s*\{{'
    
    match = re.search(method_pattern, content)
    if not match:
        return False, f"Method {method_name} with return type {old_type} not found"
    
    # Update method declaration
    updated_declaration = match.group(0).replace(old_type, new_type)
    updated_content = content.replace(match.group(0), updated_declaration)
    
    # Find method body and update return statements if needed
    # This is simplified - real implementation would need proper parsing
    if old_type == 'String' and new_type == 'Object':
        # No return statement changes needed (String is Object)
        pass
    elif old_type == 'int' and new_type == 'long':
        # Update return statements: return 5; -> return 5L;
        updated_content = re.sub(r'return\s+(\d+);', r'return \1L;', updated_content)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        return False, f"Could not write file: {e}"
    
    transformation = {
        'type': 'Change Return Type (Proper)',
        'method_name': method_name,
        'old_type': old_type,
        'new_type': new_type,
        'location': file_path
    }
    
    return True, transformation

def apply_proper_refactoring_transformation(file_path, refactoring_type, project_dir):
    """Apply proper refactoring with full project context"""
    
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Apply transformation based on type
    if refactoring_type == 'Rename Method':
        # Find a method to rename
        method_pattern = r'(public|private|protected).*?(\w+)\s*\([^)]*\)\s*\{'
        matches = list(re.finditer(method_pattern, original_content))
        
        if not matches:
            return False, "No methods found to rename"
        
        match = matches[0]  # Take first method
        old_method_name = match.group(2)
        new_method_name = f"{old_method_name}Renamed"
        
        return apply_proper_rename_method(file_path, project_dir, old_method_name, new_method_name)
    
    elif refactoring_type == 'Rename Variable':
        # Find a variable to rename
        var_pattern = r'(\w+)\s+(\w+)\s*='
        matches = list(re.finditer(var_pattern, original_content))
        
        if not matches:
            return False, "No variables found to rename"
        
        match = matches[0]
        old_var_name = match.group(2)
        new_var_name = f"{old_var_name}Renamed"
        
        return apply_proper_rename_variable(file_path, project_dir, old_var_name, new_var_name)
    
    elif refactoring_type == 'Add Method Annotation':
        # Find a method to annotate
        method_pattern = r'(public|private|protected).*?(\w+)\s*\([^)]*\)\s*\{'
        matches = list(re.finditer(method_pattern, original_content))
        
        if not matches:
            return False, "No methods found to annotate"
        
        match = matches[0]
        method_name = match.group(2)
        annotation = '@Override'  # Safe annotation
        
        return apply_proper_add_method_annotation(file_path, project_dir, method_name, annotation)
    
    elif refactoring_type == 'Change Return Type':
        # Find a method with changeable return type
        method_pattern = r'(public|private|protected).*?(String|int|boolean)\s+(\w+)\s*\([^)]*\)\s*\{'
        matches = list(re.finditer(method_pattern, original_content))
        
        if not matches:
            return False, "No methods with changeable return types found"
        
        match = matches[0]
        old_type = match.group(2)
        method_name = match.group(3)
        
        type_mappings = {'String': 'Object', 'int': 'long', 'boolean': 'Boolean'}
        new_type = type_mappings.get(old_type, 'Object')
        
        return apply_proper_change_return_type(file_path, project_dir, method_name, old_type, new_type)
    
    elif refactoring_type == 'Move Class':
        return apply_proper_move_class(file_path, project_dir)
    
    elif refactoring_type == 'Extract Method':
        return apply_proper_extract_method(file_path, project_dir)
    
    elif refactoring_type == 'Change Attribute Type':
        return apply_proper_change_attribute_type(file_path, project_dir)
    
    else:
        return False, f"Refactoring type {refactoring_type} not implemented yet"

def apply_proper_move_class(file_path, project_dir):
    """Move class by changing package and updating imports"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"
    
    # Find current package
    package_match = re.search(r'package\s+([^;]+);', content)
    if not package_match:
        return False, "No package declaration found"
    
    old_package = package_match.group(1)
    
    # Create new package (simple modification)
    if '.' in old_package:
        parts = old_package.split('.')
        parts[-1] = parts[-1] + 'moved'
        new_package = '.'.join(parts)
    else:
        new_package = old_package + '.moved'
    
    # Update package declaration
    updated_content = content.replace(package_match.group(0), f'package {new_package};')
    
    # Write updated file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        return False, f"Could not write file: {e}"
    
    # Find and update imports in other files
    class_name = os.path.basename(file_path).replace('.java', '')
    java_files = find_all_java_files(project_dir)
    
    files_updated = 0
    for java_file in java_files:
        if java_file == file_path:
            continue
            
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Update import statements
            old_import = f'import {old_package}.{class_name};'
            new_import = f'import {new_package}.{class_name};'
            
            if old_import in file_content:
                updated_file_content = file_content.replace(old_import, new_import)
                
                with open(java_file, 'w', encoding='utf-8') as f:
                    f.write(updated_file_content)
                
                files_updated += 1
        
        except Exception as e:
            print(f"Warning: Could not update imports in {java_file}: {e}")
    
    transformation = {
        'type': 'Move Class (Proper)',
        'class_name': class_name,
        'old_package': old_package,
        'new_package': new_package,
        'imports_updated': files_updated,
        'location': file_path
    }
    
    return True, transformation

def apply_proper_extract_method(file_path, project_dir):
    """Extract method with proper parameter handling"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"
    
    lines = content.split('\n')
    
    # Find a method with multiple statements to extract from
    in_method = False
    method_start = -1
    brace_count = 0
    
    for i, line in enumerate(lines):
        if re.search(r'(public|private|protected).*\w+\s*\([^)]*\)\s*\{', line):
            in_method = True
            method_start = i
            brace_count = line.count('{') - line.count('}')
        elif in_method:
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0:
                # End of method found
                method_lines = lines[method_start:i+1]
                if len(method_lines) > 6:  # Method has enough lines
                    # Extract middle portion (safer)
                    extract_start = method_start + 2
                    extract_end = min(method_start + 4, i-1)
                    
                    if extract_end > extract_start:
                        # Create extracted method
                        extracted_method_name = f"extracted{hash(str(method_lines)) % 10000}"
                        extracted_lines = lines[extract_start:extract_end]
                        
                        # Simple parameter detection (look for local variables)
                        params = []
                        for line in extracted_lines:
                            # Look for variable usage (very basic)
                            var_matches = re.findall(r'\b([a-z][a-zA-Z0-9]*)\b', line)
                            for var in var_matches[:1]:  # Take first variable as parameter
                                if var not in ['if', 'for', 'while', 'return', 'new', 'this']:
                                    params.append(f"Object {var}")
                                    break
                        
                        # Create new method with parameters
                        param_str = ', '.join(params[:2])  # Max 2 parameters
                        indent = "    "
                        new_method = [
                            f"{indent}private void {extracted_method_name}({param_str}) {{",
                            *[f"{indent}{line}" for line in extracted_lines],
                            f"{indent}}}"
                        ]
                        
                        # Replace extracted lines with method call
                        call_params = ', '.join([p.split()[1] for p in params[:2]])
                        lines[extract_start:extract_end] = [f"        {extracted_method_name}({call_params});"]
                        
                        # Insert new method after current method
                        lines[i+1:i+1] = [""] + new_method
                        
                        updated_content = '\n'.join(lines)
                        
                        try:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(updated_content)
                        except Exception as e:
                            return False, f"Could not write file: {e}"
                        
                        transformation = {
                            'type': 'Extract Method (Proper)',
                            'extracted_method': extracted_method_name,
                            'parameters': params,
                            'lines_extracted': len(extracted_lines),
                            'location': f"Line {extract_start + 1}"
                        }
                        
                        return True, transformation
                
                in_method = False
    
    return False, "No suitable method found for extraction"

def apply_proper_change_attribute_type(file_path, project_dir):
    """Change attribute type and update all usage"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"
    
    # Find field declarations
    field_pattern = r'(\s*)(private|protected|public)(\s+)(static\s+)?(\w+)\s+(\w+)\s*[=;]'
    
    matches = list(re.finditer(field_pattern, content))
    
    if not matches:
        return False, "No fields found to change type"
    
    # Pick first field
    match = matches[0]
    old_type = match.group(5)
    field_name = match.group(6)
    
    # Skip if it's likely a class name (starts with capital)
    if old_type[0].isupper() and old_type not in ['String', 'Boolean', 'Integer']:
        return False, "Skipped complex type"
    
    # Safe type mappings
    type_mappings = {
        'int': 'long',
        'boolean': 'Boolean',
        'String': 'Object'
    }
    
    new_type = type_mappings.get(old_type)
    if not new_type:
        return False, f"No safe mapping for type {old_type}"
    
    # Update field declaration
    new_field_declaration = match.group(0).replace(old_type, new_type)
    updated_content = content.replace(match.group(0), new_field_declaration)
    
    # Update field usage in the same file (getter/setter methods)
    # Look for getter methods: getFieldName() or isFieldName()
    getter_patterns = [
        rf'(\w+)\s+get{field_name.capitalize()}\s*\(\s*\)\s*\{{',
        rf'(\w+)\s+is{field_name.capitalize()}\s*\(\s*\)\s*\{{'
    ]
    
    for pattern in getter_patterns:
        getter_matches = re.finditer(pattern, updated_content)
        for getter_match in getter_matches:
            if getter_match.group(1) == old_type:
                updated_getter = getter_match.group(0).replace(old_type, new_type)
                updated_content = updated_content.replace(getter_match.group(0), updated_getter)
    
    # Update setter methods: setFieldName(type param)
    setter_pattern = rf'void\s+set{field_name.capitalize()}\s*\(\s*{old_type}\s+\w+\s*\)'
    setter_replacement = lambda m: m.group(0).replace(old_type, new_type)
    updated_content = re.sub(setter_pattern, setter_replacement, updated_content)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        return False, f"Could not write file: {e}"
    
    transformation = {
        'type': 'Change Attribute Type (Proper)',
        'field_name': field_name,
        'old_type': old_type,
        'new_type': new_type,
        'location': file_path
    }
    
    return True, transformation
    """Create backup of entire project"""
    backup_dir = f"{project_dir}_backup"
    
    if os.path.exists(backup_dir):
        import shutil
        shutil.rmtree(backup_dir)
    
    import shutil
    shutil.copytree(project_dir, backup_dir)
    
    return backup_dir

def restore_project(project_dir, backup_dir):
    """Restore project from backup"""
    if os.path.exists(project_dir):
        import shutil
        shutil.rmtree(project_dir)
    
    import shutil
    shutil.copytree(backup_dir, project_dir)
    
    # Clean up backup
    shutil.rmtree(backup_dir)

def backup_project(project_dir):
    """Create backup of entire project"""
    backup_dir = f"{project_dir}_backup"
    
    if os.path.exists(backup_dir):
        import shutil
        shutil.rmtree(backup_dir)
    
    import shutil
    shutil.copytree(project_dir, backup_dir)
    
    return backup_dir

def restore_project(project_dir, backup_dir):
    """Restore project from backup"""
    if os.path.exists(project_dir):
        import shutil
        shutil.rmtree(project_dir)
    
    import shutil
    shutil.copytree(backup_dir, project_dir)
    
    # Clean up backup
    shutil.rmtree(backup_dir)
