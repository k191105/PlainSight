SUMMARY_PROMPT = """
Please provide a plain English summary of the following contract clause.
The summary should be easy to understand for a small business owner without legal training.

Clause Title: {clause_title}

Clause Text:
```
{clause_text}
```

Guidelines for your summary:
1. Use simple, everyday language (avoid legal jargon)
2. Keep it concise (3-5 sentences is ideal)
3. Highlight the key obligations, rights, or requirements
4. Explain what this means in practical terms for an Australian small business
5. Use an active voice and direct language ("You must..." rather than "The party shall be obligated to...")

Your summary should help a small business owner understand:
- What this clause requires them to do
- What rights this clause gives them
- Any important deadlines or conditions
- Any potential financial implications
"""