"""
Module xử lý các API AI miễn phí cho deployment online
"""

import requests
import json
import time
import random
from dataclasses import dataclass
from typing import List
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
        # Danh sách các API miễn phí THỰC SỰ theo thứ tự ưu tiên
        self.apis = {
            "text_processing": {
                "enabled": True,
                "free": True,
            },
            "huggingface_inference": {
                "url": "https://api-inference.huggingface.co/models/google/flan-t5-large",
                "enabled": True,
                "free": True,
            },
        }

    def generate_with_text_processing(
        self, content: str, subject: str, num_cards: int = 10, language: str = "vi"
    ) -> List[Flashcard]:
        """
        Tạo flashcard bằng xử lý văn bản thông minh (không cần API)
        """
        try:
            flashcards = []
            
            # Tách câu và làm sạch
            sentences = [s.strip() for s in content.replace('\n', ' ').split('.') if s.strip() and len(s.strip()) > 15]
            
            # Template theo ngôn ngữ
            templates = {
                "vi": {
                    "question_starters": [
                        "Điều gì là",
                        "Hãy giải thích về",
                        "Khái niệm {} có nghĩa là gì",
                        "Tại sao {} quan trọng",
                        "Ứng dụng của {} là gì",
                        "Đặc điểm của {} là gì",
                        "Cách thức hoạt động của {} như thế nào"
                    ],
                    "key_phrases": ["là", "được", "có thể", "bao gồm", "chính là", "được định nghĩa", "có đặc điểm"]
                },
                "en": {
                    "question_starters": [
                        "What is",
                        "Explain about", 
                        "What does {} mean",
                        "Why is {} important",
                        "What are the applications of {}",
                        "What are the characteristics of {}",
                        "How does {} work"
                    ],
                    "key_phrases": ["is", "are", "can", "include", "defined as", "characterized by", "consists of"]
                }
            }
            
            template = templates.get(language, templates["vi"])
            
            # Trích xuất thuật ngữ quan trọng
            words = content.split()
            important_terms = []
            
            for word in words:
                clean_word = word.strip('.,!?()[]{}";:').lower()
                if (len(clean_word) > 4 and 
                    clean_word not in ['this', 'that', 'with', 'from', 'they', 'have', 'will', 'been', 'were', 'would'] and
                    clean_word not in important_terms):
                    important_terms.append(clean_word)
            
            # Tạo flashcard từ câu có chứa thuật ngữ quan trọng
            for i, sentence in enumerate(sentences[:num_cards]):
                if i >= num_cards:
                    break
                    
                # Tìm thuật ngữ trong câu
                key_term = None
                for term in important_terms:
                    if term in sentence.lower():
                        key_term = term
                        break
                
                if key_term:
                    # Tạo câu hỏi dựa trên thuật ngữ
                    question_template = random.choice(template["question_starters"])
                    if '{}' in question_template:
                        question = question_template.format(key_term) + "?"
                    else:
                        question = f"{question_template} {key_term}?"
                else:
                    # Câu hỏi chung
                    if language == "vi":
                        question = f"Câu hỏi {i+1} về {subject}: Nội dung này nói về điều gì?"
                    else:
                        question = f"Question {i+1} about {subject}: What does this content discuss?"
                
                # Câu trả lời là câu gốc, rút gọn nếu quá dài
                answer = sentence
                if len(answer) > 150:
                    answer = answer[:150] + "..."
                
                flashcards.append(Flashcard(front=question, back=answer))
            
            # Nếu chưa đủ, tạo thêm từ những câu còn lại
            remaining_sentences = sentences[len(flashcards):]
            for i, sentence in enumerate(remaining_sentences):
                if len(flashcards) >= num_cards:
                    break
                    
                # Câu hỏi đơn giản
                if language == "vi":
                    question = f"Theo văn bản, điều gì được đề cập trong câu số {len(flashcards)+1}?"
                else:
                    question = f"According to the text, what is mentioned in statement {len(flashcards)+1}?"
                
                answer = sentence
                if len(answer) > 150:
                    answer = answer[:150] + "..."
                    
                flashcards.append(Flashcard(front=question, back=answer))
            
            return flashcards[:num_cards]
            
        except Exception as e:
            print(f"Text processing error: {e}")
            return []

    def generate_with_huggingface_free(
        self, content: str, subject: str, num_cards: int = 10, language: str = "vi"
    ) -> List[Flashcard]:
        """
        Sử dụng Hugging Face Inference API miễn phí với model tốt hơn
        """
        try:
            # Template cải tiến cho flashcard
            templates = {
                "vi": {
                    "prompt": f"""Tạo {num_cards} thẻ ghi nhớ về {subject}:

Nội dung: {content[:500]}

Định dạng: Q: [câu hỏi] A: [câu trả lời]
Mỗi thẻ một dòng riêng.

Thẻ ghi nhớ:
"""
                },
                "en": {
                    "prompt": f"""Create {num_cards} flashcards about {subject}:

Content: {content[:500]}

Format: Q: [question] A: [answer]
Each card on separate line.

Flashcards:
"""
                }
            }

            template = templates.get(language, templates["vi"])

            # Danh sách các model miễn phí tốt
            api_urls = [
                "https://api-inference.huggingface.co/models/google/flan-t5-large",
                "https://api-inference.huggingface.co/models/google/flan-t5-base",
            ]

            for api_url in api_urls:
                try:
                    headers = {
                        "Content-Type": "application/json",
                    }

                    payload = {
                        "inputs": template["prompt"],
                        "parameters": {
                            "max_new_tokens": 400,
                            "temperature": 0.7,
                            "do_sample": True,
                            "return_full_text": False,
                        },
                    }

                    response = requests.post(
                        api_url, headers=headers, json=payload, timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()
                        generated_text = ""
                        
                        if isinstance(result, list) and len(result) > 0:
                            generated_text = result[0].get("generated_text", "")
                        elif isinstance(result, dict):
                            generated_text = result.get("generated_text", "")

                        if generated_text:
                            flashcards = self._parse_qa_format(
                                generated_text, num_cards
                            )
                            if flashcards and len(flashcards) >= 3:  # Ít nhất 3 thẻ hợp lệ
                                return flashcards

                    time.sleep(2)  # Rate limiting cho HuggingFace
                except Exception as e:
                    print(f"Error with {api_url}: {e}")
                    continue

            return []

        except Exception as e:
            print(f"HuggingFace API error: {str(e)}")
            return []

    def _parse_qa_format(self, text: str, num_cards: int) -> List[Flashcard]:
        """
        Parse flashcards from Q: ... A: ... format
        """
        flashcards = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Tìm pattern Q: ... A: ... hoặc Q: ... | A: ...
            if 'Q:' in line and ('A:' in line or '|' in line):
                try:
                    # Split bằng | hoặc A:
                    if '|' in line:
                        parts = line.split('|', 1)
                        question_part = parts[0].strip()
                        answer_part = parts[1].strip()
                    else:
                        parts = line.split('A:', 1)
                        question_part = parts[0].strip()
                        answer_part = parts[1].strip() if len(parts) > 1 else ""
                    
                    # Clean question and answer
                    question = question_part.replace('Q:', '').strip()
                    answer = answer_part.replace('A:', '').strip()
                    
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

    def _generate_simple_cards_from_content(self, content: str, count: int) -> List[Flashcard]:
        """Generate simple Q&A pairs from content when AI parsing fails"""
        cards = []
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        for i, sentence in enumerate(sentences[:count]):
            if len(sentence) > 20:  # Only meaningful sentences
                question = f"Câu hỏi {i+1}: {sentence[:50]}...?"
                answer = sentence
                cards.append(Flashcard(front=question, back=answer))
                
        return cards

    def generate_rule_based_multilang(
        self, content: str, subject: str, num_cards: int = 10, language: str = "vi"
    ) -> List[Flashcard]:
        """
        Tạo flashcard bằng rule-based method đa ngôn ngữ
        """
        try:
            flashcards = []
            sentences = [s.strip() for s in content.split('.') if s.strip() and len(s.strip()) > 10]
            
            # Templates theo ngôn ngữ
            templates = {
                "vi": {
                    "questions": [
                        "Điều gì là {}?",
                        "Hãy giải thích về {}",
                        "Khái niệm {} có nghĩa là gì?",
                        "Tại sao {} quan trọng?",
                        "Ứng dụng của {} là gì?",
                    ],
                    "definitions": [
                        "là một khái niệm",
                        "có thể hiểu là",
                        "được định nghĩa như",
                        "có đặc điểm",
                        "bao gồm",
                    ]
                },
                "en": {
                    "questions": [
                        "What is {}?",
                        "Explain about {}",
                        "What does {} mean?",
                        "Why is {} important?",
                        "What are applications of {}?",
                    ],
                    "definitions": [
                        "is a concept",
                        "can be understood as",
                        "is defined as",
                        "has characteristics",
                        "includes",
                    ]
                }
            }
            
            template = templates.get(language, templates["vi"])
            
            # Extract key terms and create cards
            words = content.split()
            key_terms = []
            
            # Simple keyword extraction
            for word in words:
                word = word.strip('.,!?()[]{}";:')
                if len(word) > 4 and word not in key_terms:
                    key_terms.append(word)
                    
            key_terms = key_terms[:num_cards]
            
            # Create flashcards
            for i, term in enumerate(key_terms):
                if i >= num_cards:
                    break
                    
                # Random question template
                question_template = random.choice(template["questions"])
                question = question_template.format(term)
                
                # Find context for answer
                answer = f"{term} "
                for sentence in sentences:
                    if term.lower() in sentence.lower():
                        answer = sentence[:200] + "..." if len(sentence) > 200 else sentence
                        break
                
                if not answer.strip() or answer == f"{term} ":
                    answer = f"{term} {random.choice(template['definitions'])} {subject}"
                
                flashcards.append(Flashcard(front=question, back=answer))
            
            # Fill remaining with sentence-based cards
            remaining = num_cards - len(flashcards)
            for i, sentence in enumerate(sentences[:remaining]):
                if len(sentence) > 20:
                    if language == "vi":
                        question = f"Câu hỏi về {subject}: Nội dung này nói về điều gì?"
                    else:
                        question = f"Question about {subject}: What does this content discuss?"
                    answer = sentence
                    flashcards.append(Flashcard(front=question, back=answer))
            
            return flashcards[:num_cards]
            
        except Exception as e:
            # Ultimate fallback
            return [
                Flashcard(
                    front=f"Câu hỏi {i+1} về {subject}",
                    back=f"Nội dung liên quan đến {subject} cần được học tập"
                )
                for i in range(num_cards)
            ]

    def generate_flashcards(
        self, content: str, subject: str, num_cards: int = 10, language: str = "vi"
    ) -> List[Flashcard]:
        """
        Main method để tạo flashcards online
        """
        # Thử các phương pháp theo thứ tự ưu tiên (chỉ APIs thực sự miễn phí)
        methods = [
            ("Text Processing AI", self.generate_with_text_processing),
            ("Hugging Face Free API", self.generate_with_huggingface_free), 
            ("Rule-based Generation", self.generate_rule_based_multilang),
        ]

        for method_name, method_func in methods:
            try:
                st.info(f"🤖 Đang thử {method_name}...")
                flashcards = method_func(content, subject, num_cards, language)
                if flashcards and len(flashcards) >= 3:  # Ít nhất 3 thẻ hợp lệ
                    st.success(f"✅ Thành công với {method_name}")
                    return flashcards
            except Exception as e:
                st.warning(f"⚠️ {method_name} thất bại: {str(e)}")
                continue

        # Fallback cuối cùng
        st.info("📝 Sử dụng phương pháp tạo tự động...")
        return self.generate_rule_based_multilang(content, subject, num_cards, language)


# Global instance
online_generator = OnlineAIGenerator()
