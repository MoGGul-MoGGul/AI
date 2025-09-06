# =====================================================================
# Stage 1: Builder - 의존성 설치를 위한 단계
# =====================================================================
FROM python:3.11-slim AS builder

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# 가상 환경 생성
RUN python -m venv /opt/venv

# 가상 환경의 pip를 사용하도록 환경 변수 설정
ENV PATH="/opt/venv/bin:$PATH"

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# --- 수정된 부분 ---
# Playwright 브라우저를 설치할 경로를 환경 변수로 지정합니다.
ENV PLAYWRIGHT_BROWSERS_PATH="/ms-playwright"
# 지정된 경로에 브라우저를 설치합니다.
RUN python -m playwright install chromium
# --------------------

# =====================================================================
# Stage 2: Final Base Image - 실제 실행을 위한 최종 이미지
# =====================================================================
FROM python:3.11-slim

# 필수 런타임 시스템 패키지 및 Playwright 의존성 수동 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgl1 \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
  && rm -rf /var/lib/apt/lists/*

# 1. 권한 없는 'app' 그룹 및 사용자 생성
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# Builder 단계에서 설치한 가상 환경 복사
COPY --from=builder /opt/venv /opt/venv
# Builder 단계에서 설치한 Playwright 브라우저 복사
COPY --from=builder /ms-playwright /ms-playwright

# 환경 변수 설정
ENV PATH="/opt/venv/bin:$PATH"
ENV PLAYWRIGHT_BROWSERS_PATH="/ms-playwright"

# 작업 디렉토리 설정
WORKDIR /app

# 2. /app 디렉토리의 소유권을 appuser에게 부여
RUN chown -R appuser:appgroup /app

# 3. 기본 사용자를 appuser로 전환
USER appuser