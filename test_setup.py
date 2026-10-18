"""
Pre-course setup verification script.
Agentic AI Engineering — Batch 2

Run this after completing the Part 2 setup guide:
    python test_setup.py

All checks must pass before Session 2.
Questions? Post in the WhatsApp group.
"""

import sys
import shutil
import subprocess
import importlib.util
import os

PASS = "  OK "
FAIL = "  FAIL"
WARN = "  WARN"

results = []

def check(label, passed, fix=None, warn=False):
    if warn:
        status = WARN
    else:
        status = PASS if passed else FAIL
    results.append((label, passed, fix, warn))
    print(f"{status}  {label}")
    if not passed and fix:
        print(f"         Fix: {fix}")


print()
print("=" * 57)
print("  Agentic AI Engineering -- Batch 2 Setup Check")
print("=" * 57)

# ── Virtual environment ────────────────────────────────────
print("\nVirtual environment")
in_venv = sys.prefix != sys.base_prefix
check(
    "Running inside a virtual environment (.venv)",
    in_venv,
    fix="Activate your venv first: source .venv/bin/activate (Mac) or .venv\\Scripts\\activate (Windows)"
)

# ── Python version ─────────────────────────────────────────
print("\nPython")
major, minor = sys.version_info[:2]
check(
    f"Python {major}.{minor} (need 3.11+)",
    major == 3 and minor >= 11,
    fix="Download Python 3.11+ from python.org"
)

# ── Core packages (Session 1) ──────────────────────────────
print("\nCore packages (Session 1)")
core = {
    "python-dotenv":   "dotenv",
    "pydantic":        "pydantic",
    "groq":            "groq",
    "langchain":       "langchain",
    "langchain-core":  "langchain_core",
    "langchain-groq":  "langchain_groq",
    "langgraph":       "langgraph",
    "langchain-ollama":"langchain_ollama",
}
for pkg, imp in core.items():
    spec = importlib.util.find_spec(imp)
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── Memory packages (Session 2) ────────────────────────────
print("\nMemory packages (Session 2)")
memory = {
    "langgraph-checkpoint-sqlite": "langgraph.checkpoint.sqlite",
    "aiosqlite":                   "aiosqlite",
}
for pkg, imp in memory.items():
    try:
        spec = importlib.util.find_spec(imp)
    except ModuleNotFoundError:   # parent package (langgraph) not installed
        spec = None
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── LangGraph Studio (Sessions 1–16) ──────────────────────
print("\nLangGraph Studio")
lgcli = importlib.util.find_spec("langgraph_cli")
check(
    "langgraph-cli[inmem]",
    lgcli is not None,
    fix="pip install 'langgraph-cli[inmem]'"
)

# ── RAG packages (Session 4) ───────────────────────────────
print("\nRAG / vector store packages (Session 4)")
rag = {
    "langchain-text-splitters":  "langchain_text_splitters",
    "chromadb":                  "chromadb",
    "langchain-chroma":          "langchain_chroma",
    "langchain-huggingface":     "langchain_huggingface",
    "sentence-transformers":     "sentence_transformers",
}
for pkg, imp in rag.items():
    spec = importlib.util.find_spec(imp)
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── Evaluation (Session 6) ─────────────────────────────────
print("\nEvaluation packages (Session 6)")
eval_pkgs = {
    "openai":          "openai",
    "langchain-openai":"langchain_openai",
}
for pkg, imp in eval_pkgs.items():
    spec = importlib.util.find_spec(imp)
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── MCP packages (Sessions 7–8) ────────────────────────────
print("\nMCP packages (Sessions 7–8)")
mcp_pkgs = {
    "mcp":                     "mcp",
    "langchain-mcp-adapters":  "langchain_mcp_adapters",
}
for pkg, imp in mcp_pkgs.items():
    spec = importlib.util.find_spec(imp)
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── Web / production packages (Sessions 11, 15–16) ─────────
print("\nWeb and production packages (Sessions 11, 15–16)")
web_pkgs = {
    "streamlit":         "streamlit",
    "fastapi":           "fastapi",
    "uvicorn":           "uvicorn",
    "httpx":             "httpx",
    "pydantic-settings": "pydantic_settings",
    "slowapi":           "slowapi",
}
for pkg, imp in web_pkgs.items():
    spec = importlib.util.find_spec(imp)
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── Test packages ──────────────────────────────────────────
print("\nTest packages")
test_pkgs = {
    "pytest":           "pytest",
    "pytest-mock":      "pytest_mock",
    "pytest-asyncio":   "pytest_asyncio",
}
for pkg, imp in test_pkgs.items():
    spec = importlib.util.find_spec(imp)
    check(pkg, spec is not None, fix=f"pip install {pkg}")

# ── .env and GROQ_API_KEY ──────────────────────────────────
print("\nAPI Keys")
env_exists = os.path.exists(".env")
check(".env file exists", env_exists, fix="Copy .env.example to .env and add your GROQ_API_KEY")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass   # already reported above as a missing package

groq_key = os.environ.get("GROQ_API_KEY", "")
check(
    "GROQ_API_KEY set",
    bool(groq_key and not groq_key.startswith("your_") and groq_key != "gsk_your_actual_key_here"),
    fix="Add your Groq API key to .env — get one free at console.groq.com"
)

# ── Groq API live test ─────────────────────────────────────
print("\nGroq API (live test)")
if groq_key and not groq_key.startswith("your_") and groq_key != "gsk_your_actual_key_here":
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": "Reply with exactly: READY"}],
            max_tokens=100,   # gpt-oss-20b is a reasoning model -- needs room to think before replying
        )
        reply = response.choices[0].message.content.strip()
        check(
            "Groq API responds (gpt-oss-20b)",
            "READY" in reply.upper()
        )
    except Exception as e:
        check("Groq API responds", False, fix=f"Error: {e}")
else:
    check("Groq API responds", False, fix="Add GROQ_API_KEY to .env first")

# ── Ollama ─────────────────────────────────────────────────
print("\nOllama (local fallback)")
try:
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True, text=True, timeout=10
    )
    ollama_ok = result.returncode == 0
    check("Ollama installed", ollama_ok, fix="Install from ollama.com")
    if ollama_ok:
        has_model = "llama3.2" in result.stdout or "llama" in result.stdout
        check(
            "llama3.2:3b model available",
            has_model,
            fix="Run: ollama pull llama3.2:3b"
        )
except FileNotFoundError:
    check("Ollama installed", False, fix="Install from ollama.com")
except Exception as e:
    check("Ollama installed", False, fix=f"Error: {e}")

# ── LangSmith (Session 9+) ─────────────────────────────────
print("\nLangSmith (needed from Session 9 — not required right now)")
langsmith_key = os.environ.get("LANGSMITH_API_KEY", "")
ls_set = bool(langsmith_key and not langsmith_key.startswith("your_") and langsmith_key != "lsv2_your_key_here")
check(
    "LANGSMITH_API_KEY set",
    ls_set,
    fix="Get a free key at smith.langchain.com and add LANGSMITH_API_KEY to .env",
    warn=not ls_set   # warn rather than fail — not needed until Session 9
)

# ── MCP Inspector ──────────────────────────────────────────
print("\nMCP Inspector (needed from Session 7)")
try:
    # Only check that npx exists -- running the inspector itself starts a server that never exits.
    result = subprocess.run(
        [shutil.which("npx") or "npx", "--version"],
        capture_output=True, text=True, timeout=30
    )
    check(
        "npx / MCP Inspector accessible",
        result.returncode == 0,
        fix="Install Node.js (LTS) from nodejs.org — npx is included"
    )
except FileNotFoundError:
    check(
        "npx / MCP Inspector accessible",
        False,
        fix="Install Node.js (LTS) from nodejs.org — npx is included"
    )
except Exception as e:
    check("npx / MCP Inspector accessible", False, fix=f"Error: {e}")

# ── Git ────────────────────────────────────────────────────
print("\nGit")
try:
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    check("Git installed", result.returncode == 0, fix="Install Git from git-scm.com")
except FileNotFoundError:
    check("Git installed", False, fix="Install Git from git-scm.com")

# ── Summary ────────────────────────────────────────────────
hard_failures = [(label, fix) for label, passed, fix, warn in results if not passed and not warn]
warnings      = [(label, fix) for label, passed, fix, warn in results if not passed and warn]

print()
print("=" * 57)

if not hard_failures:
    print()
    print("  OK   Setup complete -- you are ready for Session 2!")
    print()
    if warnings:
        print("  One item is optional right now:")
        for label, fix in warnings:
            print(f"    * {label}")
            if fix:
                print(f"      -> {fix}")
        print()
    print("  See you at Session 2. Check WhatsApp for date and time.")
    print()
else:
    print()
    print(f"  {len(hard_failures)} item(s) need attention before Session 2:\n")
    for label, fix in hard_failures:
        print(f"  * {label}")
        if fix:
            print(f"    -> {fix}")
    if warnings:
        print(f"\n  1 optional item (not needed until Session 9):")
        for label, fix in warnings:
            print(f"  * {label}")
    print()
    print("  Fix the above and run this script again.")
    print("  Need help? Post in the WhatsApp group.")
    print()

print("=" * 57)
print()
