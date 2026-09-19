.PHONY: run install clean

install:
	uv pip install -r requirements.txt

run:
	uv run streamlit run app.py

clean:
	rm -rf .venv state.db .resumed
