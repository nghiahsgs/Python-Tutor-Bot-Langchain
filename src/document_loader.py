from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import VectorIndexRetriever
from langchain.schema import BaseRetriever
from langchain.schema.document import Document
from typing import List
import os
from dotenv import load_dotenv

class LlamaIndexRetriever(BaseRetriever):
    """Wrapper để chuyển đổi LlamaIndex retriever sang LangChain retriever"""
    
    def __init__(self, retriever: VectorIndexRetriever):
        super().__init__()
        self._retriever = retriever

    def get_relevant_documents(self, query: str) -> List[Document]:
        nodes = self._retriever.retrieve(query)
        # Chuyển đổi LlamaIndex nodes sang LangChain documents
        docs = [
            Document(
                page_content=node.text,
                metadata=node.metadata
            ) for node in nodes
        ]
        return docs
    
    async def aget_relevant_documents(self, query: str) -> List[Document]:
        # Implement async version nếu cần
        return self.get_relevant_documents(query)

def create_index_from_pdfs(directory_path: str):
    """
    Tạo index từ các file PDF trong thư mục
    """
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Vui lòng thiết lập OPENAI_API_KEY")

    # Đọc tất cả file PDF trong thư mục
    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        filename_as_id=True,
        required_exts=[".pdf"]
    )
    documents = reader.load_data()
    print(f"Đã đọc được {len(documents)} file PDF")
    for doc in documents:
        print(f"- {doc.doc_id}: {len(doc.text)} ký tự")
    
    # Parse documents thành nodes
    parser = SimpleNodeParser.from_defaults(
        chunk_size=1000,
        chunk_overlap=200
    )
    nodes = parser.get_nodes_from_documents(documents)
    
    # Tạo index
    llm = OpenAI(temperature=0.7, model="gpt-3.5-turbo")
    index = VectorStoreIndex(
        nodes,
        llm=llm
    )
    
    return index

def get_retriever_from_index(index):
    """
    Tạo retriever từ index để sử dụng với LangChain
    """
    retriever = index.as_retriever(
        similarity_top_k=3
    )
    return LlamaIndexRetriever(retriever)