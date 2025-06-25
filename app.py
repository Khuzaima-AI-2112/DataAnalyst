import streamlit as st
from data_loaders import get_llm_response, load_csv_data, load_excel_data, load_json_data, format_data_for_llm
import json
import pandas as pd

def main():
    # Title and description
    st.title("📊 Ask My Data")
    st.markdown("Upload your data file and ask questions about it using AI!")
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'filename' not in st.session_state:
        st.session_state.filename = ""
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Your Data")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'json', 'xlsx', 'xls'],
            help="Upload CSV, JSON, or Excel files"
        )
        
        if uploaded_file is not None:
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            with st.spinner("Loading file..."):
                # Load data based on file type
                if file_type == 'csv':
                    data = load_csv_data(uploaded_file)
                elif file_type == 'json':
                    data = load_json_data(uploaded_file)
                elif file_type in ['xlsx', 'xls']:
                    data = load_excel_data(uploaded_file)
                else:
                    st.error("Unsupported file format")
                    data = []
                
                if data:
                    st.session_state.data = data
                    st.session_state.file_uploaded = True
                    st.session_state.filename = uploaded_file.name
                    st.success(f"✅ File loaded successfully!")
                    st.info(f"📈 Loaded {len(data)} records")
                    
                    # Show basic info only
                    st.subheader("Dataset Info")
                    st.write(f"**File:** {uploaded_file.name}")
                    st.write(f"**Total Rows:** {len(data)}")
                    if data:
                        st.write(f"**Columns:** {len(data[0].keys())}")
                        st.write("**Column Names:**")
                        for col in data[0].keys():
                            st.write(f"- {col}")
    
    # Main chat interface
    if st.session_state.file_uploaded and st.session_state.data:
        st.header(f"💬 Chat About Your Data: {st.session_state.filename}")
        
        # Display chat history
        for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
            with st.container():
                st.markdown(f"**You:** {user_msg}")
                st.markdown(f"**AI:** {ai_msg}")
                st.divider()
        
        # Chat input
        user_question = st.text_input(
            "Ask a question about your data:",
            placeholder="e.g., What are the main patterns? Show me the top 5 values in column X",
            key="user_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            send_button = st.button("Send", type="primary")
        with col2:
            clear_button = st.button("Clear Chat History")
        
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
        
        if send_button and user_question:
            with st.spinner("Analyzing your data..."):
                # Format data for LLM context
                formatted_data = format_data_for_llm(st.session_state.data)
                
                # Create prompt with data context
                prompt = f"""
You are a data analyst assistant. Here is the user's dataset:

{formatted_data}

User Question: {user_question}

Please analyze the data and answer the user's question. Be specific and reference the actual data when possible. If you need to make calculations or identify patterns, do so based on the provided data sample.
"""
                
                # Get LLM response
                response = get_llm_response(prompt)
                
                # Add to chat history
                st.session_state.chat_history.append((user_question, response))
                
                # Rerun to show new message
                st.rerun()
    
    elif not st.session_state.file_uploaded:
        # Show instructions when no file is uploaded
        st.info("👆 Please upload a data file using the sidebar to get started!")
        
        # Show example queries
        st.subheader("Example Questions You Can Ask About Your Data:")
        example_questions = [
            "What are the main trends in this data?",
            "Can you summarize the key insights?",
            "What are the most common values in each column?",
            "Show me the top 5 entries for column X",
            "Are there any interesting patterns?",
            "What can you tell me about this dataset?",
            "How many unique values are in column Y?",
            "What's the relationship between column A and B?"
        ]
        
        for question in example_questions:
            st.markdown(f"• {question}")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit and Google Gemini AI")

if __name__ == "__main__":
    main()