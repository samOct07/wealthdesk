import os

os.environ.setdefault("HF_HUB_VERBOSITY", "error")

from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------------------------
# TODO 4 of 4 — turn on LangSmith tracing
# ---------------------------------------------------------------------------
# Uncomment the block below. It maps the LANGSMITH_* variables in your .env
# onto the LANGCHAIN_* names LangChain reads, so every graph run is traced.
# Needs LANGSMITH_API_KEY and LANGSMITH_TRACING=true in .env.
# ---------------------------------------------------------------------------
# if os.getenv("LANGSMITH_API_KEY") and os.getenv("LANGSMITH_TRACING", "").lower() == "true":
#     os.environ["LANGCHAIN_TRACING_V2"] = "true"
#     os.environ.setdefault("LANGCHAIN_API_KEY", os.getenv("LANGSMITH_API_KEY", ""))
#     os.environ.setdefault("LANGCHAIN_PROJECT",  os.getenv("LANGSMITH_PROJECT", "batch1-wealthdesk"))
