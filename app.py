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

# Enterprise-Grade, Minimalist UI Design (Similar to Claude/ChatGPT)
custom_theme = gr.themes.Soft(
    primary_hue="slate",
    secondary_hue="slate",
    neutral_hue="zinc",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
)

with gr.Blocks(title="Drift AI Studio", fill_width=True) as demo:
    gr.Markdown(
        """
        # 🚀 Drift AI Studio
        **Autonomous Agent Fleet** • *Production-Grade LangGraph Architectures*
        """
    )
    
    with gr.Tabs():
        with gr.TabItem("1. Research Agent"):
            gr.Markdown("### Autonomous Research Assistant\nPowered by dynamic tool routing with a strict 6-turn limit.")
            gr.ChatInterface(
                fn=chat_a1,
                examples=["What's the best caching strategy for a read-heavy API?", "How do I implement a circuit breaker?"],
                fill_height=True
            )

        with gr.TabItem("2. Reviewer Dyad"):
            gr.Markdown("### Multi-Agent Code Synthesis\nWorker outputs Python code. Reviewer enforces architecture using strict Pydantic schema validation.")
            with gr.Row():
                with gr.Column(scale=1):
                    a2_btn = gr.Button("Initialize Dyad Protocol", variant="primary", size="lg")
                    a2_verdict = gr.Markdown("*(Awaiting Execution)*")
                with gr.Column(scale=2):
                    a2_code = gr.Code(label="Worker Output (Python)", language="python")
            a2_btn.click(run_a2_interactive, inputs=[], outputs=[a2_verdict, a2_code])
            
        with gr.TabItem("3. Resumable Memory"):
            gr.Markdown("### Fault-Tolerant State Management\nDemonstrates continuous SQLite checkpointing. The system survives fatal crashes without duplicating work.")
            with gr.Row():
                with gr.Column(scale=1):
                    a3_crash = gr.Checkbox(label="Simulate Fatal Crash on Item #3?", value=True)
                    a3_btn = gr.Button("Execute Resilient Pipeline", variant="primary", size="lg")
                with gr.Column(scale=2):
                    a3_output = gr.Code(label="SQLite Database State", language="json")
            a3_btn.click(run_a3_interactive, inputs=a3_crash, outputs=a3_output)

if __name__ == "__main__":
    demo.launch(theme=custom_theme)
