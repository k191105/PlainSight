import streamlit as st
import time
import random
import html
import datetime
import uuid
import streamlit.components.v1 as components

def get_sample_legal_phrases():
    """Return a list of sample legal phrases for the background animation"""
    return [
        "party of the first part",
        "hereinafter referred to as",
        "subject to the provisions of",
        "indemnify and hold harmless",
        "without limitation",
        "for the avoidance of doubt",
        "notwithstanding anything to the contrary",
        "except as otherwise provided herein",
        "force majeure",
        "mutatis mutandis",
        "good faith",
        "reasonable endeavors",
        "time is of the essence",
        "at their sole discretion",
        "termination for convenience",
        "governing law",
        "jurisdiction",
        "dispute resolution",
        "confidentiality",
        "intellectual property rights",
        "warranties and representations",
        "assignment and novation",
        "entire agreement",
        "severability",
        "consequential damages",
        "liquidated damages",
        "breach of contract",
    ]

def generate_contract_text_with_highlights():
    """Generate continuous contract text with proper punctuation, capitalization and highlights"""
    legal_terms = get_sample_legal_phrases()
    connectors = ["the", "and", "or", "of", "in", "to", "shall", "will", "may", "must", "by", "for"]
    punctuation = [".", ",", ";", ":", "."]
    
    # Generate continuous text with proper sentences
    terms = []
    sentence_length = 0
    capitalize_next = True
    
    # Generate about 300 terms for continuous text
    for _ in range(300):
        # Choose term
        if random.random() < 0.7:
            term = random.choice(legal_terms)
        else:
            term = random.choice(connectors)
        
        # Capitalize first word in sentence
        if capitalize_next:
            term = term.capitalize()
            capitalize_next = False
        
        # Only highlight multi-word legal terms, not connectors
        highlight_type = None
        if random.random() < 0.3 and term in legal_terms and " " in term:
            highlight_type = random.choice(["medium", "low"])
            
        if highlight_type:
            # Match React's random animation delay
            delay = round(random.random() * 3, 1)
            term = f'<span class="highlight {highlight_type}" style="animation-delay: {delay}s">{html.escape(term)}</span>'
        else:
            term = html.escape(term)
        
        terms.append(term)
        sentence_length += 1
        
        # Add punctuation and prepare for new sentence
        if sentence_length >= random.randint(5, 15):
            punct = random.choice(punctuation)
            terms.append(punct)
            sentence_length = 0
            capitalize_next = True
            
            # Add space for readability after periods
            if punct == ".":
                terms.append("<br/><br/>")
    
    # Join all terms with spaces
    continuous_text = " ".join(terms).replace(" <br/><br/>", "<br/><br/>").replace(" .", ".").replace(" ,", ",")
    
    # Return as a continuous flowing text
    return f"<div class='continuous-text'>{continuous_text}</div>"

def display_landing_page(login_callback, register_callback):
    """
    Display a modern landing page with dynamic text background, mimicking the React implementation
    
    Args:
        login_callback: Function to call when user logs in
        register_callback: Function to call when user registers
    """
    # Initialize session state for navigation and messages
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'message' not in st.session_state:
        st.session_state.message = {'text': '', 'type': ''}
    
    # Custom CSS matching the React implementation
    st.markdown("""
    <style>
    /* Main container styling */
    body {
        background-color: #121212;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    
    /* Reset some Streamlit styling */
    .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background-color: #090c14 !important; /* bg-gray-900 in Tailwind */
    }
    
    /* Background text effect */
    .text-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 120vh;
        overflow: hidden;
        opacity: 0.35; /* Increased from 0.3 for brightness */
        z-index: 0;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        color: #8b97a7; /* Brightened from #6b7280 */
        line-height: 2; /* Increased from 1.7 for better spacing */
        font-size: 17px; /* Increased from 16px for better visibility */
        padding: 30px; /* Increased from 20px */
        letter-spacing: 0.6px; /* Increased from 0.5px */
        word-spacing: 5px; /* Increased from 4px */
        white-space: pre-wrap;
    }
    
    /* Style for continuous text */
    .continuous-text {
        column-count: 2; /* Split text into columns for better presentation */
        column-gap: 60px;
        column-rule: 1px solid rgba(139, 151, 167, 0.2);
    }
    
    /* Add styling for paragraphs */
    .paragraph {
        margin-bottom: 2.5rem;
        text-indent: 2rem;
    }
    
    /* Add spacing between lines */
    .mb-8 {
        margin-bottom: 2rem;
    }
    
    /* Highlighted text - using exact React styling */
    .highlight {
        cursor: pointer;
        border-bottom-width: 2px;
        border-bottom-style: solid;
        padding: 0 2px;
        position: relative;
        border-radius: 3px;
        font-weight: 700;
        animation: pulse 3s infinite;
    }
    
    /* Medium severity colors from React */
    .highlight.medium {
        color: #b36b00;
        border-color: rgba(255, 153, 0, 0.6);
        background-color: rgba(255, 153, 0, 0.15);
    }
    
    /* Low severity colors from React */
    .highlight.low {
        color: #806600;
        border-color: rgba(255, 204, 0, 0.6);
        background-color: rgba(255, 204, 0, 0.15);
    }
    
    /* Match React's pulse animation */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; box-shadow: 0 0 8px rgba(255, 204, 0, 0.4); }
        100% { opacity: 0.5; }
    }
    
    /* Main content container */
    .content-container {
        position: relative;
        min-height: 100vh;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        z-index: 10;
        padding: 1rem;
        padding-bottom: 0 !important; /* Reduce bottom padding */
        margin-bottom: 0 !important;
    }
    
    /* Button container styling for Streamlit buttons */
    .stButton {
        margin-bottom: 0 !important;
    }
    
    /* Make buttons inside columns more consistent */
    div[data-testid="column"] .stButton {
        margin-top: 0.5rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* Make Streamlit buttons match the custom styling */
    .stButton > button {
        border-radius: 9999px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-0.25rem) !important;
    }
    
    /* Title styling to match React - Increased size and fixed specificity */
    .content-container .app-title {
        font-size: 8.4rem !important; /* Increased from 8rem */
        font-weight: 700 !important;
        background: linear-gradient(90deg, #10b981, #3b82f6) !important; /* from-green-500 to-blue-500 */
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        z-index: 20 !important;
        letter-spacing: -0.05em !important; /* tracking-tighter */
        text-align: center !important;
        line-height: 1.1 !important; /* Add line height control */
        display: block !important; /* Ensure display is block */
        margin-bottom: 0 !important;
    }
    
    /* Subtitle with reduced margin */
    .content-container .app-subtitle {
        font-size: 1.8rem !important; Reduced from 8rem */
        opacity: 0.8 !important;
        z-index: 20 !important;
        text-align: center !important;
        color: white !important;
        line-height: 1.2 !important; /* Add line height control */
        display: block !important; /* Ensure display is block */
        margin-bottom: 0 !important;
    }
    
    /* Layout for title and subtitle container */
    .title-container {
        display: block !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 0rem !important; /* Space between title/subtitle and buttons */
    }
    
    /* Make sure Streamlit elements are on top */
    .element-container, .stButton, button {
        z-index: 50 !important;
    }
    
    /* Primary button - login */
    .primary-btn {
        background-color: #10b981 !important; /* bg-green-600 */
        color: white !important;
        border: none !important;
    }
    
    .primary-btn:hover {
        background-color: #059669 !important; /* bg-green-500 */
    }
    
    /* Secondary button - signup */
    .secondary-btn {
        background-color: transparent !important;
        color: #10b981 !important; /* text-green-500 */
        border: 1px solid #10b981 !important; /* border-green-500 */
    }
    
    .secondary-btn:hover {
        background-color: rgba(16, 185, 129, 0.1) !important; /* bg-green-500 bg-opacity-10 */
    }
    
    /* Form styling */
    .auth-container {
        max-width: 28rem; /* max-w-md */
        margin: 5rem auto 0;
        padding: 2rem;
        background-color: rgba(17, 24, 39, 0.8); /* bg-gray-900 bg-opacity-80 */
        backdrop-filter: blur(12px); /* backdrop-blur-md */
        border-radius: 0.75rem; /* rounded-lg */
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2) !important; /* shadow-xl */
        z-index: 20;
    }
    
    .form-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .form-header h2 {
        font-size: 2.25rem; /* text-4xl */
        font-weight: 700;
        background: linear-gradient(90deg, #10b981, #3b82f6); /* from-green-500 to-blue-500 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .form-header p {
        color: #9ca3af; /* text-gray-400 */
        font-size: 1rem;
    }
    
    /* Fix duplicate form inputs */
    .stTextInput, .stPasswordInput {
        margin-bottom: 1rem !important;
    }
    
    /* Fix Streamlit's default form styling that may cause duplication */
    div[data-testid="stForm"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Fix input field duplication */
    div[data-baseweb="base-input"] {
        width: 100% !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
        border-radius: 0.375rem !important;
        border: 1px solid #374151 !important;
    }
    
    /* Hide label above the input box to prevent duplication */
    div[data-baseweb="form-control"] label {
        display: none !important;
    }
    
    /* Style just the input element */
    .stTextInput input, .stPasswordInput input, div[data-baseweb="input"] input {
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem !important;
    }
    
    /* Submit button styling */
    .stFormSubmitButton > button {
        width: 100% !important;
        padding: 0.75rem !important; /* p-3 */
        background-color: #10b981 !important; /* bg-green-600 */
        color: white !important;
        font-weight: 500 !important;
        border-radius: 0.375rem !important; /* rounded-md */
        transition: background-color 0.3s ease !important;
        margin-top: 0.5rem !important;
    }
    
    .stFormSubmitButton > button:hover {
        background-color: #059669 !important; /* bg-green-700 */
    }
    
    /* Back button */
    .back-button {
        text-align: center;
        margin-top: 1rem;
    }
    
    .back-button button {
        background-color: transparent !important;
        color: #9ca3af !important; /* text-gray-400 */
        border: none !important;
        box-shadow: none !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        text-decoration: underline !important;
    }
    
    .back-button button:hover {
        color: white !important;
        background-color: transparent !important;
        transform: none !important;
    }
    
    /* Toast message */
    .toast-message {
        position: fixed;
        bottom: 1rem;
        right: 1rem;
        padding: 1rem;
        border-radius: 0.375rem;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        z-index: 50;
    }
    
    .toast-success {
        background-color: #10b981;
    }
    
    .toast-error {
        background-color: #ef4444;
    }
    
    /* Remove Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    .button-container {
        position: relative;
        top: 2rem;
        z-index: 30;
        display: flex;
        justify-content: center;
        gap: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display toast message if present
    if st.session_state.message['text']:
        message_type = "toast-success" if st.session_state.message['type'] == 'success' else "toast-error"
        st.markdown(f"""
        <div class="toast-message {message_type}">
            {st.session_state.message['text']}
        </div>
        """, unsafe_allow_html=True)
        
        # Clear message after 2 seconds
        if not hasattr(st.session_state, 'message_time'):
            st.session_state.message_time = time.time()
        
        if time.time() - st.session_state.message_time > 2:
            st.session_state.message = {'text': '', 'type': ''}
            if hasattr(st.session_state, 'message_time'):
                delattr(st.session_state, 'message_time')
            st.rerun()
    
    # Current page selector
    if st.session_state.page == 'landing':
        # LANDING PAGE - Background, title, subtitle, and buttons
        # Create a full-page background container for the text
        contract_text = generate_contract_text_with_highlights()
        st.markdown(f"""
        <div class="text-background">
            {contract_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Main content container - restructured for better control
        st.markdown("""
        <div class="content-container">
            <div class="title-container">
                <h1 class="app-title">Plain Sight</h1>
                <p class="app-subtitle">Australian Contract Analysis for Small Businesses</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Replace JavaScript buttons with native Streamlit buttons within the content container
        button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
        with button_col2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Log In", type="primary", use_container_width=True):
                    st.session_state.page = 'login'
                    st.rerun()
            with col2:
                if st.button("Sign Up", use_container_width=True):
                    st.session_state.page = 'register'
                    st.rerun()
        
        # Close the content container div
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif st.session_state.page == 'login':
        # LOGIN PAGE
        # Create a full-page background container for the text
        contract_text = generate_contract_text_with_highlights()
        st.markdown(f"""
        <div class="text-background">
            {contract_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Create container for login form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.markdown("""
            <div class="form-header">
                <h2>Welcome Back</h2>
                <p>Log in to continue to Plain Sight</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Form fields
            with st.form("login_form", border=False, clear_on_submit=False):
                email = st.text_input("Email", key="login_email", label_visibility="collapsed", 
                                     placeholder="Email")
                password = st.text_input("Password", type="password", key="login_password", 
                                        label_visibility="collapsed", placeholder="Password")
                submit = st.form_submit_button("Log In", use_container_width=True)
                
                if submit:
                    if login_callback(email, password):
                        st.session_state.message = {'text': 'Logged in successfully!', 'type': 'success'}
                        st.session_state.message_time = time.time()
                        time.sleep(0.1)  # Brief pause for UI update
                        st.rerun()
                    else:
                        st.session_state.message = {'text': 'Invalid email or password', 'type': 'error'}
                        st.session_state.message_time = time.time()
                        st.rerun()
            
            # Back button
            st.markdown('<div class="back-button">', unsafe_allow_html=True)
            if st.button("Back to home", key="back_from_login"):
                st.session_state.page = 'landing'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
                
    elif st.session_state.page == 'register':
        # REGISTER PAGE
        # Create a full-page background container for the text
        contract_text = generate_contract_text_with_highlights()
        st.markdown(f"""
        <div class="text-background">
            {contract_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Create container for register form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.markdown("""
            <div class="form-header">
                <h2>Create Account</h2>
                <p>Sign up to start analyzing contracts</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Form fields
            with st.form("register_form", border=False, clear_on_submit=False):
                new_email = st.text_input("Email", key="register_email", label_visibility="collapsed", 
                                         placeholder="Email")
                new_password = st.text_input("Password", type="password", key="register_password", 
                                            label_visibility="collapsed", placeholder="Password")
                confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm", 
                                                label_visibility="collapsed", placeholder="Confirm Password")
                submit = st.form_submit_button("Sign Up", use_container_width=True)
                
                if submit:
                    success, message = register_callback(new_email, new_password, confirm_password)
                    if success:
                        st.session_state.message = {'text': message, 'type': 'success'}
                        st.session_state.message_time = time.time()
                        time.sleep(0.1)  # Brief pause for UI update
                        st.rerun()
                    else:
                        st.session_state.message = {'text': message, 'type': 'error'}
                        st.session_state.message_time = time.time()
                        st.rerun()
            
            # Back button
            st.markdown('<div class="back-button">', unsafe_allow_html=True)
            if st.button("Back to home", key="back_from_register"):
                st.session_state.page = 'landing'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)