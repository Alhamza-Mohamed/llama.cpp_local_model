import numpy as np
import hashlib 

class SimpleEmbedder:
    def __init__(self, dim : int =384):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            hash_value = int(hashlib.md5(text.encode()).hexdigest(), 16) 
            # Takes text and runs it through the MD5 hashing algorithm
            # The result MD% always turns the same text into the same long hexadecimal string
            # By converting the hex string into an int the output is a massive unique int that represetn the specific piece of text

            rng = np.random.default_rng(hash_value) # Create a new random number generator (rng), but it uses the hash_value as the seed
                                                    # if the same seed is used then we get the exact same "random" numbers everytime

            vector = rng.normal(size = self.dim) # It draws dim (default 384) numbers from a normal distribution (bell curve)
                                                 # the result is  a list of 384 numbers that look like random noise, but are uniquely tied to the input text  
            embeddings.append(vector.tolist()) # converts the numpy array into standard python list of floats adn add it to the embiddigns
        return embeddings