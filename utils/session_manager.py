import streamlit as st
from typing import Dict, List, Any, Optional
from utils.llm_interface import summarize_clause, analyze_risks

def initialize_session_state():
    """Initialize all session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    
    if 'current_file_id' not in st.session_state:
        st.session_state.current_file_id = None
    
    if 'contract_analyzed' not in st.session_state:
        st.session_state.contract_analyzed = False
    
    if 'clauses' not in st.session_state:
        st.session_state.clauses = {}
    
    if 'risk_metrics' not in st.session_state:
        st.session_state.risk_metrics = {
            'total_risks': 0,
            'high_risk_clauses': [],
            'medium_risk_clauses': [],
            'low_risk_clauses': []
        }
    
    if 'current_clause' not in st.session_state:
        st.session_state.current_clause = None
    
    if 'show_sample' not in st.session_state:
        st.session_state.show_sample = False

def update_risk_metrics(clauses):
    """Update risk metrics based on analyzed clauses"""
    # Reset risk metrics
    st.session_state.risk_metrics = {
        'total_risks': 0,
        'high_risk_clauses': [],
        'medium_risk_clauses': [],
        'low_risk_clauses': []
    }
    
    # Analyze each clause and categorize risks
    for clause_id, clause_text in clauses.items():
        # Analyze the clause text for risk indicators
        risk_indicators = {
            'high': [
                'indemnify', 'warranty', 'liability', 'termination',
                'confidential', 'exclusive', 'assignment', 'jurisdiction',
                'penalty', 'damages', 'breach', 'default'
            ],
            'medium': [
                'payment', 'fee', 'cost', 'expense', 'charge',
                'notice', 'period', 'time', 'date', 'deadline'
            ]
        }
        
        # Count risk indicators
        high_risk_count = sum(1 for indicator in risk_indicators['high'] 
                            if indicator.lower() in clause_text.lower())
        medium_risk_count = sum(1 for indicator in risk_indicators['medium'] 
                              if indicator.lower() in clause_text.lower())
        
        # Determine risk level
        if high_risk_count >= 2:
            risk_level = 'high'
        elif high_risk_count >= 1 or medium_risk_count >= 2:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        # Categorize the clause
        if risk_level == 'high':
            st.session_state.risk_metrics['high_risk_clauses'].append(clause_id)
        elif risk_level == 'medium':
            st.session_state.risk_metrics['medium_risk_clauses'].append(clause_id)
        else:
            st.session_state.risk_metrics['low_risk_clauses'].append(clause_id)
    
    # Update total risks
    st.session_state.risk_metrics['total_risks'] = (
        len(st.session_state.risk_metrics['high_risk_clauses']) +
        len(st.session_state.risk_metrics['medium_risk_clauses']) +
        len(st.session_state.risk_metrics['low_risk_clauses'])
    )

def set_current_clause(clause_title: str) -> None:
    """
    Set the current clause for detailed view
    
    Args:
        clause_title: Title of the clause to set as current
    """
    # Simply update the session state
    st.session_state.current_clause = clause_title

def get_current_clause_data() -> Dict[str, Any]:
    """
    Get data for the currently selected clause
    
    Returns:
        Dictionary with clause data including title, text, summary, risks, etc.
    """
    # Get the current clause title
    current = st.session_state.current_clause
    
    # Default empty response
    result = {
        "title": "",
        "text": "",
        "summary": "",
        "risks": [],
        "detailed_risks": [],
        "risk_level": "low",
        "user_note": ""
    }
    
    # If no clause is selected or no clauses exist, return the default
    if not current or not st.session_state.clauses:
        return result
    
    # Get clause text
    clause_text = st.session_state.clauses.get(current, "")
    
    # Get risk level from risk_metrics
    risk_metrics = st.session_state.get('risk_metrics', {
        'total_risks': 0,
        'high_risk_clauses': [],
        'medium_risk_clauses': [],
        'low_risk_clauses': []
    })
    
    # Determine risk level based on which list the clause is in
    if current in risk_metrics['high_risk_clauses']:
        risk_level = "high"
    elif current in risk_metrics['medium_risk_clauses']:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # Get summary
    summary = st.session_state.get('clause_summaries', {}).get(current, "")
    
    # Get user note
    user_note = st.session_state.get('clause_user_notes', {}).get(current, "")
    
    # Compile the result
    result = {
        "title": current,
        "text": clause_text,
        "summary": summary,
        "risks": [],  # We'll populate this based on risk level
        "detailed_risks": [],  # We'll populate this based on risk level
        "risk_level": risk_level,
        "user_note": user_note
    }
    
    # Add appropriate risks based on risk level
    if risk_level == "high":
        result["risks"] = ["Multiple high-risk indicators found in this clause"]
        result["detailed_risks"] = ["This clause contains multiple high-risk terms that may require careful review"]
    elif risk_level == "medium":
        result["risks"] = ["Some risk indicators found in this clause"]
        result["detailed_risks"] = ["This clause contains some terms that may require attention"]
    
    return result

def save_user_note(clause_title: str, note_text: str) -> None:
    """
    Save a user note for a clause
    
    Args:
        clause_title: Title of the clause
        note_text: Note text to save
    """
    st.session_state.clause_user_notes[clause_title] = note_text

def get_sample_contract_data() -> Dict[str, Any]:
    """
    Get sample contract data for demonstration
    
    Returns:
        Dictionary with sample clauses and risk information
    """
    return {
        "clauses": [
            {
                "title": "1. Definitions",
                "text": "In this Agreement: 'Service' means the consulting services provided by the Consultant to the Client as described in Schedule A; 'Deliverables' means all documents, products, and materials developed by the Consultant in relation to the Services; 'Intellectual Property Rights' means patents, rights to inventions, copyright and related rights, trademarks, trade names and domain names, rights in get-up, goodwill and the right to sue for passing off, rights in designs, rights in computer software, database rights, rights to preserve the confidentiality of information (including know-how and trade secrets) and any other intellectual property rights, in each case whether registered or unregistered and including all applications (or rights to apply) for and renewals or extensions of, such rights and all similar or equivalent rights or forms of protection which subsist or will subsist now or in the future in any part of the world.",
                "summary": "This section defines the key terms used throughout the agreement. It clarifies what constitutes the 'Service', 'Deliverables', and 'Intellectual Property Rights' so both parties have a clear understanding of these concepts when referenced elsewhere in the contract.",
                "risks": [],
                "risk_level": "low"
            },
            {
                "title": "2. Scope of Work",
                "text": "The Consultant shall provide the Services with reasonable skill and care. The Consultant shall allocate sufficient resources to provide the Services in accordance with this Agreement. The Consultant shall meet any agreed performance dates and times for the Services. Time shall not be of the essence in this Agreement.",
                "summary": "This section outlines what work the consultant must do. It requires them to use reasonable skill, allocate enough resources, and meet agreed deadlines. However, the last sentence 'time shall not be of the essence' means that missing deadlines is not automatically considered a fundamental breach of contract.",
                "risks": [],
                "risk_level": "low"
            },
            {
                "title": "3. Payment Terms",
                "text": "The Client shall pay the Consultant within 30 days of receipt of invoice. Late payment shall incur interest at 2% above the Reserve Bank of Australia cash rate calculated from the due date until the date of actual payment. The Consultant may suspend the Services if payment is not received within 45 days of the invoice date. All amounts payable by the Client are exclusive of GST.",
                "summary": "You must pay the consultant within 30 days after receiving their invoice. If you pay late, you'll be charged interest at 2% above the RBA cash rate. The consultant can stop working if you haven't paid within 45 days. All prices are subject to additional GST.",
                "risks": [
                    "The 30-day payment term may be too long for small businesses with cash flow concerns."
                ],
                "risk_level": "medium"
            },
            {
                "title": "4. Intellectual Property",
                "text": "All Intellectual Property Rights in the Deliverables shall be owned by the Client. The Consultant hereby assigns to the Client, with full title guarantee and free from all third party rights, all Intellectual Property Rights in the Deliverables. This assignment shall take effect on the date of this Agreement or as a present assignment of future rights that will take effect immediately on the creation of the Deliverables.",
                "summary": "This clause gives the client ownership of all intellectual property created during the project. The consultant transfers all rights to the client automatically, both for existing work and anything created in the future under this contract.",
                "risks": [],
                "risk_level": "low"
            },
            {
                "title": "5. Confidentiality",
                "text": "Each party shall maintain the confidentiality of all information disclosed to it by the other party which is identified as confidential or which would reasonably be understood to be confidential in nature. Neither party shall use any confidential information of the other party for any purpose other than to perform its obligations under this Agreement. The obligations of confidentiality shall survive the termination of this Agreement and continue indefinitely.",
                "summary": "Both parties must keep each other's sensitive information private and only use it for purposes related to this contract. This confidentiality requirement continues forever, even after the contract ends.",
                "risks": [
                    "The confidentiality obligations continue indefinitely, which may be overly restrictive."
                ],
                "risk_level": "medium"
            },
            {
                "title": "6. Termination",
                "text": "This Agreement may be terminated by either party with 30 days written notice to the other party. Either party may terminate this Agreement immediately if the other party commits a material breach of this Agreement which is not remedied within 14 days of written notice, or if the other party becomes insolvent. Upon termination, the Client shall pay the Consultant for all Services provided up to the date of termination.",
                "summary": "Either party can end this agreement with 30 days' notice. Immediate termination is possible if there's a serious breach that isn't fixed within 14 days, or if either party goes bankrupt. You'll still need to pay for all work completed up to the termination date.",
                "risks": [
                    "The 30-day notice period for termination may be problematic if you need to exit quickly."
                ],
                "risk_level": "medium"
            },
            {
                "title": "7. Limitation of Liability",
                "text": "The Consultant's liability shall not exceed the fees paid by the Client to the Consultant under this Agreement. Neither party shall be liable for any indirect, special, incidental or consequential damages arising out of or in connection with this Agreement. Nothing in this Agreement shall limit or exclude either party's liability for death or personal injury caused by negligence, or fraud or fraudulent misrepresentation.",
                "summary": "The consultant's liability is limited to the total amount you've paid them. Neither party is responsible for indirect damages like lost profits. However, they can't limit liability for negligence causing death/injury or for fraud.",
                "risks": [
                    "This broad limitation of liability clause may be unenforceable under Australian Consumer Law for certain types of loss.",
                    "The clause attempts to exclude liability for consequential losses which may be unfair under the ACCC's unfair contract terms guidance."
                ],
                "risk_level": "high"
            },
            {
                "title": "8. Governing Law",
                "text": "This Agreement is governed by the laws of New South Wales. The parties submit to the non-exclusive jurisdiction of the courts of New South Wales and courts of appeal from them for determining any dispute concerning this Agreement.",
                "summary": "This contract is governed by New South Wales law. If there's a legal dispute, it will be handled in NSW courts, though other courts might also be able to hear the case.",
                "risks": [],
                "risk_level": "low"
            }
        ]
    }