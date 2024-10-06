FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY src .
CMD ["fastapi", "dev", "src/kittens/main.py", "--host", "0.0.0.0"]
