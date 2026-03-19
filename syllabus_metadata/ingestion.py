import docx


def extract_text_docx(path: str) -> str:
    """Extract plain text from a Word document.

    Args:
        path: Path to a .docx file.

    Returns:
        The document's text content as a single string.
    """
    doc = docx.Document(path)
    return "\n".join(para.text for para in doc.paragraphs)
