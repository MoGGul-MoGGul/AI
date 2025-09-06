# tests/test_video_handler.py

import pytest
from unittest.mock import patch, MagicMock
import os
from youtube_transcript_api import NoTranscriptFound
from app.video_handler import is_similar, remove_overlap
from app.video_handler import (
    get_youtube_subtitles,
    download_youtube_audio,
    get_whisper_transcript,
    remove_overlap,
    get_combined_transcript,
    normalize_youtube_url,
    extract_video_id
)

@patch('app.video_handler.YouTubeTranscriptApi.get_transcript')
def test_get_youtube_subtitles_success(mock_get_transcript):
    mock_transcript = [{'text': 'Hello world'}, {'text': 'This is a test.'}]
    mock_get_transcript.return_value = mock_transcript
    subtitles = get_youtube_subtitles("test_video_id")
    assert subtitles == ["Hello world", "This is a test."]

@patch('app.video_handler.YouTubeTranscriptApi.get_transcript', side_effect=NoTranscriptFound("video_id", ["en", "ko"], {}))
def test_get_youtube_subtitles_no_transcript(mock_get_transcript):
    """자막이 없는 경우 빈 리스트 반환 테스트"""
    subtitles = get_youtube_subtitles("no_subtitle_video_id")
    assert subtitles == []

@patch('app.video_handler.yt_dlp.YoutubeDL')
def test_download_youtube_audio(mock_ydl):
    mock_ydl_instance = MagicMock()
    mock_ydl.return_value.__enter__.return_value = mock_ydl_instance
    audio_file = download_youtube_audio("https://www.youtube.com/watch?v=mock_video_id")
    mock_ydl_instance.download.assert_called_once()
    assert audio_file == "yt_audio.mp3"

@patch('app.video_handler.get_youtube_subtitles', return_value=["Youtube subtitles."])
@patch('app.video_handler.download_youtube_audio', return_value="audio.mp3")
@patch('app.video_handler.get_whisper_transcript', return_value=["Additional whisper content."])
@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_get_combined_transcript(mock_os_remove, mock_os_exists, mock_whisper, mock_download, mock_subtitles):
    combined_text = get_combined_transcript("https://www.youtube.com/watch?v=mock_video_id")
    assert "[유튜브 자막 기반]" in combined_text
    assert "Additional whisper content." in combined_text
    mock_os_remove.assert_called_once_with("audio.mp3")

def test_remove_overlap():
    whisper_lines = ["Hello world.", "This is a test.", "Goodbye."]
    subtitle_lines = ["Hello world!", "This is a test."]
    unique_lines = remove_overlap(whisper_lines, subtitle_lines)
    assert unique_lines == ["Goodbye."]

def test_normalize_youtube_url_invalid():
    """유효하지 않은 유튜브 URL 입력 시 ValueError가 발생하는지 테스트"""
    with pytest.raises(ValueError, match="유효한 유튜브 URL이 아닙니다."):
        normalize_youtube_url("https://example.com")

def test_extract_video_id_none():
    """일반 URL에서 비디오 ID 추출 시 None이 반환되는지 테스트"""
    video_id = extract_video_id("https://example.com/not-a-video")
    assert video_id is None

@patch('app.video_handler.whisper.load_model')
def test_get_whisper_transcript(mock_load_model):
    """Whisper를 이용한 음성-텍스트 변환 테스트"""
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "이것은. 테스트. 문장입니다."}
    mock_load_model.return_value = mock_model

    transcript = get_whisper_transcript("dummy_audio.mp3")
    
    assert transcript == ["이것은", "테스트", "문장입니다"]
    mock_load_model.assert_called_once_with("base")
    mock_model.transcribe.assert_called_once_with("dummy_audio.mp3")

def test_is_similar():
    """문자열 유사도가 정확히 계산되는지 테스트"""
    assert is_similar("안녕하세요", "안녕하세요!") == True
    assert is_similar("안녕하세요", "반갑습니다", threshold=85) == False