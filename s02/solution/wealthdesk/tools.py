import os

from langchain_groq import ChatGroq

from .config import MODEL_NAME, TEMPERATURE, MAX_TOKENS

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

if LLM_PROVIDER == "local":
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=os.getenv("LOCAL_LAMA_VERSION", "llama3.2:3b"),
        temperature=TEMPERATURE,
        num_predict=MAX_TOKENS,
    )
elif LLM_PROVIDER == "groq":
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found.\n"
            "Did you copy .env.example to .env and fill in your key?\n"
            "  Windows:  copy .env.example .env\n"
            "  Mac/Linux: cp .env.example .env"
        )

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
else:
    raise ValueError("LLM_PROVIDER must be 'groq' or 'local'.")