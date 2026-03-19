import docx
import pdfplumber


def extract_text_docx(path: str) -> str:
    """Extract plain text from a Word document.

    Args:
        path: Path to a .docx file.

    Returns:
        The document's text content as a single string.
    """
    doc = docx.Document(path)
    return "\n".join(para.text for para in doc.paragraphs)


def extract_text_pdf(path: str) -> str:
    """Extract plain text from a PDF document.

    Args:
        path: Path to a .pdf file.

    Returns:
        The document's text content as a single string.
    """
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages)


def extract_text(path: str) -> str:
    """Extract plain text from a .docx or .pdf file.

    Args:
        path: Path to a .docx or .pdf file.

    Returns:
        The document's text content as a single string.

    Raises:
        ValueError: If the file extension is not supported.
    """
    if path.endswith(".docx"):
        return extract_text_docx(path)
    if path.endswith(".pdf"):
        return extract_text_pdf(path)
    raise ValueError(f"Unsupported file type: {path}")
