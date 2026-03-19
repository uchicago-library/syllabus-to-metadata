import sys

from syllabus_metadata import query_llm


def read_prompt(path: str) -> str:
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    # TODO: at a later time, when we're finessing this code,
    # reconsider defaulting to "prompt.txt"
    prompt_file = sys.argv[1] if len(sys.argv) > 1 else "prompt.txt"
    prompt = read_prompt(prompt_file)
    print(query_llm(prompt))
