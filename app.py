import streamlit as st
import os
import tempfile
from utils.document_parser import extract_text_from_document
from utils.llm_interface import extract_clauses
from db import init_db, get_db, create_user, get_user_by_email, save_analysis
from models import User
import sqlalchemy.orm

# Import modularized components
from components.dashboard import display_dashboard
from components.simple_summary import display_simple_summary
from components.detailed_analysis import display_detailed_analysis
from components.full_contract import display_full_contract
from utils.session_manager import initialize_session_state, update_risk_metrics

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="ContractClarify - Australian Contract Analysis",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def login_user(email, password):
    """Authenticate user and set session state"""
    db = next(get_db())
    user = get_user_by_email(db, email)
    if user and user.check_password(password):
        st.session_state.user = user
        st.session_state.logged_in = True
        return True
    return False

def register_user(email, password):
    """Register a new user"""
    db = next(get_db())
    if get_user_by_email(db, email):
        return False, "Email already registered"
    try:
        user = create_user(db, email, password)
        return True, "Registration successful"
    except Exception as e:
        return False, str(e)

# Authentication UI
if not st.session_state.get('logged_in'):
    st.title("Plain Sight")
    st.subheader("Australian Contract Analysis for Small Businesses")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login_user(email, password):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with tab2:
        with st.form("register_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(new_email, new_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    st.stop()

# Main app content (only shown when logged in)
st.title("Plain Sight")
st.subheader("Australian Contract Analysis for Small Businesses")

# Display user info and credits
st.sidebar.write(f"Logged in as: {st.session_state.user.email}")
st.sidebar.write(f"Credits remaining: {st.session_state.user.credits}")

# File upload
uploaded_file = st.file_uploader("Upload your contract document", type=["pdf", "docx", "txt"])

# Process the document when uploaded
if uploaded_file is not None:
    if st.session_state.user.credits <= 0:
        st.error("You have no credits remaining. Please contact support.")
        st.stop()
    
    # Create a unique identifier for this file
    file_info = f"{uploaded_file.name}_{uploaded_file.size}"
    
    # Only process the document if it's new or hasn't been fully processed
    if st.session_state.get('current_file_id') != file_info or not st.session_state.get('contract_analyzed', False):
        with st.spinner("Reading document..."):
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_file_path = tmp_file.name
            
            # Extract text from document
            document_text = extract_text_from_document(temp_file_path)
            os.unlink(temp_file_path)  # Clean up the temp file
            
            # Store document text in session state
            st.session_state.document_text = document_text
            
            # Store the file identifier
            st.session_state.current_file_id = file_info
        
        # Document stats
        st.subheader("Document Overview")
        word_count = len(document_text.split())
        st.write(f"Contract length: Approximately {word_count} words")
        
        # Extract clauses from the document
        with st.spinner("Extracting and analyzing clauses..."):
            clauses = extract_clauses(document_text)
            
            # Store clauses in session state
            st.session_state.clauses = clauses
            
            # Process and store contract data
            update_risk_metrics(clauses)
            
            # Save analysis to database
            db = next(get_db())
            save_analysis(
                db,
                st.session_state.user.id,
                uploaded_file.name,
                {
                    'clauses': clauses,
                    'risk_metrics': st.session_state.risk_metrics if 'risk_metrics' in st.session_state else {
                        'total_risks': 0,
                        'high_risk_clauses': [],
                        'medium_risk_clauses': [],
                        'low_risk_clauses': []
                    }
                }
            )
            
            # Deduct credit
            st.session_state.user.credits -= 1
            db.commit()
            
            # Mark analysis as complete
            st.session_state.contract_analyzed = True
            
            # Initialize current_clause if not already set
            if 'current_clause' not in st.session_state and clauses:
                st.session_state.current_clause = next(iter(clauses.keys()))
    
    # Display progress
    progress_bar = st.progress(0)
    
    # Show dashboard
    if st.session_state.get('contract_analyzed', False):
        st.header("Contract Analysis Dashboard")
        display_dashboard()
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Simple Summary", "Detailed Analysis", "Full Contract"])
        
        with tab1:
            display_simple_summary(progress_bar)
        
        with tab2:
            display_detailed_analysis()
        
        with tab3:
            display_full_contract()
        
        # Clean up the progress bar
        progress_bar.empty()
        
        # Add download buttons for reports
        st.subheader("Download Reports")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Analysis Report (PDF)",
                data=b"Example PDF content",
                file_name="contract_analysis.pdf",
                mime="application/pdf",
                disabled=True
            )
        
        with col2:
            st.download_button(
                label="Download Summary Document (DOCX)",
                data=b"Example DOCX content",
                file_name="contract_summary.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                disabled=True
            )
        
        # Disclaimer
        st.caption("""
        **Disclaimer**: This analysis is provided for informational purposes only and does not constitute legal advice. 
        Always consult with a qualified legal professional for specific advice tailored to your situation.
        """)

else:
    # Show sample analysis or instructions when no file is uploaded
    st.info("👆 Upload a contract document to get started.")
    
    # Option to see demo with sample contract
    if st.button("Try with Sample Contract"):
        st.session_state.show_sample = True
    
    # Display sample analysis if requested
    if st.session_state.get('show_sample', False):
        st.subheader("Sample Analysis: Service Agreement")
        
        # Create tabs for sample data
        tab1, tab2, tab3 = st.tabs(["Simple Summary", "Detailed Analysis", "Full Contract"])
        
        with tab1:
            display_simple_summary(is_sample=True)
        
        with tab2:
            display_detailed_analysis(is_sample=True)
        
        with tab3:
            display_full_contract(is_sample=True)