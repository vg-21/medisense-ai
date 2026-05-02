import os
import requests
from dotenv import load_dotenv
from preprocess import preprocess_input
from prompts import PROMPT_TEMPLATE

load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def analyze_medical_input(text, input_type):
    # Call preprocess.py to clean the text
    clean_text = preprocess_input(text)
    
    # Build prompt
    prompt = PROMPT_TEMPLATE.format(input_type=input_type, text=clean_text)
    
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.2
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        generated_text = ""
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "")
        else:
            generated_text = str(result)
            
        # Parse response into 3 sections: Key Findings, Summary, Next Steps
        key_findings = "No key findings extracted."
        summary = "No summary extracted."
        next_steps = "No next steps extracted."
        
        # Parsing based on the expected exact format
        if "KEY FINDINGS:" in generated_text or "SUMMARY:" in generated_text:
            # We'll try to split based on headers
            # Fallback handling in case of missing headers
            temp_text = generated_text
            
            if "KEY FINDINGS:" in temp_text:
                parts = temp_text.split("SUMMARY:", 1)
                key_findings = parts[0].replace("KEY FINDINGS:", "").strip()
                if len(parts) > 1:
                    temp_text = "SUMMARY:" + parts[1]
                else:
                    temp_text = ""
            
            if "SUMMARY:" in temp_text:
                parts = temp_text.split("NEXT STEPS:", 1)
                summary = parts[0].replace("SUMMARY:", "").strip()
                if len(parts) > 1:
                    next_steps = parts[1].strip()
            
            # If "NEXT STEPS:" was present but "SUMMARY:" wasn't
            if "NEXT STEPS:" in generated_text and next_steps == "No next steps extracted.":
                parts = generated_text.split("NEXT STEPS:", 1)
                next_steps = parts[1].strip()

        else:
            # If the model fails to format properly, put everything in summary
            summary = generated_text.strip()
            
        # Clean up bullet points if necessary or just return the text
        return key_findings, summary, next_steps
        
    except Exception as e:
        error_msg = f"Error: API Request Failed. Exception: {str(e)}"
        return error_msg, error_msg, error_msg
