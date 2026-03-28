from typing import List, Dict

class Pipeline:
    def __init__(self, embedder, retriever, prompt_builder, llm ):
        self.embedder  = embedder
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm  
         
    def run(self, query: str, top_k: int = 5) -> str:
        # 1- Embed query
        query_vector = self.embedder.embed(query)

        # 2- Retrieve relevant documents
        documents = self.retriever.retrieve(query_vector,top_k = top_k)

        # 3- Build message
        messages = self.prompt_builder.build(query, documents)

        # 4. Generate answer from LLM
        answer = self.llm.generate(messages)

         # 5. Return final answer
        return answer