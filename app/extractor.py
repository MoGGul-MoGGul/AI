import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import logging
from app.structure_detector import extract_main_content_from_html # 새로운 함수 임포트

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 네이버 블로그 추출 로직
def _extract_naver_blog_content(url: str) -> str | None:
    """Playwright를 사용해 네이버 블로그 본문을 추출하는 도우미 함수."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=20000, wait_until='domcontentloaded')
            content_html = page.content()
            browser.close()

            soup = BeautifulSoup(content_html, 'html.parser')
            content_selectors = [
                "div.se-main-container",  # 최신 스마트에디터
                "div.post_content",        # 구버전 스마트에디터
                "div.blog_content",        # 또 다른 구버전
                "div.article",             # 일반적인 블로그 아티클
            ]

            for selector in content_selectors:
                if main_content := soup.select_one(selector):
                    text = main_content.get_text(separator='\n', strip=True)
                    if len(text) > 50:
                        logger.info(f"선택자 '{selector}'를 사용하여 텍스트를 성공적으로 추출했습니다.")
                        return text

            # 선택자로 텍스트를 찾지 못한 경우 unstructured 라이브러리를 최종적으로 시도
            logger.warning("일반 선택자로 본문 추출 실패. unstructured 라이브러리로 재시도합니다.")
            return extract_main_content_from_html(content_html)

    except Exception as e:
        logger.error(f"Playwright로 네이버 블로그 처리 중 오류 발생: {e}")
        return None


# 메인 추출 함수
def extract_text_from_url(url: str):
    """
    URL을 분석하여 콘텐츠 유형과 텍스트를 반환합니다.
    네이버 블로그는 Playwright를, 그 외에는 requests를 사용합니다.
    """
    if "blog.naver.com" in url:
        logger.info(f"네이버 블로그 URL 감지: {url}. Playwright로 처리를 시도합니다.")
        # 도우미 함수를 호출하여 네이버 블로그 본문 추출 시도
        text = _extract_naver_blog_content(url)
        if text:
            return "네이버 블로그", text

    # 네이버 블로그가 아니거나, 위에서 블로그 추출에 실패한 경우 일반 방식으로 처리
    return extract_text_with_requests(url)


# 일반 웹페이지 추출 함수
def extract_text_with_requests(url: str):
    """requests와 BeautifulSoup을 사용하여 웹페이지 텍스트를 추출하는 일반적인 방법입니다."""
    logger.info(f"일반 방식으로 URL 처리: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.body.get_text(separator='\n', strip=True)
        return content_type, text
    except requests.RequestException as e:
        logger.error(f"requests로 URL 처리 중 오류 발생: {e}")
        return "에러", f"URL 콘텐츠를 가져오는 데 실패했습니다: {e}"