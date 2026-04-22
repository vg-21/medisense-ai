import os
import requests
from dotenv import load_dotenv
from prompts import format_prompt
from preprocess import clean_input

load_dotenv()

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_TOKEN = os.getenv("HF_TOKEN")

def analyze_medical_input(text: str, input_type: str) -> str:
    if not HF_TOKEN or HF_TOKEN == "your_huggingface_token_here":
        return "1. Key Findings\nHugging Face Token missing.\n\n2. Simplified Summary\nPlease add HF_TOKEN to your .env file or Render dashboard.\n\n3. Suggested Next Steps\nUpdate credentials and try again."
        
    cleaned_text = clean_input(text)
    formatted_prompt = format_prompt(cleaned_text, input_type)
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_length": 300,
            "num_beams": 4,
            "early_stopping": True,
            "no_repeat_ngram_size": 2
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            return f"1. Key Findings\nUnexpected API response.\n\n2. Simplified Summary\n{str(result)}\n\n3. Suggested Next Steps\nCheck API status."
            
    except Exception as e:
        return f"1. Key Findings\nAPI request failed.\n\n2. Simplified Summary\n{str(e)}\n\n3. Suggested Next Steps\nCheck your network connection and token."
