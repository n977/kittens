FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./src /app/src

CMD ["fastapi", "dev", "src/main.py"]
