# tests/test_thumbnail_handler.py

import pytest
from unittest.mock import patch, MagicMock
from app.thumbnail_handler import generate_thumbnail, upload_to_s3, generate_thumbnail_and_upload_to_s3

def test_generate_thumbnail_youtube_url():
    """유튜브 URL 썸네일 생성 테스트"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result, thumb_type = generate_thumbnail(url)
    assert "https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg" == result
    assert thumb_type == "redirect"

@patch('app.thumbnail_handler.requests.head', return_value=MagicMock(headers={'Content-Type': 'image/png'}))
@patch('app.thumbnail_handler.requests.get')
def test_generate_thumbnail_image_url(mock_get, mock_head):
    """이미지 URL 썸네일 생성 테스트"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = b"image_bytes"
    mock_get.return_value = mock_response

    result, thumb_type = generate_thumbnail("https://example.com/image.png")
    assert result == b"image_bytes"
    assert thumb_type == "image"

@patch('app.thumbnail_handler.sync_playwright')
def test_generate_thumbnail_webpage_url(mock_sync_playwright):
    """일반 웹페이지 URL 스크린샷 썸네일 생성 테스트"""
    mock_page = MagicMock()
    mock_page.screenshot.return_value = b"screenshot_bytes"
    mock_browser = MagicMock()
    mock_browser.new_page.return_value = mock_page
    mock_playwright = MagicMock()
    mock_playwright.chromium.launch.return_value = mock_browser
    mock_sync_playwright.return_value.__enter__.return_value = mock_playwright

    result, thumb_type = generate_thumbnail("https://example.com")
    assert result == b"screenshot_bytes"
    assert thumb_type == "image"

@patch('app.thumbnail_handler.boto3.client')
def test_upload_to_s3_success(mock_boto_client):
    """S3 업로드 성공 테스트"""
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
