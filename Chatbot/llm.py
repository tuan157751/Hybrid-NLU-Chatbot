#Real LLM
import requests
import json
from intent_router import intent_detect


class RealLLM():
    def __init__(self, model = "llama3"):
        self.model = model

    def analyze(self, user_input):
        prompt = f"""
        Bạn là bộ phân tích ngôn ngữ tiếng Việt.

        Nhiệm vụ:
        - Xác định ý định (intent) của người dùng
        - Trích xuất thông tin (slots) nếu có
        
        Các intent hợp lệ:
        - greeting
        - introduce_name
        - introduce_age
        - ask_ai
        - goodbye
        - unknown
        
        CHỈ trả về JSON hợp lệ, không giải thích.
        Output JSON gồm:
        {{
          "intent": 
          "slots": 
          "confidence":
        }}
        
        Input: "{user_input}"
        """
        response = requests.post(
            "http://localhost:11434/api/generate",
            json = {
                "model" : self.model,
                "prompt" : prompt,
                "stream": False,
                "format": "json"
            }
        )

        try:
            result = response.json()["response"]
            parsed = json.loads(result)
            #print("RAW LLM RESPONSE:")
            #print(response.json())
        except:
            return {
                "intent": "unknown",
                "slots": {},
                "confidence": 0.0
            }
        return {
            "intent": parsed.get("intent", "unknown"),
            "slots": parsed.get("slots", {}),
            "confidence": parsed.get("confidence", 0.5)
        }

def is_valid_nlu_input(text):
    text = text.strip()
    text = text.lower()

    # quá ngắn
    if len(text) <= 2 and text != "hi":
        return False

    # không có chữ cái
    if not any(c.isalpha() for c in text):
        return False
    return True

def decide_intent(user_input, memory):
    #0 Input gate
    if not is_valid_nlu_input(user_input):
        return {
            "intent": "fallback",
            "slots": {},
            "confidence": 1.0,
            "source": "rule"
        }

    #1: Kiểm tra rule-base intent trước
    rule_result = intent_detect(user_input, memory)
    if rule_result != "unknown":
        return {
            "intent": rule_result,
            "slots": {},
            "confidence": 1.0,
            "source": "rule"
        }


    #2: Nếu rule-base không khớp -> gọi LLM check intent
    llm = RealLLM()
    llm_result= llm.analyze(user_input)

    #3: Kiểm tra kết quả json trả về (Validation)
    intent = llm_result.get("intent", "unknown")
    slots = llm_result.get("slots", {})
    confidence = llm_result.get("confidence", 0.0)


    # Quy ước slot trong intent
    INTENT_SLOT_RULES = {
        "introduce_age": ["age"],
        "introduce_name": ["name"],
        "ask_ai": [],
        "greeting": [],
        "goodbye": [],
    }


    # Slot validation: kiểm tra slots có khác với quy ước không
    allowed_slots = INTENT_SLOT_RULES.get(intent, [])
    valid_slots = {}
    invalid_slots = {}
    missing_slots = []

    for slot, value in slots.items():
        if slot in allowed_slots:
            valid_slots[slot] = value   # tìm thấy slot đúng theo quy ước intent_slot_rules -> thêm vào dict clean_slots
        else:
            invalid_slots[slot] = value  # Slots dư, trống hoặc sai quy ước -> thêm vào dict invalid_slots


    # TH1: Nếu invalid_slots không rỗng -> slot bị sai, dư -> Giữ intent, giảm confidence
    if invalid_slots:
        llm_result["confidence"] *= 0.5

    # TH2: Nếu slot thiếu -> hỏi lại
    for s in allowed_slots:
        if s not in valid_slots:
            missing_slots.append(s)


    #Th3: Slots đủ -> upload memory từ slot
    for k, v in valid_slots.items():
        memory.update(k, v)

    # Confidence check và fallback (phương án dự phòng khi hệ thống KHÔNG chắc mình hiểu đúng người dùng) khi confidence thấp
    if llm_result["confidence"] < 0.6 or llm_result["intent"] == "unknown":
        return {
            "intent": "fallback",
            "slots": {},
            "confidence": 1.0,
            "source": "llm"
        }

    return {
            "intent": intent,
            "slots": slots,
            "confidence": confidence,
            "source": "llm"
    }

