from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

def create_vectorstore():
    load_dotenv()
    
    # Kiểm tra OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Vui lòng thiết lập OPENAI_API_KEY")

    # Load tài liệu
    # loader = TextLoader("data/python_basics.txt")
    loader = TextLoader("data/framework_docs.txt")
    documents = loader.load()
    
    # Chia nhỏ text
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    texts = text_splitter.split_documents(documents)
    
    # Tạo vector store với Chroma
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(texts, embeddings)
    
    return vectorstore