from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory

class PythonTutor:
    def __init__(self, retriever):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
        
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True,
            k=3
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            verbose=True,
            return_source_documents=True
        )
    
    def ask(self, question: str) -> str:
        try:
            response = self.chain.invoke({"question": question})
            
            # In ra các documents được sử dụng
            print("\nDocuments used for context:")
            for doc in response["source_documents"]:
                print("-" * 40)
                print(doc.page_content)
            
            return response["answer"]
        except Exception as e:
            return f"Xin lỗi, có lỗi xảy ra: {str(e)}"