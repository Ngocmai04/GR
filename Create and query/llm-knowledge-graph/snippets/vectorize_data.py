import os
from langchain_openai import OpenAIEmbeddings
from langchain_neo4j import Neo4jGraph
from chunk_data import chunks_dataa
chunks = chunks_dataa()
def store_chunks_in_graph():
    """
    # Khởi tạo OpenAI embedding provider
    embedding_provider = OpenAIEmbeddings(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        model="text-embedding-ada-002"
    )

    # Kết nối tới cơ sở dữ liệu Neo4j
    graph = Neo4jGraph(
        url=os.getenv('NEO4J_URI'),
        username=os.getenv('NEO4J_USERNAME'),
        password=os.getenv('NEO4J_PASSWORD')
    )

    # Lưu trữ các đoạn văn bản trong cơ sở dữ liệu đồ thị
    for chunk in chunks:
        # Lấy tên file từ metadata
        filename = os.path.basename(chunk.metadata["source"])

        # Tạo một định danh duy nhất cho đoạn văn bản
        chunk_id = f"{filename}.{chunk.metadata['page']}"

        # Tạo embedding cho đoạn văn bản
        chunk_embedding = embedding_provider.embed_query(chunk.page_content)

        # Định nghĩa thuộc tính của nút
        properties = {
            "filename": filename,
            "chunk_id": chunk_id,
            "text": chunk.page_content,
            "embedding": chunk_embedding
        }

        # Thêm nút Document và Chunk vào đồ thị
        graph.query("""
            MERGE (d:Document {id: $filename})
            MERGE (c:Chunk {id: $chunk_id})
            SET c.text = $text
            MERGE (d)<-[:PART_OF]-(c)
            WITH c
            CALL db.create.setNodeVectorProperty(c, 'textEmbedding', $embedding)
        """, properties)

    # Tạo vector index cho các đoạn văn bản
    graph.query("""
        CREATE VECTOR INDEX `vector`
        FOR (c: Chunk) ON (c.embedding)
        OPTIONS {indexConfig: {
        `vector.dimensions`: 1536,
        `vector.similarity_function`: 'cosine'
        }};
    """)

# Gọi hàm nếu cần
# store_chunks_in_graph()
