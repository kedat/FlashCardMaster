"""
Module xử lý các API AI miễn phí cho deployment online
"""

from dataclasses import dataclass
from typing import List, Optional

import requests
import streamlit as st


@dataclass
class Flashcard:
    front: str
    back: str


class OnlineAIGenerator:
    """
    Generator sử dụng các API AI miễn phí có thể deploy online
    """

    def __init__(self):
        # Chỉ sử dụng Gemini API
        self.apis = {
            "gemini": {
                "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
                "enabled": True,
                "free": True,
            },
        }

    def generate_with_gemini_free(
        self,
        content: str,
        subject: str,
        num_cards: int = 10,
        language: str = "vi",
        gemini_api_key: Optional[str] = None,
    ) -> List[Flashcard]:
        """
        Sử dụng Google Gemini API để tạo flashcards
        """
        try:
            # Nếu không có API key, skip method này
            if not gemini_api_key:
                print("Gemini API key not provided, skipping...")
                return []

            # Template cải tiến cho flashcard với Gemini
            templates = {
                "vi": {
                    "prompt": f"""Tạo {num_cards} thẻ ghi nhớ về chủ đề "{subject}" từ nội dung sau:

{content[:800]}

Yêu cầu:
1. Mỗi thẻ có câu hỏi rõ ràng và câu trả lời chính xác
2. Câu hỏi kiểm tra hiểu biết thực tế, không chỉ ghi nhớ máy móc
3. Câu trả lời ngắn gọn nhưng đầy đủ thông tin
4. Định dạng: Q: [câu hỏi] | A: [câu trả lời]
5. Mỗi thẻ trên một dòng riêng

Tạo {num_cards} thẻ ghi nhớ:"""
                },
                "en": {
                    "prompt": f"""Create {num_cards} flashcards about "{subject}" from the following content:

{content[:800]}

Requirements:
1. Each card has clear questions and accurate answers
2. Questions test understanding, not just memorization
3. Answers are concise but complete
4. Format: Q: [question] | A: [answer]
5. Each card on a separate line

Create {num_cards} flashcards:"""
                },
            }

            template = templates.get(language, templates["vi"])

            # Google Gemini API endpoint
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"

            headers = {
                "Content-Type": "application/json",
            }

            payload = {
                "contents": [{"parts": [{"text": template["prompt"]}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 1,
                    "topP": 1,
                    "maxOutputTokens": 2048,
                },
            }

            response = requests.post(api_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    generated_text = result["candidates"][0]["content"]["parts"][0][
                        "text"
                    ]

                    if generated_text:
                        flashcards = self._parse_qa_format(generated_text, num_cards)
                        if flashcards and len(flashcards) >= 3:  # Ít nhất 3 thẻ hợp lệ
                            print("✅ Success with Gemini API")
                            return flashcards
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")

            return []

        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return []

    def _parse_qa_format(self, text: str, num_cards: int) -> List[Flashcard]:
        """
        Parse flashcards from Q: ... A: ... format
        """
        flashcards = []
        lines = text.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Tìm pattern Q: ... A: ... hoặc Q: ... | A: ...
            if "Q:" in line and ("A:" in line or "|" in line):
                try:
                    # Split bằng | hoặc A:
                    if "|" in line:
                        parts = line.split("|", 1)
                        question_part = parts[0].strip()
                        answer_part = parts[1].strip()
                    else:
                        parts = line.split("A:", 1)
                        question_part = parts[0].strip()
                        answer_part = parts[1].strip() if len(parts) > 1 else ""

                    # Clean question and answer
                    question = question_part.replace("Q:", "").strip()
                    answer = answer_part.replace("A:", "").strip()

                    if question and answer:
                        flashcards.append(Flashcard(front=question, back=answer))

                except Exception as e:
                    continue

        # Nếu không đủ thẻ, tạo thêm từ content
        if len(flashcards) < num_cards:
            additional_needed = num_cards - len(flashcards)
            additional_cards = self._generate_simple_cards_from_content(
                text, additional_needed
            )
            flashcards.extend(additional_cards)

        return flashcards[:num_cards]

    def _generate_simple_cards_from_content(
        self, content: str, count: int
    ) -> List[Flashcard]:
        """Generate simple Q&A pairs from content when AI parsing fails"""
        cards = []
        sentences = [s.strip() for s in content.split(".") if s.strip()]

        for i, sentence in enumerate(sentences[:count]):
            if len(sentence) > 20:  # Only meaningful sentences
                question = f"Câu hỏi {i+1}: {sentence[:50]}...?"
                answer = sentence
                cards.append(Flashcard(front=question, back=answer))

        return cards

    def generate_flashcards(
        self,
        content: str,
        subject: str,
        num_cards: int = 10,
        language: str = "vi",
        gemini_api_key: Optional[str] = None,
    ) -> List[Flashcard]:
        """
        Main method để tạo flashcards online - chỉ sử dụng Gemini API
        """
        # Kiểm tra Gemini API key
        if not gemini_api_key:
            st.error("❌ Cần có Gemini API key để tạo flashcards!")
            return []

        try:
            st.info("🤖 Đang tạo flashcards với Gemini API...")
            flashcards = self.generate_with_gemini_free(
                content, subject, num_cards, language, gemini_api_key
            )

            if flashcards and len(flashcards) >= 3:  # Ít nhất 3 thẻ hợp lệ
                st.success("✅ Tạo flashcards thành công!")
                return flashcards
            else:
                st.error("❌ Không thể tạo flashcards với Gemini API!")
                return []

        except Exception as e:
            st.error(f"❌ Lỗi khi tạo flashcards: {str(e)}")
            return []


# Global instance
online_generator = OnlineAIGenerator()
