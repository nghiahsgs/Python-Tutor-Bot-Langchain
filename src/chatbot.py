from langchain_community.chat_models import ChatOpenAI  # Updated import
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class PythonTutor:
    def __init__(self, vectorstore):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            verbose=True
        )
    
    def ask(self, question: str) -> str:
        try:
            response = self.chain({"question": question})
            return response["answer"]
        except Exception as e:
            return f"Xin lỗi, có lỗi xảy ra: {str(e)}" 