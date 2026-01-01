# test_api.py
# This script tests our API by uploading a test image

import requests
from PIL import Image
import io

# Create a test image (green square representing a plant leaf)
print("📸 Creating test plant image...")
test_image = Image.new('RGB', (400, 400), color='green')

# Save to bytes (in memory)
img_byte_arr = io.BytesIO()
test_image.save(img_byte_arr, format='JPEG')
img_byte_arr.seek(0)

print("🚀 Sending image to API for analysis...")

# Send to our API
try:
    response = requests.post(
        'http://localhost:5000/api/analyze',
        files={'image': ('test_plant.jpg', img_byte_arr, 'image/jpeg')}
    )
    
    # Print results
    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*60)
        print("✅ SUCCESS! Analysis complete!")
        print("="*60)
        
        data = result['data']
        print(f"\n🌱 Plant: {data['plantName']}")
        print(f"🏥 Health Status: {data['healthStatus']}")
        
        if data['diseaseDetected']:
            print(f"🦠 Disease: {data['diseaseName']}")
            print(f"📊 Confidence: {data['confidence']}%")
            print(f"⚠️ Severity: {data['severity']}")
            print(f"\n📝 Description:\n{data['description']}")
            
            print(f"\n💊 Solutions:")
            for i, solution in enumerate(data['solutions'], 1):
                print(f"  {i}. {solution}")
        else:
            print("✅ Plant is healthy!")
            
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Make sure the server is running!")
    print("   Run 'python app.py' in another terminal")