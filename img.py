import requests
import json
from planets import get_astrological_details
from extended import get_extended_details
from navamsa import get_navamsa_details

def get_horoscope_chart(birth_date, birth_time, location):
    url = "https://json.freeastrologyapi.com/horoscope-chart-url"
    
    year, month, date = map(int, birth_date.split('-'))
    hours, minutes, seconds = map(int, birth_time.split(':'))

    latitude, longitude = 17.38333, 78.4666

    payload = json.dumps({
        "year": year,
        "month": month,
        "date": date,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": 5.5,
        "config": {
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
        try:
            data = response.json()
            print("Response JSON:", data)

            image_url = data.get("output")

            if image_url:
                image_response = requests.get(image_url, stream=True)
                if image_response.status_code == 200:
                    with open("images/horoscope_chart.svg", "wb") as file:
                        for chunk in image_response.iter_content(1024):
                            file.write(chunk)
                    print("Horoscope chart saved as 'horoscope_chart.svg'")
                else:
                    print("Failed to download image. Status code:", image_response.status_code)
            else:
                print("Image URL not found in the response.")
        except json.JSONDecodeError:
            print("Response is not JSON. Unable to process.")
    else:
        print(f"API request failed with status code {response.status_code}: {response.text}")
