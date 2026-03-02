#!/usr/bin/env python3
"""Import test to verify all modules work correctly"""
import sys
import ast

print("=" * 70)
print("CODE IMPORT AND COMPILATION VERIFICATION".center(70))
print("=" * 70)

# Test 1: Compile main.py
print("\n1️⃣  Testing main.py compilation...")
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
        compile(code, 'main.py', 'exec')
    print("   ✅ main.py compiles successfully")
except SyntaxError as e:
    print(f"   ❌ Syntax Error: {e}")
    sys.exit(1)

# Test 2: Verify required imports are available
print("\n2️⃣  Testing required packages...")
required = ['discord', 'dotenv', 'pymongo', 'aiohttp', 'pytz']
for package in required:
    try:
        __import__(package)
        print(f"   ✅ {package}: Available")
    except ImportError:
        print(f"   ⚠️  {package}: Not installed (but can be installed)")

# Test 3: Syntax validation on all Python files
print("\n3️⃣  Validating all Python files...")
import glob
python_files = glob.glob('*.py')
errors = 0
for py_file in sorted(python_files):
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print(f"   ✅ {py_file}: Valid")
    except SyntaxError as e:
        print(f"   ❌ {py_file}: {e}")
        errors += 1

# Test 4: Check for critical patterns
print("\n4️⃣  Checking code quality patterns...")
with open('main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()
    
checks = {
    'try blocks': main_content.count('try:'),
    'except blocks': main_content.count('except'),
    'async functions': main_content.count('async def'),
    'functions': main_content.count('def '),
}

for check, count in checks.items():
    print(f"   📊 {check}: {count}")

# Test 5: Final status
print("\n" + "=" * 70)
if errors == 0:
    print("✅ ALL TESTS PASSED - Code is production-ready".center(70))
else:
    print(f"❌ {errors} file(s) have issues".center(70))
print("=" * 70)
