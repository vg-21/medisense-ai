import gradio as gr
from model import analyze_medical_input
import html
import datetime
import re
import textwrap
from database import save_chat_analysis, get_chat_history

# CSS for the exact design match
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body, .gradio-container {
    background-color: #FAFAFA !important; 
    font-family: 'Inter', sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
}

.landing-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background: linear-gradient(180deg, #FFFFFF 0%, #F3F4F6 100%);
}

.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 48px;
    background-color: transparent;
}

.logo {
    font-size: 20px;
    font-weight: 700;
    color: #0D9488;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-links {
    display: flex;
    gap: 32px;
    font-size: 14px;
    font-weight: 500;
    color: #6B7280;
}

.nav-links span {
    cursor: pointer;
    transition: color 0.2s;
}

.nav-links span:hover {
    color: #374151;
}

.nav-links span.active {
    color: #0D9488;
    border-bottom: 2px solid #0D9488;
    padding-bottom: 4px;
}

.btn-secondary {
    background-color: #0D9488;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 500;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.btn-secondary:hover {
    background-color: #0F766E;
}

.hero-section {
    text-align: center;
    padding: 100px 20px 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.pill {
    background-color: #E0F2FE;
    color: #0D9488;
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 32px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-transform: uppercase;
}

.tagline {
    font-size: 56px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 24px;
    margin-top: 0;
    letter-spacing: -1px;
}

.sub-tagline {
    font-size: 20px;
    color: #4B5563;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.6;
    font-weight: 400;
}

#start-btn {
    background: #0D9488 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 14px 36px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25) !important;
    transition: all 0.2s ease !important;
    width: fit-content !important;
    margin: 0 auto 80px auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

#start-btn:hover {
    background: #0F766E !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(13, 148, 136, 0.3) !important;
}

.footer {
    text-align: center;
    padding: 40px 20px;
    color: #9CA3AF;
    font-size: 12px;
    background-color: transparent;
    margin-top: auto;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-bottom: 16px;
    color: #6B7280;
    font-weight: 500;
}

.footer-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 24px;
}

footer.svelte-1rjryqp {
    display: none !important;
}

/* Screen 2 CSS */
.input-main-section {
    padding: 40px 10%;
    flex-grow: 1;
}

.input-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid #F3F4F6;
    padding: 0 !important;
    overflow: hidden;
    margin-bottom: 32px;
    display: flex;
}

.left-col {
    padding: 40px !important;
    background: #FFFFFF !important;
    border-right: 1px solid #F3F4F6 !important;
    display: flex !important;
    flex-direction: column !important;
}

.right-col {
    padding: 40px !important;
    background: #FFFFFF !important;
    display: flex !important;
    flex-direction: column !important;
}

.pro-tip {
    background: #ECFDF5;
    border-radius: 8px;
    padding: 16px;
    margin-top: auto;
}

.main-textarea textarea {
    border-radius: 8px !important;
    border: 1px solid #E5E7EB !important;
    background: #FFFFFF !important;
    padding: 16px !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
    color: #111827 !important;
    box-shadow: none !important;
    resize: none !important;
}

.main-textarea textarea:focus {
    border-color: #0D9488 !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.2) !important;
}

.analyze-btn {
    background: #0F766E !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 16px 24px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border: none !important;
    width: 100% !important;
    margin-top: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(13, 148, 136, 0.2) !important;
}

.analyze-btn:hover {
    background: #0D9488 !important;
}

.info-cards {
    display: flex;
    justify-content: space-between;
    gap: 24px;
}

.info-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border: 1px solid #F3F4F6;
}

.info-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #EEF2FF;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4F46E5;
}

.info-title {
    font-size: 11px;
    font-weight: 700;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.info-value {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
}

.pill-radio {
    margin-top: 16px;
    background: transparent;
    display: flex;
    width: fit-content;
}

/* Screen 3 Loading CSS */
.loading-main-section {
    padding: 40px 10%;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.wave-bar {
    width: 6px;
    background: #5EEAD4;
    border-radius: 9999px;
    animation: wave 1.2s infinite ease-in-out;
}

@keyframes wave {
    0%, 100% { transform: scaleY(0.4); background: #99F6E4; }
    50% { transform: scaleY(1); background: #0D9488; }
}

.progress-fill {
    animation: indeterminate-progress 2s infinite ease-in-out;
}

@keyframes indeterminate-progress {
    0% { left: -50%; width: 50%; }
    100% { left: 100%; width: 50%; }
}

/* Screen 4 Results CSS */
.results-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid #E5E7EB;
    padding: 24px;
    margin-bottom: 24px;
}

.results-card-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 18px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 20px;
}

.results-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #F0FDF4;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #047857;
    font-size: 16px;
}

.bullet-item {
    display: flex;
    gap: 12px;
    margin-bottom: 12px;
    padding: 16px;
    border-radius: 8px;
    background: #F9FAFB;
}

.bullet-item.warning {
    background: #FEF2F2;
    color: #991B1B;
}

.bullet-item.success {
    background: #F0FDF4;
    color: #065F46;
}

.step-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    position: relative;
    padding-bottom: 24px;
}

.step-item:last-child {
    padding-bottom: 0;
}

.step-line {
    position: absolute;
    left: 4px;
    top: 16px;
    bottom: -8px;
    width: 2px;
    background: #E5E7EB;
}

.step-item:last-child .step-line {
    display: none;
}

.step-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #8B5CF6;
    margin-top: 6px;
    z-index: 1;
}

#results-btn-row {
    margin-top: 24px;
    display: flex;
    gap: 16px;
    align-items: center;
}

#followup-btn {
    background: transparent !important;
    color: #0D9488 !important;
    border: 1px solid #0D9488 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    flex: 1 !important;
}

#followup-btn:hover {
    background: #F0FDF4 !important;
}

#start-over-btn {
    background: #0D9488 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 6px -1px rgba(13, 148, 136, 0.2) !important;
    flex: 1 !important;
}

#start-over-btn:hover {
    background: #0F766E !important;
}

.disclaimer-banner {
    background: #F3F4F6;
    border-radius: 8px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #6B7280;
    font-size: 13px;
    margin-top: 40px;
    justify-content: center;
}
"""

def start_loading(text):
    if not text:
        text = "No documentation submitted."
    
    truncated_text = html.escape(text)
    if len(truncated_text) > 300:
        truncated_text = truncated_text[:300] + "..."
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M GMT")
    
    html_content = f"""
    <div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 12px; padding: 24px; text-align: left; width: 100%; max-width: 800px; margin: 40px auto; box-sizing: border-box;">
        <div style="font-size: 11px; font-weight: 700; color: #6B7280; letter-spacing: 0.5px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2ZM18 20H6V4H13V9H18V20Z"/></svg>
            SUBMITTED DOCUMENTATION
        </div>
        <div style="color: #9CA3AF; font-size: 15px; line-height: 1.6; margin-bottom: 24px; background: transparent; pointer-events: none;">
            {truncated_text}
        </div>
        <div style="display: flex; justify-content: space-between; border-top: 1px solid #E5E7EB; padding-top: 16px; font-size: 12px;">
            <div>
                <div style="color: #9CA3AF; margin-bottom: 4px; font-weight: 600; font-size: 10px; letter-spacing: 0.5px;">METADATA</div>
                <div style="color: #6B7280; font-weight: 500;">ID: MS-88291-TX</div>
            </div>
            <div>
                <div style="color: #9CA3AF; margin-bottom: 4px; font-weight: 600; font-size: 10px; letter-spacing: 0.5px;">TIMESTAMP</div>
                <div style="color: #6B7280; font-weight: 500;">{timestamp}</div>
            </div>
        </div>
    </div>
    """
    
    return [gr.update(visible=False), gr.update(visible=True), gr.update(value=html_content)]

def finish_analysis(text, input_type):
    if not text:
        return [gr.update(visible=False), gr.update(visible=False), gr.update(), gr.update(), gr.update()]

    response = analyze_medical_input(text, input_type)
    
    sections = {
        "Key Findings": "",
        "Simplified Summary": "",
        "Suggested Next Steps": ""
    }
    
    findings_match = re.search(r'(?:1\.\s*)?Key Findings\s*[:\n]+(.*?)(?:(?:2\.\s*)?Simplified Summary|$)', response, re.IGNORECASE | re.DOTALL)
    summary_match = re.search(r'(?:2\.\s*)?Simplified Summary\s*[:\n]+(.*?)(?:(?:3\.\s*)?Suggested Next Steps|$)', response, re.IGNORECASE | re.DOTALL)
    steps_match = re.search(r'(?:3\.\s*)?Suggested Next Steps\s*[:\n]+(.*)$', response, re.IGNORECASE | re.DOTALL)
    
    if findings_match:
        sections["Key Findings"] = findings_match.group(1).strip()
    if summary_match:
        sections["Simplified Summary"] = summary_match.group(1).strip()
    if steps_match:
        sections["Suggested Next Steps"] = steps_match.group(1).strip()
        
    if not any(sections.values()):
        sections["Simplified Summary"] = response
        
    # Save to Supabase
    save_chat_analysis(
        input_type=input_type,
        user_input=text,
        key_findings=sections["Key Findings"],
        summary=sections["Simplified Summary"],
        next_steps=sections["Suggested Next Steps"]
    )

    # Render Key Findings
    findings_html = ""
    if sections["Key Findings"]:
        points = [p.strip() for p in sections["Key Findings"].split('\\n') if p.strip()]
        for p in points:
            p = re.sub(r'^[\-\*•\d\.]+\s*', '', p)
            findings_html += f"""
            <div class="bullet-item success">
                <div style="margin-top: 2px;">✅</div>
                <div style="font-size: 14px; line-height: 1.5;">{p}</div>
            </div>
            """
    else:
        findings_html = "<div style='color: #6B7280; font-size: 14px;'>No key findings identified.</div>"

    # Render Summary
    summary_text = sections["Simplified Summary"].replace('\\n', '<br>')
    summary_html = f"<div style='font-size: 14px; line-height: 1.6; color: #4B5563;'>{summary_text}</div>"
    
    # Render Steps
    steps_html = ""
    if sections["Suggested Next Steps"]:
        points = [p.strip() for p in sections["Suggested Next Steps"].split('\\n') if p.strip()]
        for p in points:
            p = re.sub(r'^[\-\*•\d\.]+\s*', '', p)
            steps_html += f"""
            <div class="step-item">
                <div class="step-line"></div>
                <div class="step-dot"></div>
                <div style="font-size: 14px; line-height: 1.5; color: #374151;">{p}</div>
            </div>
            """
    else:
        steps_html = "<div style='color: #6B7280; font-size: 14px;'>No next steps suggested.</div>"
        
    right_col_html = f"""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 32px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Analysis Results</h1>
        <p style="color: #4B5563; font-size: 15px; margin: 0;">AI-generated interpretation of clinical data and reported symptoms.</p>
    </div>
    
    <div class="results-card">
        <div class="results-card-title">
            <div class="results-icon">📊</div>
            Key Findings
        </div>
        {findings_html}
    </div>
    
    <div class="results-card">
        <div class="results-card-title">
            <div class="results-icon">📄</div>
            Simplified Summary
        </div>
        {summary_html}
    </div>
    
    <div class="results-card">
        <div class="results-card-title">
            <div class="results-icon">📋</div>
            Suggested Next Steps
        </div>
        <div style="padding-left: 8px;">
            {steps_html}
        </div>
    </div>
    """
    
    truncated_text = html.escape(text)
    date_str = datetime.datetime.now().strftime("%b %d, %Y")
    
    left_col_html = f"""
    <div style="background: #F9FAFB; border-radius: 12px; padding: 24px; border: 1px solid #E5E7EB; margin-top: 50px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div style="font-size: 11px; font-weight: 600; color: #6B7280; letter-spacing: 0.5px;">ORIGINAL INQUIRY</div>
            <div style="background: #D1FAE5; color: #065F46; font-size: 10px; font-weight: 600; padding: 4px 8px; border-radius: 9999px; text-transform: uppercase;">{input_type}</div>
        </div>
        <div style="font-size: 14px; line-height: 1.6; color: #4B5563; font-style: italic; border-left: 2px solid #D1D5DB; padding-left: 12px; margin-bottom: 24px;">
            "{truncated_text}"
        </div>
        <div style="border-top: 1px solid #E5E7EB; padding-top: 16px; display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #4B5563;">
                <span style="color: #0D9488;">📅</span> Analyzed: {date_str}
            </div>
            <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #4B5563;">
                <span style="color: #0D9488;">✔️</span> HIPAA Secured Processing
            </div>
        </div>
    </div>
    """

    # Fetch History
    history = get_chat_history(3)
    history_html = ""
    if not history:
        history_html = "<div style='color: #6B7280; font-size: 13px; text-align: center; padding: 20px;'>No past consultations found.</div>"
    else:
        for item in history:
            short_input = textwrap.shorten(item.get("user_input", ""), width=60, placeholder="...")
            raw_date = item.get("created_at", "")
            if "T" in raw_date:
                date_part = raw_date.split("T")[0]
                time_part = raw_date.split("T")[1][:5]
                hist_date_str = f"{date_part} • {time_part} UTC"
            else:
                hist_date_str = "Unknown Date"
                
            history_html += f"""
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="background: #E0F2FE; color: #0284C7; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 9999px; text-transform: uppercase;">
                        {item.get('input_type', 'Unknown')}
                    </div>
                    <div style="color: #9CA3AF; font-size: 11px;">{hist_date_str}</div>
                </div>
                <div style="font-size: 13px; color: #374151; font-weight: 500; margin-bottom: 8px; font-style: italic;">
                    "{short_input}"
                </div>
                <div style="font-size: 12px; color: #6B7280; line-height: 1.5; border-left: 2px solid #D1D5DB; padding-left: 8px;">
                    {textwrap.shorten(item.get("summary", ""), width=80, placeholder="...")}
                </div>
            </div>
            """
    
    return [
        gr.update(visible=False), 
        gr.update(visible=True), 
        gr.update(value=left_col_html), 
        gr.update(value=right_col_html),
        gr.update(value=history_html)
    ]

with gr.Blocks(css=custom_css, title="MediSense AI") as demo:
    # --- SCREEN 1: LANDING ---
    with gr.Column(visible=True, elem_classes="landing-container") as landing_screen:
        gr.HTML('''
        <div class="header-bar">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="4" width="20" height="16" rx="2" stroke="#0D9488" stroke-width="2"/>
                    <path d="M8 12H16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                    <path d="M12 8V16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                </svg>
                MediSense AI
            </div>
            <div class="nav-links">
                <span class="active">Solutions</span>
                <span>Technology</span>
                <span>Research</span>
                <span>Compliance</span>
            </div>
            <div>
                <button class="btn-secondary">Get Started</button>
            </div>
        </div>
        
        <div class="hero-section">
            <div class="pill">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="#0D9488"/>
                </svg>
                NEXT GENERATION MEDICAL ANALYSIS
            </div>
            <h1 class="tagline">Understand your health, clearly.</h1>
            <p class="sub-tagline">AI-powered medical insights from your symptoms and reports.<br>Experience a new era of personal health management.</p>
        </div>
        ''')
        
        start_button = gr.Button("Start Consultation →", elem_id="start-btn")
            
        gr.HTML('''
        <div class="footer">
            <div class="footer-logo">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="4" width="20" height="16" rx="2" stroke="#0D9488" stroke-width="2"/>
                    <path d="M8 12H16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                    <path d="M12 8V16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                </svg>
                MediSense AI
            </div>
            <div class="footer-links" style="justify-content: center;">
                <span>Privacy Policy</span>
                <span>Terms of Service</span>
                <span>HIPAA Compliance</span>
                <span>Contact</span>
            </div>
            <p>© 2024 MediSense AI. For informational purposes only. Not a substitute for professional medical advice.</p>
        </div>
        ''')

    # --- SCREEN 2: INPUT ---
    with gr.Column(visible=False, elem_classes="landing-container") as input_screen:
        gr.HTML('''
        <div class="header-bar" style="background: white; border-bottom: 1px solid #F3F4F6;">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="4" width="20" height="16" rx="2" stroke="#0D9488" stroke-width="2"/>
                    <path d="M8 12H16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                    <path d="M12 8V16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                </svg>
                MediSense AI
            </div>
            <div class="nav-links">
                <span class="active">Solutions</span>
                <span>Technology</span>
                <span>Research</span>
                <span>Compliance</span>
            </div>
            <div>
                <button class="btn-secondary">Get Started</button>
            </div>
        </div>
        ''')

        with gr.Column(elem_classes="input-main-section"):
            gr.HTML('''
                <div style="margin-bottom: 24px;">
                    <div style="color: #0D9488; font-size: 13px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">Diagnostic Engine</div>
                    <h1 style="font-size: 32px; font-weight: 700; color: #111827; margin: 0;">Analyze Patient Records</h1>
                </div>
            ''')
            
            with gr.Row(elem_classes="input-card"):
                with gr.Column(scale=1, elem_classes="left-col", min_width=300):
                    gr.HTML('''
                        <h2 style="font-size: 20px; font-weight: 600; color: #111827; margin-top: 0; margin-bottom: 12px;">Inquiry Details</h2>
                        <p style="color: #4B5563; font-size: 14px; line-height: 1.6; margin-bottom: 16px;">Provide specific clinical details or upload a digital health record. Our AI cross-references input against the latest medical research to provide diagnostic probabilities.</p>
                    ''')
                    
                    input_type = gr.Radio(
                        choices=["Symptoms", "Medical Report"],
                        value="Symptoms",
                        show_label=False,
                        elem_classes="pill-radio"
                    )
                    
                    gr.HTML('''
                        <div class="pro-tip">
                            <div style="display: flex; align-items: center; gap: 8px; color: #065F46; font-weight: 600; font-size: 13px; margin-bottom: 6px;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 2C8.13 2 5 5.13 5 9C5 11.38 6.19 13.47 8 14.74V17C8 17.55 8.45 18 9 18H15C15.55 18 16 17.55 16 17V14.74C17.81 13.47 19 11.38 19 9C19 5.13 15.87 2 12 2ZM14 15H10V13.88C9.56 13.63 9.15 13.33 8.78 12.98C7.68 11.96 7 10.54 7 9C7 6.24 9.24 4 12 4C14.76 4 17 6.24 17 9C17 10.54 16.32 11.96 15.22 12.98C14.85 13.33 14.44 13.63 14 13.88V15ZM13 19H11V20C11 20.55 11.45 21 12 21C12.55 21 13 20.55 13 20V19Z"/>
                                </svg>
                                PRO TIP
                            </div>
                            <p style="color: #374151; font-size: 13px; margin: 0; line-height: 1.5;">Include duration, severity, and any known patient history for higher diagnostic accuracy.</p>
                        </div>
                    ''')
                
                with gr.Column(scale=2, elem_classes="right-col", min_width=500):
                    user_input = gr.Textbox(
                        lines=10,
                        placeholder="Type or paste patient symptoms, clinical observations, or laboratory findings here...",
                        show_label=False,
                        elem_classes="main-textarea"
                    )
                    gr.Markdown("<p style='color: #6B7280; font-size: 13px; margin-top: -16px; margin-bottom: 24px;'>You can paste lab results, doctor notes, or describe how you feel</p>")
                    
                    analyze_btn = gr.Button("📊 Analyze Findings", elem_classes="analyze-btn")

            # Bottom info cards
            gr.HTML('''
                <div class="info-cards">
                    <div class="info-card">
                        <div class="info-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="#6366F1" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1ZM12 11.99H19C18.47 16.11 15.72 19.78 12 20.92V12H5V6.3L12 3.19V11.99Z" fill="currentColor"/>
                            </svg>
                        </div>
                        <div>
                            <div class="info-title">PRIVACY</div>
                            <div class="info-value">256-bit Encryption</div>
                        </div>
                    </div>
                    <div class="info-card">
                        <div class="info-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="#6366F1" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" fill="currentColor"/>
                            </svg>
                        </div>
                        <div>
                            <div class="info-title">COMPLIANCE</div>
                            <div class="info-value">HIPAA Certified</div>
                        </div>
                    </div>
                    <div class="info-card">
                        <div class="info-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="#6366F1" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11.99 2C6.47 2 2 6.48 2 12C2 17.52 6.47 22 11.99 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4C16.42 4 20 7.58 20 12C20 16.42 16.42 20 12 20ZM12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                            </svg>
                        </div>
                        <div>
                            <div class="info-title">PROCESSING</div>
                            <div class="info-value">Real-time Analysis</div>
                        </div>
                    </div>
                </div>
            ''')
            
        gr.HTML('''
        <div class="footer">
            <div class="footer-links" style="justify-content: center;">
                <span>Privacy Policy</span>
                <span>Terms of Service</span>
                <span>HIPAA Compliance</span>
                <span>Contact</span>
            </div>
            <p>© 2024 MediSense AI. For informational purposes only. Not a substitute for professional medical advice.</p>
        </div>
        ''')

    # --- SCREEN 3: LOADING ---
    with gr.Column(visible=False, elem_classes="landing-container") as loading_screen:
        gr.HTML('''
        <div class="header-bar" style="background: transparent;">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="4" width="20" height="16" rx="2" stroke="#0D9488" stroke-width="2"/>
                    <path d="M8 12H16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                    <path d="M12 8V16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                </svg>
                MediSense AI
            </div>
        </div>
        ''')

        with gr.Column(elem_classes="loading-main-section"):
            gr.HTML('''
                <div style="text-align: center; width: 100%; max-width: 800px; margin: 0 auto; padding-top: 60px;">
                    <div style="display: flex; justify-content: center; align-items: center; gap: 6px; height: 64px; margin-bottom: 32px;">
                        <div class="wave-bar" style="height: 40%; animation-delay: 0.0s;"></div>
                        <div class="wave-bar" style="height: 60%; animation-delay: 0.1s;"></div>
                        <div class="wave-bar" style="height: 100%; animation-delay: 0.2s;"></div>
                        <div class="wave-bar" style="height: 80%; animation-delay: 0.3s;"></div>
                        <div class="wave-bar" style="height: 100%; animation-delay: 0.4s;"></div>
                        <div class="wave-bar" style="height: 60%; animation-delay: 0.5s;"></div>
                        <div class="wave-bar" style="height: 40%; animation-delay: 0.6s;"></div>
                    </div>
                    
                    <h1 style="font-size: 36px; font-weight: 700; color: #111827; margin: 0 0 40px 0; letter-spacing: -1px;">Analyzing your report...</h1>
                    
                    <div style="width: 100%; max-width: 400px; height: 6px; background: #E5E7EB; border-radius: 9999px; margin: 0 auto; overflow: hidden; position: relative;">
                        <div class="progress-fill" style="position: absolute; top: 0; height: 100%; background: #0D9488; border-radius: 9999px;"></div>
                    </div>
                </div>
            ''')
            
            submitted_text_display = gr.HTML()
            
            gr.HTML('''
                <div style="text-align: center; margin-top: 16px; margin-bottom: 80px;">
                    <div style="background: #D1FAE5; color: #047857; padding: 12px 24px; border-radius: 9999px; display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 500;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="#047857"/>
                        </svg>
                        AI core cross-referencing with 4.2M clinical studies
                    </div>
                </div>
            ''')

    # --- SCREEN 4: RESULTS ---
    with gr.Column(visible=False, elem_classes="landing-container") as results_screen:
        gr.HTML('''
        <div class="header-bar" style="background: white; border-bottom: 1px solid #F3F4F6;">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="4" width="20" height="16" rx="2" stroke="#0D9488" stroke-width="2"/>
                    <path d="M8 12H16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                    <path d="M12 8V16" stroke="#0D9488" stroke-width="2" stroke-linecap="round"/>
                </svg>
                MediSense AI
            </div>
            <div class="nav-links">
                <span class="active">Solutions</span>
                <span>Technology</span>
                <span>Research</span>
                <span>Compliance</span>
            </div>
        </div>
        ''')

        with gr.Row(elem_classes="input-main-section"):
            with gr.Column(scale=1, min_width=300):
                results_left = gr.HTML()
                
            with gr.Column(scale=2, min_width=500):
                results_right = gr.HTML()
                
                with gr.Row(elem_id="results-btn-row"):
                    followup_btn = gr.Button("Ask a Follow-up", elem_id="followup-btn")
                    start_over_btn = gr.Button("Start Over", elem_id="start-over-btn")
                    
                gr.HTML('''
                    <div class="disclaimer-banner">
                        <div style="background: #9CA3AF; color: white; border-radius: 50%; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold;">i</div>
                        This AI-generated analysis is for informational purposes and is not a professional medical diagnosis.
                    </div>
                    
                    <div style="margin-top: 48px; border-top: 1px solid #E5E7EB; padding-top: 32px;">
                        <h3 style="font-size: 16px; font-weight: 600; color: #111827; margin-top: 0; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM16.24 16.24C16.14 16.34 16.02 16.39 15.89 16.39C15.76 16.39 15.64 16.34 15.54 16.24L11.64 12.35C11.55 12.25 11.5 12.13 11.5 12V7C11.5 6.72 11.72 6.5 12 6.5C12.28 6.5 12.5 6.72 12.5 7V11.79L16.24 15.53C16.44 15.73 16.44 16.05 16.24 16.24Z" fill="#6B7280"/>
                            </svg>
                            Recent History
                        </h3>
                    </div>
                ''')
                
                history_area = gr.HTML()

        gr.HTML('''
        <div class="footer">
            <p>© 2024 MediSense AI. For informational purposes only. Not a substitute for professional medical advice.</p>
        </div>
        ''')

    # --- WIRING LOGIC ---
    start_button.click(
        fn=lambda: (gr.update(visible=False), gr.update(visible=True)),
        outputs=[landing_screen, input_screen]
    )

    analyze_btn.click(
        fn=start_loading,
        inputs=[user_input],
        outputs=[input_screen, loading_screen, submitted_text_display]
    ).then(
        fn=finish_analysis,
        inputs=[user_input, input_type],
        outputs=[loading_screen, results_screen, results_left, results_right, history_area]
    )

    followup_btn.click(
        fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
        outputs=[input_screen, results_screen]
    )
    
    start_over_btn.click(
        fn=lambda: (
            gr.update(visible=True), 
            gr.update(visible=False),
            gr.update(value="Symptoms"),
            gr.update(value="")
        ),
        outputs=[landing_screen, results_screen, input_type, user_input]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
