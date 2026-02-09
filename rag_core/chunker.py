from rag_core.document import Document
import re

def chunk_document(doc: Document, chunk_size: int = 500, overlap_sentences: int = 2) -> list[Docuemnt]:
    #split text into sentences using a simple regex
    sentences = re.split(r'?<=[.!?]\s+',doc .text) # re.split() → splits the string based on a regex, 
                                                  #(?<=[.!?]) → positive lookbehind: split after ., !, or ?, \s+ → one or more whitespace characters
    chunks = []
    chunk_start_char = 0 # character index of current chunk start in original doc
    i = 0                # sentence index
    
    while i < len (sentences): # stop if reached the last sentece
        chunk_sentences = [] # sentences collected for this chunk
        current_length = 0   # number of characters in the chunk
        start_idx = chunk_start_char   # starting character index for metadata

        while i < len (sentences) and current_length + len(sentences) <= chunk_size: #ensure chunk does not exceed chunk_size
            chunk_sentences.append (sentences[i])
            current_length += len(sentences[i]) + 1 # +1 for space/new line
            i += 1 # move to next sentece

    chunk_text = " ".join(chunk_sentences) # merge sentences into single string for the LLM
    end_idx = start_idx + len(chunk_text)

    chunk_doc = Document (
        text = chunk_text,
        metadata={
            "source" : doc.metadata["source"], # get the name of the source
            "start": start_idx,
            "end": end_idx
        }
    )
    chunks.append(chunk_doc)

    i = max(i - overlap_sentences, 0) # after creating the chunk the counter i moves forward and instead of starting the next chunk exactly where teh last one ended, 
                                      # it steps back by the number of overlap_sentences
    chunk_start_char = end_idx - sum(len(s) + 1 for s in chunk_sentences[-overlap_sentences:] )