import pytest
from app.text_filter import clean_text

def test_clean_text_basic_filtering():
    """기본적인 필터링 키워드가 제거되는지 테스트"""
    raw_text = "안녕하세요. 이것은 본문 내용입니다.\nURL복사\n이웃\n공감\n"
    expected_text = "안녕하세요. 이것은 본문 내용입니다."
    cleaned_text = clean_text(raw_text)
    assert cleaned_text == expected_text

def test_clean_text_no_keywords():
    """필터링 키워드가 없는 경우 원본 텍스트가 유지되는지 테스트"""
    raw_text = "This is a clean sentence.\nAnother one."
    cleaned_text = clean_text(raw_text)
    assert cleaned_text == raw_text

def test_clean_text_partial_line_match():
    """한 줄에 여러 키워드가 있어도 해당 줄 전체가 제거되는지 테스트"""
    raw_text = "내용1\n이것은 URL복사 와 공감 버튼입니다.\n내용2"
    expected_text = "내용1\n내용2"
    cleaned_text = clean_text(raw_text)
    assert cleaned_text == expected_text

def test_clean_text_empty_string():
    """빈 문자열 입력 테스트"""
    cleaned_text = clean_text("")
    assert cleaned_text == ""

def test_clean_text_only_keywords():
    """키워드로만 이루어진 텍스트 테스트"""
    raw_text = "공감\nURL복사\n댓글"
    cleaned_text = clean_text(raw_text)
    assert cleaned_text == ""
