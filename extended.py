import requests
import json
from datetime import datetime

def get_extended_details(birth_date, birth_time, location):
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
            url = "https://json.apiastro.com/planets/extended"
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
                    "ayanamsha": "lahiri",
                    "language": "en"
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

        def convert_astrology_data_to_text(astrology_data):
            output = astrology_data.get('output', {})
            if not output:
                return "No astrology data available."

            text_output = []
            for planet, details in output.items():
                planet_name = planet
                zodiac_sign_name = details.get('zodiac_sign_name', 'Unknown')
                zodiac_sign_lord = details.get('zodiac_sign_lord', 'Unknown')
                nakshatra_name = details.get('nakshatra_name', 'Unknown')
                nakshatra_pada = details.get('nakshatra_pada', 'Unknown')
                nakshatra_lord = details.get('nakshatra_vimsottari_lord', 'Unknown')
                is_retrograde = "Retrograde" if details.get('isRetro') == 'true' else "Direct"
                degree = details.get('normDegree', 0)

                text_output.append(
                    f"{planet_name}:"
                    f"\n  Zodiac Sign: {zodiac_sign_name} (Lord: {zodiac_sign_lord})"
                    f"\n  Degree: {degree:.2f}°"
                    f"\n  Nakshatra: {nakshatra_name} (Pada: {nakshatra_pada}, Lord: {nakshatra_lord})"
                    f"\n  Motion: {is_retrograde}\n"
                )

            return "\n".join(text_output)

        return convert_astrology_data_to_text(astrology_data)
    
    except Exception as e:
        return f"Error: {e}"
