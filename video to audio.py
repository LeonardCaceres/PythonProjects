import pyfiglet
pyfiglet.print_figlet('Video   =>   Audio', font = 'slant')
import moviepy.editor
from pathlib import Path

if __name__ == '__main__':
    try:
        video_path = input('       Hello!\nEnter the path to the file: ')
        pyfiglet.print_figlet('...Checking...')
        video_file = Path(video_path)
        video = moviepy.editor.VideoFileClip(f'{video_file}')
        audio = video.audio
        audio.write_audiofile(f'{video_file.stem}.mp3')
        pyfiglet.print_figlet('completed')
    except:
        print('\n\n\n\nSomething went wrong...\nMake sure everything is correct\n------------exit---------------')