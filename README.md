# 📚 FlashCard Master - AI Flashcard Generator

Ứng dụng tạo thẻ ghi nhớ thông minh từ nội dung học tập bằng AI, hỗ trợ đa ngôn ngữ và deployment online.

## ✨ Tính năng chính

### 🌍 Đa ngôn ngữ

- **Việt Nam** 🇻🇳 - Tiếng Việt đầy đủ
- **English** 🇺🇸 - Full English support
- **日本語** 🇯🇵 - Japanese interface
- **Français** 🇫🇷 - Interface en français

### 🤖 AI Methods

- **Online AI**: Sử dụng các API AI miễn phí (HuggingFace, etc.)
- **Google Gemini**: High-quality AI với API key

### 📝 Input Methods

- **Upload Files**: PDF, PowerPoint (.pptx)
- **Text Input**: Nhập trực tiếp nội dung

### 💾 Flashcard Management

- Tạo và chỉnh sửa flashcards
- Lưu và quản lý bộ thẻ
- Export/Import bộ thẻ
- Navigation dễ dàng giữa các thẻ

## 🚀 Cài đặt và Chạy

### Yêu cầu

- Python 3.8+
- pip hoặc uv package manager

### Cài đặt

```bash
# Clone repository
git clone <your-repo-url>
cd FlashCardMaster

# Cài đặt dependencies
pip install -r requirements.txt
# hoặc với uv
uv sync

# Chạy ứng dụng
streamlit run app.py
```

## 🔧 Cấu hình

### Google Gemini API (Tùy chọn)

1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Đăng nhập bằng tài khoản Google
3. Tạo API key miễn phí
4. Nhập vào ứng dụng

## 📁 Cấu trúc Project

```
FlashCardMaster/
├── app.py                 # Main Streamlit application
├── flashcard_generator.py # Core flashcard generation logic
├── online_ai.py          # Online AI APIs integration
├── utils.py              # Utility functions (PDF, PPT processing)
├── lang_manager.py       # Multilingual support
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
└── .gitignore           # Git ignore rules
```

## 🌐 Deployment

### Streamlit Cloud

1. Push code lên GitHub
2. Kết nối với [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy trực tiếp từ repository

### Heroku

```bash
# Tạo Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔄 API Integration

### Supported Free APIs

- **HuggingFace Inference API**: Completely free
- **Google Gemini**: Free tier with API key

### Adding New APIs

1. Implement method in `online_ai.py`
2. Add to API priority list
3. Update language files if needed

## 🐛 Troubleshooting

### Common Issues

- **Upload fails**: Check file format (PDF/PPTX only)
- **AI generation errors**: Try different AI method
- **Language not switching**: Clear browser cache

### Performance

- Large files may take time to process
- AI generation depends on API response time
- Use rule-based method for offline usage

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- HuggingFace for free AI APIs
- Google for Gemini AI
- OpenAI for inspiration
