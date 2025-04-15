"""
Risk analysis module specifically for Australian contract law.
This provides rule-based analysis to supplement the LLM analysis.
"""

from typing import Dict, List, Tuple, Set
import re

# Key terms and phrases that often indicate unfair terms under Australian Consumer Law
UNFAIR_TERM_INDICATORS = {
    "termination": [
        "terminate without notice",
        "terminate immediately",
        "terminate at any time",
        "sole discretion to terminate",
        "unilateral right to terminate"
    ],
    "liability": [
        "no liability whatsoever",
        "no liability under any circumstances",
        "excludes all liability",
        "not liable for any loss",
        "not be liable for any damage",
        "disclaims all warranties"
    ],
    "amendment": [
        "modify terms at any time",
        "change the terms without notice",
        "reserve the right to amend",
        "unilaterally vary the agreement", 
        "sole discretion to change"
    ],
    "penalty": [
        "liquidated damages",
        "penalty fee",
        "late payment fee",
        "cancellation fee",
        "early termination fee"
    ],
    "indemnity": [
        "indemnify and hold harmless",
        "fully indemnify",
        "unlimited indemnity",
        "indemnify against all claims",
        "broad indemnification"
    ]
}

# Australian-specific legal references for common clause issues
AUSTRALIAN_LAW_REFERENCES = {
    "unfair_terms": "Under the Australian Consumer Law (Competition and Consumer Act 2010), a term is unfair if it causes a significant imbalance in the parties' rights, is not reasonably necessary to protect legitimate interests, and would cause detriment if relied upon.",
    "consumer_guarantees": "The Australian Consumer Law provides automatic guarantees for goods and services, and these cannot be excluded, restricted or modified by contract terms.",
    "misleading_conduct": "Section 18 of the Australian Consumer Law prohibits misleading or deceptive conduct in trade or commerce.",
    "penalty_clauses": "Australian contract law generally does not enforce 'penalty' clauses that impose punitive damages rather than a genuine pre-estimate of loss.",
    "implied_terms": "Certain terms are implied into contracts under Australian law, including reasonable care and skill, fitness for purpose, and reasonable time for performance.",
    "small_business_protections": "Since November 2016, the unfair contract terms protections extend to small business contracts (businesses with fewer than 20 employees) where the upfront price is under $300,000 (or $1 million for contracts longer than 12 months)."
}

# ACCC guidelines on unfair contract terms
ACCC_UNFAIR_TERMS_GUIDANCE = {
    "one_sided_terms": "Terms that allow one party (but not the other) to avoid or limit their obligations",
    "termination_terms": "Terms that allow one party (but not the other) to terminate the contract",
    "penalty_terms": "Terms that penalize one party (but not the other) for breaching or terminating the contract",
    "variation_terms": "Terms that allow one party to vary the terms of the contract without the other party's consent",
    "liability_terms": "Terms that limit one party's right to sue the other party",
    "assignment_terms": "Terms that allow one party to assign the contract without the other party's consent",
    "entire_agreement_terms": "Terms that limit one party's right to rely on statements made by the other party",
    "early_termination_terms": "Terms that impose excessive early termination charges"
}

def analyze_clause_risks(clause_title: str, clause_text: str) -> List[str]:
    """
    Rule-based risk analysis for contract clauses based on Australian law
    
    Args:
        clause_title: Title or identifier of the clause
        clause_text: Full text of the clause
        
    Returns:
        List of potential risk statements with Australian legal context
    """
    risks = []
    clause_text_lower = clause_text.lower()
    clause_title_lower = clause_title.lower()
    
    # Check for unfair term indicators
    for category, phrases in UNFAIR_TERM_INDICATORS.items():
        for phrase in phrases:
            if phrase.lower() in clause_text_lower:
                if category == "termination":
                    risks.append(f"This clause contains potentially unfair termination language ('{phrase}'). Under Australian Consumer Law, termination rights should be balanced between parties.")
                elif category == "liability":
                    risks.append(f"This clause contains broad liability exclusions ('{phrase}'). The Australian Consumer Law limits how much a business can exclude liability, especially for negligence or statutory guarantees.")
                elif category == "amendment":
                    risks.append(f"This clause allows unilateral changes to terms ('{phrase}'). The ACCC guidelines highlight this as potentially unfair under Australian Consumer Law.")
                elif category == "penalty":
                    risks.append(f"This clause includes what may be considered penalty provisions ('{phrase}'). Australian courts generally won't enforce penalty clauses that aren't a genuine pre-estimate of loss.")
                elif category == "indemnity":
                    risks.append(f"This clause contains broad indemnity language ('{phrase}'). Overly broad indemnities may be considered unfair for small businesses under Australian Consumer Law.")
    
    # Check for specific clause types
    if "govern" in clause_title_lower and "law" in clause_title_lower:
        if "arbitration" in clause_text_lower and ("international" in clause_text_lower or "foreign" in clause_text_lower):
            risks.append("This governing law clause specifies international arbitration, which may make dispute resolution more complex and expensive for Australian small businesses.")
    
    if "termination" in clause_title_lower:
        # Check for imbalanced notice periods
        notice_periods = extract_notice_periods(clause_text)
        if len(notice_periods) >= 2 and max(notice_periods) / min(notice_periods) > 2:
            risks.append(f"This termination clause has significantly different notice periods ({min(notice_periods)} days vs {max(notice_periods)} days). The ACCC may consider such imbalanced notice periods unfair.")
    
    if "payment" in clause_title_lower or "fee" in clause_title_lower:
        # Check for excessive late fees
        late_fees = extract_percentage_fees(clause_text)
        if any(fee > 10 for fee in late_fees):
            risks.append(f"This clause includes a late payment fee of {max(late_fees)}%, which may be considered excessive under Australian case law. Courts typically view late fees above 10% as potential penalties rather than genuine pre-estimates of loss.")
    
    if "limitation of liability" in clause_title_lower or "liability" in clause_title_lower:
        if "consequential" in clause_text_lower and "loss" in clause_text_lower:
            risks.append("This limitation of liability clause excludes consequential losses, which may conflict with Australian Consumer Law guarantees for certain types of contracts.")
    
    # Check for automatic renewal clauses
    if "renew" in clause_text_lower and "automatic" in clause_text_lower:
        risks.append("This clause contains an automatic renewal provision. The ACCC has flagged automatic renewals without adequate notice as potentially unfair contract terms for small businesses.")
    
    # Check for entire agreement clauses
    if "entire agreement" in clause_text_lower or "whole agreement" in clause_text_lower:
        risks.append("This 'entire agreement' clause may attempt to exclude liability for pre-contractual representations. Under Australian law, businesses cannot contract out of liability for misleading or deceptive conduct.")
    
    return risks

def extract_notice_periods(text: str) -> List[int]:
    """Extract notice periods (in days) from text"""
    notice_periods = []
    
    # Look for patterns like "X days notice" or "notice of X days"
    patterns = [
        r'(\d+)\s*(?:calendar|business)?\s*days[\'\s]*notice',
        r'notice\s*(?:period|)\s*(?:of|)\s*(\d+)\s*(?:calendar|business)?\s*days',
        r'(\d+)\s*(?:calendar|business)?\s*days[\'\s]*(?:written|advance|prior)\s*notice',
        r'(\d+)\s*(?:calendar|business)?\s*days[\'\s]*(?:before|prior)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                days = int(match)
                notice_periods.append(days)
            except (ValueError, TypeError):
                continue
    
    return notice_periods

def extract_percentage_fees(text: str) -> List[float]:
    """Extract percentage fees from text"""
    percentage_fees = []
    
    # Look for patterns like "X% fee" or "fee of X%"
    patterns = [
        r'(\d+(?:\.\d+)?)\s*%\s*(?:fee|charge|penalty|interest)',
        r'(?:fee|charge|penalty|interest)\s*(?:of|is|at)\s*(\d+(?:\.\d+)?)\s*%'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                percentage = float(match)
                percentage_fees.append(percentage)
            except (ValueError, TypeError):
                continue
    
    return percentage_fees

def get_australian_law_reference(risk_category: str) -> str:
    """Get relevant Australian legal references for a risk category"""
    return AUSTRALIAN_LAW_REFERENCES.get(risk_category, "")

def get_relevant_accc_guidance(term_type: str) -> str:
    """Get relevant ACCC guidance for a type of unfair term"""
    return ACCC_UNFAIR_TERMS_GUIDANCE.get(term_type, "")