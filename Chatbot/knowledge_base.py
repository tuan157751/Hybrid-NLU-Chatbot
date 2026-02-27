# Kho tri thức


KNOWLEDGE = {
    "game_ai": "Game AI là hệ thống điều khiển hành vi NPC như tìm đường, chiến đấu, đối thoại.",
    "npc": "NPC là nhân vật không do người chơi điều khiển.",
    "ai": "AI là hệ thống mô phỏng hành vi thông minh của con người.",
    "life_purpose": "Cuộc sống vốn không có ý nghĩa nào cả, vì vậy điều duy nhất bạn có thể làm để vui vẻ đó là theo đuổi điều mình thích và thưởng thức vẻ đẹp của nó mà thôi"
}

def search_knowledge(keyword):
    return KNOWLEDGE.get(keyword, None)