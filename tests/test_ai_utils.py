import pytest
from unittest.mock import patch, MagicMock
from app.ai_utils import summarize_and_tag

@patch('app.ai_utils.openai.chat.completions.create')
def test_summarize_and_tag_success(mock_create):
    """OpenAI API 호출 성공 시 정상적인 결과 반환 테스트"""
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "[테스트 제목]\n테스트 요약 내용입니다.\n태그1, 태그2, 태그3, 태그4, 태그5"
    mock_response.choices = [mock_choice]
    mock_create.return_value = mock_response

    text = "이것은 테스트를 위한 긴 텍스트입니다."
    result = summarize_and_tag(text)

    assert result["title"] == "테스트 제목"
    assert result["summary"] == "테스트 요약 내용입니다."
    assert result["tags"] == ["태그1", "태그2", "태그3", "태그4", "태그5"]

@patch('app.ai_utils.openai.chat.completions.create', side_effect=Exception("API Error"))
def test_summarize_and_tag_failure(mock_create):
    """OpenAI API 호출 실패 시 기본값 반환 테스트"""
    text = "이것은 테스트를 위한 텍스트입니다."
    result = summarize_and_tag(text)

    assert result["title"] == "제목 생성 실패"
    assert result["summary"] == "요약 실패"
    assert result["tags"] == ["실패", "에러", "요약불가", "GPT오류", "기본"]
