import os
from dotenv import load_dotenv
import google.generativeai as genai
from IPython.display import display, HTML
import pandas as pd
import csv
import json
import io
import streamlit as st


load_dotenv()  # Load variables from .env into environment


def get_llm_response(prompt):
    """
    Sends a prompt to Gemini AI and returns its response.
    
    Args:
        prompt (str): Question or text to send to Gemini
        
    Returns:
        str: Gemini's response or an error message
    """
    try:
        # Access the API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Error: API key not found in environment variables."

        genai.configure(api_key=api_key)
        
        # Use Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response - Gemini takes the prompt directly, no messages array
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        return response.text

    except Exception as e:
        return f"Error: Could not get response from Gemini\nDetails: {e}"
    
def load_csv_data(uploaded_file):
    """Load and parse CSV file"""
    try:
        # Read the file content
        content = uploaded_file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))
        data = [row for row in csv_reader]
        return data
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []

def load_json_data(uploaded_file):
    """Load and parse JSON file"""
    try:
        content = uploaded_file.read().decode('utf-8')
        data = json.loads(content)
        if isinstance(data, dict):
            data = [data]  # Convert single dict to list
        return data
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return []
    
def load_excel_data(uploaded_file):
    """Load and parse Excel file"""
    try:
        df = pd.read_excel(uploaded_file)
        return df.to_dict('records')
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        return []
    
def format_data_for_llm(data, max_rows=10):
    """Format data for LLM context - show sample rows and structure"""
    if not data:
        return "No data available."
    
    # Get data structure info
    total_rows = len(data)
    columns = list(data[0].keys()) if data else []
    
    # Create a sample of the data
    sample_data = data[:max_rows]
    
    formatted_output = f"""
Dataset Information:
- Total Rows: {total_rows}
- Columns: {', '.join(columns)}

Sample Data (first {min(max_rows, total_rows)} rows):
"""
    
    for i, row in enumerate(sample_data, 1):
        formatted_output += f"\nRow {i}: {row}"
    
    if total_rows > max_rows:
        formatted_output += f"\n\n... and {total_rows - max_rows} more rows"
    
    return formatted_output




