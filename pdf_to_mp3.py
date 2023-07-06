from gtts import gTTS
import pdfplumber
from pathlib import Path
import pyfiglet

def pdf_to_mp3(file_path= "file.pdf", language="en"):
    if Path(file_path).is_file() and Path(file_path).suffix == ".pdf":
        with pdfplumber.PDF(open(file=file_path, mode="rb")) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        text = ''.join(pages)
        text = text.replace('\n', '')
        my_audio = gTTS(text=text, lang=language, slow=False)
        file_name = Path(file_path).stem
        print(f"[+] {file_name}.mp3 saved")
        my_audio.save(f"{file_name}.mp3")
    else:
        print("File not exists!")

if __name__ == '__main__':
    pyfiglet.print_figlet('PDF TO MP3')
    file_path = input('Enter file path - ')
    language = input("Enter the language('ru', 'en') - ")
    pyfiglet.print_figlet("Start//")
    pdf_to_mp3(file_path=file_path, language=language)