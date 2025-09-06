# tests/test_image_handler.py

import pytest
from unittest.mock import patch, MagicMock
from app.image_handler import process_image_tip, get_ocr_reader

# EasyOCR Reader 객체 초기화 로직을 테스트
@patch('app.image_handler.easyocr.Reader')
def test_get_ocr_reader_initialization(mock_reader):
    """get_ocr_reader가 처음 호출될 때만 초기화되는지 테스트"""
    # 전역 변수 초기화를 위해
    from app import image_handler
    image_handler.reader = None

    get_ocr_reader()
    get_ocr_reader() # 두 번 호출
    
    # easyocr.Reader는 한 번만 호출되어야 함
    mock_reader.assert_called_once_with(['ko', 'en'])

@patch('app.image_handler.extract_text_from_image', return_value="이미지에서 추출된 텍스트입니다.")
@patch('app.image_handler.clean_text', return_value="불용어 제거된 텍스트")
@patch('app.image_handler.summarize_and_tag')
def test_process_image_tip(mock_summarize, mock_clean, mock_extract):
    """이미지 처리 파이프라인 전체가 올바르게 호출되는지 테스트"""
    mock_summarize.return_value = {
        "title": "이미지 제목",
        "summary": "이미지 요약",
        "tags": ["태그"]
    }
    
    image_path = "path/to/image.jpg"
    result = process_image_tip(image_path)
    
    # 각 함수가 올바른 인자와 함께 호출되었는지 확인
    mock_extract.assert_called_once_with(image_path)
    mock_clean.assert_called_once_with("이미지에서 추출된 텍스트입니다.")
    mock_summarize.assert_called_once_with("불용어 제거된 텍스트")
    
    # 최종 결과 구조 확인
    assert result["cleaned_text"] == "불용어 제거된 텍스트"
    assert result["summary_and_tags"]["title"] == "이미지 제목"