import os
import uuid
import boto3
import requests
from botocore.exceptions import NoCredentialsError
from playwright.sync_api import sync_playwright
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_to_s3(data, file_extension):
    """S3에 썸네일 데이터를 업로드하고 URL을 반환합니다."""
    try:
        # .env 파일에서 AWS 계정 ID를 가져옵니다.
        aws_account_id = os.getenv("AWS_ACCOUNT_ID")
        if not aws_account_id:
            logger.error("AWS_ACCOUNT_ID가 .env 파일에 설정되지 않았습니다.")
            return None

        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name='ap-northeast-2'
        )
        bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        file_name = f"thumbnails/{uuid.uuid4()}.{file_extension}"

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data,
            ContentType=f'image/{file_extension}',
            # 버킷 소유자 계정을 확인하는 파라미터
            ExpectedBucketOwner=aws_account_id
        )
        
        return f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_name}"

    except NoCredentialsError:
        logger.error("S3 자격 증명을 찾을 수 없습니다. .env 파일을 확인해주세요.")
        return None
    except Exception as e:
        logger.error(f"S3 업로드 중 오류 발생: {e}")
        return None

def generate_thumbnail(url):
    """URL 유형에 따라 썸네일(이미지 데이터 또는 URL)을 생성합니다."""
    # 유튜브 URL 처리
    if "youtube.com/watch?v=" in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f"https://img.youtube.com/vi/{video_id}/0.jpg", "redirect"
    elif "youtu.be/" in url:
        video_id = url.split('/')[-1].split('?')[0]
        return f"https://img.youtube.com/vi/{video_id}/0.jpg", "redirect"

    # 이미지 URL 처리
    try:
        headers = requests.head(url, timeout=5, allow_redirects=True).headers
        content_type = headers.get('Content-Type', '').lower()
        if 'image' in content_type:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content, "image"
    except requests.RequestException as e:
        logger.warning(f"이미지 URL 처리 중 오류: {e}")
        # 이미지 URL이 아니면 웹페이지로 간주하고 계속 진행
    
    # 일반 웹페이지 처리 (Playwright 사용)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=15000)
            screenshot_bytes = page.screenshot()
            browser.close()
            return screenshot_bytes, "image"
    except Exception as e:
        logger.error(f"웹페이지 스크린샷 생성 중 오류 발생: {e}")
        return None, None

def generate_thumbnail_and_upload_to_s3(url):
    """썸네일을 생성하고, 필요한 경우 S3에 업로드하여 최종 URL을 반환합니다."""
    try:
        thumbnail_data, thumb_type = generate_thumbnail(url)

        if not thumbnail_data:
            return None

        if thumb_type == "image":
            # 생성된 이미지 데이터를 S3에 업로드하고 URL을 받음
            return upload_to_s3(thumbnail_data, "png")
        elif thumb_type == "redirect":
            # 유튜브 썸네일처럼 이미 URL인 경우 그대로 반환
            return thumbnail_data
            
    except Exception as e:
        logger.error(f"썸네일 처리 및 업로드 과정에서 오류 발생: {e}")
        return None