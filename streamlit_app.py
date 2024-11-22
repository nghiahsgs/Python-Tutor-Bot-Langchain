import streamlit as st
from src.ingest import create_vectorstore
from src.chatbot import PythonTutor

def initialize_chatbot():
    if 'tutor' not in st.session_state:
        vectorstore = create_vectorstore()
        st.session_state.tutor = PythonTutor(vectorstore)

def initialize_chat_history():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("Andie's Chatbot 🤖")
    
    # Khởi tạo chatbot và lịch sử chat
    initialize_chatbot()
    initialize_chat_history()
    
    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Hãy đặt câu hỏi của bạn"):
        # Hiển thị câu hỏi của user
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hiển thị câu trả lời của bot
        with st.chat_message("assistant"):
            response = st.session_state.tutor.ask(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
    # streamlit run streamlit_app.py