from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import fitz
import docx
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from elevenlabs import VoiceSettings
from flask import send_from_directory

load_dotenv()

client = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx','doc','txt'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = 'audio'
AUDIO_FOLDER = app.config['AUDIO_FOLDER']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_doc(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        text = file.read().decode('utf-8', errors='ignore')
    return text

def text_to_speech_file(text: str, filename: str) -> str:
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    # Save inside the 'audio' folder
    output_folder = "audio"
    os.makedirs(output_folder, exist_ok=True)
    save_file_path = os.path.join(output_folder, filename)

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path


@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)



@app.route('/', methods=['GET', 'POST'])
def index():
    content = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No File uploaded"
        
        file = request.files['file']
        if file.filename == '':
            return "No File selected"
        
        if file and allowed_file(file.filename):
            filename =  secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.endswith('.txt'):
                content = read_txt(file_path)
            elif filename.endswith('.pdf'):
                content = read_pdf(file_path)
            elif filename.endswith('.docx'):
                content = read_docx(file_path)
            elif filename.endswith('.doc'):
                content = read_doc(file_path)

            if content:
                audio_filename = f"{os.path.splitext(filename)[0]}.mp3"  # e.g., document.mp3
                text_to_speech_file(content, audio_filename)
                audio_url = f"/audio/{audio_filename}"  # Used in HTML to load the audio
                return render_template('index.html', content=content, audio_url=audio_url)

            else:
                return "Unsupported file type"
    
    return render_template('index.html', content=content)
        
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    app.run(debug=True)
