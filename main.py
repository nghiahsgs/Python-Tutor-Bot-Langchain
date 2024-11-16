import os
from src.ingest import create_vectorstore
from src.chatbot import PythonTutor

def main():
    try:
        # Khởi tạo vector store
        print("Đang khởi tạo chatbot...")
        vectorstore = create_vectorstore()
        
        # Khởi tạo chatbot
        tutor = PythonTutor(vectorstore)
        
        print("\nPython Tutor Bot (gõ 'quit' để thoát)")
        print("----------------------------------------")
        
        while True:
            user_input = input("\nBạn: ").strip()
            if user_input.lower() == 'quit':
                print("\nTạm biệt! Hẹn gặp lại!")
                break
                
            if user_input:
                response = tutor.ask(user_input)
                print(f"\nTutor: {response}")
            
    except Exception as e:
        print(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    main() 