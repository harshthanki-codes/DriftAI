# Assignment 3: Resumable Agent with Basic Self-Check

## Task Description
An agent processes 4 items (company updates) sequentially. It saves its state to a SQLite database (`state.db`) after every step. To prove resumability, the script simulates a fatal crash exactly halfway through. When re-run, it correctly skips the finished items and picks up where it left off.

At the end of processing, a Validation Check node uses an LLM-as-a-judge to ensure all summaries are accurate and non-empty. We deliberately poison the 3rd item's summary to prove the validation check works and flags the error.

## Running

1. **Start the run (it will simulate a crash halfway):**
```bash
uv run python assignment-3/agent.py
```
You will see it process Items 1 and 2, and then deliberately exit.

2. **Resume the run:**
```bash
uv run python assignment-3/agent.py
```
You will see it skip Items 1 and 2, and resume directly at Item 3. It will finish processing, and then the self-check validation node will catch the deliberately poisoned item.

## Architecture
- **State Persistence**: Uses `langgraph.checkpoint.sqlite.SqliteSaver` to write state checkpoints to disk. 
- **Resumability**: The `get_state` and `update_state` methods allow us to seamlessly resume a `thread_id`.
- **Validation**: The final node iterates over all items and uses structured outputs to check for validity, acting as an autonomous QA layer.
