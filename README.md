# 🌌 AstroTech - AI-Powered Spiritual Guide  

AstroTech is a groundbreaking platform combining the mystique of astrology with the power of artificial intelligence. Designed to provide **personalized spiritual insights**, AstroTech empowers users to better understand their journey in life across dimensions such as **career**, **relationships**, **personal growth**, **family**, and **social connections**.  

---

## 🚀 Features  

### 🪐 **Astrological Insights**  
AstroTech utilizes the **FreeAstrology API** to provide highly detailed astrological data:  
1. **Planets - Rasi Chart**: A comprehensive analysis of planetary positions in the Rasi chart.  
2. **Planets - Extended Information**: In-depth insights into planetary influences and their implications.  
3. **Navamsa Chart Info**: Detailed Navamsa chart data for refined predictions.  

### 🔮 **Tailored Spiritual Guidance**  
- Input: Users provide their **Birthdate**, **Birth Time**, and **Location of Birth**.  
- Processing: The app extracts and integrates data from the APIs.  
- Insights: We pass the combined data to the **Gemini LLM model** to generate:  
  - Predictions and advice on **career**, **relationships**, and **personal growth**.  
  - **Daily and monthly horoscopes** tailored to the user’s unique profile.  

### 🤖 **AI-Powered Chatbot**  
AstroTech features a **context-aware AI chatbot** powered by the **Gemini LLM**:  
- Combines API responses with AI-generated insights.  
- Provides **robust, highly personalized responses** to user queries.  
- Delivers insights with depth and clarity, enhancing the user experience.  

### 📂 **Advanced Database Management with Astra DB**  
- **Astra DB by DataStax** powers our backend with exceptional performance and reliability.  
- Ensures seamless handling of complex datasets, including user queries and chatbot interactions.  
- Offers **scalability, security, and high-speed data access**, making it a critical asset for our project.  

---

## 🛠️ Tools & Technologies Used  

### **Backend**:  
- Python  
- Flask  

### **Frontend**:  
- HTML  
- CSS  
- JavaScript  

### **APIs & AI**:  
- **FreeAstrology API** for astrological data.  
- **Gemini LLM** and **Generative AI (GenAI)** for insightful predictions and chat interactions.  

### **Database**:  
- **Astra DB** (DataStax) for storing and managing user data with cutting-edge scalability.  

### **Other Libraries**:  
- Various Python libraries for API integration and data processing.  

---

## 🌟 Why AstroTech Stands Out  

1. **Unique Integration of Astrology and AI**: Combines the timeless wisdom of astrology with the innovative capabilities of AI.  
2. **Powerful Database Solution**: Leverages Astra DB to ensure optimal performance, scalability, and security.  
3. **User-Centric Design**: Provides an intuitive interface with **real-time, meaningful insights**.  
4. **Robust Chatbot**: Features a highly capable AI chatbot that enhances user interaction with precise, context-aware responses.  

---

---

## 🛠️ Getting Started  

### **Run the Project Locally**  

1. **Clone the repository**:

    Clone the project to your local machine:

    ```bash
    git clone https://github.com/Sid3503/AstroTech.git
    cd AstraTech
    ``` 

2. Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate # For macOS/Linux
    venv\Scripts\activate # For Windows
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure Astra DB:
   
    - Set up your Astra DB account and create a new collection for social media engagement data.
    - Update connection details in `config.py`.

5. Run the Flask app:

    ```bash
    python app.py
    ```

6. Access the app:

    Open a web browser and go to `http://127.0.0.1:5000` to interact with the app.

## 🧑‍💻 Authors
[@Siddharth Mishra](https://github.com/Sid3503)
[@Manoday Kadam](https://github.com/Manoday10)
