FROM python:3.10-slim
RUN useradd -ms vacatorrent
USER vacatorrent
WORKDIR /home/vacatorrent
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "api"]