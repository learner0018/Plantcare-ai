import os

print("Checking project structure...")
print("="*50)

files_to_check = [
    'app.py',
    'model_handler.py',
    'disease_database.py',
    'templates/index.html',
    'static/js/app.js'
]

for file in files_to_check:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"{status} {file}")

print("="*50)

if os.path.exists('templates/index.html'):
    size = os.path.getsize('templates/index.html')
    print(f"\nindex.html size: {size} bytes")
    if size < 100:
        print("⚠️ Warning: index.html seems too small!")
else:
    print("\n❌ templates/index.html is MISSING!")
    print("👉 Create it in VS Code:")
    print("   1. Right-click 'templates' folder")
    print("   2. Click 'New File'")
    print("   3. Name it 'index.html'")
    print("   4. Paste the HTML code")