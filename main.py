import os
from pytube import YouTube
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_youtube_video(youtube_url, output_path, format):
    try:
        yt = YouTube(youtube_url)
        
        if format == 'mp3':
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=output_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            
            from moviepy.editor import AudioFileClip
            audio_clip = AudioFileClip(out_file)
            audio_clip.write_audiofile(new_file)
            audio_clip.close()
            
            os.remove(out_file)
            logging.info(f"Downloaded and converted to MP3: {new_file}")
        elif format == 'mp4':
            video = yt.streams.get_highest_resolution()
            out_file = video.download(output_path=output_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp4'
            
            os.rename(out_file, new_file)
            logging.info(f"Downloaded and saved as MP4: {new_file}")
        else:
            logging.error(f"Unsupported format: {format}")
            return None

        return new_file
    except Exception as e:
        logging.error(f"Failed to download {youtube_url}: {e}")
        return None

def main():
    input_file = 'url_list.txt'
    output_path = 'downloaded_files'
    os.makedirs(output_path, exist_ok=True)
    
    format = input("Enter the desired format (mp3/mp4): ").strip().lower()
    if format not in ['mp3', 'mp4']:
        logging.error("Invalid format. Please enter 'mp3' or 'mp4'.")
        return
    
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        logging.error(f"Failed to read input file {input_file}: {e}")
        return
    
    for line in lines:
        youtube_url = line.strip()
        if youtube_url:
            logging.info(f"Processing {youtube_url}...")
            download_youtube_video(youtube_url, output_path, format)

if __name__ == "__main__":
    main()
