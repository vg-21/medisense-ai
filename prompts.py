MEDICAL_PROMPT_TEMPLATE = """You are a helpful medical assistant. A patient has shared their {input_type}. Analyze it and respond with:
1. Key Findings
2. Simplified Summary
3. Suggested Next Steps

Patient input: {text}"""

def format_prompt(text: str, input_type: str) -> str:
    return MEDICAL_PROMPT_TEMPLATE.format(text=text, input_type=input_type)
