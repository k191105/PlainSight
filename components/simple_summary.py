import streamlit as st
from utils.llm_interface import summarize_clause
from utils.session_manager import get_sample_contract_data

def display_simple_summary(progress_bar=None, is_sample=False):
    """
    Display the simple summary tab
    
    Args:
        progress_bar: Optional progress bar to update
        is_sample: Whether to use sample data
    """
    st.subheader("Simple Contract Summary")
    st.write("Key points from your contract in plain English:")
    
    if is_sample:
        # Use sample data
        sample_data = get_sample_contract_data()
        
        for clause in sample_data["clauses"]:
            st.markdown(f"**{clause['title']}**")
            st.write(clause['summary'])
            st.divider()
    else:
        # Process real clauses
        key_clauses_summary = []
        
        clauses = st.session_state.clauses
        for i, (title, text) in enumerate(list(clauses.items())[:5]):  # Just show top 5 for simple view
            summary = summarize_clause(title, text)
            key_clauses_summary.append((title, summary))
            
            # Update progress bar if provided
            if progress_bar:
                progress_bar.progress((i + 1) / len(clauses))
        
        for title, summary in key_clauses_summary:
            st.markdown(f"**{title}**")
            st.write(summary)
            st.divider()