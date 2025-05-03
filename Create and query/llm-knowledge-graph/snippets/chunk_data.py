import os
from load_data import load_documents
from langchain.text_splitter import CharacterTextSplitter


# Tải tài liệu
docs = load_documents()

# Kiểm tra nếu docs được tải thành công
if not docs:
    raise ValueError("No documents loaded. Check DOCS_PATH in load_data.py.")

def chunks_dataa():
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1500,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


# This code splits the text into paragraphs (every time there is a double newline \n\n).