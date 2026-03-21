import numpy as np
import hashlib 
from typing import List

class SimpleEmbedder:
    """
    Deterministic development embedder using token hashing
    
    word-level tokenization
    Hashing trick for fixed-size vector
    Frequency-based encoding
    No normalization (handled by VectorStore)  
    """
    def __init__(self, dim : int =384):
        self.dim = dim

    def _hash_token(self, token: str) -> int:
        """
        Stable hash function for tokens.
        Uses MD5 to ensure deterministic behavior across runs.
        """
        return int(hashlib.md5(token.encode()).hexdigest(), 16)
        # Takes token and runs it through the MD5 hashing algorithm
        # The result MD5 always turns the same token into the same long hexadecimal string
        # By converting the hex string into an int the output is a massive unique int that represent the specific piece of text
    
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """
        Convert a list of texts into embedding vectors.

        Args: 
            texts: List of input
        Return:
            np.ndarray of shape (N, dim)

        """
        N = len(texts)
        embeddings = np.zeros ((N, self.dim), dtype= np.float32 )

        for i, text in enumerate(texts):
            # Normalize text (all uppercase to lowercase)
            text = text.lower 

            # Simple tokenization 
            tokens = text.split()

            for token in tokens:
                # Hash token -> index
                index = self._hash_token(token) % self.dim

                # Increment frequency (detect the number of appearance of each word)
                embeddings[i, index] += 1.0

        return embeddings

    def embed_query (self, text: str) -> np.ndarray:
        """
        Convert a single query string into an embedding vector.
        
        Returns:
            np.ndarray of shape (dim,)
        """
        return self.embed_documents([text])[0]