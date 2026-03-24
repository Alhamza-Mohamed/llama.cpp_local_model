from typing import List, Dict
from rag_core.document import Document

class PromptBuilder:
    def __init__(self, default_instruction: str | None = None):
        self.default_instruction = default_instruction or (
            "You are a helpful assistant. "
            "Answer ONLY using the provided context. "
            "If the answer is not in the context, say you don't know. "
        )
    
    def build (self, query: str, documents: List[Document], instruction: str | None = None
    ) -> List  [Dict[str,  str]]:  
        # Resolve instruction  (default vs override)
        instruction = instruction or self.default_instruction

        system_msg = self._format_instruction(instruction)
        context = self._format_context(documents)
        user_msg =  self._format_user_message(query, context)

        return[system_msg,user_msg]
    
    def _format_instruction(self, instruction: str) -> Dict[str, str]:
        return {
            "role":"system",
            "content":instruction
        }
    
    def _format_context(self, documents: List[Document]) -> str:
        chunks = []

        for i,doc in enumerate(documents, start=1):
            source = doc.metadata.get("source", "unknown")
            start = doc.metadata.get("start", "N/A")
            end = doc.metadata.get("end", "N/A")

            chunk_text = (
                f"[Chunk{i} | Source: {source} |start: {start} | End: {end}] \n"
                f"{doc.text}"
            )

            chunks.append(chunk_text)

        return  "\n\n".join(chunks)

    def _format_user_message(self, query: str, context: str) -> Dict[str,str]:
        content =(
            "Context:\n"
            f"{context}\n\n"
            "Question:\n"
            f"{query}"
        )

        return{
            "role": "user",
            "content": content
        }