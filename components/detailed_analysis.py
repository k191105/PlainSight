import streamlit as st
from utils.session_manager import get_current_clause_data, set_current_clause, save_user_note, get_sample_contract_data
from utils.text_highlighter import annotate_clause_risks
from utils.lucide_icons import get_risk_icon

LUCIDE_ICON_HIGH_RISK = get_risk_icon("high")
LUCIDE_ICON_MEDIUM_RISK = get_risk_icon("medium")
LUCIDE_ICON_LOW_RISK = get_risk_icon("low")

def display_detailed_analysis(is_sample=False):
    """
    Display the detailed clause analysis tab with highlighted problematic text
    
    Args:
        is_sample: Whether to use sample data
    """
    st.subheader("Detailed Clause Analysis")
    
    if is_sample:
        # Use sample data
        sample_data = get_sample_contract_data()
        clauses = sample_data["clauses"]
        
        # Ensure sample_clause exists in session state
        if "sample_clause" not in st.session_state and clauses:
            st.session_state.sample_clause = clauses[0]['title']
        
        # Create a layout with sidebar and main content
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### Contract Clauses")
            
            # Create clause navigation
            for i, clause in enumerate(clauses):
                # Determine icon based on risk level
                if clause["risk_level"] == "high":
                    icon = "⚠️"
                elif clause["risk_level"] == "medium":
                    icon = "⚠"
                else:
                    icon = "✓"
                
                # Display clause button
                is_selected = st.session_state.sample_clause == clause['title']
                button_type = "primary" if is_selected else "secondary"
                
                # Use a unique key for each button
                button_key = f"sample_clause_{i}_{clause['title']}"
                if st.button(f"{icon} {clause['title']}", 
                             key=button_key, 
                             type=button_type,
                             use_container_width=True):
                    st.session_state.sample_clause = clause['title']
                    st.rerun()
        
        with col2:
            # Get the selected clause
            selected_sample = st.session_state.sample_clause
            sample_clause = next((c for c in clauses if c['title'] == selected_sample), clauses[0])
            
            # Display risk level badge
            risk_color = "red" if sample_clause["risk_level"] == "high" else \
                        "orange" if sample_clause["risk_level"] == "medium" else \
                        "green"
            risk_text = "HIGH RISK" if sample_clause["risk_level"] == "high" else \
                        "MEDIUM RISK" if sample_clause["risk_level"] == "medium" else \
                        "LOW RISK"
            
            st.markdown(f"# {sample_clause['title']} <span style='background-color: {risk_color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 16px; vertical-align: middle;'>{risk_text}</span>", unsafe_allow_html=True)
            
            # Navigation buttons
            cols = st.columns(2)
            with cols[0]:
                # Get current index
                current_index = next((i for i, c in enumerate(clauses) if c['title'] == sample_clause['title']), 0)
                if current_index > 0:
                    prev_clause = clauses[current_index - 1]['title']
                    if st.button("← Previous Clause", key="prev_sample_button", use_container_width=True):
                        st.session_state.sample_clause = prev_clause
                        st.rerun()
                else:
                    st.button("← Previous Clause", key="prev_sample_button", disabled=True, use_container_width=True)
                    
            with cols[1]:
                # Get current index
                current_index = next((i for i, c in enumerate(clauses) if c['title'] == sample_clause['title']), 0)
                if current_index < len(clauses) - 1:
                    next_clause = clauses[current_index + 1]['title']
                    if st.button("Next Clause →", key="next_sample_button", use_container_width=True):
                        st.session_state.sample_clause = next_clause
                        st.rerun()
                else:
                    st.button("Next Clause →", key="next_sample_button", disabled=True, use_container_width=True)
            
            # Annotated Clause Text with Highlighted Issues
            if "detailed_risks" in sample_clause and sample_clause["detailed_risks"]:
                annotate_clause_risks(sample_clause["text"], sample_clause["detailed_risks"])
            else:
                # No detailed risks available, display the standard clause text
                st.markdown("### Clause Text")
                # Show context around the clause to indicate it's part of a larger contract
                st.markdown(f"""
                <div class="clause-text">
                ... [Previous clause content] ...<br><br>
                {sample_clause["text"]}<br><br>
                ... [Next clause content] ...
                </div>
                """, unsafe_allow_html=True)
                
                # Simple risk display if no detailed risks
                if sample_clause["risks"]:
                    st.markdown("### Risk Analysis")
                    for risk in sample_clause["risks"]:
                        st.markdown(f"- {risk}")
                else:
                    st.markdown("### Annotation Details")
                    st.markdown("No significant risks identified in this clause.")

            # User notes
            note_key = f"sample_note_{sample_clause['title']}"
            if note_key not in st.session_state:
                st.session_state[note_key] = ""
                
            st.markdown("### Your Notes")
            st.text_area("Add your notes for this clause", 
                         value=st.session_state[note_key], 
                         height=100, 
                         key=f"note_input_{sample_clause['title']}",
                         on_change=lambda: setattr(st.session_state, note_key, 
                                                 st.session_state[f"note_input_{sample_clause['title']}"]))
            
            # Plain English Summary is now moved above the clause text
            st.markdown("### Plain English Summary")
            st.markdown(sample_clause["summary"])
    else:
        # Check if contract has been analyzed
        if not st.session_state.get('contract_analyzed', False):
            st.warning("Please upload and analyze a contract first.")
            return
        
        # Create a layout with sidebar and main content
        col1, col2 = st.columns([1, 3])
        
        # Ensure current_clause is initialized
        clauses = st.session_state.clauses
        if 'current_clause' not in st.session_state and clauses:
            st.session_state.current_clause = next(iter(clauses.keys()))
        
        with col1:
            st.markdown("### Contract Clauses")
            
            # Create clause navigation
            for i, clause_title in enumerate(clauses.keys()):
                # Determine risk level from risk_metrics
                risk_metrics = st.session_state.get('risk_metrics', {
                    'total_risks': 0,
                    'high_risk_clauses': [],
                    'medium_risk_clauses': [],
                    'low_risk_clauses': []
                })
                
                # Determine risk level based on which list the clause is in
                if clause_title in risk_metrics['high_risk_clauses']:
                    risk_level = "high"
                elif clause_title in risk_metrics['medium_risk_clauses']:
                    risk_level = "medium"
                else:
                    risk_level = "low"
                
                # Determine icon based on risk level
                if risk_level == "high":
                    icon = "⚠️"
                elif risk_level == "medium":
                    icon = "⚠"
                else:
                    icon = "✓"
                
                # Highlight current clause
                is_current = st.session_state.current_clause == clause_title
                button_type = "primary" if is_current else "secondary"
                
                # Use a unique key for each button
                button_key = f"clause_button_{i}_{clause_title}"
                if st.button(
                    f"{icon} {clause_title}", 
                    key=button_key,
                    type=button_type,
                    use_container_width=True
                ):
                    st.session_state.current_clause = clause_title
                    st.rerun()
        
        with col2:
            # Get current clause data
            clause_data = get_current_clause_data()
            
            if not clause_data["title"]:
                st.warning("No clauses found. Please upload and analyze a contract.")
                return
            
            # Display risk level badge
            risk_color = "red" if clause_data["risk_level"] == "high" else \
                        "orange" if clause_data["risk_level"] == "medium" else \
                        "green"
            risk_text = "HIGH RISK" if clause_data["risk_level"] == "high" else \
                        "MEDIUM RISK" if clause_data["risk_level"] == "medium" else \
                        "LOW RISK"
            
            st.markdown(f"# {clause_data['title']} <span style='background-color: {risk_color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 16px; vertical-align: middle;'>{risk_text}</span>", unsafe_allow_html=True)
            
            # Navigation buttons
            col_prev, col_next = st.columns(2)
            
            # Get all clause titles for navigation
            all_clauses = list(st.session_state.clauses.keys())
            current_index = all_clauses.index(clause_data["title"]) if clause_data["title"] in all_clauses else 0
            
            with col_prev:
                if current_index > 0:
                    prev_clause = all_clauses[current_index - 1]
                    if st.button("← Previous Clause", key="prev_clause_button", use_container_width=True):
                        st.session_state.current_clause = prev_clause
                        st.rerun()
                else:
                    st.button("← Previous Clause", key="prev_clause_button", disabled=True, use_container_width=True)
            
            with col_next:
                if current_index < len(all_clauses) - 1:
                    next_clause = all_clauses[current_index + 1]
                    if st.button("Next Clause →", key="next_clause_button", use_container_width=True):
                        st.session_state.current_clause = next_clause
                        st.rerun()
                else:
                    st.button("Next Clause →", key="next_clause_button", disabled=True, use_container_width=True)
            
            # Annotated Clause Text with Highlighted Issues
            if "detailed_risks" in clause_data and clause_data["detailed_risks"]:
                annotate_clause_risks(clause_data["text"], clause_data["detailed_risks"])
            else:
                # No detailed risks available, display the standard clause text
                st.markdown("### Clause Text")
                st.text_area("", clause_data["text"], height=150, 
                            key=f"clause_text_display_{clause_data['title']}", 
                            disabled=True)
                
                # Simple risk display if no detailed risks
                if clause_data["risks"]:
                    st.markdown("### Annotation Details")
                    for risk in clause_data["risks"]:
                        st.markdown(f"- {risk}")
                else:
                    st.markdown("### Annotation Details")
                    st.markdown("No significant risks identified in this clause.")

            # User notes
            st.markdown("### Your Notes")
            note_key = f"user_note_{clause_data['title']}"
            
            # Initialize note in session state if not present
            if note_key not in st.session_state:
                st.session_state[note_key] = clause_data["user_note"]
                
            note_text = st.text_area("Add your notes for this clause", 
                                    value=st.session_state[note_key],
                                    height=100, 
                                    key=f"note_input_{clause_data['title']}")
            
            # Save the note if it changes
            if note_text != st.session_state[note_key]:
                st.session_state[note_key] = note_text
                save_user_note(clause_data["title"], note_text)
            
            # Plain English Summary
            st.markdown("### Plain English Summary")
            st.markdown(clause_data["summary"])