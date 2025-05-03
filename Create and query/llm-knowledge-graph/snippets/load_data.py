from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

DOCS_PATH = "llm-knowledge-graph/data"

loader = DirectoryLoader(DOCS_PATH, glob="Stock.pdf", loader_cls=PyPDFLoader)

docs = loader.load()