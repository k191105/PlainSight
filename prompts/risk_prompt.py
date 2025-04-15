RISK_PROMPT = """
Please analyze the following contract clause for potential legal risks from the perspective of an Australian small business. 
Focus on identifying clauses that may be unfair, unusually onerous, or potentially unenforceable under Australian law.

Clause Title: {clause_title}

Clause Text:
```
{clause_text}
```

Analyze this clause for the following types of risks:
1. Unfair contract terms under Australian Consumer Law (especially for standard form contracts)
2. Overly broad indemnities or limitations of liability
3. Unreasonable termination provisions
4. Excessive penalties or fees
5. Imbalanced rights and obligations between parties
6. Potentially unenforceable terms under Australian law
7. Conflicts with ACCC guidelines on unfair contract terms

For each risk you identify:
1. Extract the EXACT problematic text segment (word-for-word from the clause)
2. Explain why this specific text is problematic under Australian law
3. Reference the specific Australian legal principle or regulation it may conflict with

Return your analysis in the following JSON format:
```json
[
  {{
    "problematic_text": "exact text from the clause that is problematic",
    "explanation": "explanation of why this text is problematic",
    "legal_reference": "relevant Australian legal principle or regulation",
    "severity": "high|medium|low"
  }}
]
```

If no risks are identified, return:
```json
[]
```
"""