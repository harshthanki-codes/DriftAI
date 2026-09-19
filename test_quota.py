import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

models_to_test = [
    "gemini-3.5-flash",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest"
]

api_keys = [os.environ.get(f"GEMINI_API_KEY_{i}") for i in range(1, 6) if os.environ.get(f"GEMINI_API_KEY_{i}")]
key = api_keys[0] if api_keys else None

for model in models_to_test:
    print(f"Testing {model} on Key 1...")
    try:
        llm = ChatGoogleGenerativeAI(model=model, temperature=0, max_retries=0, api_key=key)
        res = llm.invoke("Say hi")
        print(f"SUCCESS: {model}")
        break
    except Exception as e:
        print(f"FAILED: {model} - {str(e)[:100]}")
