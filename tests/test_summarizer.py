import pytest
from unittest.mock import patch, MagicMock
from app.summarizer import process_url_task

# 의존성 모의(Mocking)
@pytest.fixture
def mock_dependencies():
    with patch('app.summarizer.generate_thumbnail_and_upload_to_s3') as mock_thumbnail, \
         patch('app.summarizer.requests.head') as mock_head, \
         patch('app.summarizer.run_langchain_pipeline') as mock_langchain:
        
        mock_thumbnail.return_value = "https://example.com/thumbnail.png"
        mock_head.return_value = MagicMock(headers={'Content-Type': 'text/html'})
        mock_langchain.return_value = {
            "title": "테스트 제목",
            "summary": "테스트 요약",
            "tags": ["테스트", "태그"]
        }
        yield mock_thumbnail, mock_head, mock_langchain

def test_process_url_task_web(mock_dependencies):
    """웹페이지 URL에 대한 Celery 태스크를 테스트합니다."""
    with patch('app.summarizer.extract_text_from_url', return_value=("text/html", "테스트 본문 내용입니다.")):
        result = process_url_task.apply(args=["https://example.com"]).get()
        
        assert result["type"] == "text/html"
        assert result["title"] == "테스트 제목"
        assert "thumbnail_url" in result
        
def test_process_url_task_image(mock_dependencies):
    """이미지 URL에 대한 Celery 태스크를 테스트합니다."""
    with patch('app.summarizer.requests.head') as mock_head, \
         patch('app.summarizer.process_image_tip') as mock_image_process:
        
        mock_head.return_value = MagicMock(headers={'Content-Type': 'image/jpeg'})
        mock_image_process.return_value = {
            "summary_and_tags": {
                "title": "이미지 제목",
                "summary": "이미지 요약",
                "tags": ["이미지", "OCR"]
            }
        }
        
        result = process_url_task.apply(args=["https://example.com/image.jpg"]).get()
        
        assert result["type"] == "이미지"
        assert result["title"] == "이미지 제목"

def test_process_url_task_youtube(mock_dependencies):
    """유튜브 URL에 대한 Celery 태스크를 테스트합니다."""
    _, mock_head, mock_langchain = mock_dependencies
    
    mock_head.return_value = MagicMock(headers={'Content-Type': 'text/html'})
    
    with patch('app.summarizer.get_combined_transcript', return_value="유튜브 자막과 음성 내용입니다.") as mock_get_transcript:
        result = process_url_task.apply(args=["https://www.youtube.com/watch?v=some_video_id"]).get()

        mock_get_transcript.assert_called_once()
        mock_langchain.assert_called_once()
        assert result["type"] == "유튜브"
        assert result["title"] == "테스트 제목"

@patch('app.summarizer.generate_thumbnail_and_upload_to_s3', side_effect=Exception("S3 Upload Error"))
def test_process_url_task_failure(mock_thumbnail):
    """Celery 작업 중 예외 발생 시 task가 실패하는지 테스트"""
    # .apply().get()은 작업이 실패하면 예외를 발생시킵니다.
    with pytest.raises(Exception, match="S3 Upload Error"):
        process_url_task.apply(args=["https://example.com"]).get()