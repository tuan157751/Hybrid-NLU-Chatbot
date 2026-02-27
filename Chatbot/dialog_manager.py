# Dialog Manager kiểm tra và xử lý slot
import re

def name_extract(user_input):
    text = user_input.lower()
    match = re.search(r"mình tên là\s+(.+)", text)
    match2 = re.search(r"tôi tên là\s+(.+)", text)
    match3 = re.search(r"tôi là\s+(.+)", text)
    match4 = re.search(r"mình là\s+(.+)", text)
    match5 = re.search(r"mình tên\s+(.+)", text)
    match6 = re.search(r"tôi tên\s+(.+)", text)
    if match:
        name = match.group(1).strip()
    elif match2:
        name = match2.group(1).strip()
    elif match3:
        name = match3.group(1).strip()
    elif match4:
        name = match4.group(1).strip()
    elif match5:
        name = match5.group(1).strip()
    elif match6:
        name = match6.group(1).strip()
    else:
        return None
    return name
def age_extract(user_input):
    text = user_input.lower()
    match = re.search(r"\b(1[01][0-9]|[1-9]?[0-9]|120)\b", text)
    if match:
        age = match.group(1).strip()
    else:
        return None
    return age

def Dialog_manager(user_input, memory, intent, llm_result):
    slots = llm_result["slots"]

    # Chờ name
    waiting = memory.get("waiting_for")
    if waiting == "name":
        name = name_extract(user_input)
        if name:  # None -> False, not None -> True
            memory.update("user_name", name.title())
            memory.update("waiting_for", None)
            return "name_captured"
        else:
            return "name_failed"

    # Chờ age
    if waiting == "age":
        age = age_extract(user_input)
        if age:
            memory.update("age", age)
            memory.update("waiting_for", None)
            return  "age_captured"
        else:
            return "age_failed"

    # Chờ xác nhận đổi tên
    if waiting == "confirm_name_change":
        if intent == "confirm_yes":
            memory.update("user_name", memory.get("pending_name").title())
            memory.update("waiting_for", None)
            memory.update("pending_name", None)
            return "confirm_name_yes"
        elif intent == "confirm_no":
            memory.update("waiting_for", None)
            memory.update("pending_name", None)
            return "confirm_name_no"
        else:
            return "confirm_unknown"

    # fallback logic
    if waiting == "fallback_choice":
        choice = user_input.strip()
        mapping = {
            "1": "greeting",
            "2": "introduce_age",
            "3": "ask_ai"
        }

        if choice in mapping:
            memory.update("waiting_for", None)
            return mapping[choice]
        else:
            return "fallback_repeat"


    # đủ slot → update memory
    if slots:
        for slot, value in slots.items():
            memory.update(slot, value)
    return None