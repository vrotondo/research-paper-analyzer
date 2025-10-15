"""
Utility helper functions
"""
import os
from typing import List


def ensure_dir(directory: str) -> None:
    """Create directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def format_citations(sources: List[str]) -> str:
    """Format a list of sources into citation format"""
    if not sources:
        return "No sources provided"
    
    citations = []
    for i, source in enumerate(sources, 1):
        citations.append(f"[{i}] {source}")
    
    return "\n".join(citations)