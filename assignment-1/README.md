# Assignment 1: Tool-Using Research Agent

## Setup and Running

Ensure you have a valid `GEMINI_API_KEY` set in your environment (e.g. via an `.env` file at the root).

### Running a Clean Trace
To see the agent successfully plan its steps, execute tools, and output an answer:
```bash
uv run python assignment-1/agent.py
```

### Running with Mocked Failure
To see the agent hit an injected failure (a timeout on its very first tool call), notice the failure, and recover:
```bash
uv run python assignment-1/agent.py fail
```

## Tools Used
1. `search_caching_strategies`: Mocks a knowledge base lookup for architectural patterns.
2. `calculate_latency_budget`: Simple calculator for adding up latency components.
3. `fetch_system_metrics`: Mocked real-time performance lookup.

## Question Answered
> "What's the best caching strategy for a read-heavy API with 10k req/sec? Also calculate my latency budget if DB is 150ms, Network is 20ms, Compute is 50ms."

## Architecture Notes
- We use a custom **LangGraph StateGraph** to enforce explicit failure handling and tool limits.
- The state tracks `tool_call_count`, gracefully exiting if it hits 6 calls.
- By intercepting tool execution in the `execute_tools` node, we can inject deterministic failures to prove the LLM's recovery capabilities without risking flaky network dependencies.
