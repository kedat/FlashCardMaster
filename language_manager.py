# Hệ thống đa ngôn ngữ cho FlashCard Master
import json
import os


class LanguageManager:
    def __init__(self):
        self.languages = {
            "vi": "Tiếng Việt 🇻🇳",
            "en": "English 🇺🇸", 
            "ja": "日本語 🇯🇵",
            "fr": "Français 🇫🇷",
        }
        self.current_language = "vi"
        self.translations = self._load_all_translations()

    def _load_all_translations(self):
        """Load all translations"""
        return {            "vi": self._get_vietnamese_translations(),
            "en": self._get_english_translations(), 
            "ja": self._get_japanese_translations(),
            "fr": self._get_french_translations(),
        }

    def set_language(self, lang_code):
        """Set current language"""
        if lang_code in self.languages:
            self.current_language = lang_code
            return True
        return False

    def get_available_languages(self):
        """Get list of available languages"""
        return self.languages

    def get_text(self, key, **kwargs):
        """Get translated text with formatting"""
        try:
            text = self.translations[self.current_language].get(
                key, self.translations["vi"].get(key, key)
            )
            if kwargs:
                return text.format(**kwargs)
            return text
        except:
            return key

    def get_ai_method_text(self, method):
        """Get AI method translation"""
        ai_methods = self.get_text("ai_methods")
        if isinstance(ai_methods, dict):
            return ai_methods.get(method, method)
        return method

    def get_ai_method_help(self, method):
        """Get AI method help text"""
        ai_help = self.get_text("ai_method_help")
        if isinstance(ai_help, dict):
            return ai_help.get(method, "")
        return ""

    def _get_vietnamese_translations(self):
        """Vietnamese translations"""
        return {
            # App basics
            "app_title": "📚 Thẻ Ghi Nhớ AI",
            "app_subtitle": "Tạo thẻ ghi nhớ học tập từ nội dung giáo dục của bạn bằng AI",
            
            # Settings
            "settings": "Cài Đặt",
            "language": "Ngôn ngữ",
            "ai_method": "Phương pháp AI",
            "api_key_label": "Google Gemini API Key (tùy chọn)",
            "api_key_help": "Chỉ cần nếu muốn sử dụng Gemini AI",
            "use_sample_cards": "Sử dụng thẻ mẫu nếu tạo thất bại",
            "use_sample_cards_help": "Nếu được chọn, hệ thống sẽ tạo thẻ mẫu khi AI bị lỗi",
            
            # Navigation
            "create_flashcards": "Tạo Thẻ Ghi Nhớ",
            "view_flashcards": "Xem Thẻ Ghi Nhớ", 
            "saved_sets": "Bộ Thẻ Đã Lưu",
            "no_flashcards_available": "Không có thẻ ghi nhớ nào. Hãy tạo một số thẻ trước!",
            
            # Input section
            "create_new_flashcards": "Tạo Thẻ Ghi Nhớ Mới",
            "select_input_method": "Chọn phương thức nhập:",
            "upload_method": "Tải Lên File",
            "text_method": "Nhập Văn Bản",
            "upload_files": "Tải lên file của bạn (PDF hoặc PPT)",
            "upload_success": "Đã trích xuất nội dung thành công từ {filename}",
            "upload_error": "Lỗi khi trích xuất nội dung: {error}",
            "extracted_content": "Nội dung đã trích xuất (bạn có thể chỉnh sửa nếu cần):",
            "enter_text": "Nhập nội dung học tập của bạn:",
            "subject_topic": "Môn học/Chủ đề:",
            "num_cards": "Số lượng thẻ ghi nhớ cần tạo:",
            
            # Generate
            "generate_btn": "Tạo Thẻ Ghi Nhớ",
            "content_required": "Vui lòng cung cấp nội dung để tạo thẻ ghi nhớ",
            "generating_auto": "Đang tự động chọn phương pháp tạo thẻ tốt nhất...",
            "generating_gemini": "Đang tạo thẻ ghi nhớ bằng Gemini AI...",
            "generating_rule": "Đang tạo thẻ ghi nhớ tự động...",
            "success_created": "✅ Đã tạo {count} thẻ ghi nhớ thành công!",
            "error_creating": "Không thể tạo thẻ ghi nhớ. Vui lòng thử lại.",
            "error_with_fallback": "Lỗi khi tạo thẻ ghi nhớ: {error}",
            "using_sample_fallback": "Sử dụng thẻ ghi nhớ mẫu thay thế.",
            
            # View section
            "flashcards_title": "Thẻ Ghi Nhớ",
            "set_name": "Tên bộ thẻ:",
            "save_set": "Lưu Bộ Thẻ", 
            "current_set": "Bộ thẻ hiện tại: {name}",
            "edit_flashcard": "Chỉnh Sửa Thẻ Ghi Nhớ",
            "front_question": "Mặt trước (Câu hỏi):",
            "back_answer": "Mặt sau (Câu trả lời):",
            "save_changes": "Lưu Thay Đổi",
            "cancel": "Hủy",
            "flip_card": "Lật Thẻ",
            "previous": "⬅️ Trước",
            "next": "➡️ Tiếp",
            "edit": "✏️ Sửa",
            "delete": "🗑️ Xóa",
            "card_counter": "Thẻ {current} trong {total}",
            "no_flashcards": "Không có thẻ ghi nhớ nào để hiển thị",
            
            # Sets section
            "saved_flashcard_sets": "Bộ Thẻ Ghi Nhớ Đã Lưu",
            "no_saved_sets": "Chưa có bộ thẻ ghi nhớ nào được lưu. Hãy tạo và lưu một số thẻ ghi nhớ trước!",
            "set_name_col": "Tên Bộ Thẻ",
            "cards_count_col": "Số Thẻ",
            "select_set": "Chọn một bộ thẻ:",
            "load_set": "Tải Bộ Thẻ",
            "delete_set": "Xóa Bộ Thẻ",
            
            # Set operations
            "set_save_error_name": "Vui lòng nhập tên cho bộ thẻ ghi nhớ này",
            "set_save_error_exists": "Bộ thẻ '{name}' đã tồn tại. Vui lòng chọn tên khác.",
            "set_save_error_empty": "Không có thẻ ghi nhớ nào để lưu",
            "set_save_success": "Đã lưu {count} thẻ ghi nhớ vào '{name}'",
            "set_delete_success": "Đã xóa bộ thẻ '{name}'",
            "set_not_found": "Không tìm thấy bộ thẻ '{name}'",
            
            # AI methods
            "ai_methods": {
                "gemini": "Google Gemini", 
            },
            "ai_method_help": {
                "auto": "Tự động chọn API AI miễn phí tốt nhất",
                "online": "Sử dụng API AI miễn phí online (Cohere, Groq)",
                "gemini": "Google Gemini (cần API key)",
                "rule": "Tạo tự động không cần AI",
            },
        }

    def _get_english_translations(self):
        """English translations"""
        return {
            # App basics
            "app_title": "📚 AI Flashcards",
            "app_subtitle": "Create study flashcards from your educational content using AI",
            
            # Settings
            "settings": "Settings",
            "language": "Language",
            "ai_method": "AI Method",
            "api_key_label": "Google Gemini API Key (optional)",
            "api_key_help": "Only needed if you want to use Gemini AI",
            "use_sample_cards": "Use sample cards if generation fails",
            "use_sample_cards_help": "If checked, system will generate sample cards when AI fails",
            
            # Navigation
            "create_flashcards": "Create Flashcards",
            "view_flashcards": "View Flashcards",
            "saved_sets": "Saved Sets",
            "no_flashcards_available": "No flashcards available. Create some first!",
            
            # Input section
            "create_new_flashcards": "Create New Flashcards",
            "select_input_method": "Select input method:",
            "upload_method": "Upload Files",
            "text_method": "Enter Text",
            "upload_files": "Upload your files (PDF or PPT)",
            "upload_success": "Successfully extracted content from {filename}",
            "upload_error": "Error extracting content: {error}",
            "extracted_content": "Extracted content (you can edit if needed):",
            "enter_text": "Enter your study content:",
            "subject_topic": "Subject/Topic:",
            "num_cards": "Number of flashcards to generate:",
            
            # Generate
            "generate_btn": "Generate Flashcards",
            "content_required": "Please provide content to generate flashcards",
            "generating_auto": "Automatically selecting best generation method...",
            "generating_online": "Generating flashcards with online AI...",
            "generating_gemini": "Generating flashcards with Gemini AI...",
            "generating_rule": "Generating flashcards automatically...",
            "success_created": "✅ Successfully created {count} flashcards!",
            "error_creating": "Failed to generate flashcards. Please try again.",
            "error_with_fallback": "Error generating flashcards: {error}",
            "using_sample_fallback": "Using sample flashcards instead.",
            
            # View section
            "flashcards_title": "Flashcards",
            "set_name": "Set name:",
            "save_set": "Save Set",
            "current_set": "Current set: {name}",
            "edit_flashcard": "Edit Flashcard",
            "front_question": "Front (Question):",
            "back_answer": "Back (Answer):",
            "save_changes": "Save Changes",
            "cancel": "Cancel",
            "flip_card": "Flip Card",
            "previous": "⬅️ Previous",
            "next": "➡️ Next",
            "edit": "✏️ Edit",
            "delete": "🗑️ Delete",
            "card_counter": "Card {current} of {total}",
            "no_flashcards": "No flashcards to display",
            
            # Sets section
            "saved_flashcard_sets": "Saved Flashcard Sets",
            "no_saved_sets": "No saved flashcard sets yet. Create and save some flashcards first!",
            "set_name_col": "Set Name",
            "cards_count_col": "Cards",
            "select_set": "Select a set:",
            "load_set": "Load Set",
            "delete_set": "Delete Set",
            
            # Set operations
            "set_save_error_name": "Please enter a name for this flashcard set",
            "set_save_error_exists": "Set '{name}' already exists. Please choose a different name.",
            "set_save_error_empty": "No flashcards to save",
            "set_save_success": "Saved {count} flashcards to '{name}'",
            "set_delete_success": "Deleted set '{name}'",
            "set_not_found": "Set '{name}' not found",
            
            # AI methods
            "ai_methods": {
                "auto": "Auto",
                "online": "Online AI",
                "gemini": "Google Gemini",
                "rule": "Rule-based",
            },
            "ai_method_help": {
                "auto": "Automatically choose best free AI API",
                "online": "Use free online AI APIs (Cohere, Groq)",
                "gemini": "Google Gemini (requires API key)",
                "rule": "Auto-generate without AI",
            },
        }

    def _get_japanese_translations(self):
        """Japanese translations"""
        return {
            # App basics
            "app_title": "📚 AI単語カード",
            "app_subtitle": "AIを使って学習コンテンツから単語カードを作成",
            
            # Settings
            "settings": "設定",
            "language": "言語",
            "ai_method": "AI方法",
            "api_key_label": "Google Gemini APIキー（オプション）",
            "api_key_help": "Gemini AIを使用する場合のみ必要",
            "use_sample_cards": "生成に失敗した場合サンプルカードを使用",
            "use_sample_cards_help": "チェックすると、AI失敗時にサンプルカードを生成",
            
            # Navigation
            "create_flashcards": "単語カード作成",
            "view_flashcards": "単語カード表示",
            "saved_sets": "保存済みセット",
            "no_flashcards_available": "単語カードがありません。まず作成してください！",
            
            # Input section
            "create_new_flashcards": "新しい単語カードを作成",
            "select_input_method": "入力方法を選択：",
            "upload_method": "ファイルアップロード",
            "text_method": "テキスト入力",
            "upload_files": "ファイルをアップロード（PDFまたはPPT）",
            "upload_success": "{filename}からコンテンツを正常に抽出しました",
            "upload_error": "コンテンツ抽出エラー：{error}",
            "extracted_content": "抽出されたコンテンツ（必要に応じて編集可能）：",
            "enter_text": "学習コンテンツを入力：",
            "subject_topic": "科目/トピック：",
            "num_cards": "生成する単語カード数：",
            
            # Generate
            "generate_btn": "単語カード生成",
            "content_required": "単語カード生成にはコンテンツが必要です",
            "generating_auto": "最適な生成方法を自動選択中...",
            "generating_online": "オンラインAIで単語カード生成中...",
            "generating_gemini": "Gemini AIで単語カード生成中...",
            "generating_rule": "自動で単語カード生成中...",
            "success_created": "✅ {count}枚の単語カードを正常に作成しました！",
            "error_creating": "単語カード生成に失敗しました。もう一度お試しください。",
            "error_with_fallback": "単語カード生成エラー：{error}",
            "using_sample_fallback": "代わりにサンプル単語カードを使用します。",
            
            # View section
            "flashcards_title": "単語カード",
            "set_name": "セット名：",
            "save_set": "セット保存",
            "current_set": "現在のセット：{name}",
            "edit_flashcard": "単語カード編集",
            "front_question": "表面（質問）：",
            "back_answer": "裏面（回答）：",
            "save_changes": "変更を保存",
            "cancel": "キャンセル",
            "flip_card": "カードを裏返す",
            "previous": "⬅️ 前へ",
            "next": "➡️ 次へ",
            "edit": "✏️ 編集",
            "delete": "🗑️ 削除",
            "card_counter": "カード {current} / {total}",
            "no_flashcards": "表示する単語カードがありません",
            
            # Sets section
            "saved_flashcard_sets": "保存済み単語カードセット",
            "no_saved_sets": "保存済みセットがありません。まず単語カードを作成・保存してください！",
            "set_name_col": "セット名",
            "cards_count_col": "カード数",
            "select_set": "セットを選択：",
            "load_set": "セット読み込み",
            "delete_set": "セット削除",
            
            # Set operations
            "set_save_error_name": "この単語カードセットの名前を入力してください",
            "set_save_error_exists": "セット'{name}'は既に存在します。別の名前を選択してください。",
            "set_save_error_empty": "保存する単語カードがありません",
            "set_save_success": "{count}枚の単語カードを'{name}'に保存しました",
            "set_delete_success": "セット'{name}'を削除しました",
            "set_not_found": "セット'{name}'が見つかりません",
            
            # AI methods
            "ai_methods": {
                "auto": "自動",
                "online": "オンラインAI",
                "gemini": "Google Gemini",
                "rule": "ルールベース",
            },
            "ai_method_help": {
                "auto": "最適な無料AI APIを自動選択",
                "online": "無料オンラインAI APIを使用（Cohere、Groq）",
                "gemini": "Google Gemini（APIキー必要）",
                "rule": "AIなしで自動生成",
            },
        }

    def _get_french_translations(self):
        """French translations"""
        return {
            # App basics
            "app_title": "📚 Cartes Mémoire IA",
            "app_subtitle": "Créez des cartes mémoire d'étude à partir de votre contenu éducatif avec l'IA",
            
            # Settings
            "settings": "Paramètres",
            "language": "Langue",
            "ai_method": "Méthode IA",
            "api_key_label": "Clé API Google Gemini (optionnelle)",
            "api_key_help": "Nécessaire seulement si vous voulez utiliser Gemini IA",
            "use_sample_cards": "Utiliser des cartes d'exemple en cas d'échec",
            "use_sample_cards_help": "Si coché, génère des cartes d'exemple quand l'IA échoue",
            
            # Navigation
            "create_flashcards": "Créer des Cartes",
            "view_flashcards": "Voir les Cartes",
            "saved_sets": "Jeux Sauvegardés",
            "no_flashcards_available": "Aucune carte disponible. Créez-en d'abord !",
            
            # Input section
            "create_new_flashcards": "Créer de Nouvelles Cartes Mémoire",
            "select_input_method": "Sélectionnez la méthode d'entrée :",
            "upload_method": "Télécharger des Fichiers",
            "text_method": "Saisir du Texte",
            "upload_files": "Téléchargez vos fichiers (PDF ou PPT)",
            "upload_success": "Contenu extrait avec succès de {filename}",
            "upload_error": "Erreur d'extraction du contenu : {error}",
            "extracted_content": "Contenu extrait (vous pouvez le modifier si nécessaire) :",
            "enter_text": "Entrez votre contenu d'étude :",
            "subject_topic": "Sujet/Thème :",
            "num_cards": "Nombre de cartes mémoire à générer :",
            
            # Generate
            "generate_btn": "Générer les Cartes",
            "content_required": "Veuillez fournir du contenu pour générer les cartes",
            "generating_auto": "Sélection automatique de la meilleure méthode...",
            "generating_online": "Génération de cartes avec l'IA en ligne...",
            "generating_gemini": "Génération de cartes avec Gemini IA...",
            "generating_rule": "Génération automatique de cartes...",
            "success_created": "✅ {count} cartes mémoire créées avec succès !",
            "error_creating": "Échec de la génération des cartes. Veuillez réessayer.",
            "error_with_fallback": "Erreur de génération des cartes : {error}",
            "using_sample_fallback": "Utilisation de cartes d'exemple à la place.",
            
            # View section
            "flashcards_title": "Cartes Mémoire",
            "set_name": "Nom du jeu :",
            "save_set": "Sauvegarder le Jeu",
            "current_set": "Jeu actuel : {name}",
            "edit_flashcard": "Modifier la Carte Mémoire",
            "front_question": "Recto (Question) :",
            "back_answer": "Verso (Réponse) :",
            "save_changes": "Sauvegarder les Modifications",
            "cancel": "Annuler",
            "flip_card": "Retourner la Carte",
            "previous": "⬅️ Précédent",
            "next": "➡️ Suivant",
            "edit": "✏️ Modifier",
            "delete": "🗑️ Supprimer",
            "card_counter": "Carte {current} sur {total}",
            "no_flashcards": "Aucune carte mémoire à afficher",
            
            # Sets section
            "saved_flashcard_sets": "Jeux de Cartes Mémoire Sauvegardés",
            "no_saved_sets": "Aucun jeu sauvegardé. Créez et sauvegardez d'abord des cartes !",
            "set_name_col": "Nom du Jeu",
            "cards_count_col": "Cartes",
            "select_set": "Sélectionnez un jeu :",
            "load_set": "Charger le Jeu",
            "delete_set": "Supprimer le Jeu",
            
            # Set operations
            "set_save_error_name": "Veuillez entrer un nom pour ce jeu de cartes",
            "set_save_error_exists": "Le jeu '{name}' existe déjà. Choisissez un nom différent.",
            "set_save_error_empty": "Aucune carte à sauvegarder",
            "set_save_success": "{count} cartes sauvegardées dans '{name}'",
            "set_delete_success": "Jeu '{name}' supprimé",
            "set_not_found": "Jeu '{name}' introuvable",
            
            # AI methods
            "ai_methods": {
                "auto": "Auto",
                "online": "IA En Ligne",
                "gemini": "Google Gemini",
                "rule": "Règles",
            },
            "ai_method_help": {
                "auto": "Choisir automatiquement la meilleure API IA gratuite",
                "online": "Utiliser des API IA en ligne gratuites (Cohere, Groq)",
                "gemini": "Google Gemini (nécessite une clé API)",
                "rule": "Génération automatique sans IA",
            },
        }


# Global language manager instance
language_manager = LanguageManager()
