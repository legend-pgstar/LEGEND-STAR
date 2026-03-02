#!/usr/bin/env python
"""Identify and list unnecessary markdown files for cleanup"""
import os

# Essential documentation files to keep
ESSENTIAL_DOCS = {
    'README.md',
    'DOCUMENTATION_INDEX.md',
    'FINAL_IMPLEMENTATION_REPORT.md',
    'QUICK_START_v2.md',
    'ADVANCED_UPDATE_COMPLETION.md',
    'requirements.txt'
}

# Find all markdown files
md_files = [f for f in os.listdir('.') if f.endswith('.md')]

# Categorize
essential = []
unnecessary = []

for file in sorted(md_files):
    if file in ESSENTIAL_DOCS:
        essential.append(file)
    else:
        unnecessary.append(file)

print("=" * 80)
print("DOCUMENTATION CLEANUP ANALYSIS")
print("=" * 80)
print()

print(f"✅ ESSENTIAL DOCUMENTATION ({len(essential)} files):")
for f in essential:
    size = os.path.getsize(f) / 1024
    print(f"   • {f:50} ({size:>7.1f} KB)")

print()
print(f"❌ UNNECESSARY DOCUMENTATION ({len(unnecessary)} files):")
for f in unnecessary:
    size = os.path.getsize(f) / 1024
    print(f"   • {f:50} ({size:>7.1f} KB)")

print()
print("=" * 80)
print("DELETION LIST:")
print("=" * 80)
for f in unnecessary:
    print(f'Remove-Item "{f}" -Force -ErrorAction SilentlyContinue')

print()
print(f"Total space to save: {sum(os.path.getsize(f) for f in unnecessary) / 1024:.1f} KB")
print()
