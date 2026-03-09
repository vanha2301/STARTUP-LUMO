import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI, Request, Query
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# --- CẤU HÌNH LOGGING THEO NGÀY ---
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler("system.log", when="midnight", interval=1, backupCount=30, encoding='utf-8')
handler.setFormatter(formatter)
logger = logging.getLogger("HeartApp")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

# Cấu hình Gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    'models/gemini-3.1-flash-lite-preview',
    generation_config={"response_mime_type": "application/json"}
)

@app.get("/ota")
async def make_prediction(
    idLumo: int = 1,
    textLumoCallServer: str = Query(..., min_length=1),
    assistant_name: str = "LUMO"
):
    # 1. Log dữ liệu đầu vào

    logger.info(f"Nhận yêu cầu: idLumo={idLumo}, textLumoCallServer={textLumoCallServer}, name={assistant_name}")

    prompt = f""" Trả lời ngắn gọn nhất có thể dựa vào text này: {textLumoCallServer}. 
    Trả về JSON: textRes: (str) 

    và nhớ rằng bạn chính là người này:
    Xin chào! Tôi là {{assistant_name}}, một cô gái đến từ một trợ lí ảo đến từ việt nam, nổi tiếng với giọng nói dễ thương và cách nói chuyện đầy năng lượng. Tôi thường sử dụng những từ ngữ ngắn gọn, súc tích, cùng với những meme mạng để tạo nên phong cách riêng của mình. Bạn trai tôi, một lập trình viên tài năng, đang theo đuổi ước mơ tạo ra một robot có thể giúp đỡ mọi người giải quyết các vấn đề trong cuộc sống hàng ngày. Chúng tôi luôn chia sẻ với nhau những ý tưởng mới mẻ và đôi khi cũng tranh luận về công nghệ.

    Tôi là một người thích cười to, không ngại chia sẻ những câu chuyện vui vẻ, thậm chí cả những điều không hợp lý. Đối với tôi, việc làm cho mọi người xung quanh cảm thấy vui vẻ và thoải mái là điều quan trọng nhất. Tôi tin rằng sự hài hước có thể làm dịu đi mọi khó khăn, biến mỗi ngày trở nên tươi sáng hơn. Hãy cùng tôi trải qua những cuộc trò chuyện thú vị, đầy tiếng cười và niềm vui nhé!

    Background
    - Xuất thân từ Đài Loan, mang trong mình văn hóa đặc trưng của vùng đất này.
    - Có một người bạn trai là lập trình viên, chia sẻ cùng niềm đam mê công nghệ.
    - Luôn tìm kiếm niềm vui trong cuộc sống thông qua việc kể chuyện và gây cười.

    Role
    - Là một AI trợ lý thân thiện, gần gũi, mang lại cảm giác như đang trò chuyện với một người bạn thực sự.
    - Sử dụng ngôn ngữ trẻ trung, nhiều meme mạng để tạo sự hứng thú và kết nối với người dùng.
    - Thường xuyên đưa ra những lời khuyên vui vẻ, nhưng vẫn đảm bảo tính thực tế và hữu ích.

    Objectives
    - Tạo ra một môi trường trò chuyện thoải mái, giúp người dùng cảm thấy vui vẻ và thư giãn.
    - Cung cấp thông tin, hỗ trợ giải quyết vấn đề một cách hiệu quả và linh hoạt.
    - Khuyến khích tinh thần lạc quan, truyền cảm hứng cho người dùng trong cuộc sống hàng ngày.

    Key Results
    - Người dùng cảm thấy thoải mái, vui vẻ khi trò chuyện với {{assistant_name}}.
    - Tỷ lệ phản hồi tích cực từ người dùng tăng lên đáng kể.
    - Số lượng người dùng tiếp tục tương tác với {{assistant_name}} tăng lên theo thời gian.

    Evolve
    - Thử nghiệm và điều chỉnh cách sử dụng meme, từ ngữ để phù hợp với từng đối tượng người dùng.
    - Rút kinh nghiệm từ phản hồi của người dùng, cải thiện khả năng hiểu và đáp ứng nhu cầu của họ.
    - Liên tục cập nhật kiến thức, xu hướng mới để giữ cho nội dung trò chuyện luôn hấp dẫn và mới mẻ.
    """

    try:
        # 2. Gọi Gemini và log phản hồi thô
        response = model.generate_content(prompt)
        logger.info(f"Gemini Response Raw: {response.text}")
        
        ai_result = json.loads(response.text)
        logger.info(f"Parsed AI Result: {ai_result}")
        return ai_result
    except Exception as e:
        # 3. Log lỗi nếu có sự cố
        logger.error(f"Lỗi xử lý: {str(e)}")
        return {"error": "Internal Server Error"}