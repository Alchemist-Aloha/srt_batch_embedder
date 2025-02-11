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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed SRT subtitles into an M4V video file.")
    parser.add_argument("video", help="Path to the input M4V video file.")
    parser.add_argument("subtitle", help="Path to the input SRT subtitle file.")
    parser.add_argument("--output", help="Path to the output MP4 file (optional).", default=None)
    
    args = parser.parse_args()
    
    embed_srt(args.video, args.subtitle, args.output)