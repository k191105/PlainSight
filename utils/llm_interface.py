import os
import json
import time
import hashlib
import re
from typing import Dict, List, Any, Optional, Tuple
from openai import OpenAI
from prompts.extraction_prompt import EXTRACTION_PROMPT
from prompts.summary_prompt import SUMMARY_PROMPT
from prompts.risk_prompt import RISK_PROMPT
from dotenv import load_dotenv
import streamlit as st

# Add this for debugging
import traceback
import sys
from datetime import datetime

# Debug logging function
def debug_log(message, data=None):
    """Write debug info to a file with absolute path"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # Use absolute path in user's home directory for reliable access
    log_path = os.path.join(os.path.expanduser("~"), "plainsight_debug.log")
    try:
        with open(log_path, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
            if data is not None:
                f.write(f"DATA: {str(data)[:1000]}")
                if len(str(data)) > 1000:
                    f.write("... (truncated)")
                f.write("\n")
            f.write("-" * 80 + "\n")
        # Also print to stderr for immediate visibility
        print(f"DEBUG: {message}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"ERROR LOGGING: {str(e)}", file=sys.stderr, flush=True)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mock data for development without API calls
MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() == "true"

# Cache the extraction function
@st.cache_data(ttl=3600, show_spinner=False)
def extract_clauses(document_text: str) -> Dict[str, str]:
    """
    Extract clauses from contract text using GPT
    
    Args:
        document_text: Full text of the contract document
        
    Returns:
        Dictionary with clause titles as keys and clause text as values
    """
    if MOCK_MODE:
        # Return mock data for development
        return {
            "1. Definitions": "In this Agreement: 'Service' means the consulting services...",
            "2. Scope of Work": "The Consultant shall provide the following services to the Client...",
            "3. Payment Terms": "The Client shall pay the Consultant within 30 days of receipt of invoice...",
            "4. Intellectual Property": "All intellectual property created during the provision of services...",
            "5. Confidentiality": "Each party shall maintain the confidentiality of all information...",
            "6. Termination": "This Agreement may be terminated by either party with 30 days notice...",
            "7. Limitation of Liability": "The Consultant's liability shall not exceed the fees paid...",
            "8. Governing Law": "This Agreement is governed by the laws of New South Wales..."
        }
    
    # Prepare prompt with the document text
    prompt = EXTRACTION_PROMPT.format(document_text=document_text)
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(model="gpt-4o-mini",  # or "gpt-3.5-turbo" for lower cost
            messages=[
                {"role": "system", "content": "You are a legal assistant specializing in Australian contract law. Your task is to extract and identify distinct clauses from contracts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for more consistent results
            max_tokens=2000
        )
        
        # Parse the response
        try:
            clauses_json = response.choices[0].message.content
            # Extract JSON if it's within markdown code blocks
            if "```json" in clauses_json:
                clauses_json = clauses_json.split("```json")[1].split("```")[0]
            elif "```" in clauses_json:
                clauses_json = clauses_json.split("```")[1].split("```")[0]
            
            # Parse the JSON response
            clauses = json.loads(clauses_json)
            return clauses
        except json.JSONDecodeError:
            # Fallback to regex-based extraction if JSON parsing fails
            from utils.document_parser import identify_clauses_regex
            return identify_clauses_regex(document_text)
            
    except Exception as e:
        print(f"Error in GPT clause extraction: {str(e)}")
        # Fallback to regex-based extraction
        from utils.document_parser import identify_clauses_regex
        return identify_clauses_regex(document_text)

# Cache the summarization function
@st.cache_data(ttl=3600, show_spinner=False)
def summarize_clause(clause_title: str, clause_text: str) -> str:
    """
    Generate a plain English summary of a contract clause
    
    Args:
        clause_title: Title or identifier of the clause
        clause_text: Full text of the clause
        
    Returns:
        Plain English summary of the clause
    """
    if MOCK_MODE:
        # Return mock data for development
        mock_summaries = {
            "1. Definitions": "This section defines key terms used throughout the agreement, including what constitutes the 'Service' and who the parties are.",
            "2. Scope of Work": "This outlines exactly what work the consultant will do, including deliverables and timelines.",
            "3. Payment Terms": "You must pay within 30 days of receiving an invoice. Late payments may incur additional fees.",
            "4. Intellectual Property": "Any work created during the project belongs to the client after payment is complete.",
            "5. Confidentiality": "Both parties must keep sensitive business information private and not share it with others.",
            "6. Termination": "Either party can end the agreement with 30 days written notice. Immediate termination is possible if there's a serious breach.",
            "7. Limitation of Liability": "The consultant won't be responsible for damages beyond the amount you've paid them.",
            "8. Governing Law": "If there's a dispute, New South Wales law applies and any legal proceedings must happen in NSW courts."
        }
        
        # Return mock summary if available, otherwise generate a generic one
        return mock_summaries.get(clause_title, f"This clause covers {clause_title.lower()} terms.")
    
    # Prepare prompt
    prompt = SUMMARY_PROMPT.format(clause_title=clause_title, clause_text=clause_text)
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a legal assistant specializing in explaining Australian contract law in plain English. Your goal is to make complex legal language understandable for small business owners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Slightly higher for more natural language
            max_tokens=500
        )
        
        # Return the summary
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error in GPT summarization: {str(e)}")
        # Return a generic summary if API call fails
        return f"This clause appears to address {clause_title.lower()}. Please review the original text for details."

# Cache the risk analysis function
@st.cache_data(ttl=3600, show_spinner=False)
def analyze_risks(clause_title: str, clause_text: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Analyze a clause for potential legal risks based on Australian law
    
    Args:
        clause_title: Title or identifier of the clause
        clause_text: Full text of the clause
        
    Returns:
        Tuple containing:
        - List of risk statements (for backward compatibility)
        - List of dictionaries with detailed risk information including problematic text
    """
    debug_log(f"Starting risk analysis for clause: {clause_title}")
    debug_log("Clause text sample", clause_text[:100])
    
    if MOCK_MODE:
        debug_log("Using MOCK_MODE, returning mock data")
        # Return mock data for development
        mock_risks = {
            "1. Definitions": [],
            "2. Scope of Work": [],
            "3. Payment Terms": [
                {
                    "problematic_text": "The Client shall pay the Consultant within 30 days of receipt of invoice",
                    "explanation": "The 30-day payment term may be too long for small businesses with cash flow concerns.",
                    "legal_reference": "ACCC guidelines on fair payment terms for small businesses",
                    "severity": "medium"
                }
            ],
            "4. Intellectual Property": [],
            "5. Confidentiality": [
                {
                    "problematic_text": "Each party shall maintain the confidentiality of all information",
                    "explanation": "The confidentiality obligations continue indefinitely, which may be overly restrictive.",
                    "legal_reference": "Australian common law on restraint of trade",
                    "severity": "medium"
                }
            ],
            "6. Termination": [
                {
                    "problematic_text": "This Agreement may be terminated by either party with 30 days notice",
                    "explanation": "The 30-day notice period for termination may be problematic if you need to exit quickly.",
                    "legal_reference": "ACCC guidelines on fair termination clauses",
                    "severity": "low"
                }
            ],
            "7. Limitation of Liability": [
                {
                    "problematic_text": "The Consultant's liability shall not exceed the fees paid",
                    "explanation": "This broad limitation of liability clause may be unenforceable under Australian Consumer Law for certain types of loss.",
                    "legal_reference": "Section 64A of the Australian Consumer Law",
                    "severity": "high"
                }
            ],
            "8. Governing Law": []
        }
        
        # Get the detailed risk information
        detailed_risks = mock_risks.get(clause_title, [])
        
        # For backward compatibility, also return the simple risk statements
        simple_risks = [risk["explanation"] for risk in detailed_risks]
        
        return simple_risks, detailed_risks
    
    # Prepare prompt
    prompt = RISK_PROMPT.format(clause_title=clause_title, clause_text=clause_text)
    debug_log("Prompt prepared", prompt)
    
    def call_llm(model_name="gpt-4o"):
        """Helper function to call OpenAI API with error handling"""
        debug_log(f"Calling OpenAI API with model: {model_name}")
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a legal risk analysis system specializing in Australian contract law. Identify potential risks in contract clauses for small businesses, focusing on unfair contract terms under the Australian Consumer Law and ACCC guidelines. You must respond with valid JSON in the exact format specified in the prompt."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Low temperature for consistency
                max_tokens=800
            )
            response_text = response.choices[0].message.content.strip()
            debug_log(f"Raw response from {model_name}", response_text)
            return response_text
        except Exception as e:
            error_str = str(e).lower()
            # Check for common rate limit errors
            if "rate limit" in error_str or "quota" in error_str or "capacity" in error_str or "limit" in error_str:
                debug_log(f"⚠️ RATE LIMIT ERROR with {model_name}: {str(e)}")
                print(f"⚠️ OPENAI RATE LIMIT DETECTED: {str(e)}", file=sys.stderr, flush=True)
                
                # Add this message to your UI
                st.error(f"OpenAI API rate limit reached. Please try again later or check your usage limits.")
            else:
                debug_log(f"Error calling {model_name}: {str(e)}")
            return None
    
    try:
        # First try with GPT-4o
        response_text = call_llm("gpt-4o")
        
        # Check if response looks generic
        generic_patterns = [
            "multiple high-risk terms",
            "may require careful review",
            "This clause contains",
            "potential risks"
        ]
        
        is_generic = False
        if response_text:
            is_generic = all(pattern.lower() in response_text.lower() for pattern in generic_patterns[:2])
            
        # If response looks generic, try with GPT-4-turbo
        if is_generic:
            debug_log("Got generic response from GPT-4o, trying GPT-4-turbo")
            backup_response = call_llm("gpt-4-turbo")
            if backup_response:
                response_text = backup_response
                debug_log("Using GPT-4-turbo response instead")
            else:
                # If both GPT-4 models fail, try GPT-3.5-turbo as a last resort
                debug_log("GPT-4 models failed, trying GPT-3.5-turbo as fallback")
                fallback_response = call_llm("gpt-3.5-turbo")
                if fallback_response:
                    response_text = fallback_response
                    debug_log("Using GPT-3.5-turbo response as last resort")
                    # Add a notice in the UI
                    st.warning("Using GPT-3.5 model due to API limitations. Results may be less accurate.")
        
        if not response_text:
            debug_log("No response received from OpenAI models")
            return [], []
            
        # Rest of processing remains the same
        # Try to parse as JSON
        detailed_risks = []
        simple_risks = []
        
        try:
            debug_log("Attempting to parse JSON response")
            # First try to find JSON in the response
            json_str = None
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0]
                debug_log("Found JSON in ```json block", json_str)
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0]
                debug_log("Found JSON in ``` block", json_str)
            else:
                # Try to find JSON array in the text
                json_match = re.search(r'\[\s*\{.*\}\s*\]', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    debug_log("Found JSON array in text", json_str)
                else:
                    json_str = response_text
                    debug_log("Using entire response as JSON", json_str)
            
            # Clean up the JSON string
            json_str = json_str.strip()
            # Remove any trailing commas
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            debug_log("Cleaned JSON string", json_str)
            
            # Parse the JSON
            try:
                detailed_risks = json.loads(json_str)
                debug_log("Successfully parsed JSON", detailed_risks)
            except json.JSONDecodeError as e:
                debug_log(f"JSON parsing error: {str(e)}", json_str)
                raise
            
            # Validate the structure
            if not isinstance(detailed_risks, list):
                error_msg = "Response is not a JSON array"
                debug_log(error_msg, detailed_risks)
                raise ValueError(error_msg)
            
            # Extract simple risks for backward compatibility
            for risk_item in detailed_risks:
                if not isinstance(risk_item, dict):
                    error_msg = "Risk item is not a dictionary"
                    debug_log(error_msg, risk_item)
                    raise ValueError(error_msg)
                if "explanation" not in risk_item:
                    error_msg = "Risk item missing 'explanation' field"
                    debug_log(error_msg, risk_item)
                    raise ValueError(error_msg)
                simple_risks.append(risk_item.get("explanation", ""))
                
            # Add clear error for generic responses
            if detailed_risks and all(not risk.get("problematic_text") for risk in detailed_risks):
                debug_log("WARNING: Response contains no specific problematic text references")
            
            debug_log(f"Returning {len(simple_risks)} risks, {len(detailed_risks)} detailed risks")
            return simple_risks, detailed_risks
        
        except (json.JSONDecodeError, ValueError, IndexError) as e:
            debug_log(f"Exception during JSON parsing: {type(e).__name__}: {str(e)}")
            debug_log("Traceback", traceback.format_exc())
            
            # Fallback to the old method for backward compatibility
            debug_log("Falling back to manual text parsing")
            if "no significant risks" in response_text.lower() or "no risks" in response_text.lower():
                debug_log("No risks detected in response")
                return [], []
            
            # Extract risk points
            for line in response_text.split('\n'):
                line = line.strip()
                # Look for list items or paragraphs that describe risks
                if (line.startswith('- ') or line.startswith('• ') or 
                    line.startswith('* ') or line.startswith('Risk:')):
                    # Clean up the line
                    risk = line.lstrip('- •*').strip()
                    if risk.lower().startswith('risk:'):
                        risk = risk[5:].strip()
                    
                    if risk and len(risk) > 10:  # Only include substantial risk descriptions
                        debug_log(f"Extracted risk: {risk}")
                        # Create a proper dictionary structure for the risk
                        risk_dict = {
                            "problematic_text": "",  # We don't have the exact text in this case
                            "explanation": risk,
                            "legal_reference": "General Australian contract law principles",
                            "severity": "medium"  # Default to medium severity
                        }
                        detailed_risks.append(risk_dict)
                        simple_risks.append(risk)
            
            # If we couldn't parse list items but there's content, use the whole response
            if not detailed_risks and len(response_text) > 10:
                debug_log("Using entire response as a single risk")
                risk_dict = {
                    "problematic_text": "",  # We don't have the exact text in this case
                    "explanation": response_text,
                    "legal_reference": "General Australian contract law principles",
                    "severity": "medium"  # Default to medium severity
                }
                detailed_risks = [risk_dict]
                simple_risks = [response_text]
                
        except Exception as e:
            debug_log(f"Uncaught exception in analyze_risks: {type(e).__name__}: {str(e)}")
            debug_log("Traceback", traceback.format_exc())
            print(f"Error in GPT risk analysis: {str(e)}", file=sys.stderr, flush=True)
            # Return empty lists if API call fails
            return [], []
    except Exception as e:
        debug_log(f"Uncaught exception in analyze_risks: {type(e).__name__}: {str(e)}")
        debug_log("Traceback", traceback.format_exc())
        print(f"Error in GPT risk analysis: {str(e)}", file=sys.stderr, flush=True)
        # Return empty lists if API call fails
        return [], []