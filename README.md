# 모꿀모꿀 (MoggulMoggul) - AI 서비스
![header](https://capsule-render.vercel.app/api?type=cylinder&color=EAC149&height=130&section=header&text=MOGGUL-MOGGUL%20AI&fontSize=55&animation=scaleIn&fontColor=FFF)

<p align="center">
  <img src="https://img.shields.io/badge/python-3776AB.svg?&style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/fastapi-%23009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/docker-%232496ED.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/openai-%23412991.svg?&style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/langchain-%232D69A4.svg?&style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/pytorch-%23EE4C2C.svg?&style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/playwright-%232EAD33.svg?&style=for-the-badge&logo=playwright&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/postgresql-%234169E1.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/redis-%23DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/amazon s3-%23569A31.svg?&style=for-the-badge&logo=amazons3&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon EC2-%23FF9900.svg?&style=for-the-badge&logo=amazon-ec2&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon RDS-%23527FFF.svg?&style=for-the-badge&logo=amazon-rds&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon ElastiCache-%23FF9900.svg?&style=for-the-badge&logo=amazon-elasticache&logoColor=white"/>
  <br>
</p>

---

----
## 프로젝트 개요
웹페이지, 유튜브, 이미지 등 다양한 형태의 온라인 콘텐츠를 자동으로 분석하여 제목, 요약, 태그, 썸네일을 생성하고, 처리된 데이터를 백엔드 서버에 제공하는 비동기 콘텐츠 처리 AI 서비스 입니다.

## 팀원 소개
| **이름** | **역할**        | **GitHub**                   |
|--------|---------------|------------------------------|
| 구강현    | 백엔드 / 배포 / AI | https://github.com/GangHyoun |
| 송보민    | 백엔드 / AI      | https://github.com/Songbomin |
| 정혜지    | 프론트엔드 / 디자인        | https://github.com/heartggs  |

----

## 프로젝트 구성

### 주요 기능
- **비동기 콘텐츠 처리**: Celery를 사용하여 URL(웹페이지, 유튜브, 이미지)을 비동기적으로 처리하여 메인 서버의 부하를 줄입니다.
- **다양한 콘텐츠 요약 및 태깅**:
    - **웹페이지**: 동적/정적 웹페이지의 본문을 추출(`Playwright`, `BeautifulSoup`)하고 `OpenAI`를 통해 요약 및 태그를 생성합니다.
    - **유튜브**: 영상의 자막과 음성을 `Whisper`로 추출하여 텍스트로 변환한 후 요약 및 태그를 생성합니다.
    - **이미지**: `EasyOCR`로 이미지 내 텍스트를 추출(OCR)하여 요약 및 태그를 생성합니다.
- **썸네일 자동 생성**:
    - `Playwright`를 사용하여 웹페이지의 스크린샷을 찍거나, 유튜브/이미지 URL에서 직접 썸네일을 추출합니다.
    - 생성된 썸네일은 **AWS S3**에 업로드되어 URL로 관리됩니다.
- **벡터 데이터베이스 활용**: LangChain 파이프라인을 통해 처리된 텍스트를 벡터로 변환하고 **PGVector**에 저장하여 추후 검색 및 활용 가능성을 열어둡니다.
- 자세한 API 명세는 [API 명세서 주소](https://www.notion.so/AI-API-2648aa8cd0958058a783c722aafeff3d?source=copy_link) 참고하세요.

## 툴체인 & 프레임워크

### 프레임워크

| 분류 | 사용 기술 | 설명 |
|---|---|---|
| **언어** | Python 3.10+ | AI 모델링 및 비동기 처리를 위한 주력 개발 언어 |
| **웹 프레임워크** | FastAPI | 비동기 API 서버를 구축하여 높은 성능과 빠른 응답 속도 보장 |
| **비동기 작업 큐** | Celery with Redis | URL 콘텐츠 처리 작업을 비동기적으로 실행하여 메인 서버 부하 감소 |
| **AI/ML** | OpenAI, LangChain | 텍스트 요약, 태그 생성 등 자연어 처리 파이프라인 구축 |
| **AI/ML** | Whisper, EasyOCR | 유튜브 음성 및 이미지 내 텍스트를 추출하여 데이터 소스 확장 |
| **웹 스크래핑** | Playwright, BeautifulSoup | 동적/정적 웹페이지의 본문 콘텐츠를 정확하게 추출 |
| **데이터베이스** | PostgreSQL with PGVector | 텍스트 벡터 데이터를 저장하여 향후 검색 및 AI 기능 확장성 확보 |
| **클라우드 서비스** | AWS S3 | 생성된 썸네일 이미지를 안정적으로 저장하고 URL로 관리 |

### 툴체인

| 분류 | 사용 기술 | 설명 |
|---|---|---|
| **IDE** | Visual Studio Code | Python 개발 및 디버깅에 최적화된 통합 개발 환경 |
| **패키지 매니저** | Pip | `requirements.txt`를 통해 Python 프로젝트 의존성 관리 |
| **컨테이너화** | Docker, Docker Compose | 개발 환경을 컨테이너화하여 일관된 배포 및 실행 환경 보장 |
| **버전 관리** | Git + GitHub | 소스 코드 버전 관리 및 팀 협업을 위한 플랫폼 |
| **CI/CD** | GitHub Actions | main 브랜치 push 시 Docker 이미지를 빌드하여 EC2에 자동 배포 |
| **배포** | AWS EC2 | Docker 컨테이너를 이용한 서비스 애플리케이션 배포 환경 |
| **테스트 도구** | Postman | FastAPI로 구축된 API 엔드포인트 테스트 및 명세 확인 |
| **런타임 환경** | Python 3.10+ | AI 서비스 애플리케이션 실행 환경 |
| **인프라 관리** | AWS Console | EC2, RDS, S3 등 클라우드 인프라 구성 및 모니터링 |

---

## 프로젝트 프로그램 설치방법

### 사전 요구사항
- **Docker** 및 **Docker Compose** 설치
- **AWS S3** 버킷 및 IAM 자격 증명
- **OpenAI API Key**
- **PostgreSQL** 데이터베이스 (로컬 또는 원격)

### 설치 과정
1. **프로젝트 클론**
   ```bash
   git clone [https://github.com/your-username/moggulmoggul-ai.git](https://github.com/your-username/moggulmoggul-ai.git)
   cd moggulmoggul-ai
    ```
2. **.env 파일 설정**
   # OpenAI API 설정
    ```
    OPENAI_API_KEY="sk-..."
    ```

    # PostgreSQL 연결 정보 (Docker Compose 내부 네트워크 기준)
    ```
    POSTGRES_DB=momo
    POSTGRES_USER=user
    POSTGRES_PASSWORD=p1234
    PGVECTOR_CONNECTION_STRING=postgresql+psycopg2://user:p1234@db:5432/momo
    ```

    # Redis 연결 정보 (Docker Compose 내부 네트워크 기준)
    ```
    REDIS_URL=redis://redis:6379/0
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    ```

    # AWS S3 자격 증명
    ```
    AWS_ACCESS_KEY_ID="your_access_key"
    AWS_SECRET_ACCESS_KEY="your_secret_key"
    AWS_S3_BUCKET_NAME="your_bucket_name"
    ```

3. **Docker 이미지 빌드 및 컨테이너 실행**
    ```
    docker-compose up --build
    ```

----

### 프로그램 사용법
1. **애플리케이션 실행 확인**
<br/>
Docker 컨테이너가 정상적으로 실행되면, FastAPI 웹 서버는 http://localhost:8000에서 접근할 수 있습니다.

2. **API 엔드 포인트**
- 비동기 요약 작업 생성: `POST` `/async-index/`
    - Request Body: `{"url": "요약할 URL"}`
    - Response: `{"task_id": "생성된 작업 ID"}`

- 작업 상태 및 결과 조회: `GET` `/summary-result/{task_id}`
    - Response (완료 시):
        ```
        {
            "summary": "생성된 요약 내용",
            "title": "생성된 제목",
            "tags": ["태그1", "태그2"],
            "thumbnail_url": "S3에 업로드된 썸네일 URL"
        }
        ```
    - Response (진행 중) : `HTTP 202 Accepted` 상태 코드와 함께 진행 중 메시지 반환
- 썸네일 생성: `POST` `/thumbnail`

    - Request Body: `{"url": "썸네일 생성할 URL"}`

    - Response: 생성된 썸네일 이미지(PNG) 또는 유튜브 썸네일 URL로 리다이렉트

API 테스트는 Postman과 같은 도구를 사용하거나 FastAPI에서 제공하는 Swagger UI (http://localhost:8000/docs)를 통해 할 수 있습니다.

---

### 메인 파이프라인 (async-index)
이 파이프라인은 URL을 입력받아 콘텐츠 유형에 따라 적절한 처리 과정을 거쳐 최종 결과를 생성합니다.

1.  **URL 입력**: 사용자가 `POST /async-index/` 엔드포인트에 URL을 전송합니다.
2.  **작업 등록**: FastAPI 애플리케이션(`app/main.py`)은 Celery 큐에 `process_url_task` 작업을 등록하고, 즉시 작업 ID를 반환합니다.
3.  **썸네일 생성**: Celery 워커는 `app/summarizer.py`의 `process_url_task`를 실행하여, 먼저 `app/thumbnail_handler.py`를 통해 썸네일을 생성하고 AWS S3에 업로드합니다.
4.  **콘텐츠 유형 감지**: 워커는 `requests.head`를 사용하여 URL의 `Content-Type`을 확인하고, 유튜브 URL은 별도로 식별합니다.
5.  **콘텐츠 추출 및 처리**:
    * **웹페이지**:
        * `app/extractor.py`를 사용하여 웹페이지 본문을 추출합니다. 네이버 블로그는 `Playwright`를 사용하고, 그 외는 `requests`와 `BeautifulSoup`를 사용합니다.
        * `app/text_filter.py`를 통해 불필요한 텍스트를 제거합니다.
    * **유튜브**:
        * `app/video_handler.py`를 사용하여 영상의 자막(`YouTubeTranscriptApi`)과 음성(`Whisper`)을 추출하여 통합된 텍스트를 만듭니다.
    * **이미지**:
        * `app/image_handler.py`를 사용하여 이미지에서 `EasyOCR`로 텍스트를 추출합니다.
6.  **AI 요약 및 태그 생성**: 추출된 텍스트를 `app/langchain_pipe.py`로 전달하여, `app/ai_utils.py`의 `summarize_and_tag` 함수를 통해 OpenAI 모델로 제목, 요약, 태그를 생성합니다.
7.  **결과 반환**: 최종 결과(제목, 요약, 태그, 썸네일 URL)를 딕셔너리 형태로 반환하며, 이 결과는 Celery에 저장됩니다.
8.  **결과 조회**: 클라이언트는 `GET /summary-result/{task_id}` 엔드포인트를 주기적으로 호출(폴링)하여 작업 완료 상태를 확인하고 최종 결과를 받습니다.

### 썸네일 생성 파이프라인 (thumbnail)
이 파이프라인은 썸네일 생성만을 담당합니다.

1.  **URL 입력**: 사용자가 `POST /thumbnail` 엔드포인트에 URL을 전송합니다.
2.  **썸네일 유형 감지**: `app/thumbnail_handler.py`의 `generate_thumbnail` 함수는 URL이 유튜브, 이미지, 또는 일반 웹페이지인지 감지합니다.
3.  **썸네일 생성**:
    * **유튜브**: 고정된 유튜브 썸네일 URL로 리디렉션 응답을 반환합니다.
    * **이미지/웹페이지**: `Playwright`를 사용하여 웹페이지 스크린샷을 찍거나, 이미지를 직접 다운로드하여 PNG 형식의 바이트 데이터를 반환합니다.

---

## 프로젝트 URL
- **Main** : https://github.com/MoGGulMoGGul
- **FrontEnd** : https://github.com/MoGGulMoGGul/Frontend
- **BackEnd** : https://github.com/MoGGulMoGGul/Backend
- **AI** : https://github.com/MoGGulMoGGul/AI/tree/main