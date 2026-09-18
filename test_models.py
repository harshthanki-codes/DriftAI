import os
from langchain_google_genai import ChatGoogleGenerativeAI

models_to_test = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-pro-latest",
    "gemini-flash-latest",
    "gemini-3.1-pro-preview",
    "gemini-3.5-flash-lite"
]

for model in models_to_test:
    print(f"Testing {model}...")
    try:
        llm = ChatGoogleGenerativeAI(model=model, max_retries=0, timeout=10)
        res = llm.invoke("Say hi")
        print(f"SUCCESS: {model}")
        break
    except Exception as e:
        print(f"FAILED: {model} - {str(e)[:100]}")
