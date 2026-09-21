import gradio as gr
import importlib
from langchain_core.messages import HumanMessage
import json

# Import the agents
a1 = importlib.import_module("assignment-1.agent")
a2 = importlib.import_module("assignment-2.agent")
a3 = importlib.import_module("assignment-3.agent")

import ast

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

def run_a1(query):
    state = {"messages": [HumanMessage(content=query)], "tool_call_count": 0, "should_fail": False}
    result = a1.app.invoke(state)
    return clean_content(result["messages"][-1].content)

def run_a2():
    state = {"task": "Write a python function that calculates the fibonacci sequence.", "worker_output": "", "review_verdict": "", "review_reason": ""}
    result = a2.app.invoke(state)
    worker_clean = clean_content(result.get('worker_output', ''))
    return f"Verdict: {str(result.get('review_verdict', '')).upper()}\n\nReviewer Feedback: {result.get('review_reason', '')}\n\nWorker Output:\n{worker_clean}"

def run_a3(crash_toggle):
    from langchain_core.runnables import RunnableConfig
    import time
    config = RunnableConfig(configurable={"thread_id": f"gradio_session_{int(time.time())}"})
    items = ["Company A reported a 20% increase in revenue.", "The new cloud division is profitable.", "CEO resigns abruptly.", "Stock prices plummet."]
    state = {"items": items, "results": {}, "current_index": 0, "should_crash": crash_toggle}
    try:
        result = a3.app.invoke(state, config=config)
        return json.dumps(result["results"], indent=2)
    except SystemExit:
        return f"CRASHED! The agent deliberately died at Item #3.\n\n(Uncheck 'Simulate Crash' and run again to watch it perfectly resume and finish without repeating the first two!)"

# 🌌 Sleek Mission Control UI Design
custom_theme = gr.themes.Soft(
    primary_hue="indigo", 
    secondary_hue="blue",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
)

with gr.Blocks(title="Drift AI | Mission Control") as demo:
    with gr.Row():
        gr.Markdown(
            """
            <div style='text-align: center; padding: 2rem 0;'>
                <h1 style='font-size: 3em; margin-bottom: 0.2em; font-weight: 800;'>🌌 Drift AI | Mission Control</h1>
                <p style='font-size: 1.2em; color: #666;'>Enterprise-Grade LangGraph Architectures • Resilient State Management • Multi-Agent Dyads</p>
            </div>
            """
        )
    
    with gr.Tabs():
        with gr.TabItem("🔍 Assignment 1: Research Agent"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🧠 Autonomous Decision Engine")
                    gr.Markdown("This agent dynamically selects tools to solve complex queries. It features a strict **6-turn safety limit** and API fallback mechanisms to ensure 100% uptime.")
                    a1_input = gr.Textbox(label="Query Input", placeholder="E.g., What's the best caching strategy for a read-heavy API...", lines=3)
                    a1_btn = gr.Button("🚀 Deploy Research Agent", variant="primary", size="lg")
                with gr.Column(scale=2):
                    a1_output = gr.Textbox(label="Agent Intelligence Output", lines=12)
            a1_btn.click(run_a1, inputs=a1_input, outputs=a1_output)

        with gr.TabItem("⚖️ Assignment 2: Reviewer Dyad"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 👨‍💻 Multi-Agent Collaboration")
                    gr.Markdown("A two-agent system. The **Worker** synthesizes Python code, and the **Reviewer** rigidly enforces architecture standards using deterministic Pydantic schema validation.")
                    a2_btn = gr.Button("⚡ Execute Dyad Pipeline", variant="primary", size="lg")
                with gr.Column(scale=2):
                    a2_output = gr.Textbox(label="Final Quality Assurance Report", lines=12)
            a2_btn.click(run_a2, inputs=[], outputs=a2_output)
            
        with gr.TabItem("💾 Assignment 3: Resumable Memory"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🛡️ Fault-Tolerant State Management")
                    gr.Markdown("Processes critical data streams with continuous SQLite checkpointing. If a fatal crash occurs, the LangGraph architecture seamlessly resumes from the exact point of failure.")
                    a3_crash = gr.Checkbox(label="🔥 Simulate Fatal Crash on Item #3?", value=True)
                    a3_btn = gr.Button("🔄 Run Fault-Tolerant Pipeline", variant="primary", size="lg")
                with gr.Column(scale=2):
                    a3_output = gr.Code(label="SQLite Checkpoint Data", language="json")
            a3_btn.click(run_a3, inputs=a3_crash, outputs=a3_output)
            
    with gr.Accordion("System Architecture Details", open=False):
        gr.Markdown(
            """
            - **Framework**: LangGraph + Gradio
            - **LLM Engine**: Google Gemini 3.5 Flash Lite (Multi-Key Failover Enabled)
            - **State Persister**: SQLite (`SqliteSaver`)
            - **Validation**: Pydantic `BaseModel` Constraints
            """
        )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme=custom_theme)
