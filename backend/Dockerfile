FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv pip install --system \
    fastapi \
    uvicorn \
    google-genai \
    python-dotenv \
    pydantic

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]