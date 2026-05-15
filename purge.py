import os
import re

# --- CONFIGURATION ---
POSTS_DIR = '_posts'

# This pattern targets lines that are JUST the links [Previous], [ToC], [Next], or [**Discord...**]
# It also handles variations in spacing or trailing slashes
PATTERNS = [
    r'^\[Previous\].*?$',
    r'^\[Next\].*?$',
    r'^\[ToC\].*?$',
    r'^\[\*\*Discord here\*\*\].*?$',
    r'^\[Chapter - \d+-\d+.*?$' # Optional: catch those old translation links if they are separate
]

def cleanup_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changed = False

    for line in lines:
        match_found = False
        for p in PATTERNS:
            if re.match(p, line.strip()):
                match_found = True
                changed = True
                break
        
        if not match_found:
            new_lines.append(line)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

print("Running aggressive purge of hardcoded navigation...")
count = 0
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        if cleanup_file(os.path.join(POSTS_DIR, filename)):
            count += 1

print(f"Done! Cleaned up navigation links in {count} chapters.")