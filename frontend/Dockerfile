FROM python:3.13

WORKDIR /app

COPY frontend/ .

RUN pip install uv

RUN uv pip install --system \
    streamlit \
    requests

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]