import os
import google.generativeai as genai
from dataclasses import dataclass

@dataclass
class Flashcard:
    front: str  # Question/term
    back: str  # Answer/definition


def setup_gemini_model(api_key=None):
    """
    Set up and configure the Gemini model

    Args:
        api_key: Optional API key provided by the user

    Returns:
        The configured Gemini model
    """
    # Use the provided API key, or try to get it from environment variables
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("Google API Key is required")

    genai.configure(api_key=api_key)

    # Return the generative model
    return genai.GenerativeModel("gemini-2.0-flash")


def get_sample_flashcards(subject):
    """
    Create sample flashcards when Gemini generation fails

    Args:
        subject: The subject/topic entered by the user

    Returns:
        List of sample flashcard objects
    """
    sample_cards = [
        Flashcard(
            f"{subject} là gì?",
            f"{subject} là một lĩnh vực học tập bao gồm nhiều khái niệm và nguyên lý khác nhau.",
        ),
        Flashcard(
            f"Ai là người tiên phong trong {subject} hiện đại?",
            f"Nhiều nhân vật quan trọng đã đóng góp vào sự phát triển của {subject} thông qua các nghiên cứu và lý thuyết đột phá.",
        ),
        Flashcard(
            f"Những nguyên lý chính của {subject} là gì?",
            f"Các nguyên lý chính bao gồm những lý thuyết và thực hành cơ bản tạo nên nền tảng của {subject}.",
        ),
        Flashcard(
            f"{subject} được áp dụng như thế nào trong thực tế?",
            f"{subject} được áp dụng trong nhiều ngành công nghiệp và bối cảnh khác nhau để giải quyết vấn đề và cải thiện quy trình.",
        ),
        Flashcard(
            f"Tương lai của {subject} như thế nào?",
            f"Tương lai của {subject} bao gồm các công nghệ mới nổi và phương pháp tiến hóa sẽ định hình sự phát triển của nó.",
        ),
        Flashcard(
            f"Định nghĩa phạm vi của {subject}",
            f"Phạm vi của {subject} bao gồm khung lý thuyết, ứng dụng thực tiễn và các kết nối liên ngành.",
        ),
        Flashcard(
            f"Những thách thức nào tồn tại trong {subject} ngày nay?",
            f"Các thách thức hiện tại trong {subject} bao gồm hạn chế về công nghệ, cân nhắc đạo đức và rào cản triển khai.",
        ),
        Flashcard(
            f"{subject} đã phát triển như thế nào theo thời gian?",
            f"{subject} đã phát triển thông qua nhiều thay đổi mô hình và đổi mới đã tái định nghĩa các khái niệm cốt lõi.",
        ),
        Flashcard(
            f"Những kỹ năng nào cần thiết để xuất sắc trong {subject}?",
            f"Để xuất sắc trong {subject} cần có tư duy phân tích, khả năng giải quyết vấn đề và kiến thức chuyên ngành.",
        ),
        Flashcard(
            f"Các chuyên gia đánh giá thành công trong {subject} như thế nào?",
            f"Thành công trong {subject} thường được đo lường thông qua các chỉ số đã thiết lập, kết quả đạt được và đánh giá tác động.",
        ),
    ]

    return sample_cards


def generate_flashcards(
    content,
    subject,
    num_cards=10,
    api_key=None,
    use_sample_on_error=False,
    use_local_model=True,
):
    """
    Generate flashcards using various AI models (Gemini, Local AI, or rule-based)

    Args:
        content (str): The educational content to convert to flashcards
        subject (str): The subject or topic of the content
        num_cards (int): Number of flashcards to generate
        api_key (str, optional): Google API key for Gemini model
        use_sample_on_error (bool): Whether to return sample cards on error
        use_local_model (bool): Whether to try local AI models first

    Returns:
        list: List of Flashcard objects
    """
    # Thử local model trước nếu được bật
    # Thử Gemini nếu có API key
    if api_key or os.getenv("GOOGLE_API_KEY"):
        try:
            return generate_flashcards_gemini(content, subject, num_cards, api_key)
        except Exception as e:
            print(f"Gemini failed: {e}")

    # Fallback về sample cards
    if use_sample_on_error:
        return get_sample_flashcards(subject)[:num_cards]
    else:
        raise Exception("Không thể tạo thẻ ghi nhớ với bất kỳ phương pháp nào")


def generate_flashcards_gemini(content, subject, num_cards=10, api_key=None):
    """
    Generate flashcards specifically using Google's Gemini model
    """
    try:
        model = setup_gemini_model(api_key)
        # Prompt engineering for better results
        prompt = f"""
        Tạo {num_cards} thẻ ghi nhớ học tập chi tiết về {subject} dựa trên nội dung sau. 
        Cho mỗi thẻ ghi nhớ, hãy tạo:
        1. Một câu hỏi hoặc thuật ngữ rõ ràng, ngắn gọn ở mặt trước
        2. Một câu trả lời hoặc định nghĩa đầy đủ ở mặt sau
        
        Đảm bảo các thẻ ghi nhớ:
        - Bao quát những khái niệm quan trọng nhất từ nội dung
        - Có tính giáo dục và chính xác
        - Bao gồm các thuật ngữ chính, định nghĩa và giải thích
        - Đa dạng về độ khó và loại câu hỏi
        
        Nội dung cần phân tích:
        {content}
        
        Định dạng đầu ra:
        THẺ 1
        Mặt trước: [Câu hỏi hoặc thuật ngữ]
        Mặt sau: [Câu trả lời hoặc định nghĩa]
        
        THẺ 2
        Mặt trước: [Câu hỏi hoặc thuật ngữ]
        Mặt sau: [Câu trả lời hoặc định nghĩa]
        
        (và cứ thế cho tất cả {num_cards} thẻ)
        """

        response = model.generate_content(prompt)
        response_text = response.text
        # Parse the response to extract flashcards
        flashcards = []
        card_blocks = response_text.split("THẺ ")

        for block in card_blocks[1:]:  # Skip the first empty block
            # Extract front and back content
            lines = block.strip().split("\n")

            front = ""
            back = ""
            front_section = True

            for line in lines[1:]:  # Skip the card number line
                if line.startswith("Mặt trước:"):
                    front = line.replace("Mặt trước:", "").strip()
                    continue
                if line.startswith("Mặt sau:"):
                    back = line.replace("Mặt sau:", "").strip()
                    front_section = False
                    continue  # If not a header line, append to appropriate section
                if front_section:
                    if front and not line.startswith("Mặt trước:"):
                        front += " " + line.strip()
                else:
                    if back and not line.startswith("Mặt sau:"):
                        back += " " + line.strip()

            if front and back:
                flashcards.append(Flashcard(front, back))

        return flashcards[:num_cards]  # Ensure we only return the requested number

    except Exception as e:
        raise Exception(f"Lỗi khi tạo thẻ ghi nhớ: {str(e)}")
