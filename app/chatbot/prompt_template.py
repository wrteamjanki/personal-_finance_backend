def build_prompt(user_input: str) -> str:
    return f"""
You are a smart finance assistant.

Extract data from this input:
"{user_input}"

Return ONLY a valid JSON object in this exact format:

{{
  "type": "expense" or "income",
  "amount": number (no currency symbol),
  "category": "string",
  "date": "YYYY-MM-DD" (default to today if not given),
  "note": "string"
}}

DO NOT return any other text, explanation, or commentary.
"""
