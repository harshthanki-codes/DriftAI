import gradio as gr
import importlib
from langchain_core.messages import HumanMessage
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
    state = {"messages": [HumanMessage(content=message)], "tool_call_count": 0, "should_fail": False}
    result = a1.app.invoke(state)
    return clean_content(result["messages"][-1].content)

def run_a2_interactive():
    state = {"task": "Write a python function that calculates the fibonacci sequence.", "worker_output": "", "review_verdict": "", "review_reason": ""}
    result = a2.app.invoke(state)
    worker_clean = clean_content(result.get('worker_output', ''))
    
    is_approved = "approved" in str(result.get('review_verdict', '')).lower()
    verdict_md = f"### {'🟢 APPROVED' if is_approved else '🔴 REJECTED'}\n\n**Critic Feedback:** {result.get('review_reason', '')}"
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
        return f"🔥 FATAL CRASH DETECTED AT ITEM #3\n\nDatabase Checkpoint State Right Before Crash:\n{json.dumps(completed, indent=2)}\n\n(Uncheck 'Simulate Crash' and run again to watch it perfectly resume without duplicating work!)"

# 🌌 Hyper-Modern Chat & Dashboard UI
custom_theme = gr.themes.Ocean(
    primary_hue="cyan", 
    secondary_hue="blue",
    font=[gr.themes.GoogleFont("Outfit"), "system-ui", "sans-serif"]
)

css = """
h1 {text-align: center; font-size: 3.5em; background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px;}
.subtitle {text-align: center; color: #888; font-size: 1.2em; margin-top: 0px; margin-bottom: 20px;}
.gradio-container {background-color: #f4f7f6;}
"""

with gr.Blocks(title="Drift AI | Mission Control") as demo:
    gr.HTML("<h1>🌌 Drift AI Core</h1><p class='subtitle'>Next-Generation Autonomous Multi-Agent Systems</p>")
    
    with gr.Tabs():
        with gr.TabItem("💬 Assignment 1: Chat Assistant"):
            gr.Markdown("### 🤖 LangGraph Research Agent (6-Turn Memory)")
            gr.ChatInterface(
                fn=chat_a1,
                examples=["What's the best caching strategy for a read-heavy API?", "How do I implement a circuit breaker?"]
            )

        with gr.TabItem("👨‍💻 Assignment 2: The Critic Dyad"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### ⚖️ Multi-Agent Collaboration")
                    gr.Markdown("Watch two agents argue. The Worker synthesizes Python code, while the Reviewer acts as an architectural critic enforcing strict Pydantic schemas.")
                    a2_btn = gr.Button("⚡ Trigger Code Synthesis", variant="primary", size="lg")
                    a2_verdict = gr.Markdown("*(Verdict will appear here)*")
                with gr.Column(scale=2):
                    a2_code = gr.Code(label="Synthesized Worker Code", language="python")
            a2_btn.click(run_a2_interactive, inputs=[], outputs=[a2_verdict, a2_code])
            
        with gr.TabItem("💾 Assignment 3: Resilient State"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🛡️ SQLite Checkpointing")
                    gr.Markdown("Processes critical data streams with continuous SQLite checkpoints. Simulate a fatal server crash to watch the agent seamlessly resume from the exact point of failure.")
                    a3_crash = gr.Checkbox(label="🔥 Simulate Fatal Crash on Item #3?", value=True)
                    a3_btn = gr.Button("🔄 Execute Fault-Tolerant Pipeline", variant="primary", size="lg")
                with gr.Column(scale=2):
                    a3_output = gr.Code(label="Database Checkpoint Output", language="json")
            a3_btn.click(run_a3_interactive, inputs=a3_crash, outputs=a3_output)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme=custom_theme, css=css)
