from flask import Flask, request, jsonify, render_template
import requests
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
from planets import get_astrological_details
from extended import get_extended_details
from navamsa import get_navamsa_details
from img import get_horoscope_chart
from zodiac import get_zodiac_sign, get_horoscope
import markdown
from flask import Flask, request, jsonify, render_template, session
import os
import requests
import json
import google.generativeai as genai
import markdown

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_data(combined_data):
    default_prompt = f"""
    Explain in brief the astrological details, nakshatra details, tithi details, extended details, and navamsa details of a person based on the following data: {combined_data}.
    """

    prompts = [
        "Provide a detailed overview of the astrological profile for a person with the following data: {combined_data}. Highlight key traits, significant influences, and potential life themes.",
        
        "Explain how the Nakshatra and Tithi influence the personality and life path of an individual. Include insights from both Vedic astrology and lunar phases.",
        
        "Summarize the extended astrological details for an individual, incorporating their Nakshatra, Tithi, and Navamsa details. Discuss how these elements interact to shape their character and experiences.",
        
        "Analyze the compatibility of a person with the following astrological details: {combined_data}. Discuss potential strengths in relationships and areas for growth.",
        
        "Using the combined data of Nakshatra, Tithi, Astro, Extended, and Navamsa details, predict significant life events and challenges that may arise for this individual. Provide guidance on navigating these experiences.",
        
        "Based on the combined astrological inputs of {combined_data}, suggest personalized strategies for career development, relationships, and personal growth.",
        
        "Discuss how the Navamsa details impact an individual's relationships, particularly in the context of their Nakshatra and Tithi. What insights can be drawn about their approach to partnerships?",
        
        "Generate a monthly forecast that incorporates insights from Nakshatra, Tithi, Astro, Extended, and Navamsa details. Highlight key themes to focus on during this period.",
        
        "Explore how the combination of Nakshatra and Navamsa influences spiritual growth for an individual. What practices or paths may be beneficial based on these astrological insights?",
        
        "Conduct a holistic analysis of an individual's life using their Nakshatra, Tithi, Astro details, Extended insights, and Navamsa chart. Discuss how these elements create a unique life narrative."

        "Baed on {combined_data}, you will provide insights, recommendations, and rituals based on user birth details. This is main and necessary. Add your creativity to it too"
    ]

    all_prompts = [default_prompt] + prompts

    model = genai.GenerativeModel("gemini-1.5-pro")
    response_stream = model.generate_content(
        all_prompts,
        generation_config=genai.types.GenerationConfig(temperature=0.7),
        stream=True
    )

    summary_output = ""
    for message in response_stream:
        summary_output += message.text
    response_stream.resolve()

    return summary_output

def combine_responses(nakshatra_details, tithi_details, astro_details, extended_details, navamsa_details):
    return {
        "Nakshatra Details": nakshatra_details,
        "Tithi Details": tithi_details,
        "Astrological Details": astro_details,
        "Extended Details": extended_details,
        "Navamsa Details": navamsa_details,
    }

def get_horoscope_chart(birth_date, birth_time, location):
    chart_svg_path = 'images/horoscope_chart.svg'

    with open(chart_svg_path, 'w') as svg_file:
        svg_content = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">
            <rect width="500" height="500" fill="lightblue"/>
            <text x="250" y="250" font-size="20" text-anchor="middle" fill="black">
                Horoscope Chart
            </text>
        </svg>
        """
        svg_file.write(svg_content)

    return chart_svg_path

def convert_nakshatra_to_text(response_text):
    data = json.loads(response_text)
    if data.get("statusCode") == 200:
        nakshatra_data = json.loads(data["output"])
        return {
            "Nakshatra Name": nakshatra_data.get("name"),
            "Nakshatra Number": nakshatra_data.get("number"),
            "Starts At": nakshatra_data.get("starts_at"),
            "Ends At": nakshatra_data.get("ends_at"),
            "Remaining Percentage": nakshatra_data.get("remaining_percentage_at_given_time"),
        }
    return {"error": "Failed to retrieve Nakshatra data."}

def convert_tithi_to_text(response_text):
    data = json.loads(response_text)
    if data.get("statusCode") == 200:
        tithi_data = json.loads(data["output"])
        return {
            "Tithi Name": tithi_data.get("name"),
            "Tithi Number": tithi_data.get("number"),
            "Paksha": tithi_data.get("paksha"),
            "Completes At": tithi_data.get("completes_at"),
            "Remaining Percentage": tithi_data.get("left_precentage"),
        }
    return {"error": "Failed to retrieve Tithi data."}

def fetch_astrological_data(url, payload, headers):
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_details', methods=['GET', 'POST'])
def get_details():
    if request.method == 'POST':
        birth_date = request.form['birth_date']
        birth_time = request.form['birth_time']
        location = request.form['location']

        session["birth_date"] = birth_date
        session["birth_time"] = birth_time
        session["location"] = location

        latitude, longitude = 17.38333, 78.4666

        payload = json.dumps({
            "year": int(birth_date.split('-')[0]),
            "month": int(birth_date.split('-')[1]),
            "date": int(birth_date.split('-')[2]),
            "hours": int(birth_time.split(':')[0]),
            "minutes": int(birth_time.split(':')[1]),
            "seconds": int(birth_time.split(':')[2]),
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

        nakshatra_url = "https://json.freeastrologyapi.com/nakshatra-durations"
        nakshatra_response = fetch_astrological_data(nakshatra_url, payload, headers)
        nakshatra_details = convert_nakshatra_to_text(nakshatra_response) if nakshatra_response else {"error": "Nakshatra API failed."}

        tithi_url = "https://json.freeastrologyapi.com/tithi-durations"
        tithi_response = fetch_astrological_data(tithi_url, payload, headers)
        tithi_details = convert_tithi_to_text(tithi_response) if tithi_response else {"error": "Tithi API failed."}

        astro_details = get_astrological_details(birth_date, birth_time, location)
        extended_details = get_extended_details(birth_date, birth_time, location)
        navamsa_details = get_navamsa_details(birth_date, birth_time, location)

        chart_svg_path = get_horoscope_chart(birth_date, birth_time, location)

        birth_day_month = "-".join(birth_date.split('-')[2:0:-1])
        zodiac_sign, zodiac_sign_num = get_zodiac_sign(birth_day_month)
        horoscope = get_horoscope(zodiac_sign_num=zodiac_sign_num, day="today") if zodiac_sign_num != -1 else "Unable to determine horoscope."

        combined_data = combine_responses(
            nakshatra_details,
            tithi_details,
            astro_details,
            extended_details,
            navamsa_details
        )

        combined_data["Zodiac Sign"] = zodiac_sign.capitalize()
        combined_data["Daily Horoscope"] = horoscope

        combined_output = summarize_data(json.dumps(combined_data))

        session['combined_data'] = json.dumps(combined_data)
        session['combined_output'] = combined_output

        session['nakshatra_details'] = nakshatra_details
        session['tithi_details'] = tithi_details
        session['astro_details'] = astro_details
        session['extended_details'] = extended_details
        session['navamsa_details'] = navamsa_details
        session['chart_svg_path'] = chart_svg_path
        session['zodiac_sign'] = zodiac_sign
        session['horoscope'] = horoscope
        session['combined_output'] = combined_output

        return render_template(
            'details.html',
            nakshatra_details=nakshatra_details,
            tithi_details=tithi_details,
            astro_details=astro_details,
            extended_details=extended_details,
            navamsa_details=navamsa_details,
            chart_svg_path=chart_svg_path,
            combined_output=combined_output,
            zodiac_sign=zodiac_sign,
            horoscope=horoscope,
            show_results=True
        )

    if 'combined_output' in session:
        return render_template(
            'details.html',
            nakshatra_details=session.get('nakshatra_details'),
            tithi_details=session.get('tithi_details'),
            astro_details=session.get('astro_details'),
            extended_details=session.get('extended_details'),
            navamsa_details=session.get('navamsa_details'),
            chart_svg_path=session.get('chart_svg_path'),
            combined_output=session.get('combined_output'),
            zodiac_sign=session.get('zodiac_sign'),
            horoscope=session.get('horoscope'),
            show_results=True
        )

    return render_template('details.html', show_results=False)

def get_astro_response(user_message):
    system_prompt = """
    You are an expert Vedic astrologer with deep knowledge of astronomy, astrology, Hindu mythology, 
    and ancient astrological texts. You can:
    - Explain planetary positions and their effects
    - Discuss nakshatras, zodiac signs, and houses
    - Interpret astrological charts and transits
    - Share knowledge about astrological remedies
    - Explain concepts from Vedic astrology
    - Discuss the relationship between karma and planetary positions
    - Guide people on auspicious timings and muhurtas
    
    Keep your responses focused on astrological knowledge while being respectful and ethical. 
    Avoid making definitive predictions about health, relationships, or financial matters.
    Instead, provide guidance based on astrological principles.
    Provide insights, recommendations, and rituals based on user birth details(CORE COMPONENT).
    Give Zodiac Sign and Horoscopes for the Data.
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    chat = model.start_chat(history=[])
    
    try:
        response = chat.send_message(
            [system_prompt, f"User Query: {user_message}"],
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40
            )
        )
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}"

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form.get('message', '')

        if not user_message:
            return jsonify({'response': 'Please enter a message'})

        combined_data = session.get('combined_data', None)
        combined_output = session.get('combined_output', None)

        if not combined_data or not combined_output:
            return jsonify({'response': 'Session data not found. Please generate details first.'})

        context_prompt = f"""
        The following are astrological details derived for the user:
        {combined_output}

        User's astrological chart details (in JSON format):
        {combined_data}

        Based on the above information, respond to the user's query.
        """

        response = get_astro_response(f"{context_prompt}\nUser Query: {user_message}")
        return jsonify({'response': response})

    return render_template(
        'chatbot.html', 
        birth_date=session.get('birth_date'),
        birth_time=session.get('birth_time'),
        location=session.get('location')
    )

if __name__ == '__main__':
    app.run(debug=True)
