FROM python:3.11-bullseye
RUN useradd -md /src vacatorrent
USER vacatorrent
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "api"]
