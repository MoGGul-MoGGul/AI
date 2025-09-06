# tests/test_main_endpoints.py

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

# AsyncResult를 모킹하여 Celery의 실제 결과 객체를 모방합니다.
@patch('app.main.AsyncResult')
def test_get_summary_result_success(mock_async_result):
    """요약 결과 조회 성공 케İ스 테스트 (상태: SUCCESS)"""
    mock_instance = MagicMock()
    mock_instance.ready.return_value = True
    mock_instance.successful.return_value = True
    mock_instance.result = {
        "summary": "테스트 요약",
        "title": "테스트 제목",
        "tags": ["태그1"],
        "thumbnail_url": "https://example.com/thumb.png"
    }
    mock_async_result.return_value = mock_instance
    
    response = client.get("/summary-result/some_task_id")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "테스트 요약"
    assert data["title"] == "테스트 제목"

@patch('app.main.AsyncResult')
def test_get_summary_result_pending(mock_async_result):
    """요약 작업이 아직 진행 중인 케이스 테스트 (상태: PENDING)"""
    mock_instance = MagicMock()
    mock_instance.ready.return_value = False
    mock_async_result.return_value = mock_instance

    response = client.get("/summary-result/some_task_id")
    assert response.status_code == 202 # HTTPException(status_code=202)
    assert "아직 완료되지 않았습니다" in response.json()["detail"]

@patch('app.main.AsyncResult')
def test_get_summary_result_failure(mock_async_result):
    """요약 작업이 실패한 케이스 테스트 (상태: FAILURE)"""
    mock_instance = MagicMock()
    mock_instance.ready.return_value = True
    mock_instance.successful.return_value = False
    mock_instance.result = "An error occurred"
    mock_async_result.return_value = mock_instance

    response = client.get("/summary-result/some_task_id")
    assert response.status_code == 500
    assert "작업이 실패했습니다" in response.json()["detail"]

@patch('app.main.process_url_task.delay')
def test_async_index(mock_delay):
    """URL을 받아 비동기 작업을 시작하는지 테스트"""
    mock_task = MagicMock()
    mock_task.id = "test_task_id"
    mock_delay.return_value = mock_task

    response = client.post("/async-index/", json={"url": "https://example.com"})
    
    assert response.status_code == 200
    assert response.json() == {"task_id": "test_task_id"}
    mock_delay.assert_called_once_with("https://example.com")

@patch('app.main.AsyncResult')
def test_get_status(mock_async_result):
    """작업 상태를 정상적으로 조회하는지 테스트"""
    mock_instance = MagicMock()
    mock_instance.status = "PENDING"
    mock_instance.ready.return_value = False
    mock_async_result.return_value = mock_instance
    
    response = client.get("/task-status/some_task_id")
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"
    assert response.json()["result"] is None


@patch('app.main.generate_thumbnail', return_value=("https://youtube.com/thumb.jpg", "redirect"))
def test_create_thumbnail_redirect(mock_generate_thumbnail):
    """썸네일 생성 시 redirect를 잘 처리하는지 테스트"""
    response = client.post("/thumbnail", json={"url": "https://youtube.com"})
    
    # 최종 응답이 아닌, 리다이렉션 히스토리를 검사합니다.
    assert len(response.history) == 1  # 리다이렉션이 한 번 발생했는지 확인
    redirect_response = response.history[0]  # 첫 번째 리다이렉션 응답을 가져옴

    assert redirect_response.status_code == 307  # 리다이렉션 응답의 상태 코드가 307인지 확인
    assert redirect_response.headers["location"] == "https://youtube.com/thumb.jpg"