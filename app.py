import streamlit as st
import os
import pandas as pd
import time
from utils import extract_text_from_pdf, extract_text_from_pptx
from flashcard_generator import generate_flashcards, Flashcard, get_sample_flashcards

# Set page configuration
st.set_page_config(
    page_title="Gemini Flashcards",
    page_icon="📚",
    layout="wide",
)

# Initialize session state variables
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'current_card_index' not in st.session_state:
    st.session_state.current_card_index = 0
if 'card_flipped' not in st.session_state:
    st.session_state.card_flipped = False
if 'sets' not in st.session_state:
    st.session_state.sets = {}
if 'current_set' not in st.session_state:
    st.session_state.current_set = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edit_card_index' not in st.session_state:
    st.session_state.edit_card_index = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'input'  # 'input', 'view', 'sets'

def clear_flashcards():
    st.session_state.flashcards = []
    st.session_state.current_card_index = 0
    st.session_state.card_flipped = False
    st.session_state.edit_mode = False
    st.session_state.edit_card_index = None

def next_card():
    if st.session_state.flashcards:
        st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(st.session_state.flashcards)
        st.session_state.card_flipped = False

def prev_card():
    if st.session_state.flashcards:
        st.session_state.current_card_index = (st.session_state.current_card_index - 1) % len(st.session_state.flashcards)
        st.session_state.card_flipped = False

def flip_card():
    st.session_state.card_flipped = not st.session_state.card_flipped

def save_set(set_name):
    if not set_name:
        st.error("Please enter a name for this flashcard set")
        return
    
    if set_name in st.session_state.sets:
        st.error(f"Set '{set_name}' already exists. Please choose a different name.")
        return
    
    if not st.session_state.flashcards:
        st.error("No flashcards to save")
        return
    
    st.session_state.sets[set_name] = st.session_state.flashcards.copy()
    st.session_state.current_set = set_name
    st.success(f"Saved {len(st.session_state.flashcards)} flashcards to '{set_name}'")
    st.session_state.view_mode = 'sets'
    st.rerun()

def load_set(set_name):
    if set_name in st.session_state.sets:
        st.session_state.flashcards = st.session_state.sets[set_name].copy()
        st.session_state.current_card_index = 0
        st.session_state.card_flipped = False
        st.session_state.current_set = set_name
        st.session_state.view_mode = 'view'
        st.rerun()
    else:
        st.error(f"Set '{set_name}' not found")

def delete_set(set_name):
    if set_name in st.session_state.sets:
        del st.session_state.sets[set_name]
        st.success(f"Deleted set '{set_name}'")
        if st.session_state.current_set == set_name:
            st.session_state.current_set = None
            st.session_state.flashcards = []
            st.session_state.current_card_index = 0
        st.rerun()
    else:
        st.error(f"Set '{set_name}' not found")

def delete_card(index):
    if 0 <= index < len(st.session_state.flashcards):
        st.session_state.flashcards.pop(index)
        if st.session_state.current_card_index >= len(st.session_state.flashcards):
            st.session_state.current_card_index = max(0, len(st.session_state.flashcards) - 1)
        st.rerun()

def enter_edit_mode(index):
    st.session_state.edit_mode = True
    st.session_state.edit_card_index = index
    st.rerun()

def save_edit(front, back):
    if st.session_state.edit_card_index is not None and 0 <= st.session_state.edit_card_index < len(st.session_state.flashcards):
        st.session_state.flashcards[st.session_state.edit_card_index] = Flashcard(front, back)
        st.session_state.edit_mode = False
        st.session_state.edit_card_index = None
        st.rerun()

# Initialize API key in session state if not present
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'use_sample_cards' not in st.session_state:
    st.session_state.use_sample_cards = False

# Application header
st.title("📚 Gemini Flashcards")
st.markdown("Generate study flashcards from your educational content using Google's Gemini AI")

# API Key input (sidebar)
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input(
        "Enter your Google Gemini API Key:",
        type="password",
        help="Get your API key from https://makersuite.google.com/app/apikey",
        value=st.session_state.api_key if st.session_state.api_key else ""
    )
    
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input if api_key_input.strip() else None
    
    st.session_state.use_sample_cards = st.checkbox(
        "Use sample cards if generation fails", 
        value=st.session_state.use_sample_cards,
        help="If checked, sample cards will be generated when the API fails"
    )
    
    st.markdown("---")
    st.markdown("""
    ### How to Get an API Key
    1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with your Google account
    3. Create an API key
    4. Copy and paste it here
    """)

# Navigation
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("Create Flashcards"):
        st.session_state.view_mode = 'input'
        st.rerun()
with nav_col2:
    if st.button("View Flashcards"):
        if st.session_state.flashcards:
            st.session_state.view_mode = 'view'
            st.rerun()
        else:
            st.error("No flashcards available. Create some first!")
with nav_col3:
    if st.button("Saved Sets"):
        st.session_state.view_mode = 'sets'
        st.rerun()

# Main content based on view mode
if st.session_state.view_mode == 'input':
    st.header("Create New Flashcards")
    
    # Input method selection
    input_method = st.radio("Select input method:", ["Upload Slides", "Enter Text"], horizontal=True)
    
    content_text = ""
    
    if input_method == "Upload Slides":
        uploaded_file = st.file_uploader("Upload your slides (PDF or PPT)", type=["pdf", "pptx"])
        
        if uploaded_file is not None:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            try:
                if file_extension == ".pdf":
                    content_text = extract_text_from_pdf(uploaded_file)
                elif file_extension == ".pptx":
                    content_text = extract_text_from_pptx(uploaded_file)
                
                st.success(f"Successfully extracted content from {uploaded_file.name}")
                st.text_area("Extracted Content (you can edit if needed):", content_text, height=250)
            except Exception as e:
                st.error(f"Error extracting content: {str(e)}")
    
    else:  # Text input
        content_text = st.text_area("Enter your study content:", height=250)
    
    # Subject and number of cards selection
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subject/Topic:")
    with col2:
        num_cards = st.slider("Number of flashcards to generate:", min_value=3, max_value=20, value=10)
    
    # Generate button
    if st.button("Generate Flashcards", key="generate_btn"):
        if not content_text.strip():
            st.error("Please provide content to generate flashcards")
        else:
            with st.spinner("Generating flashcards with Gemini AI..."):
                try:
                    clear_flashcards()
                    if not st.session_state.api_key and not os.getenv("GOOGLE_API_KEY"):
                        if st.session_state.use_sample_cards:
                            st.warning("No API key provided. Using sample flashcards.")
                            st.session_state.flashcards = get_sample_flashcards(subject)[:num_cards]
                        else:
                            st.error("Please enter your Google Gemini API key in the sidebar to generate flashcards.")
                    else:
                        # Generate flashcards with API key
                        st.session_state.flashcards = generate_flashcards(
                            content_text, 
                            subject, 
                            num_cards, 
                            api_key=st.session_state.api_key,
                            use_sample_on_error=st.session_state.use_sample_cards
                        )
                    
                    if st.session_state.flashcards:
                        st.session_state.view_mode = 'view'
                        st.rerun()
                    else:
                        st.error("Failed to generate flashcards. Please try again.")
                except Exception as e:
                    if st.session_state.use_sample_cards:
                        st.warning(f"Error with API: {str(e)}. Using sample flashcards instead.")
                        st.session_state.flashcards = get_sample_flashcards(subject)[:num_cards]
                        st.session_state.view_mode = 'view'
                        st.rerun()
                    else:
                        st.error(f"Error generating flashcards: {str(e)}")

elif st.session_state.view_mode == 'view':
    if not st.session_state.flashcards:
        st.warning("No flashcards to display")
        st.session_state.view_mode = 'input'
        st.rerun()
    
    st.header("Flashcards")
    
    # Save set controls
    save_col1, save_col2, save_col3 = st.columns([2, 1, 1])
    with save_col1:
        set_name = st.text_input("Set name:", key="set_name_input")
    with save_col2:
        if st.button("Save Set", key="save_set_btn"):
            save_set(set_name)
    with save_col3:
        if st.session_state.current_set:
            st.write(f"Current set: {st.session_state.current_set}")
    
    # Display the current flashcard
    if st.session_state.flashcards:
        current_card = st.session_state.flashcards[st.session_state.current_card_index]
        
        # Edit mode
        if st.session_state.edit_mode and st.session_state.edit_card_index == st.session_state.current_card_index:
            st.subheader("Edit Flashcard")
            edit_front = st.text_area("Front (Question):", current_card.front, height=150)
            edit_back = st.text_area("Back (Answer):", current_card.back, height=150)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes"):
                    save_edit(edit_front, edit_back)
            with col2:
                if st.button("Cancel"):
                    st.session_state.edit_mode = False
                    st.session_state.edit_card_index = None
                    st.rerun()
        
        # View mode
        else:
            # Card display
            card_placeholder = st.container()
            with card_placeholder:
                card_col1, card_col2, card_col3 = st.columns([1, 5, 1])
                with card_col2:
                    card_style = """
                    <div style="
                        background-color: white;
                        border-radius: 8px;
                        padding: 20px;
                        min-height: 200px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        margin: 10px 0;
                        cursor: pointer;
                    ">
                    <h3>{content}</h3>
                    </div>
                    """
                    
                    if st.session_state.card_flipped:
                        st.markdown(card_style.format(content=current_card.back), unsafe_allow_html=True)
                    else:
                        st.markdown(card_style.format(content=current_card.front), unsafe_allow_html=True)
                    
                    # Flip button under the card
                    if st.button("Flip Card", key="flip_btn"):
                        flip_card()
                        st.rerun()
            
            # Navigation controls
            nav_cols = st.columns([1, 1, 2, 1, 1])
            with nav_cols[0]:
                if st.button("⬅️ Previous", key="prev_btn"):
                    prev_card()
                    st.rerun()
            with nav_cols[1]:
                if st.button("➡️ Next", key="next_btn"):
                    next_card()
                    st.rerun()
            with nav_cols[3]:
                if st.button("✏️ Edit", key="edit_btn"):
                    enter_edit_mode(st.session_state.current_card_index)
            with nav_cols[4]:
                if st.button("🗑️ Delete", key="delete_btn"):
                    delete_card(st.session_state.current_card_index)
            
            # Card counter
            st.write(f"Card {st.session_state.current_card_index + 1} of {len(st.session_state.flashcards)}")

elif st.session_state.view_mode == 'sets':
    st.header("Saved Flashcard Sets")
    
    if not st.session_state.sets:
        st.info("No saved flashcard sets yet. Create and save some flashcards first!")
    else:
        # Display a table of saved sets
        set_data = []
        for set_name, cards in st.session_state.sets.items():
            set_data.append({"Set Name": set_name, "Cards": len(cards)})
        
        if set_data:
            df = pd.DataFrame(set_data)
            st.dataframe(df, use_container_width=True)
            
            # Set selection and actions
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_set = st.selectbox("Select a set:", list(st.session_state.sets.keys()))
            with col2:
                if st.button("Load Set", key="load_set_btn"):
                    load_set(selected_set)
            with col3:
                if st.button("Delete Set", key="delete_set_btn"):
                    delete_set(selected_set)
