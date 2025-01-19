import requests
import json
from datetime import datetime

def get_navamsa_details(birth_date, birth_time, location):
    try:
        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")

        def get_lat_lon(location):
            api_key = '9ae28a6c893d4346987d519cdc6b25a4'
            url = f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}'
            response = requests.get(url)
            data = response.json()
            if data['results']:
                latitude = data['results'][0]['geometry']['lat']
                longitude = data['results'][0]['geometry']['lng']
                return latitude, longitude
            else:
                raise Exception(f"Location '{location}' not found.")

        latitude, longitude = get_lat_lon(location)
        print(f"Latitude: {latitude}, Longitude: {longitude}")

        def get_astrology_data(birth_datetime, latitude, longitude):
            url = "https://json.freeastrologyapi.com/navamsa-chart-info"
            payload = json.dumps({
                "year": birth_datetime.year,
                "month": birth_datetime.month,
                "date": birth_datetime.day,
                "hours": birth_datetime.hour,
                "minutes": birth_datetime.minute,
                "seconds": birth_datetime.second,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": 5.5,
                "settings": {
                    "observation_point": "topocentric",
                    "ayanamsha": "lahiri"
                }
            })
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': 'MDzGiJoZCL9xAeIrJpXAG1HdGODZXcb01mLXlAgk'
            }
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error fetching astrology data: {response.status_code} - {response.text}")

        astrology_data = get_astrology_data(birth_datetime, latitude, longitude)

        def convert_json_to_text(json_response):
            output = json_response.get('output', {})
            if not output:
                return "No data available"

            text_output = []
            for key, planet_data in output.items():
                name = planet_data.get('name', 'Unknown')
                current_sign = planet_data.get('current_sign', 'Unknown')
                retrograde_status = "Retrograde" if planet_data.get('isRetro') == 'true' else "Direct"
                text_output.append(f"{name}: Sign {current_sign} ({retrograde_status})")

            return '\n'.join(text_output)

        return convert_json_to_text(astrology_data)
    
    except Exception as e:
        return f"Error: {e}"
