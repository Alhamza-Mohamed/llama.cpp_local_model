from rag_core.document import Document

doc = Document(
    text="sky is blue",
    metadata = {
    "source":"sample.txt",
    "start":4,
    "end":15
    }
)

print (doc)