import requests
import json

url = "https://api.iapp.co.th/license-plate-recognition/file"
path = "images\Test5.jpg"  # Path to your image file
file_name = "Test.png"

payload = {}
files = [
    ('file', (file_name, open(path, 'rb'), 'image/jpeg'))  # Updated to use 'file' as key
]
headers = {
    'apikey': 'ZBLMnKYVOC1ujNiGvL5QhmDLcdFs4Gc8'
}

response = requests.post(url, headers=headers, files=files)

# Convert response text to JSON
response_json = response.json()

# Access lp_number
lp_number = response_json.get('lp_number', '')

# Print lp_number in a readable format
print("Raw lp_number:", lp_number)
