from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from prompts import format_prompt
from preprocess import clean_input

MODEL_NAME = "google/flan-t5-base"

# Load tokenizer and model lazily to avoid blocking during import
tokenizer = None
model = None

def init_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        try:
            print(f"Loading {MODEL_NAME}...")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")

def analyze_medical_input(text: str, input_type: str) -> str:
    init_model()
    
    if model is None or tokenizer is None:
        return "1. Key Findings\nModel failed to load.\n\n2. Simplified Summary\nPlease check your setup.\n\n3. Suggested Next Steps\nRestart the application."
        
    cleaned_text = clean_input(text)
    formatted_prompt = format_prompt(cleaned_text, input_type)
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    
    # Generate output
    outputs = model.generate(
        **inputs,
        max_length=300,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
