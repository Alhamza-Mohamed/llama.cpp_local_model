from dataclasses import dataclass
from typing import Dict

@dataclass
class Document:
    #Represents a single unit of retrievable text
    
    text: str # The actual text content that can be used by the LLM
    metadata: Dict # Dictionary containing tracing/debug info like source filename, start and character positions in the original document.