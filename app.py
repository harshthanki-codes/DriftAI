import gradio as gr
import importlib
from langchain_core.messages import HumanMessage
import json

# Import the agents
a1 = importlib.import_module("assignment-1.agent")
a2 = importlib.import_module("assignment-2.agent")
a3 = importlib.import_module("assignment-3.agent")

def run_a1(query):
    state = {"messages": [HumanMessage(content=query)], "tool_call_count": 0, "should_fail": False}
    result = a1.app.invoke(state)
    content = result["messages"][-1].content
    if isinstance(content, list):
        return content[0].get("text", "") if isinstance(content[0], dict) else str(content)
    return str(content)

def run_a2():
    state = {"task": "Write a python function that calculates the fibonacci sequence.", "worker_output": "", "reviewer_feedback": "", "is_approved": False, "loop_count": 0}
    result = a2.app.invoke(state)
    return f"Verdict: {'APPROVED' if result['is_approved'] else 'REJECTED'}\n\nReviewer Feedback: {result['reviewer_feedback']}\n\nWorker Output:\n{result['worker_output']}"

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

# Sleek UI Design
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("<h1 style='text-align: center;'>🚀 Drift AI | Autonomous Agent Fleet</h1>")
    gr.Markdown("<p style='text-align: center;'>Production-grade LangGraph architectures, now running on the industry-standard Gradio framework.</p>")
    
    with gr.Tab("Assignment 1: Research Agent"):
        gr.Markdown("Agent that decides which tools to use with a strict 6-turn limit.")
        a1_input = gr.Textbox(label="Ask the agent a question", value="What's the best caching strategy for a read-heavy API with 10k req/sec?")
        a1_btn = gr.Button("Execute Research Agent", variant="primary")
        a1_output = gr.Textbox(label="Agent Response", lines=10)
        a1_btn.click(run_a1, inputs=a1_input, outputs=a1_output)

    with gr.Tab("Assignment 2: Worker-Reviewer Dyad"):
        gr.Markdown("Worker outputs code, Reviewer enforces strict validation via Pydantic.")
        a2_btn = gr.Button("Execute Multi-Agent Dyad", variant="primary")
        a2_output = gr.Textbox(label="Final Report", lines=10)
        a2_btn.click(run_a2, inputs=[], outputs=a2_output)
        
    with gr.Tab("Assignment 3: Resumable Memory"):
        gr.Markdown("SQLite checkpointing. If it crashes, it resumes exactly where it left off.")
        a3_crash = gr.Checkbox(label="Simulate Crash on Item 3?", value=True)
        a3_btn = gr.Button("Execute Processing Pipeline", variant="primary")
        a3_output = gr.Code(label="Database Results", language="json")
        a3_btn.click(run_a3, inputs=a3_crash, outputs=a3_output)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
