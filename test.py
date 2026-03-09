import requests

# 1. Cấu hình URL và tham số
BASE_URL = "https://lumo.vanha2301.online/ota"

# Đây là các tham số Hà muốn truyền vào dấu ? sau URL
params = {
    "idLumo": 1,
    "textLumoCallServer": "bạn là ai vậy",
    "assistant_name": "LUMO"
}

def test_lumo_api():
    print(f"🚀 Đang gửi yêu cầu tới: {BASE_URL}...")
    
    try:
        # 2. Gửi yêu cầu GET với params
        # requests sẽ tự biến thành: /ota?idLumo=1&textLumoCallServer=b%E1%BA%A1n...
        response = requests.get(BASE_URL, params=params, timeout=10)

        # 3. Kiểm tra mã trạng thái (200 là OK)
        if response.status_code == 200:
            print("✅ Kết quả từ Gemini:")
            print(response.json()) # In ra kết quả JSON nhận được
        else:
            print(f"❌ Lỗi: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"💥 Đã xảy ra lỗi khi kết nối: {str(e)}")

if __name__ == "__main__":
    test_lumo_api()