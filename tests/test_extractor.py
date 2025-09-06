# tests/test_extractor.py

import pytest
import requests
from unittest.mock import patch, MagicMock
from app.extractor import extract_text_from_url, extract_text_with_requests
from app.structure_detector import extract_main_content_from_html

@patch('app.extractor.requests.get')
def test_extract_text_with_requests_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_response.content = b"<html><body><p>This is test content.</p></body></html>"
    mock_get.return_value = mock_response

    content_type, text = extract_text_with_requests("https://example.com")
    assert content_type == 'text/html'
    assert "This is test content." in text
    
@patch('app.extractor.requests.get', side_effect=requests.RequestException("Network Error"))
def test_extract_text_with_requests_failure(mock_get):
    content_type, text = extract_text_with_requests("https://invalid-url.com")
    assert content_type == "에러"
    assert "URL 콘텐츠를 가져오는 데 실패했습니다" in text
    
@patch('app.extractor._extract_naver_blog_content')
@patch('app.extractor.extract_text_with_requests')
def test_extract_text_from_url_naver_blog(mock_requests_extract, mock_naver_blog_extract):
    mock_naver_blog_extract.return_value = "네이버 블로그 본문입니다."
    
    content_type, text = extract_text_from_url("https://blog.naver.com/post")
    assert content_type == "네이버 블로그"
    assert "네이버 블로그 본문입니다." in text
    
    extract_text_from_url("https://example.com/not-naver-blog")
    mock_requests_extract.assert_called_once()

# [수정] Mock 텍스트의 길이를 100자 이상으로 늘려 조건문을 통과하도록 합니다.
def test_extract_main_content_unstructured_success():
    """structure_detector.py의 주력 로직(unstructured) 테스트"""
    html_content = "<html><body><p>Some content.</p></body></html>"
    
    with patch('app.structure_detector.partition_html') as mock_partition:
        mock_element = MagicMock()
        mock_element.text = "This is a mocked unstructured content that is definitely longer than one hundred characters to pass the length check in the function."
        mock_partition.return_value = [mock_element]
        
        result = extract_main_content_from_html(html_content)
        assert result == mock_element.text

def test_extract_main_content_fallback_logic():
    """structure_detector.py의 폴백 로직(BeautifulSoup) 테스트"""
    html_content = """
    <html><body>
        <div id="header">Header</div>
        <div id="main-content"><p>This is the main content.</p></div>
    </body></html>
    """
    with patch('app.structure_detector.partition_html', side_effect=Exception("unstructured error")):
        result = extract_main_content_from_html(html_content)
        assert "This is the main content." in result
        assert "Header" not in result