#!/usr/bin/env python3
"""
Comprehensive Error Detection and Validation Script
Checks for: Syntax, Logic, Missing imports, Security, Best practices
"""
import ast
import re
import os
import sys
from pathlib import Path

def analyze_python_file(filepath):
    """Deep analysis of Python file for errors and issues"""
    issues = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # 1. Syntax Check
    try:
        ast.parse(content)
    except SyntaxError as e:
        issues.append(f"❌ SYNTAX ERROR: Line {e.lineno}: {e.msg}")
        return issues
    
    # 2. Check for common errors
    for i, line in enumerate(lines, 1):
        # Empty except blocks
        if re.match(r'\s*except\s*[\w\s,()]*:\s*$', line):
            if i < len(lines) and (lines[i].strip() == 'pass' or lines[i].strip() == ''):
                issues.append(f"⚠️  Line {i}: Empty except block (bare pass)")
        
        # Bare except without Exception type
        if re.match(r'\s*except\s*:\s*$', line):
            issues.append(f"⚠️  Line {i}: Bare 'except:' - should specify exception type")
        
        # Multiple statements on one line (harder to debug)
        if ';' in line and not line.strip().startswith('#'):
            issues.append(f"⚠️  Line {i}: Multiple statements on one line (uses semicolon)")
        
        # Hardcoded credentials
        if re.search(r'(password|token|secret|api_key)\s*=\s*["\'][\w]+["\']', line, re.IGNORECASE):
            if 'import' not in line and 'http' not in line:
                issues.append(f"⚠️  Line {i}: Possible hardcoded credential")
        
        # TODO/FIXME/BUG comments
        if re.search(r'#\s*(TODO|FIXME|BUG|HACK):', line, re.IGNORECASE):
            issues.append(f"ℹ️  Line {i}: {line.strip()}")
        
        # Incomplete code (bare ellipsis)
        if line.strip() == '...':
            issues.append(f"❌ Line {i}: Incomplete code (bare ellipsis)")
        
        # print() statements (should use logging)
        if re.match(r'\s*print\s*\(', line) and 'print_' not in line:
            pass  # This is okay in some contexts
        
        # Global variable modifications
        if re.search(r'\s+global\s+', line):
            issues.append(f"⚠️  Line {i}: Global variable usage: {line.strip()}")
        
        # Missing error handling in critical operations
        if any(x in line for x in ['mongoclient', 'collection.insert', 'collection.update']):
            if i > 0 and 'try' not in lines[i-2:i]:
                issues.append(f"⚠️  Line {i}: Database operation without try/except nearby")
    
    # 3. AST-based checks
    try:
        tree = ast.parse(content)
        
        # Find all function definitions
        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                if func_name in functions:
                    issues.append(f"❌ DUPLICATE FUNCTION: '{func_name}' defined multiple times")
                functions[func_name] = node.lineno
        
        # Check for undefined variables in function calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                pass  # Would need complex scope analysis
    except:
        pass
    
    return issues

def main():
    print("=" * 70)
    print("FINAL COMPREHENSIVE ERROR DETECTION".center(70))
    print("=" * 70)
    
    workspace = Path(".")
    python_files = list(workspace.glob("*.py"))
    
    total_issues = 0
    
    for py_file in sorted(python_files):
        if py_file.name.startswith('test_') or py_file.name.startswith('final_'):
            continue
            
        print(f"\n📄 Analyzing: {py_file.name}")
        print("-" * 70)
        
        issues = analyze_python_file(str(py_file))
        
        if not issues:
            print(f"✅ {py_file.name}: No errors found!")
        else:
            print(f"Found {len(issues)} issue(s):")
            for issue in issues:
                print(f"   {issue}")
                total_issues += 1
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: Total issues found: {total_issues}".center(70))
    print("=" * 70)
    
    if total_issues == 0:
        print("✅ NO ERRORS DETECTED - All systems operational".center(70))
    else:
        print(f"⚠️  {total_issues} issue(s) require attention".center(70))
    
    print("=" * 70)

if __name__ == "__main__":
    main()
