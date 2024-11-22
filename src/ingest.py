from src.document_loader import create_index_from_pdfs, get_retriever_from_index

def create_vectorstore():
    # Tạo index từ thư mục chứa PDF
    index = create_index_from_pdfs("data/pdfs")
    
    # Trả về retriever để sử dụng với LangChain
    return get_retriever_from_index(index)