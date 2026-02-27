from dialog_manager import name_extract, age_extract

class MockLMM:
    def analyze(self, text):
        text = text.lower()

        result = {
            "intent" : None,
            "slots": {},
            "confidence": 0.0
        }

        if any(x in text for x in ["tên", "mình là", 'tôi là']):
            result["intent"] = "introduce_name"
            result["confidence"] = 0.9

        elif any(x in text for x in ["tuổi", "năm nay"]):
            result["intent"] = "introduce_age"
            result["confidence"] = 0.9

        elif any(x in text for x in ["chào", "hello", "hi"]):
            result["intent"] = "greeting"
            result["confidence"] = 0.9

        elif any(x in text for x in ["bye", "tạm biệt"]):
            result["intent"] = "goodbye"
            result["confidence"] = 0.9

        else:

            result["intent"] = "unknown"
            result["confidence"] = 0.3

        name = name_extract(text)
        if name:
            result["slots"]["name"] = name.title()
        age = age_extract(text)
        if age:
            result["slots"]["age"] = age

        return result

