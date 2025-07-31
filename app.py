from flask import Flask, request, jsonify
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

import os

import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Authenticate Google Sheets client using credentials loaded from an environment variable
credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)


# Open the Google Sheet
sheet = client.open("CV AI")

# Load data from each tab
def load_sheet_data(sheet_name):
    worksheet = sheet.worksheet(sheet_name)
    return worksheet.get_all_records()

# Load data from all the tabs
general_info = load_sheet_data("General Info")
skills = load_sheet_data("Skills")
working_experience = load_sheet_data("Working Experience")
education = load_sheet_data("Education")
certifications = load_sheet_data("Certification")
volunteer = load_sheet_data("Volunteer")
awards = load_sheet_data("Awards")
projects = load_sheet_data("Project")
tools_technology = load_sheet_data("Tools / Technology")
speaking_engagements = load_sheet_data("Speaking Engagements")
research_experience = load_sheet_data("Research Experience")

# Consolidate all data into cv_data
cv_data = {
    "general_info": general_info,
    "skills": skills,
    "working_experience": working_experience,
    "education": education,
    "certifications": certifications,
    "volunteer": volunteer,
    "awards": awards,
    "projects": projects,
    "tools_technology": tools_technology,
    "speaking_engagements": speaking_engagements,
    "research_experience": research_experience
}

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Updated get_response function
def get_response(query, cv_data):
    print("Processing query:", query)

    # Generate the message for ChatGPT
    system_message = (
        "You are an assistant helping recruiters understand Nadya CV. "
        "Respond concisely and professionally in C2 English. "
        "Avoid incomplete sentences and keep answers in the same context. "
        "Focus on strategic and tactical decision-making expertise in supply chain and technology roles. "
        "Provide actionable insights."
    )

    user_message = (
        f"Based on this CV data: {json.dumps(cv_data)}, "
        f"answer the following query: {query}. "
        f"Avoid incomplete sentences and stay in context. "
        f"Respond on strategic and tactical skills. "
        f"Follow a concise STAR framework."
    )

    # Invoke OpenAI ChatCompletion API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        response_text = response.choices[0].message["content"]

        # Debugging logs for response
        print("ChatGPT Response:", response_text)

        # Split the response into sentences for formatting
        sentences = response_text.split('. ')
        rows = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
        return rows
    except Exception as e:
        print("Error while generating ChatGPT response:", str(e))
        return ["An error occurred while generating the response."]

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get input data
    data = request.json

    # Validate that data exists
    if not data:
        return jsonify({"error": "No input data provided."}), 400

    # Debug print for incoming data
    print("Incoming Data:", data)

    query = data.get("query")

    # Validate query: Ensure it's provided
    if not query:
        return jsonify({"error": "Missing 'query' in request data."}), 400

    # Generate response
    try:
        response_rows = get_response(query, cv_data)
        return jsonify({"response": response_rows})
    except Exception as e:
        print("Error processing the chatbot request:", str(e))
        return jsonify({"error": "An error occurred while processing your request."}), 500

@app.route('/', methods=['GET'])
def home():
    return "Chatbot server is running!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    
