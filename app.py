import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Drift AI Assignments", page_icon="🤖", layout="wide")

st.title("Drift AI - AI Engineer Assignments Interface")
st.markdown("Welcome to the interactive test interface for the Drift AI assignments. Use the sidebar to navigate between assignments and test them in real-time.")

st.sidebar.title("Assignments")
assignment = st.sidebar.radio("Select Assignment", [
    "1. Tool-Using Research Agent",
    "2. Multi-Agent Task with Review",
    "3. Resumable Agent with Self-Check"
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Senior Architecture Notes:**")
st.sidebar.info("All agents are built using **LangGraph** for robust state management. They feature deterministic tool constraints, SQLite persistence, and strict Pydantic parsing.")

def run_script(command):
    with st.spinner("Running Agent... (If this takes longer than 15s, Google's free tier API is currently congested)"):
        try:
            # We use text=True to get string output and stream it
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True,
                cwd=os.getcwd()
            )
            
            output_container = st.empty()
            full_output = ""
            
            for line in process.stdout:
                full_output += line
                output_container.code(full_output, language="text")
                
            process.wait()
            if process.returncode != 0:
                st.error(f"Agent execution failed with return code {process.returncode}")
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

if assignment == "1. Tool-Using Research Agent":
    st.header("Assignment 1: Tool-Using Research Agent")
    st.markdown("Tests a LangGraph agent with strict tool constraints (Max 6 loops) and failure recovery.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Clean Mode (Normal)", type="primary", use_container_width=True):
            run_script("uv run python assignment-1/agent.py clean")
    with col2:
        if st.button("Run Fail Mode (Injects Mock Timeout)", use_container_width=True):
            run_script("uv run python assignment-1/agent.py fail")

elif assignment == "2. Multi-Agent Task with Review":
    st.header("Assignment 2: Multi-Agent Task with Review")
    st.markdown("Tests a dual-agent workflow where a Worker writes code and a Reviewer grades it using strict Pydantic schemas.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Approved Scenario", type="primary", use_container_width=True):
            run_script("uv run python assignment-2/agent.py approve")
    with col2:
        if st.button("Run Rejected Scenario (Fails criteria)", use_container_width=True):
            run_script("uv run python assignment-2/agent.py reject")

elif assignment == "3. Resumable Agent with Self-Check":
    st.header("Assignment 3: Resumable Agent with Self-Check")
    st.markdown("Tests LangGraph's `SqliteSaver`. It will process 2 items and deliberately crash. Clicking it again will resume perfectly.")
    
    if st.button("Run Iteration (Click twice to prove resumability)", type="primary"):
        run_script("uv run python assignment-3/agent.py")
