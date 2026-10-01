import json
import os
import urllib.request
from pathlib import Path

import boto3
import openai
from dotenv import load_dotenv

BEDROCK_DEFAULT_REGION = "us-east-1"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:latest"
BEDROCK_MODEL = "us.anthropic.claude-sonnet-4-6"
OPENAI_MODEL = "gpt-4o"

CONFIG_PATH = Path("~/.openai").expanduser()
load_dotenv(dotenv_path=CONFIG_PATH)

def _call_ollama(prompt: str) -> str:
    payload = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result["response"]


def _call_bedrock(prompt: str) -> str:
    region = os.environ.get("AWS_DEFAULT_REGION") or BEDROCK_DEFAULT_REGION
    client = boto3.client("bedrock-runtime", region_name=region)
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    response = client.invoke_model(modelId=BEDROCK_MODEL, body=body)
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def _call_openai(prompt: str, api_key: str | None = None) -> str:
    # api_key=None falls back to the OPENAI_API_KEY env variable
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if not (stripped.startswith("```") and stripped.endswith("```")):
        return text
    lines = stripped.split("\n")[1:-1]  # drop the fence lines themselves
    return "\n".join(lines)


def _dispatch(prompt: str, backend: str, api_key: str | None = None) -> str:
    if backend == "bedrock":
        result = _call_bedrock(prompt)
    elif backend == "openai":
        result = _call_openai(prompt, api_key)
    else:
        result = _call_ollama(prompt)
    return _strip_code_fence(result)


def query_llm(prompt: str, backend: str = "openai", api_key: str | None = None) -> str:
    """Submit a prompt to the LLM and return the response.

    Args:
        prompt: The prompt string to send to the LLM.
        backend: Which LLM backend to use: "openai" (default), "bedrock", or "ollama".
        api_key: API key for the "openai" backend. If omitted, falls back to
            the OPENAI_API_KEY env variable. Ignored by other backends.

    Returns:
        The LLM's response as a string.
    """
    return _dispatch(prompt, backend, api_key)


def extract_citations(
    prompt: str, doc_text: str, backend: str = "openai", api_key: str | None = None
) -> str:
    """Extract bibliographic citations from document text.

    Args:
        prompt: Instructions telling the LLM what to extract and how to format output.
        doc_text: The plain text of the syllabus document.
        backend: Which LLM backend to use: "openai" (default), "bedrock", or "ollama".
        api_key: API key for the "openai" backend. If omitted, falls back to
            the OPENAI_API_KEY env variable. Ignored by other backends.

    Returns:
        TSV-formatted citation data as returned by the LLM.
    """
    return _dispatch(f"{prompt}\n\n{doc_text}", backend, api_key)
