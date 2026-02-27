# Xác định intent
from mock_lmm import MockLMM


def intent_detect(user_input, memory):
    text = user_input.lower()
    #name
    if memory.get("waiting_for") == "name":
        return "introduce_name"

    #age/name
    if memory.get("waiting_for") == "age":
        return "introduce_age"
    if "tôi năm nay" in text or "mình năm nay" in text:
        return "introduce_age"
    if "tôi tên" in text or "mình tên" in text:
        return "introduce_name"
    if "tên tôi" in text or "tên mình" in text:
        return "introduce_name"

    #greeting
    if "chào" in text or "xin chào" in text:
        return "greeting"

    #goodbye
    if "bye" in text or "tạm biệt" in text:
        return "goodbye"

    #asking
    if "ai là gì" in text:
        return "ask_ai"
    if "ý nghĩa cuộc sống" in text:
        return "life_purpose"

    #confirm
    if "có" in text or "yes" in text:
        return "confirm_yes"
    if "không" in text or "no" in text:
        return "confirm_no"

    else:
        return "unknown"





