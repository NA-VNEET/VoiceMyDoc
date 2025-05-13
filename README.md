
# 📄🔊 VoiceMyDoc:  AI Document Reader with Text-to-Speech


**AI Document Reader** is a web-based tool built using Python Flask and ElevenLabs AI that allows users to **upload documents** and **listen to them as audio**. It intelligently extracts text from files like PDFs, Word documents, and plain text files, and uses **realistic AI-generated voices** to convert the text into speech.


# 🚀 Features

- 📄 Upload and read text from:
  - PDF files
  - Word Documents (`.docx`, `.doc`)
  - Plain Text files (`.txt`)
- 🧠 Uses **ElevenLabs API** for AI-based voice generation
- 🔊 Converts long documents into realistic voiceovers
## 🛠️ Tech Stack

- Python 3.10+
- Flask
- ElevenLabs Text-to-Speech API
- `fitz` (PyMuPDF) for PDF reading
- `python-docx` for Word files
## Installation



```bash
## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/NA-VNEET/VoiceMyDoc.git

cd VoiceMyDoc

python app.py

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

ELEVENLABS_API_KEY=<Your_api_key>



