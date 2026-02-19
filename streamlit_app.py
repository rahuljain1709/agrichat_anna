import streamlit as st
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Add the repo root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your custom modules
from chroma_pops_builder import ChromaPopsBuilder

# Page configuration
st.set_page_config(
    page_title="AgriBuddy Chat",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pops_builder" not in st.session_state:
        st.session_state.pops_builder = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def load_pops_builder():
    """Load or initialize the ChromaPopsBuilder"""
    if st.session_state.pops_builder is None:
        with st.spinner("Loading knowledge base..."):
            try:
                st.session_state.pops_builder = ChromaPopsBuilder()
                st.success("Knowledge base loaded successfully!")
            except Exception as e:
                st.error(f"Error loading knowledge base: {str(e)}")
    return st.session_state.pops_builder

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🌾 AgriBuddy Chat")
    st.subheader("Your AI-Powered Agricultural Assistant")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        st.markdown("---")
        
        # Load knowledge base button
        if st.button("Load Knowledge Base", key="load_kb"):
            load_pops_builder()
        
        # Display knowledge base status
        if st.session_state.pops_builder is not None:
            st.success("✓ Knowledge Base Loaded")
        else:
            st.warning("⚠ Knowledge Base Not Loaded")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        AgriBuddy is an intelligent chatbot designed to provide 
        agricultural guidance and support using advanced AI and 
        knowledge retrieval systems.
        """)
    
    # Main chat interface
    st.markdown("---")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    st.subheader("Ask a Question")
    user_input = st.chat_input("Type your agricultural question here...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Load knowledge base if not already loaded
        pops_builder = load_pops_builder()
        
        if pops_builder is not None:
            # Get response from the knowledge base
            with st.chat_message("assistant"):
                try:
                    # Query the knowledge base (customize this based on your actual implementation)
                    response = "Thank you for your question! Response generation coming soon."
                    st.markdown(response)
                    
                    # Add assistant message to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
        else:
            st.error("Please load the knowledge base first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    Made with ❤️ for agricultural communities
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()