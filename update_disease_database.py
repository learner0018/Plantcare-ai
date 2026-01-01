# update_disease_database.py
# Generates disease database for all 38 PlantVillage classes

# Read classes from model
with open('model/classes.txt', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

print(f"Found {len(classes)} classes in model")
print("\nGenerating disease_database.py...")

# Create basic database entries
database_code = """# disease_database.py
# Auto-generated database for PlantVillage diseases

DISEASE_DATABASE = {
"""

for class_name in classes:
    parts = class_name.split('___')
    plant = parts[0].replace('_', ' ')
    disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
    
    is_healthy = 'healthy' in disease.lower()
    
    database_code += f"""    '{class_name}': {{
        'plantName': '{plant}',
        'diseaseName': {'None' if is_healthy else f"'{disease}'"},
        'description': '{'Plant appears healthy' if is_healthy else f'{disease} detected in {plant}'}',
        'symptoms': [],
        'solutions': [] if {is_healthy} else ['Consult agricultural expert', 'Apply appropriate treatment'],
        'preventiveCare': ['Regular monitoring', 'Proper watering', 'Good air circulation'],
        'severity': 'None' if {is_healthy} else 'Moderate',
        'environmentalFactors': {{
            'idealTemp': '20-28°C',
            'humidity': '50-70%',
            'sunlight': '6-8 hours daily',
            'wateringFreq': 'Every 2-3 days',
            'soilPH': '6.0-7.0'
        }}
    }},
"""

database_code += """
}

def get_disease_info(disease_key):
    return DISEASE_DATABASE.get(disease_key, None)

def is_healthy(disease_key):
    return 'healthy' in disease_key.lower()

def get_all_diseases():
    return list(DISEASE_DATABASE.keys())
"""

# Write to file
with open('disease_database.py', 'w') as f:
    f.write(database_code)

print("✅ Created disease_database.py with all 38 classes!")
print("\n💡 You can now customize each disease with detailed info")