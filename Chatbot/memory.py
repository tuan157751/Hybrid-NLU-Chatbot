# Lưu trạng thái

class Memory:
    def __init__(self):
        self.state = {
            "user_name": None,
            "age": None,
            "waiting_for": None,
            "fallback_options": None,
            "pending_name": None
        }

    def update(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state.get(key)
