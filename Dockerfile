FROM python:3.12.1-bookworm

WORKDIR /app

RUN pip install poetry==1.7.1
COPY pyproject.toml poetry.lock ./

RUN poetry export > requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]