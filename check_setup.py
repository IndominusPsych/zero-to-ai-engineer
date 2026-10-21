"""Checks that every tool and package used in the course is installed."""
import importlib
import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv

PACKAGES = {
    "Month 1": ["numpy", "pandas", "matplotlib", "sklearn", "joblib", "requests", "dotenv", "pydantic", "pytest"],
    "Month 2": ["anthropic", "tiktoken", "sentence_transformers", "chromadb", "rank_bm25", "pypdf", "streamlit"],
    "Month 3": ["langchain", "langchain_anthropic", "langgraph", "feedparser", "mcp", "apscheduler",
                "fastapi", "uvicorn", "pydantic_settings", "httpx"],
}
TOOLS = {"git": "Lesson 03", "gh": "optional, Lesson 03/17", "node": "Lesson 15 (MCP Inspector)",
         "docker": "optional, Lesson 16"}

ok = True
print(f"Python {sys.version.split()[0]}", "OK" if sys.version_info >= (3, 12) else "-> please use 3.13 or 3.14")
for month, names in PACKAGES.items():
    print(f"\n{month}")
    for name in names:
        try:
            mod = importlib.import_module(name)
            print(f"  OK       {name} {getattr(mod, '__version__', '')}")
        except ImportError:
            ok = False
            print(f"  MISSING  {name}")

print("\nCommand-line tools")
for tool, where in TOOLS.items():
    path = shutil.which(tool)
    version = subprocess.run([tool, "--version"], check=False, capture_output=True, text=True).stdout.split("\n")[0] if path else ""
    print(f"  {'OK      ' if path else 'MISSING '} {tool:7} {version}  ({where})")

print("\nAPI key")
load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY", "")
print("  OK       ANTHROPIC_API_KEY found" if key.startswith("sk-ant-") else "  MISSING  ANTHROPIC_API_KEY (needed from Lesson 08)")

print("\nAll Python packages installed!" if ok else "\nSome packages are missing: see 00_SETUP_Install_Guide.md")
