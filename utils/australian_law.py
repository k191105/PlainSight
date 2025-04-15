"""
Provides Australian-specific legal references and resources for contract analysis.
"""

from typing import Dict, List, Tuple

# Major Australian legislation relevant to contracts
RELEVANT_LEGISLATION = {
    "acl": {
        "name": "Australian Consumer Law",
        "description": "Schedule 2 of the Competition and Consumer Act 2010 (Cth), which provides consumer protections including unfair contract terms provisions.",
        "url": "https://www.legislation.gov.au/Details/C2021C00528",
        "relevant_sections": {
            "23": "Unfair terms of consumer contracts and small business contracts",
            "24": "Meaning of unfair",
            "25": "Examples of unfair terms",
            "54-62": "Consumer guarantees for goods",
            "60-63": "Consumer guarantees for services"
        }
    },
    "corporations_act": {
        "name": "Corporations Act 2001 (Cth)",
        "description": "The primary legislation regulating companies in Australia, including provisions related to contracts entered into by corporations.",
        "url": "https://www.legislation.gov.au/Details/C2021C00516",
        "relevant_sections": {}
    },
    "acnc_act": {
        "name": "Australian Charities and Not-for-profits Commission Act 2012 (Cth)",
        "description": "Legislation governing charities and not-for-profits in Australia.",
        "url": "https://www.legislation.gov.au/Details/C2022C00176",
        "relevant_sections": {}
    }
}

# Major regulatory bodies
REGULATORY_BODIES = {
    "accc": {
        "name": "Australian Competition and Consumer Commission (ACCC)",
        "description": "Promotes competition, fair trading, and regulates national infrastructure services.",
        "url": "https://www.accc.gov.au/",
        "resources": {
            "unfair_terms": "https://www.accc.gov.au/business/business-rights-protections/unfair-contract-terms",
            "small_business": "https://www.accc.gov.au/business/business-rights-protections/business-rights"
        }
    },
    "asic": {
        "name": "Australian Securities and Investments Commission (ASIC)",
        "description": "Australia's corporate, markets, financial services and consumer credit regulator.",
        "url": "https://asic.gov.au/",
        "resources": {}
    },
    "oaic": {
        "name": "Office of the Australian Information Commissioner (OAIC)",
        "description": "The independent national regulator for privacy and freedom of information.",
        "url": "https://www.oaic.gov.au/",
        "resources": {
            "privacy": "https://www.oaic.gov.au/privacy/your-privacy-rights"
        }
    }
}

# Recent landmark legal cases related to contract law in Australia
LANDMARK_CASES = {
    "accc_v_bytescard": {
        "name": "ACCC v Chrisco Hampers Australia Ltd [2015] FCA 1204",
        "description": "The Federal Court found that a 'HeadStart' term in Chrisco's hamper contracts was unfair under the ACL. The term allowed Chrisco to continue taking payments after customers had fully paid for their hampers, unless they opted out.",
        "url": "https://www.judgments.fedcourt.gov.au/judgments/Judgments/fca/single/2015/2015fca1204"
    },
    "paciocco_v_anz": {
        "name": "Paciocco v Australia and New Zealand Banking Group Limited [2016] HCA 28",
        "description": "The High Court held that ANZ Bank's late payment fees were not penalties and were therefore enforceable. This case has implications for how liquidated damages and penalty clauses are interpreted in Australia.",
        "url": "https://www.hcourt.gov.au/cases/paciocco-v-australia-and-new-zealand-banking-group-limited"
    },
    "accc_v_jetstar": {
        "name": "ACCC v Jetstar Airways Pty Ltd [2017] FCA 205",
        "description": "The Federal Court found Jetstar had made false or misleading representations about consumer guarantee rights under the ACL in relation to flight bookings.",
        "url": "https://www.judgments.fedcourt.gov.au/judgments/Judgments/fca/single/2017/2017fca0205"
    }
}

# Common unfair terms in Australian contracts with explanations
UNFAIR_TERMS_EXPLANATIONS = {
    "unilateral_variation": {
        "description": "Terms that allow one party to vary the contract without consent from the other party",
        "example": "The provider may modify any of the terms and conditions of this agreement at any time without prior notice.",
        "explanation": "Under s25(1)(d) of the ACL, terms that permit one party to vary the terms of the contract without the consent of the other party may be considered unfair.",
        "risk_level": "High"
    },
    "entire_agreement": {
        "description": "Terms that attempt to limit one party's right to rely on representations made by the other",
        "example": "This agreement constitutes the entire understanding between the parties and supersedes all prior communications.",
        "explanation": "While entire agreement clauses are common, they cannot exclude liability for misleading or deceptive conduct under the ACL.",
        "risk_level": "Medium"
    },
    "excessive_termination_fees": {
        "description": "Terms that impose excessive fees for ending the contract early",
        "example": "If you cancel this contract before the minimum term, you must pay 100% of the remaining fees.",
        "explanation": "Terms requiring the consumer to pay a disproportionately high amount in compensation if they fail to fulfill their obligations may be unfair under s25(1)(c) of the ACL.",
        "risk_level": "High"
    },
    "broad_indemnities": {
        "description": "Terms requiring one party to indemnify the other in a very broad range of circumstances",
        "example": "The customer shall indemnify the company against any and all claims, losses, and expenses arising from the use of the service, regardless of cause.",
        "explanation": "Overly broad indemnities may be unfair, especially when they require a small business to indemnify a larger business for losses outside their control.",
        "risk_level": "High"
    },
    "unilateral_termination": {
        "description": "Terms that allow one party to terminate the contract at any time without reason",
        "example": "The company may terminate this agreement at any time in its sole discretion.",
        "explanation": "Terms that allow one party to terminate without similar rights for the other party may be unfair under s25(1)(a) of the ACL.",
        "risk_level": "Medium"
    },
    "liability_limitation": {
        "description": "Terms that limit or exclude liability for breach of contract or negligence",
        "example": "The company shall not be liable for any loss or damage whatsoever arising from the use of the service.",
        "explanation": "Broad liability exclusions may be unfair, especially when they attempt to exclude non-excludable consumer guarantees under the ACL.",
        "risk_level": "High"
    },
    "automatic_renewal": {
        "description": "Terms that automatically renew contracts without adequate notice",
        "example": "This agreement will automatically renew for another 12 months unless cancelled 30 days before the renewal date.",
        "explanation": "Automatic renewal clauses with inadequate notice or difficult cancellation processes may be considered unfair, particularly for small businesses.",
        "risk_level": "Medium"
    }
}

# Special considerations for specific contract types
CONTRACT_TYPE_GUIDANCE = {
    "lease": {
        "name": "Commercial Lease Agreements",
        "key_legislation": "Retail Leases Act (varies by state/territory)",
        "special_considerations": [
            "Most states have specific retail lease legislation that may override certain contract terms",
            "Disclosure statements are typically required before signing retail leases",
            "Some jurisdictions have minimum lease terms and specific requirements for rent reviews"
        ],
        "resources": "https://business.gov.au/planning/leasing-buying-or-building-property/leasing-business-premises"
    },
    "employment": {
        "name": "Employment Contracts",
        "key_legislation": "Fair Work Act 2009 (Cth)",
        "special_considerations": [
            "Must comply with National Employment Standards (NES)",
            "Cannot contract below minimum wage or conditions in applicable awards",
            "Restraint of trade clauses must be reasonable to be enforceable"
        ],
        "resources": "https://www.fairwork.gov.au/employment-conditions/contracts"
    },
    "services": {
        "name": "Service Agreements",
        "key_legislation": "Australian Consumer Law",
        "special_considerations": [
            "Consumer guarantees apply regardless of what the contract says",
            "Services must be provided with due care and skill",
            "Services must be fit for purpose and delivered within a reasonable time"
        ],
        "resources": "https://www.accc.gov.au/consumers/consumer-rights-guarantees/consumer-guarantees"
    },
    "nda": {
        "name": "Non-Disclosure Agreements",
        "key_legislation": "Common law of contract, Corporations Act 2001 (Cth)",
        "special_considerations": [
            "Overly broad or long confidentiality periods may be unenforceable",
            "Should clearly define what constitutes confidential information",
            "Should include reasonable exceptions (e.g., publicly available information)"
        ],
        "resources": "https://business.gov.au/planning/protecting-your-ideas/non-disclosure-agreements"
    }
}

def get_legislation_details(legislation_key: str) -> Dict:
    """Get details about specific Australian legislation"""
    return RELEVANT_LEGISLATION.get(legislation_key, {})

def get_regulatory_body_info(body_key: str) -> Dict:
    """Get information about a specific Australian regulatory body"""
    return REGULATORY_BODIES.get(body_key, {})

def get_unfair_term_explanation(term_type: str) -> Dict:
    """Get explanation and examples for a specific type of unfair term"""
    return UNFAIR_TERMS_EXPLANATIONS.get(term_type, {})

def get_contract_type_guidance(contract_type: str) -> Dict:
    """Get specific guidance for a type of contract"""
    return CONTRACT_TYPE_GUIDANCE.get(contract_type, {})

def get_relevant_case(case_key: str) -> Dict:
    """Get information about a specific landmark case"""
    return LANDMARK_CASES.get(case_key, {})

def get_acl_section_description(section_number: str) -> str:
    """Get description of a specific section of the Australian Consumer Law"""
    acl = RELEVANT_LEGISLATION.get("acl", {})
    sections = acl.get("relevant_sections", {})
    return sections.get(section_number, "Section description not available")