FROM python:3.9
WORKDIR /app
RUN apt-get -y update && \
    apt install wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt -y install ./google-chrome-stable_current_amd64.deb   # Google Chrome 다운로드 및 설치

COPY requirements.txt .  # requirements.txt 파일
COPY selenium_test.py .  # python app 파일
RUN pip install --no-cache-dir -r requirements.txt  # 패키지 의존성 설치
CMD [ "python", "selenium_test.py" ]  # python 실행
