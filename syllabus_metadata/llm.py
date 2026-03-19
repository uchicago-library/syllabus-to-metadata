import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:latest"


def _call_ollama(prompt: str) -> str:
    payload = json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result["response"]


def query_llm(prompt: str) -> str:
    """Submit a prompt to the LLM and return the response.

    Args:
        prompt: The prompt string to send to the LLM.

    Returns:
        The LLM's response as a string.
    """
    return _call_ollama(prompt)


def extract_citations(prompt: str, doc_text: str) -> str:
    """Extract bibliographic citations from document text.

    Args:
        prompt: Instructions telling the LLM what to extract and how to format output.
        doc_text: The plain text of the syllabus document.

    Returns:
        TSV-formatted citation data as returned by the LLM.
    """
    return _call_ollama(f"{prompt}\n\n{doc_text}")
