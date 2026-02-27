# Nơi chạy chatbot
from intent_router import intent_detect
from memory import Memory
from rules import handle_intent
from dialog_manager import Dialog_manager
from llm import RealLLM, decide_intent

memory = Memory()

def run_chatbot():
    memory = Memory()
    print("NPC Chatbot đã sẵn sàng!")

    while True:
        user_input = input("Bạn: ")
        llm_result = decide_intent(user_input, memory)

        # Kiểm tra nếu dialog manager đang waiting = đang chờ nhận slots (câu trả lời) -> xét intent theo rule-base, nếu không waiting = người dùng hỏi, nói gì đó -> gọi LLM đoán intent
        if memory.get("waiting_for") is None:
            intent = llm_result["intent"]
        else:
            intent = intent_detect(user_input, memory)

        # Truyền intent vừa có, input và memory vào dialog manager để kiểm tra có đang waiting slots không, nếu có -> xử lý, trả về intent mới

        dialog_intent = Dialog_manager(user_input, memory, intent, llm_result)
        if dialog_intent:
            intent = dialog_intent

        # Nhận intent phía trên, input và memory, đối chiếu với rules để xuất text response
        response = handle_intent(intent, user_input, memory)
        if response:
            print("Bot:", response)

        if intent == "goodbye":
            break

run_chatbot()

