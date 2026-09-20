import streamlit as st
import subprocess
import os

# --- Page Config & CSS ---
st.set_page_config(page_title="Drift AI - Agent Fleet", page_icon="🚀", layout="wide")



# --- Header ---
st.title("🚀 Drift AI | Autonomous Agent Fleet")
st.subheader("Production-Grade LangGraph Architectures • Pydantic Structured Outputs • SQLite Checkpointing")

# --- Sidebar Telemetry ---
with st.sidebar:
    st.markdown("### ⚙️ System Telemetry")
    st.metric(label="Model Engine", value="Gemini 3.5 Flash")
    st.metric(label="Orchestration", value="LangGraph")
    st.metric(label="State Persistence", value="Active (SQLite)")
    st.divider()
    st.markdown("#### Built For Drift AI")
    st.info("Demonstrates fault-tolerance, multi-agent cyclic reviews, and absolute deterministic output validation.")

# --- Execution Function ---
def run_agent_workflow(command, title):
    with st.container(border=True):
        st.markdown(f"### 📡 Live Execution: {title}")
        
        progress_text = "Initializing LangGraph Nodes..."
        my_bar = st.progress(0, text=progress_text)
        
        output_container = st.empty()
        full_output = ""
        
        try:
            my_bar.progress(20, text="Establishing Google GenAI Connection...")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True,
                cwd=os.getcwd()
            )
            
            my_bar.progress(50, text="Streaming LLM Reasoning Engine...")
            for line in process.stdout:
                full_output += line
                # Render beautifully with syntax highlighting
                output_container.code(full_output, language="yaml")
                
            process.wait()
            
            if process.returncode == 0 or process.returncode == 1:
                my_bar.progress(100, text="Execution Complete.")
                st.toast("Workflow executed successfully!", icon="✅")
                if "WORKFLOW COMPLETE" in full_output:
                    st.balloons()
            else:
                st.error(f"Execution failed with return code {process.returncode}")
                
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")


# --- Main Application ---
tab1, tab2, tab3 = st.tabs([
    "🔍 Assignment 1: Research Agent", 
    "⚖️ Assignment 2: Multi-Agent Review", 
    "💾 Assignment 3: Resumable Memory"
])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### The Tool-Using Researcher")
        st.write("An autonomous agent that plans its own sequence of actions. It is strictly constrained to a maximum of 6 tool calls to prevent infinite loops.")
        st.write("**Architecture highlights:**")
        st.markdown("""
        - Dynamic Tool Binding
        - Transparent LLM Reasoning Traces
        - Explicit Fallback/Recovery mechanisms
        """)
        
        st.divider()
        if st.button("🚀 Run Standard Workflow", key="a1_clean", use_container_width=True, type="primary"):
            run_agent_workflow("uv run python assignment-1/agent.py clean", "Research Agent (Standard)")
            
        if st.button("⚠️ Inject Mock Failure (Test Recovery)", key="a1_fail", use_container_width=True):
            run_agent_workflow("uv run python assignment-1/agent.py fail", "Research Agent (Fault Tolerant)")

    with col2:
        st.info("👈 Click a button on the left to stream the agent's live reasoning trace.")

with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### The Worker / Reviewer Dyad")
        st.write("A strictly linear multi-agent workflow. The Worker generates code, and the Reviewer evaluates it based on strict corporate guidelines.")
        st.write("**Architecture highlights:**")
        st.markdown("""
        - Pydantic-enforced Structured Outputs
        - Boolean verdicts with explainable reasoning
        - Custom Token Tracker Callbacks
        """)
        
        st.divider()
        if st.button("✅ Run 'Approved' Scenario", key="a2_app", use_container_width=True, type="primary"):
            run_agent_workflow("uv run python assignment-2/agent.py approve", "Multi-Agent Review (Approved)")
            
        if st.button("❌ Run 'Rejected' Scenario", key="a2_rej", use_container_width=True):
            run_agent_workflow("uv run python assignment-2/agent.py reject", "Multi-Agent Review (Rejected)")

    with col2:
        st.info("👈 Click a button on the left to watch the Reviewer evaluate the Worker's output in real-time.")

with tab3:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Resumable State Machine")
        st.write("Demonstrates true persistence using LangGraph's SqliteSaver. The process will intentionally crash halfway through.")
        st.write("**Architecture highlights:**")
        st.markdown("""
        - Disk-based SQLite Checkpointing
        - Fault-tolerant pause and resume
        - LLM-as-a-judge output validation
        """)
        
        st.divider()
        st.warning("Click the button below twice. The first click simulates a fatal crash. The second click resumes state perfectly.")
        if st.button("🔄 Run Checkpointed Iteration", key="a3_run", use_container_width=True, type="primary"):
            run_agent_workflow("uv run python assignment-3/agent.py", "Resumable Agent")

    with col2:
        st.info("👈 First click: Will crash on Item #3. Second click: Will skip items #1 and #2 and finish successfully.")
