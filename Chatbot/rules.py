# Rule-based câu trả lời

from knowledge_base import *
from memory import Memory
from    dialog_manager import Dialog_manager, name_extract, age_extract


def handle_intent(intent, userinput, memory):
    # greeting
    if intent == "greeting":
        if memory.get("user_name"):
            print( f"Bot: Chào {memory.state['user_name']}")

        else:
            memory.update("waiting_for", "name")
            return "Chào bạn! Mình chưa biết tên bạn, bạn tên là gì?"

    # name introduce
    if intent == "introduce_name":
        new_name = name_extract(userinput)
        if new_name:
            if memory.get("user_name") is None:
                memory.update("user_name", new_name)
                return f"Chào {new_name} nha 😄"

            if memory.get("user_name") and memory.get("user_name") != new_name.title():
                memory.update("waiting_for", "confirm_name_change")
                memory.update("pending_name", new_name.title())
                return f"Mình đang nhớ bạn tên là {memory.get("user_name")}, bạn có muốn đổi qua {memory.get("pending_name")} không?"
        else:
            memory.update("waiting_for", "name")
            return "Mình chưa nghe rõ tên bạn, bạn nói lại giúp mình nhé 🙂"

    # age introduce
    if intent == "introduce_age":
        if memory.get("age"):
            print( f"Bot: Bạn năm nay {memory.state['age']} tuổi")
        else:
            memory.update("waiting_for", "age")
            return "Mình chưa biết tuổi của bạn, bạn cho mình biết được không?"

    # getting user's name and age
    if intent == "name_captured":
        return f"Rất vui được gặp bạn, {memory.get("user_name")} 😄"
    if intent == "name_failed":
        return "Mình chưa nghe rõ tên bạn, nói lại giúp mình nhé 🙂"
    if intent == "age_captured":
        return f"Đã hiểu, bạn năm nay {memory.get("age")} tuổi 😄"
    if intent == "age_failed":
        return "Mình chưa nghe rõ tuổi của bạn, nói lại giúp mình nhé 🙂"

    # name change confirm
    if intent == "confirm_name_yes":
        return f"OK! Từ giờ mình sẽ gọi bạn là {memory.get("user_name")}."
    if intent == "confirm_name_no":
        return f"OK! Mình vẫn sẽ gọi bạn là {memory.get("user_name")}."
    if intent == "confirm_unknown":
        return "Bạn chỉ cần trả lời *có* hoặc *không* thôi nha 🙂"

    # Answer user questions
    if intent == "ask_ai":
        return search_knowledge("ai")
    if intent == "life_purpose":
        return search_knowledge("life_purpose")

    # unknown input
    # if intent == "unknown":
    #     memory.update("waiting_for", "fallback_choice")
    #     return

    # fallbace logic
    if intent == "fallback":
        memory.update("waiting_for", "fallback_choice")
        return (
            "Bot: Mình chưa chắc đã hiểu 🤔\n"
            "1️⃣ Giới thiệu tên\n"
            "2️⃣ Nói tuổi\n"
            "3️⃣ Hỏi về AI"
        )

    if intent == "fallback_repeat":
        return (
            "Mình chưa hiểu lựa chọn 😅\n"
            "1️⃣ Giới thiệu tên\n"
            "2️⃣ Nói tuổi\n"
            "3️⃣ Hỏi về AI"
        )

    #goodbye
    if intent == "goodbye":
        return "Tạm biệt! Hẹn gặp lại 🎮"

