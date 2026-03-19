import json
import os
import urllib.request

import boto3

BEDROCK_DEFAULT_REGION = "us-east-1"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:latest"
BEDROCK_MODEL = "us.anthropic.claude-sonnet-4-6"


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


def _dispatch(prompt: str, backend: str) -> str:
    if backend == "bedrock":
        return _call_bedrock(prompt)
    return _call_ollama(prompt)


def query_llm(prompt: str, backend: str = "ollama") -> str:
    """Submit a prompt to the LLM and return the response.

    Args:
        prompt: The prompt string to send to the LLM.
        backend: Which LLM backend to use: "ollama" (default) or "bedrock".

    Returns:
        The LLM's response as a string.
    """
    return _dispatch(prompt, backend)


def extract_citations(prompt: str, doc_text: str, backend: str = "ollama") -> str:
    """Extract bibliographic citations from document text.

    Args:
        prompt: Instructions telling the LLM what to extract and how to format output.
        doc_text: The plain text of the syllabus document.
        backend: Which LLM backend to use: "ollama" (default) or "bedrock".

    Returns:
        TSV-formatted citation data as returned by the LLM.
    """
    return _dispatch(f"{prompt}\n\n{doc_text}", backend)
