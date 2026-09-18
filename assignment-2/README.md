# Assignment 2: Multi-Agent Task with Review

## Task Description
A two-agent system where Agent A (Worker) writes a Python function, and Agent B (Reviewer) evaluates it against strict criteria. There is no revision loop. 

## Approval Criteria
Agent B strictly evaluates the code against three rules:
1. Must use the standard library `time` module for sleeping.
2. Must include Python type hints.
3. Must not contain any syntax errors or incomplete code.

If any criterion fails, Agent B rejects the code and provides a specific, concrete reason using structured output (Pydantic).

## Running
Ensure your `GEMINI_API_KEY` is set.

To run a task that will be approved (simple function with type hints):
```bash
uv run python assignment-2/agent.py approve
```

To run a task that will be rejected (complex task explicitly asking to omit type hints):
```bash
uv run python assignment-2/agent.py reject
```

## Architecture
- **LangGraph Sequential Chain**: `Worker Node -> Reviewer Node`.
- **Structured Outputs**: The reviewer leverages LangChain's `.with_structured_output()` to guarantee it returns a boolean verdict and a string reason, preventing vague "looks fine" responses.
- **Token Tracking**: We use a custom `BaseCallbackHandler` bound to the LLM to accurately track `total_calls` and `total_tokens`.
