import os
import re

# --- CONFIGURATION ---
POSTS_DIR = '_posts'

# This regex finds the Discord link and the Previous/ToC/Next stack
# It looks for the common patterns found in your export
NAV_PATTERN = r'\[\*\*Discord here\*\*\].*?(\n\s*)*\[Previous\].*?(\n\s*)*\[ToC\].*?(\n\s*)*\[Next\].*?(\n|$)'

def cleanup_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the specific Discord/Prev/ToC/Next block
    new_content = re.sub(NAV_PATTERN, '', content, flags=re.DOTALL)
    
    # 2. Also catch individual loose ToC links that might be left over
    new_content = re.sub(r'\[ToC\].*?(\n|$)', '', new_content)

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content.strip() + "\n")
        return True
    return False

print("Purging hardcoded navigation links...")
count = 0
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        if cleanup_file(os.path.join(POSTS_DIR, filename)):
            count += 1

print(f"Done! Cleaned up {count} chapters.")