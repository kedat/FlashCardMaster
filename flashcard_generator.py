import os
import google.generativeai as genai
from dataclasses import dataclass

@dataclass
class Flashcard:
    front: str  # Question/term
    back: str   # Answer/definition

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
        Flashcard(f"What is {subject}?", f"{subject} is a field of study that encompasses various concepts and principles."),
        Flashcard(f"Who pioneered modern {subject}?", f"Several key figures contributed to the development of {subject} through their groundbreaking research and theories."),
        Flashcard(f"What are the key principles of {subject}?", f"The key principles include fundamental theories and practices that form the foundation of {subject}."),
        Flashcard(f"How is {subject} applied in real world scenarios?", f"{subject} is applied in various industries and contexts to solve problems and improve processes."),
        Flashcard(f"What is the future of {subject}?", f"The future of {subject} involves emerging technologies and evolving methodologies that will shape its development."),
        Flashcard(f"Define the scope of {subject}", f"The scope of {subject} includes its theoretical framework, practical applications, and interdisciplinary connections."),
        Flashcard(f"What challenges exist in {subject} today?", f"Current challenges in {subject} include technological limitations, ethical considerations, and implementation hurdles."),
        Flashcard(f"How has {subject} evolved over time?", f"{subject} has evolved through various paradigm shifts and innovations that have redefined its core concepts."),
        Flashcard(f"What skills are needed to excel in {subject}?", f"Excellence in {subject} requires analytical thinking, problem-solving abilities, and domain-specific knowledge."),
        Flashcard(f"How do experts measure success in {subject}?", f"Success in {subject} is typically measured through established metrics, outcomes, and impact assessments.")
    ]
    
    return sample_cards

def generate_flashcards(content, subject, num_cards=10, api_key=None, use_sample_on_error=False):
    """
    Generate flashcards using Google's Gemini model
    
    Args:
        content (str): The educational content to convert to flashcards
        subject (str): The subject or topic of the content
        num_cards (int): Number of flashcards to generate
        api_key (str, optional): Google API key for Gemini model
        use_sample_on_error (bool): Whether to return sample cards on error
    
    Returns:
        list: List of Flashcard objects
    """
    try:
        model = setup_gemini_model(api_key)
        
        # Prompt engineering for better results
        prompt = f"""
        Create {num_cards} detailed study flashcards about {subject} based on the following content. 
        For each flashcard, generate:
        1. A clear, concise question or term on the front
        2. A comprehensive answer or definition on the back
        
        Make sure the flashcards:
        - Cover the most important concepts from the content
        - Are educational and accurate
        - Include key terminology, definitions, and explanations
        - Vary in difficulty and question types
        
        Content to analyze:
        {content}
        
        Output format:
        CARD 1
        Front: [Question or term]
        Back: [Answer or definition]
        
        CARD 2
        Front: [Question or term]
        Back: [Answer or definition]
        
        (and so on for all {num_cards} cards)
        """
        
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Parse the response to extract flashcards
        flashcards = []
        card_blocks = response_text.split("CARD ")
        
        for block in card_blocks[1:]:  # Skip the first empty block
            # Extract front and back content
            lines = block.strip().split("\n")
            
            front = ""
            back = ""
            front_section = True
            
            for line in lines[1:]:  # Skip the card number line
                if line.startswith("Front:"):
                    front = line.replace("Front:", "").strip()
                    continue
                if line.startswith("Back:"):
                    back = line.replace("Back:", "").strip()
                    front_section = False
                    continue
                
                # If not a header line, append to appropriate section
                if front_section:
                    if front and not line.startswith("Front:"):
                        front += " " + line.strip()
                else:
                    if back and not line.startswith("Back:"):
                        back += " " + line.strip()
            
            if front and back:
                flashcards.append(Flashcard(front, back))
        
        return flashcards[:num_cards]  # Ensure we only return the requested number
    
    except Exception as e:
        if use_sample_on_error:
            return get_sample_flashcards(subject)[:num_cards]
        else:
            raise Exception(f"Error generating flashcards: {str(e)}")
