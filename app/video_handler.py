# app/video_handler.py
import re
import os
import whisper
from rapidfuzz import fuzz
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def normalize_youtube_url(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("유효한 유튜브 URL이 아닙니다.")
    video_id = match.group(1)
    return f"https://www.youtube.com/watch?v={video_id}"

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_youtube_subtitles(video_id: str) -> list[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko", "en"])
        return [entry["text"] for entry in transcript if entry["text"].strip()]
    except NoTranscriptFound:
        return []

def download_youtube_audio(url: str, filename: str = "yt_audio") -> str:
    url = normalize_youtube_url(url)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'noplaylist': True,
        # 컨테이너에 ffmpeg 설치되어 있으므로 별도 경로 지정 불필요
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename + ".mp3"

def get_whisper_transcript(audio_path: str) -> list[str]:
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    lines = result["text"].replace('.', '').split(" ")
    return [line.strip() for line in lines if line.strip()]

def is_similar(a: str, b: str, threshold: int = 85) -> bool:
    return fuzz.ratio(a, b) > threshold

def remove_overlap(whisper_lines: list[str], subtitle_lines: list[str]) -> list[str]:
    unique = []
    for w_line in whisper_lines:
        if not any(is_similar(w_line, s_line) for s_line in subtitle_lines):
            unique.append(w_line)
    return unique

def get_combined_transcript(url: str) -> str:
    url = normalize_youtube_url(url)
    video_id = extract_video_id(url)

    subtitles = get_youtube_subtitles(video_id)
    audio_file = download_youtube_audio(url)
    whisper_lines = get_whisper_transcript(audio_file)

    whisper_unique = remove_overlap(whisper_lines, subtitles)

    if os.path.exists(audio_file):
        os.remove(audio_file)

    combined = ["[유튜브 자막 기반]"] + subtitles + ["", "[Whisper에서 잡힌 추가 내용]"] + whisper_unique
    return "\n".join(combined)
