# 📊 Data Analyst

A Streamlit application that allows users to upload CSV, JSON, or Excel files and ask questions about their data using Google's Gemini AI.

## Features
- Upload CSV, JSON, and Excel files
- Ask natural language questions about your data
- AI-powered data analysis using Google Gemini
- Interactive chat interface
- Data preview and basic statistics

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. Create a `.env` file with your API key:
GEMINI_API_KEY=your_api_key_here
5. Run the app: `streamlit run app.py`

## Usage
1. Upload a data file using the sidebar
2. Ask questions about your data in natural language
3. Get AI-powered insights and analysis

## Example Questions
- "What are the main trends in this data?"
- "Show me the top 5 values in column X"
- "How many unique values are in each column?"
- "What patterns do you see?"
🚀 Step 2: Initialize Git Repository
Open terminal/command prompt in your project directory:
bash# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: AskMyData - AI-powered data analysis tool"
