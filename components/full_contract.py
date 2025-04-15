import streamlit as st

def display_full_contract(is_sample=False):
    """
    Display the full contract text tab
    
    Args:
        is_sample: Whether to use sample data
    """
    st.subheader("Full Contract Text")
    
    pdf_file = st.session_state.get("uploaded_contract")

    if pdf_file is not None:
        st.download_button(label="Download Contract PDF", data=pdf_file.getvalue(), file_name="contract.pdf")
        st.pdf(pdf_file)
    else:
        st.warning("No contract PDF uploaded.")