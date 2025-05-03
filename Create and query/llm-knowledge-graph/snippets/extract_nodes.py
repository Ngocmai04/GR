import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from chunk_data import chunks_dataa  # Đảm bảo hàm chunks_dataa được định nghĩa và hoạt động
from vectorize_data import store_chunks_in_graph  # Đảm bảo hàm này trả về dữ liệu hợp lệ

# Tải biến môi trường từ tệp .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Khóa API OpenAI chưa được thiết lập trong biến môi trường hoặc tệp .env.")

# Khởi tạo mô hình GPT từ OpenAI
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-4",
   
)

# Tạo bộ chuyển đổi tài liệu thành đồ thị
doc_transformer = LLMGraphTransformer(llm=llm)
chunks=chunks_dataa()  # Lấy dữ liệu từ hàm chunks_dataa
store_chunks_in_graph()  
# Xử lý từng chunk
for chunk in chunks:
        graph_docs = doc_transformer.convert_to_graph_documents([chunk])
        for doc in graph_docs:
            print(doc)  # In hoặc lưu kết quả của graph_docs
  