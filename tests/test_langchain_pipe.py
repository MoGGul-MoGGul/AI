# tests/test_langchain_pipe.py

import pytest
from unittest.mock import patch, MagicMock
from app.langchain_pipe import run_langchain_pipeline

@patch('app.langchain_pipe.summarize_and_tag')
@patch('app.langchain_pipe.PGVector.from_documents')
@patch('app.langchain_pipe.OpenAIEmbeddings')
@patch('app.langchain_pipe.RecursiveCharacterTextSplitter')
def test_run_langchain_pipeline_success(mock_splitter, mock_embeddings, mock_pgvector, mock_summarize):
    """Langchain 파이프라인 성공 경로 테스트"""
    # 각 Mock 객체의 반환값 설정
    mock_splitter.return_value.create_documents.return_value = ["doc1", "doc2"]
    mock_summarize.return_value = {
        "title": "AI 제목",
        "summary": "AI 요약",
        "tags": ["AI", "태그"]
    }

    raw_text = "이것은 긴 원본 텍스트입니다."
    result = run_langchain_pipeline(raw_text)

    # 각 주요 함수가 호출되었는지 확인
    mock_splitter.return_value.create_documents.assert_called_once_with([raw_text])
    mock_pgvector.assert_called_once()
    mock_summarize.assert_called_once_with(raw_text)

    # 결과 확인
    assert result["chunks"] == 2
    assert result["title"] == "AI 제목"
    assert result["tags"] == ["AI", "태그"]

@patch('app.langchain_pipe.summarize_and_tag', side_effect=Exception("API Error"))
@patch('app.langchain_pipe.PGVector.from_documents')
def test_run_langchain_pipeline_summarize_fails(mock_pgvector, mock_summarize):
    """AI 요약/태그 생성 실패 시 예외 처리 테스트"""
    raw_text = "이것은 긴 원본 텍스트입니다."
    result = run_langchain_pipeline(raw_text)

    # 요약은 실패했지만, PGVector 저장 로직은 정상 호출되어야 함
    mock_pgvector.assert_called_once()
    
    # 실패 시 기본값들이 반환되는지 확인
    assert result["summary"] == ""
    assert result["title"] == ""
    assert result["tags"] == []