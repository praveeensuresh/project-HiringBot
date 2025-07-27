"""
TalentScout Hiring Assistant Chatbot
Main Streamlit application file
"""

import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import HiringAssistant

# Load environment variables
load_dotenv()

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="TalentScout Hiring Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    # Title and description
    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown("Welcome! I'm here to help with your initial screening process.")
    
    # Initialize chatbot in session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HiringAssistant()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_msg = st.session_state.chatbot.get_welcome_message()
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your response here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.process_message(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
