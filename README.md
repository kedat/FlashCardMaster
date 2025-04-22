# Gemini Flashcards

Gemini Flashcards is a Streamlit-based web application that allows users to generate study flashcards from educational content using Google's Gemini AI. Users can upload slides (PDF or PPTX) or enter text to create flashcards, save sets, and review them interactively.

## Features
- Generate flashcards from PDF or PPTX files.
- Create flashcards from manually entered text.
- Save and manage flashcard sets.
- Flip, edit, and delete flashcards.
- Use sample flashcards when API generation fails.

---

## Prerequisites

Before running the app locally, ensure you have the following installed:
- Python 3.11 or higher
- Pip (Python package manager)

---

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have a Google Gemini API key. You can obtain one from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## Running the App Locally

1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:5000` (or the port specified in the terminal).

---

## How to Use the App

### 1. Enter Your API Key
- In the sidebar, enter your Google Gemini API key. This is required to generate flashcards using the Gemini AI model.

### 2. Create Flashcards
- **Upload Slides**: Upload a PDF or PPTX file to extract content and generate flashcards.
- **Enter Text**: Manually input text to generate flashcards.

### 3. Save Flashcard Sets
- After generating flashcards, you can save them as a set for future use.

### 4. View and Manage Flashcards
- Navigate to the "View Flashcards" section to review, flip, edit, or delete flashcards.
- Use the "Saved Sets" section to load or delete previously saved flashcard sets.

---

## Troubleshooting

- **No API Key**: If you don't have an API key, you can enable the "Use sample cards" option in the sidebar to use pre-defined flashcards.
- **Error with File Upload**: Ensure the uploaded file is a valid PDF or PPTX format.

---

## Deployment

This app is configured to run on Replit. To deploy:
1. Push the code to your Replit workspace.
2. The app will automatically start using the `.replit` configuration.

---

## License

This project is licensed under the MIT License.