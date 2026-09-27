import gradio as gr
import importlib
from langchain_core.messages import HumanMessage, SystemMessage
import ast

a1 = importlib.import_module("assignment-1.agent")
a2 = importlib.import_module("assignment-2.agent")
a3 = importlib.import_module("assignment-3.agent")

def clean_content(content):
    if isinstance(content, str) and content.startswith("[{"):
        try:
            parsed = ast.literal_eval(content)
            if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
                return parsed[0].get("text", content)
        except:
            pass
    elif isinstance(content, list):
        return content[0].get("text", "") if isinstance(content[0], dict) else str(content)
    return str(content)

def chat_a1(message, history):
    system_prompt = "You are the flagship Autonomous Agent for Drift AI. Drift AI is a cutting-edge AI research startup revolutionizing enterprise agentic architectures with production-grade LangGraph, resumable memory systems, and multi-agent dyads. If anyone asks what Drift AI is doing, or who you are, explain these incredible technical capabilities with massive enthusiasm and never say you don't know!"
    state = {"messages": [SystemMessage(content=system_prompt), HumanMessage(content=message)], "tool_call_count": 0, "should_fail": False}
    result = a1.app.invoke(state)
    return clean_content(result["messages"][-1].content)

def run_a2_interactive():
    state = {"task": "Write a python function that calculates the fibonacci sequence.", "worker_output": "", "review_verdict": "", "review_reason": ""}
    result = a2.app.invoke(state)
    worker_clean = clean_content(result.get('worker_output', ''))
    
    is_approved = "approved" in str(result.get('review_verdict', '')).lower()
    verdict_md = f"### {'✅ APPROVED' if is_approved else '❌ REJECTED'}\n\n**Reviewer Feedback:**\n> {result.get('review_reason', '')}"
    return verdict_md, worker_clean

def run_a3_interactive(crash_toggle):
    from langchain_core.runnables import RunnableConfig
    config = RunnableConfig(configurable={"thread_id": "test_session_1", "crash_at_item_3": crash_toggle})
    
    import json
    try:
        a3.app.invoke({"items": ["Company A experienced a 20% revenue growth.", "The new cloud division is profitable.", "Stock prices drop sharply."]}, config=config)
        
        final_state = a3.app.get_state(config).values
        completed = final_state.get("completed_items", {})
        return json.dumps(completed, indent=2)
    except SystemExit:
        final_state = a3.app.get_state(config).values
        completed = final_state.get("completed_items", {})
        return f"🚨 FATAL CRASH INTERCEPTED (Item #3)\n\nSystem state safely persisted to SQLite.\n\nDatabase Snapshot:\n{json.dumps(completed, indent=2)}\n\n(Uncheck 'Simulate Crash' and run again to watch the checkpointer perfectly resume.)"

# 🔥 Modern Interactive "Orange & White" UI Design
custom_theme = gr.themes.Default(
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
    primary_hue="orange",
    secondary_hue="amber",
    neutral_hue="slate"
)

css = """
/* Force light mode globally by overriding Gradio's internal CSS variables */
:root, .dark, body, .gradio-container {
    --background-fill-primary: #ffffff !important;
    --background-fill-secondary: #fff7ed !important;
    --border-color-primary: rgba(249, 115, 22, 0.2) !important;
    --block-background-fill: rgba(255, 255, 255, 0.8) !important;
    --block-border-color: rgba(249, 115, 22, 0.2) !important;
    --panel-background-fill: #ffffff !important;
    --body-text-color: #1e293b !important;
    --body-text-color-subdued: #64748b !important;
    --input-background-fill: #ffffff !important;
    --input-border-color: rgba(249, 115, 22, 0.3) !important;
}

@keyframes gradient-bg {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
body, .gradio-container { 
    background: linear-gradient(-45deg, #ffffff, #fff7ed, #ffedd5, #ffffff) !important;
    background-size: 400% 400% !important;
    animation: gradient-bg 15s ease infinite !important;
    color: #1e293b !important;
}

/* Aggressively destroy all Gradio default top spacing */
.gradio-container, .gradio-container > .main, .gradio-container > .main > .wrap, .wrap, .contain {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

.glow-header { 
    text-align: center; 
    font-size: 5rem; 
    font-weight: 900; 
    background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #f59e0b 100%); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
    margin: 0 !important; 
    padding-top: 0 !important;
    line-height: 1.1;
    letter-spacing: -3px; 
    text-shadow: 0 10px 30px rgba(249, 115, 22, 0.2);
}

.sub-header { 
    text-align: center; 
    color: #64748b; 
    font-size: 1.2rem; 
    font-weight: 600; 
    letter-spacing: 6px; 
    text-transform: uppercase; 
    margin-top: 5px !important;
    margin-bottom: 10px !important; 
}

/* Chatbot Specific Styling */
.chatbot {
    background-color: #ffffff !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(249, 115, 22, 0.08) !important;
    border: 1px solid rgba(249, 115, 22, 0.2) !important;
}

/* User Message Bubble */
.message-wrap .message.user {
    background: linear-gradient(90deg, #f97316 0%, #ea580c 100%) !important;
    color: #ffffff !important;
    border-radius: 20px 20px 4px 20px !important;
    box-shadow: 0 4px 15px rgba(249, 115, 22, 0.2) !important;
    border: none !important;
}

/* AI Message Bubble */
.message-wrap .message.bot {
    background: #fff7ed !important;
    color: #1e293b !important;
    border: 1px solid rgba(249, 115, 22, 0.2) !important;
    border-radius: 20px 20px 20px 4px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
}

/* Input Area */
textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid rgba(249, 115, 22, 0.3) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
}
textarea:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.15) !important;
}

/* General Layout Elements */
.glass { 
    background: rgba(255, 255, 255, 0.8) !important; 
    border: 1px solid rgba(249, 115, 22, 0.1) !important; 
    border-radius: 24px !important; 
    box-shadow: 0 20px 40px 0 rgba(0, 0, 0, 0.05), 0 1px 3px 0 rgba(249, 115, 22, 0.1) !important; 
    backdrop-filter: blur(20px) !important; 
    -webkit-backdrop-filter: blur(20px) !important;
    overflow: hidden;
}

.gradio-button.primary {
    background: linear-gradient(90deg, #f97316 0%, #ea580c 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 20px rgba(249, 115, 22, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.gradio-button.primary:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 30px rgba(234, 88, 12, 0.4) !important;
}
"""

with gr.Blocks(title="Drift AI Nexus", theme=custom_theme, css=css) as demo:
    gr.HTML("<h1 class='glow-header'>DRIFT AI</h1><div class='sub-header'>Neural Interface Nexus</div>")
    
    with gr.Tabs(elem_classes="glass"):
        with gr.TabItem("📡 Core 1: Neural Researcher"):
            gr.ChatInterface(
                fn=chat_a1,
                examples=["What's the best caching strategy for a read-heavy API?", "How do I implement a circuit breaker?"],
                fill_height=True
            )

        with gr.TabItem("🧠 Core 2: Architect Dyad"):
            with gr.Row(elem_classes="glass", variant="panel"):
                with gr.Column(scale=1):
                    gr.Markdown("### 👨‍💻 Adversarial Synthesis\nWatch two agents debate. The Worker writes Python, the Critic enforces strict architectural schemas.")
                    a2_btn = gr.Button("⚡ Initialize Neural Dyad", variant="primary", size="lg")
                    a2_verdict = gr.Markdown("*(Awaiting Execution)*")
                with gr.Column(scale=2):
                    a2_code = gr.Code(label="Synthesized Architecture (Python)", language="python")
            a2_btn.click(run_a2_interactive, inputs=[], outputs=[a2_verdict, a2_code])
            
        with gr.TabItem("💾 Core 3: Quantum Memory"):
            with gr.Row(elem_classes="glass", variant="panel"):
                with gr.Column(scale=1):
                    gr.Markdown("### 🛡️ Indestructible Checkpointing\nProcesses data with SQLite checkpoints. Survives terminal crashes without losing state.")
                    a3_crash = gr.Checkbox(label="🔥 Simulate Kernel Panic (Crash at #3)?", value=True)
                    a3_btn = gr.Button("🔄 Execute Resilient Pipeline", variant="primary", size="lg")
                with gr.Column(scale=2):
                    a3_output = gr.Code(label="SQLite State Manifold", language="json")
            a3_btn.click(run_a3_interactive, inputs=a3_crash, outputs=a3_output)

if __name__ == "__main__":
    demo.launch()
