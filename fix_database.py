# fix_database.py
# Fixes encoding issues in disease_database.py

print("🔧 Fixing disease_database.py encoding...")

# Read the file
with open('disease_database.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace problematic characters
content = content.replace('°C', 'C')
content = content.replace('�C', 'C')
content = content.replace('°', '')

# Write back
with open('disease_database.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed! Try running app.py again")