FROM python:3.10-slim
RUN useradd -md /src vacatorrent
USER vacatorrent
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "api"]
