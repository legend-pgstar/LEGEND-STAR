#!/usr/bin/env python3
"""Fix bare except blocks in main.py"""
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all bare except: blocks
# Pattern: \n    except:\n
# Replace with: \n    except Exception:\n

content = re.sub(r'\n(\s+)except:\n', r'\n\1except Exception:\n', content)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all bare 'except:' blocks to 'except Exception:'")
