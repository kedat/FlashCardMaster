import streamlit as st
import os
import pandas as pd
import time
from utils import extract_text_from_pdf, extract_text_from_pptx
from flashcard_generator import generate_flashcards, Flashcard, get_sample_flashcards
from lang_manager import language_manager as lang_manager
from online_ai import online_generator

# Set page configuration
st.set_page_config(
    page_title=lang_manager.get_text("app_title"),
    page_icon="📚",
    layout="wide",
)

# Initialize session state variables
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "current_card_index" not in st.session_state:
    st.session_state.current_card_index = 0
if "card_flipped" not in st.session_state:
    st.session_state.card_flipped = False
if "sets" not in st.session_state:
    st.session_state.sets = {}
if "current_set" not in st.session_state:
    st.session_state.current_set = None
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edit_card_index" not in st.session_state:
    st.session_state.edit_card_index = None
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "input"  # 'input', 'view', 'sets'
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "use_sample_cards" not in st.session_state:
    st.session_state.use_sample_cards = False
if "ai_method" not in st.session_state:
    st.session_state.ai_method = "gemini"
if "language" not in st.session_state:
    st.session_state.language = "vi"

# Set current language
lang_manager.set_language(st.session_state.language)


def clear_flashcards():
    st.session_state.flashcards = []
    st.session_state.current_card_index = 0
    st.session_state.card_flipped = False
    st.session_state.edit_mode = False
    st.session_state.edit_card_index = None


def next_card():
    if st.session_state.flashcards:
        st.session_state.current_card_index = (
            st.session_state.current_card_index + 1
        ) % len(st.session_state.flashcards)
        st.session_state.card_flipped = False


def prev_card():
    if st.session_state.flashcards:
        st.session_state.current_card_index = (
            st.session_state.current_card_index - 1
        ) % len(st.session_state.flashcards)
        st.session_state.card_flipped = False


def flip_card():
    st.session_state.card_flipped = not st.session_state.card_flipped


def save_set(set_name):
    if not set_name:
        st.error(lang_manager.get_text("set_save_error_name"))
        return

    if set_name in st.session_state.sets:
        st.error(lang_manager.get_text("set_save_error_exists", name=set_name))
        return

    if not st.session_state.flashcards:
        st.error(lang_manager.get_text("set_save_error_empty"))
        return

    st.session_state.sets[set_name] = st.session_state.flashcards.copy()
    st.session_state.current_set = set_name
    st.success(
        lang_manager.get_text(
            "set_save_success", count=len(st.session_state.flashcards), name=set_name
        )
    )
    st.session_state.view_mode = "sets"
    st.rerun()


def load_set(set_name):
    if set_name in st.session_state.sets:
        st.session_state.flashcards = st.session_state.sets[set_name].copy()
        st.session_state.current_card_index = 0
        st.session_state.card_flipped = False
        st.session_state.current_set = set_name
        st.session_state.view_mode = "view"
        st.rerun()
    else:
        st.error(lang_manager.get_text("set_not_found", name=set_name))


def delete_set(set_name):
    if set_name in st.session_state.sets:
        del st.session_state.sets[set_name]
        st.success(lang_manager.get_text("set_delete_success", name=set_name))
        if st.session_state.current_set == set_name:
            st.session_state.current_set = None
            st.session_state.flashcards = []
            st.session_state.current_card_index = 0
        st.rerun()
    else:
        st.error(lang_manager.get_text("set_not_found", name=set_name))


def delete_card(index):
    if 0 <= index < len(st.session_state.flashcards):
        st.session_state.flashcards.pop(index)
        if st.session_state.current_card_index >= len(st.session_state.flashcards):
            st.session_state.current_card_index = max(
                0, len(st.session_state.flashcards) - 1
            )
        st.rerun()


def enter_edit_mode(index):
    st.session_state.edit_mode = True
    st.session_state.edit_card_index = index
    st.rerun()


def save_edit(front, back):
    if (
        st.session_state.edit_card_index is not None
        and 0 <= st.session_state.edit_card_index < len(st.session_state.flashcards)
    ):
        st.session_state.flashcards[st.session_state.edit_card_index] = Flashcard(
            front, back
        )
        st.session_state.edit_mode = False
        st.session_state.edit_card_index = None
        st.rerun()


# Application header
st.title(lang_manager.get_text("app_title"))
st.markdown(lang_manager.get_text("app_subtitle"))

# API Key input (sidebar)
with st.sidebar:
    st.header(lang_manager.get_text("settings"))

    # Language selection
    available_languages = lang_manager.get_available_languages()
    language_options = list(available_languages.keys())
    language_labels = list(available_languages.values())

    current_lang_index = (
        language_options.index(st.session_state.language)
        if st.session_state.language in language_options
        else 0
    )

    selected_language = st.selectbox(
        lang_manager.get_text("language"),
        options=language_options,
        format_func=lambda x: available_languages[x],
        index=current_lang_index,
        key="language_selector",
    )

    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        lang_manager.set_language(selected_language)
        st.rerun()

    st.markdown("---")  # AI Method selection
    ai_method_options = ["gemini"]

    # Get AI methods text safely
    ai_methods_dict = lang_manager.get_text("ai_methods")
    ai_method_help_dict = lang_manager.get_text("ai_method_help")

    current_method_index = (
        ai_method_options.index(st.session_state.ai_method)
        if st.session_state.ai_method in ai_method_options
        else 0
    )

    ai_method = st.selectbox(
        lang_manager.get_text("ai_method"),
        options=ai_method_options,
        format_func=lambda x: (
            ai_methods_dict.get(x, x) if isinstance(ai_methods_dict, dict) else x
        ),
        index=current_method_index,
        help="Chọn phương pháp AI phù hợp cho deployment online",
    )
    st.session_state.ai_method = ai_method

    # API Key cho Gemini
    if ai_method == "gemini":
        api_key_input = st.text_input(
            lang_manager.get_text("api_key_label"),
            type="password",
            help=lang_manager.get_text("api_key_help"),
            value=st.session_state.api_key if st.session_state.api_key else "",
        )

        if api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input if api_key_input.strip() else None

    st.session_state.use_sample_cards = st.checkbox(
        lang_manager.get_text("use_sample_cards"),
        value=st.session_state.use_sample_cards,
        help=lang_manager.get_text("use_sample_cards_help"),
    )

    st.markdown("---")
    if ai_method == "gemini":
        st.markdown(
            f"""
        ### {lang_manager.get_text("gemini_api_guide", default="Cách Lấy API Key Gemini (Miễn Phí)")}
        1. {lang_manager.get_text("visit_studio", default="Truy cập")} [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. {lang_manager.get_text("login_google", default="Đăng nhập bằng tài khoản Google")}
        3. {lang_manager.get_text("create_api_key", default="Tạo API key")}
        4. {lang_manager.get_text("copy_paste", default="Sao chép và dán vào đây")}
        """
        )

# Navigation
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button(lang_manager.get_text("create_flashcards")):
        st.session_state.view_mode = "input"
        st.rerun()
with nav_col2:
    if st.button(lang_manager.get_text("view_flashcards")):
        if st.session_state.flashcards:
            st.session_state.view_mode = "view"
            st.rerun()
        else:
            st.error(lang_manager.get_text("no_flashcards_available"))
with nav_col3:
    if st.button(lang_manager.get_text("saved_sets")):
        st.session_state.view_mode = "sets"
        st.rerun()

# Main content based on view mode
if st.session_state.view_mode == "input":
    st.header(lang_manager.get_text("create_new_flashcards"))  # Input method selection
    input_method = st.radio(
        lang_manager.get_text("select_input_method"),
        [lang_manager.get_text("upload_method"), lang_manager.get_text("text_method")],
        horizontal=True,
    )

    content_text = ""

    if input_method == lang_manager.get_text("upload_method"):
        uploaded_file = st.file_uploader(
            lang_manager.get_text("upload_files"), type=["pdf", "pptx"]
        )

        if uploaded_file is not None:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            try:
                if file_extension == ".pdf":
                    content_text = extract_text_from_pdf(uploaded_file)
                elif file_extension == ".pptx":
                    content_text = extract_text_from_pptx(uploaded_file)

                st.success(
                    lang_manager.get_text("upload_success", filename=uploaded_file.name)
                )
                st.text_area(
                    lang_manager.get_text("extracted_content"),
                    content_text,
                    height=250,
                )
            except Exception as e:
                st.error(lang_manager.get_text("upload_error", error=str(e)))

    else:  # Text input
        content_text = st.text_area(lang_manager.get_text("enter_text"), height=250)
    # Subject and number of cards selection
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input(lang_manager.get_text("subject_topic"))
    with col2:
        num_cards = st.slider(
            lang_manager.get_text("num_cards"), min_value=3, max_value=20, value=10
        )

    # Generate button
    if st.button(lang_manager.get_text("generate_btn"), key="generate_btn"):
        if not content_text.strip():
            st.error(lang_manager.get_text("content_required"))
        else:
            with st.spinner("🧠 " + lang_manager.get_text("generating_gemini")):
                try:
                    clear_flashcards()
                    # Sử dụng online_generator với Gemini API key
                    api_key = st.session_state.api_key
                    st.session_state.flashcards = online_generator.generate_flashcards(
                        content_text,
                        subject,
                        num_cards,
                        st.session_state.language,
                        api_key,
                    )

                    if st.session_state.flashcards:
                        st.success(
                            lang_manager.get_text(
                                "success_created",
                                count=len(st.session_state.flashcards),
                            )
                        )
                        st.session_state.view_mode = "view"
                        st.rerun()
                    else:
                        st.error(lang_manager.get_text("error_creating"))
                except Exception as e:
                    st.error(lang_manager.get_text("error_with_fallback", error=str(e)))
                    # Thử fallback methods
                    if st.session_state.use_sample_cards:
                        st.warning(lang_manager.get_text("using_sample_fallback"))
                        st.session_state.flashcards = get_sample_flashcards(subject)[
                            :num_cards
                        ]
                        st.session_state.view_mode = "view"
                        st.rerun()

elif st.session_state.view_mode == "view":
    if not st.session_state.flashcards:
        st.warning(lang_manager.get_text("no_flashcards_to_display"))
        st.session_state.view_mode = "input"
        st.rerun()

    st.header(lang_manager.get_text("flashcards_title"))
    # Save set controls
    save_col1, save_col2, save_col3 = st.columns([2, 1, 1])
    with save_col1:
        set_name = st.text_input(
            lang_manager.get_text("set_name_label"), key="set_name_input"
        )
    with save_col2:
        if st.button(lang_manager.get_text("save_set_btn"), key="save_set_btn"):
            save_set(set_name)
    with save_col3:
        if st.session_state.current_set:
            st.write(
                f"{lang_manager.get_text('current_set_label')}: {st.session_state.current_set}"
            )

    # Display the current flashcard
    if st.session_state.flashcards:
        current_card = st.session_state.flashcards[
            st.session_state.current_card_index
        ]  # Edit mode
        if (
            st.session_state.edit_mode
            and st.session_state.edit_card_index == st.session_state.current_card_index
        ):
            st.subheader(lang_manager.get_text("edit_flashcard_title"))
            edit_front = st.text_area(
                lang_manager.get_text("front_side_label"),
                current_card.front,
                height=150,
            )
            edit_back = st.text_area(
                lang_manager.get_text("back_side_label"), current_card.back, height=150
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(lang_manager.get_text("save_changes_btn")):
                    save_edit(edit_front, edit_back)
            with col2:
                if st.button(lang_manager.get_text("cancel_btn")):
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
                        st.markdown(
                            card_style.format(content=current_card.back),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            card_style.format(content=current_card.front),
                            unsafe_allow_html=True,
                        )  # Flip button under the card
                    if st.button(
                        lang_manager.get_text("flip_card_btn"), key="flip_btn"
                    ):
                        flip_card()
                        st.rerun()
            # Navigation controls
            nav_cols = st.columns([1, 1, 2, 1, 1])
            with nav_cols[0]:
                if st.button(f"⬅️ {lang_manager.get_text('prev_btn')}", key="prev_btn"):
                    prev_card()
                    st.rerun()
            with nav_cols[1]:
                if st.button(f"➡️ {lang_manager.get_text('next_btn')}", key="next_btn"):
                    next_card()
                    st.rerun()
            with nav_cols[3]:
                if st.button(f"✏️ {lang_manager.get_text('edit_btn')}", key="edit_btn"):
                    enter_edit_mode(st.session_state.current_card_index)
            with nav_cols[4]:
                if st.button(
                    f"🗑️ {lang_manager.get_text('delete_btn')}", key="delete_btn"
                ):
                    delete_card(st.session_state.current_card_index)

            # Card counter
            st.write(
                lang_manager.get_text(
                    "card_counter",
                    current=st.session_state.current_card_index + 1,
                    total=len(st.session_state.flashcards),
                )
            )

elif st.session_state.view_mode == "sets":
    st.header(lang_manager.get_text("saved_sets_title"))

    if not st.session_state.sets:
        st.info(lang_manager.get_text("no_saved_sets_info"))
    else:
        # Display a table of saved sets
        set_data = []
        for set_name, cards in st.session_state.sets.items():
            set_data.append(
                {
                    lang_manager.get_text("set_name_column"): set_name,
                    lang_manager.get_text("card_count_column"): len(cards),
                }
            )

        if set_data:
            df = pd.DataFrame(set_data)
            st.dataframe(df, use_container_width=True)

            # Set selection and actions
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_set = st.selectbox(
                    lang_manager.get_text("select_set_label"),
                    list(st.session_state.sets.keys()),
                )
            with col2:
                if st.button(lang_manager.get_text("load_set_btn"), key="load_set_btn"):
                    load_set(selected_set)
            with col3:
                if st.button(
                    lang_manager.get_text("delete_set_btn"), key="delete_set_btn"
                ):
                    delete_set(selected_set)
