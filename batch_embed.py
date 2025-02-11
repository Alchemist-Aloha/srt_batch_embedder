import subprocess
import os
import argparse

def embed_srt(video_path, subtitle_path, output_path=None):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(subtitle_path):
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")
    
    if output_path is None:
        output_path = os.path.splitext(video_path)[0] + "_subtitled.mp4"
    
    command = [
        "ffmpeg", "-i", video_path,
        "-i", subtitle_path,
        "-c", "copy", "-c:s", "mov_text",
        output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Subtitle embedded successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error embedding subtitles: {e}")

def batch_embed_srt(directory):
    files = os.listdir(directory)
    videos = {os.path.splitext(f)[0]: os.path.join(directory, f) for f in files if f.endswith(".m4v")}
    subtitles = {os.path.splitext(f)[0]: os.path.join(directory, f) for f in files if f.endswith(".srt")}
    
    for base_name in videos.keys() & subtitles.keys():
        embed_srt(videos[base_name], subtitles[base_name])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch embed SRT subtitles into M4V video files in a directory.")
    parser.add_argument("directory", help="Path to the folder containing M4V and SRT files.")
    
    args = parser.parse_args()
    
    batch_embed_srt(args.directory)
