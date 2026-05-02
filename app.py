import gradio as gr
from model import analyze_medical_input
from database import save_analysis, get_history

# Global custom CSS for styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body, .gradio-container {
    background-color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar styling */
.sidebar {
    background-color: white !important;
    padding: 24px !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    height: 100% !important;
    display: flex;
    flex-direction: column;
}

.app-logo {
    font-size: 2.5rem;
    margin-bottom: 8px;
}

.app-name {
    color: #0D9488;
    font-weight: 700;
    font-size: 1.5rem;
    margin-bottom: 4px;
}

.app-tagline {
    color: #64748B;
    font-size: 0.9rem;
    margin-bottom: 24px;
}

.nav-item {
    padding: 12px 16px;
    margin: 4px 0;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    color: #334155;
    transition: background-color 0.2s;
}

.nav-item:hover, .nav-item.active {
    background-color: #F1F5F9;
    color: #0D9488;
}

.disclaimer {
    font-size: 0.75rem;
    color: #94A3B8;
    text-align: center;
    padding-top: 24px;
    border-top: 1px solid #E2E8F0;
}

/* Primary Button */
.primary-btn {
    background-color: #0D9488 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 12px !important;
    transition: background-color 0.2s !important;
    width: 100% !important;
}

.primary-btn:hover {
    background-color: #0F766E !important;
}

/* Secondary Button */
.secondary-btn {
    background-color: white !important;
    color: #0D9488 !important;
    border: 1px solid #0D9488 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px !important;
    transition: all 0.2s !important;
}

.secondary-btn:hover {
    background-color: #F0FDFA !important;
}

/* Cards */
.result-card {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    border: 1px solid #E2E8F0 !important;
}

.result-card h3 {
    margin-top: 0;
    color: #0F172A;
    font-size: 1.1rem;
    margin-bottom: 12px;
    font-weight: 600;
}

/* Header Text */
.main-header h2 {
    color: #0F172A !important;
    font-weight: 600 !important;
    margin-bottom: 16px !important;
}

/* Hide default borders where possible */
.block {
    border: none !important;
    box-shadow: none !important;
}
"""

sidebar_html = """
<div style="display:flex; flex-direction:column; height: 100%; min-height: 80vh;">
    <div>
        <div class="app-logo">🏥</div>
        <div class="app-name">MediSense AI</div>
        <div class="app-tagline">Understand your health, clearly.</div>
        <hr style="border-top: 1px solid #E2E8F0; margin: 16px 0; width: 100%;"/>
        <div class="nav-item active">🔍 New Analysis</div>
        <div class="nav-item">📋 History</div>
    </div>
    <div style="flex-grow: 1;"></div>
    <div class="disclaimer">
        Not a substitute for professional medical advice
    </div>
</div>
"""

with gr.Blocks(css=custom_css, title="MediSense AI", theme=gr.themes.Default(font=[gr.themes.GoogleFont("Inter"), "sans-serif"])) as demo:
    with gr.Row():
        # Left sidebar (25% width)
        with gr.Column(scale=1, elem_classes=["sidebar"]):
            gr.HTML(sidebar_html)
            
        # Right main area (75% width)
        with gr.Column(scale=3):
            with gr.Tabs():
                # Tab 1: New Analysis
                with gr.Tab("New Analysis"):
                    gr.Markdown("## What brings you in today?", elem_classes=["main-header"])
                    input_text = gr.Textbox(
                        lines=8, 
                        placeholder="Describe your symptoms or paste your medical report here...",
                        show_label=False
                    )
                    analysis_type = gr.Radio(
                        choices=["Symptoms", "Medical Report"], 
                        value="Symptoms",
                        show_label=False
                    )
                    analyze_btn = gr.Button("Analyze", elem_classes=["primary-btn"])
                    
                # Tab 2: Results
                with gr.Tab("Results"):
                    with gr.Column(elem_classes=["result-card"]):
                        key_findings_md = gr.Markdown("### 🔍 Key Findings\n\n*Your analysis results will appear here.*")
                    with gr.Column(elem_classes=["result-card"]):
                        summary_md = gr.Markdown("### 📋 Simplified Summary\n\n*A clear, easy-to-understand summary will be generated.*")
                    with gr.Column(elem_classes=["result-card"]):
                        next_steps_md = gr.Markdown("### 💡 Suggested Next Steps\n\n*Actionable recommendations based on your input.*")
                    
                    with gr.Row():
                        follow_up_btn = gr.Button("Ask Follow-up", elem_classes=["secondary-btn"])
                        start_over_btn = gr.Button("Start Over", elem_classes=["secondary-btn"])
                        
                # Tab 3: History
                with gr.Tab("History"):
                    history_table = gr.Dataframe(
                        headers=["Date", "Type", "Summary"],
                        datatype=["str", "str", "str"],
                        value=get_history(),
                        interactive=False,
                        row_count=10
                    )

    def process_analysis(text, input_type):
        kf, summ, ns = analyze_medical_input(text, input_type)
        # Save to database automatically
        save_analysis(input_type, text, kf, summ, ns)
        # Refresh history table
        updated_history = get_history()
        
        return (
            f"### 🔍 Key Findings\n\n{kf}",
            f"### 📋 Simplified Summary\n\n{summ}",
            f"### 💡 Suggested Next Steps\n\n{ns}",
            updated_history
        )

    analyze_btn.click(
        fn=process_analysis,
        inputs=[input_text, analysis_type],
        outputs=[key_findings_md, summary_md, next_steps_md, history_table]
    )

if __name__ == "__main__":
    demo.launch()
