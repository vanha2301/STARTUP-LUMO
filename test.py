import re

def get_lumo_history_string(file_path, limit=20):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            log_data = f.read()

        # 1. Trích xuất tất cả câu hỏi của User
        user_queries = re.findall(r"textLumoCallServer=(.*?), name", log_data)
        
        # 2. Trích xuất tất cả phản hồi từ Parsed AI Result
        llm_responses = re.findall(r"Parsed AI Result: \{['\"]textRes['\"]: ['\"](.*?)['\"]\}", log_data)

        # 3. Kết hợp và lấy 20 cặp cuối cùng
        history = list(zip(user_queries, llm_responses))
        latest_history = history[-limit:]

        if not latest_history:
            return ""

        # 4. Gom tất cả thành một chuỗi duy nhất
        history_lines = []
        for user, llm in latest_history:
            history_lines.append(f"user: {user}")
            history_lines.append(f"LLM: {llm}")
        
        # Trả về chuỗi các cặp hội thoại cách nhau bởi dấu xuống dòng
        return "\n".join(history_lines)

    except FileNotFoundError:
        return f"Error: File {file_path} not found."
    except Exception as e:
        return f"Error: {str(e)}"

# --- CÁCH SỬ DỤNG ---

# Bây giờ bạn có thể cộng vào prompt của mình
system_prompt = "Bạn là trợ lý ảo LUMO. Dưới đây là lịch sử trò chuyện gần đây:\n" + get_lumo_history_string("system.log", limit=20)

print(system_prompt)