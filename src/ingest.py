from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

def create_vectorstore():
    # Kiểm tra OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Vui lòng thiết lập OPENAI_API_KEY")

    # Load tài liệu
    loader = TextLoader("data/python_basics.txt")
    documents = loader.load()
    
    # Chia nhỏ text
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    texts = text_splitter.split_documents(documents)
    
    # Tạo vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    return vectorstore 