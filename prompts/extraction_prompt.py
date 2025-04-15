EXTRACTION_PROMPT = """
Your task is to extract all identifiable clauses from the contract document provided below. 
Please analyze the document and identify distinct clauses or sections.

For each clause:
1. Identify the clause title or number
2. Extract the full text of that clause
3. Maintain the exact order as they appear in the original document

Contract Document:
```
{document_text}
```

Return your response in the following JSON format with each clause title as a key and the clause text as its value:

```json
{{
  "Clause Title 1": "Full text of clause 1...",
  "Clause Title 2": "Full text of clause 2...",
  ...
}}
```

Important instructions:
- Preserve the exact clause titles as they appear in the document
- Include the complete text of each clause
- Maintain the exact order of clauses as they appear in the original document
- If clause titles are not present, use numbered sections like "Section 1", "Section 2", etc.
- Focus on contractual clauses, not introductory text or signatures
- If a clause has subclauses, include them as part of the main clause text
- Ensure the clause numbering/ordering matches the original document exactly
- If there are any special characters or symbols in clause titles, preserve them exactly
"""